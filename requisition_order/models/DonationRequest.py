from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.osv import expression


class DonationRequest(models.Model):
    _name = 'donation.request'
    _description = 'Donations'

    @api.model
    def create(self, values):
        sequence_code = 'donation.request'
        values['name'] = self.env['ir.sequence'].with_context(
            ir_sequence_date=values['date']).next_by_code(sequence_code)
        return super(DonationRequest, self).create(values)

    def _default_department(self):
        employee = self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)],
            limit=1)
        if employee:
            if employee.department_id:
                return employee.department_id.id
        return False

    def _default_analytic_account(self):
        employee = self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)],
            limit=1)
        if employee:
            if employee.department_id:
                if employee.department_id.analytic_account_id:
                    return employee.department_id.analytic_account_id.id
        return False

    name = fields.Char(string='Name')
    date = fields.Date(
        string='Request Date', required=True, help='Get the current date',
        default=fields.Date.context_today)

    donor_id = fields.Many2one(comodel_name='res.partner', required=True, string='Donor')

    user_id = fields.Many2one(comodel_name='res.users', string='Request user',
                              required=False, default=lambda self: self.env.user)

    company_id = fields.Many2one(string='Company', comodel_name='res.company',
                                 default=lambda self: self.env.user.company_id)

    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user.company_id.currency_id.id)

    department_id = fields.Many2one(
        comodel_name='hr.department', required=True, string='Requesting Party',
        default=_default_department)

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account',
        default=_default_analytic_account)

    purpose = fields.Selection(string='Donation nature', required=True, selection=[
        ('expense', 'Restricted'), ('income', 'Non Restricted'), ])

    expend_type = fields.Selection(string='Donation nature', selection=[
        ('now', 'Now'), ('scheduled', 'Scheduled'), ('with_request', 'With Request'), ],
        default='with_request')

    service_id = fields.Many2one(
        comodel_name='product.product', string='Donation Service',
        required=True,
        domain=[('type', '=', 'service'),
                ('nature', 'in', ['expense', 'income'])])

    # must change the comodel when integrate with segele
    childs_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='donation_child_ref',
        column1='donation_id',
        column2='child_id',
        string='restricted childs')

    childs_num = fields.Integer(string='restricted childs Number')

    attached_file = fields.Binary(string='Attached File', attachment=True)

    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('done', 'Done'),
         ('cancel', 'Cancel')],
        default='draft', string='Status', readonly=True)

    description = fields.Text(string='Description')

    amount = fields.Monetary(
        string='Amount',
        required=True,
        help="Total amount")

    voucher_id = fields.Many2one('account.voucher', 'voucher', copy=False)

    # restriction purposes
    requisition_ids = fields.One2many(comodel_name='requisition.request.line',
                                      inverse_name='restriction', string='Requisition Requests')

    restriction_remain = fields.Monetary(
        string='Restriction Remain Amount', store=True, readonly=True, compute='_compute_remain',
        copy=False)

    @api.one
    @api.depends(
        'requisition_ids.amount', 'state')
    def _compute_remain(self):
        if self.purpose == 'expense':
            self.restriction_remain = self.amount - sum(
                x.amount for x in self.requisition_ids)
            if self.state == 'done' and not self.requisition_ids:
                self.restriction_remain = self.amount

    @api.multi
    @api.constrains('restriction_remain')
    def _check_restriction_remain(self):
        for obj in self:
            if obj.restriction_remain < 0:
                raise ValidationError(
                    _('''restriction remain must be greater than zero  '''))

    @api.depends('company_id', 'donor_id')
    def _compute_payment_journal_id(self):
        for rec in self:
            domain = [
                ('type', 'in', ('bank', 'cash')),
                ('company_id', '=', rec.company_id.id),
            ]
            if self.donor_id.property_account_receivable_id and\
                    self.donor_id.property_account_receivable_id.internal_type == 'liquidity':
                field = 'default_debit_account_id'
                domain.append((field, '=', self.donor_id.property_account_receivable_id.id))

            rec.payment_journal_id = self.env['account.journal'].search(domain, limit=1)

    def _inverse_payment_journal_id(self):
        for rec in self:
            rec.account_id = rec.payment_journal_id.default_debit_account_id

    @api.onchange('department_id')
    def _onchange_department(self):
        for line in self:
            if line.department_id:
                if line.department_id.analytic_account_id:
                    line.analytic_account_id = line.department_id.analytic_account_id.id
                else:
                    line.analytic_account_id = False
            else:
                line.analytic_account_id = False

    @api.onchange('purpose')
    def _onchange_purpose(self):
        self.service_id = False

    @api.multi
    def confirm(self):
        """
        change state to confirm and check budget
        """
        self.write({'state': 'confirmed'})

    @api.multi
    def done(self):
        """
        change state to done and create voucher
        """

        self.create_voucher()

        self.write({'state': 'done'})

    @api.multi
    def get_voucher_lines(self):
        """
        prepare voucher lines from details lines
        for voucher creation
        """
        self.ensure_one()

        if self.purpose == "income":
            account_id = self.service_id.property_account_income_id.id
        elif self.purpose == "expense":
            if not self.service_id.account_restricted_income_id:
                raise ValidationError(_(''' please set restricted income account in settings '''))
            account_id = self.service_id.account_restricted_income_id.id

        lines = [
            {
                'name': self.description,
                'product_id': self.service_id.id,
                'service_id': self.service_id.id,
                'account_id': account_id,
                'price_unit': self.amount,
                'quantity': 1,  # only one service
                'account_analytic_id': self.analytic_account_id.id,
            }
        ]

        lines = [(0, 0, x) for x in lines]
        return lines

    @api.multi
    def create_voucher(self):
        """
        create voucher for the current request
        """
        self.ensure_one()
        lines = self.get_voucher_lines()

        journal_id = False

        if not self.company_id.default_income_journal_id:
            raise ValidationError(_(''' please set income journal in settings '''))

        journal_id = self.company_id.default_income_journal_id.id

        company_id = self.company_id.id
        p = self.donor_id if not company_id else self.donor_id.with_context(
            force_company=company_id)

        rec_account = p.property_account_receivable_id
        pay_account = p.property_account_payable_id
        if not rec_account and not pay_account:
            raise ValidationError(
                _(''' please set donor's payable and receivable accounts first '''))

        data = {
            'name': self.name,
            'reference': self.name,
            'voucher_type': 'sale',
            'date': self.date,
            'account_date': self.date,
            'date_due': self.date,
            'narration': self.description,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.donor_id.id,
            'journal_id': journal_id,
            'account_id': self.donor_id.property_account_receivable_id.id,
            'line_ids': lines,
            'res_model':  'donation.request',
            'res_id': self.id,
            'pay_now': 'pay_now',
            'restricted': self.purpose == 'expense',
        }
        voucher_id = self.env['account.voucher'].create(data)
        self.voucher_id = voucher_id.id

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """
        inherit the name search to only show the allowed donations
        when the pass it the context
        """
        context = dict(self.env.context)

        if 'get_my_restrictions' in context:
            get_my_restrictions = context.get('get_my_restrictions', False)
            beneficiary_id = context.get('beneficiary_id', False)
            expense_service = context.get('expense_service', False)

            if get_my_restrictions and expense_service:
                donations = self.search(
                    [('state', '=', 'done'),
                     ('purpose', '=', 'expense'),
                     ('service_id', '=', expense_service)])
                analytic_obj = self.env['account.analytic.account']
                returned_list = []

                for don in donations:
                    if get_my_restrictions in analytic_obj.search(
                        ['|', ('id', 'child_of', don.analytic_account_id.id),
                         ('id', '=', don.analytic_account_id.id)]).ids:
                        if not don.childs_ids:
                            returned_list.append(don.id)
                            continue
                        if don.childs_ids and beneficiary_id in don.childs_ids.ids:
                            returned_list.append(don.id)
                domain = [('id', 'in', returned_list)]
                args = expression.AND([domain, args])
            else:
                domain = [('id', '=', 0)]
                args = expression.AND([domain, args])

        return super(DonationRequest, self).name_search(name, args,
                                                        operator, limit)
