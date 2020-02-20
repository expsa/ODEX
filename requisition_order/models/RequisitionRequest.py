# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError
from odoo.addons import decimal_precision as dp
from datetime import date, datetime


class RequisitionRequest(models.Model):
    _name = 'requisition.request'
    _description = 'users Requisition Requests'
    _inherit = ['mail.thread']
    _order = "create_date desc"

    @api.model
    def create(self, values):
        sequence_code = 'requisition.request.internal'
        values['name'] = self.env['ir.sequence'].with_context(
            ir_sequence_date=values['date']).next_by_code(sequence_code)
        return super(RequisitionRequest, self).create(values)

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

    beneficiary_id = fields.Many2one(comodel_name='res.partner',
                                     required=True, string='Beneficiary')

    department_id = fields.Many2one(
        comodel_name='hr.department', required=True, string='Requesting Party',
        default=_default_department)

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account',
        default=_default_analytic_account)

    purpose = fields.Selection(string='Purpose', required=True, selection=[(
        'expense', 'Expense'), ('custodies', 'Custodies'), ])

    custody_id = fields.Many2one(
        comodel_name='product.product', string='Custody',
        required=False,
        domain=[('type', '=', 'service'),
                ('nature', '=', 'custody')],
        ondelete='restrict',
        help='used for custody purpose')

    payment_id = fields.Many2one(
        'account.payment',
        string="Payment", copy=False, readonly=True,
        help='used for custody purpose')

    move_id = fields.Many2one('account.move', 'Journal Entry', copy=False,
                              help='used for custody purpose')

    description = fields.Text(string='Description')

    state = fields.Selection(
        [('draft', 'Draft'),
         ('requested', 'Requested'),
         ('approved', 'Approved'),
         ('done', 'Done'),
         ('running', 'Running'),
         ('budget_confirmed', 'Budget Confirmed'),
         ('budget_not_confirmed', 'Budget Not Confirmed'),
         ('posted', 'Posted'),
         ('closed', 'Closed'),
         ('cancel', 'Cancel')],
        default='draft', string='Status', readonly=True, track_visibility='always')

    user_id = fields.Many2one(comodel_name='res.users', string='Request user',
                              required=False, default=lambda self: self.env.user)

    company_id = fields.Many2one(string='Company', comodel_name='res.company',
                                 default=lambda self: self.env.user.company_id)

    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user.company_id.currency_id.id)

    lines_ids = fields.One2many(
        comodel_name='requisition.request.line', inverse_name='request_id', string='Details',
        copy=False)

    total_amount = fields.Monetary(
        string='Total Amount', store=True, readonly=True, compute='_compute_total',
        help="Total Amount of the services requested", copy=False)

    custody_total_amount = fields.Monetary(
        string='custody lines amount', store=True, readonly=True, compute='_compute_total',
        help="custody lines amount", copy=False)

    custody_residual_amount = fields.Monetary(
        string='residual amount', store=True, readonly=True, compute='_compute_total',
        help="custody residual amount", copy=False)

    custody_amount = fields.Monetary(
        string='Amount',
        help="Custody amount")

    budget_confirmation_id = fields.Many2one(
        comodel_name='budget.confirmation',
        string='Budget Confirmation', copy=False)

    invoice_id = fields.Many2one('account.invoice', 'Invoice', copy=False)

    closing_journal_id = fields.Many2one(
        'account.journal', string='Payment Journal',
        domain=[('type', 'in', ('bank', 'cash'))], copy=False)

    closing_payment_method_id = fields.Many2one(
        'account.payment.method', string='Payment Method Type',
        help="Manual: Get paid by cash, check or any other method outside of Odoo.\n"
        "Electronic:Get paid automatically through a payment acquirer by requesting a transaction\n"
        "on a card saved by the customer when buying or subscribing online (payment token).\n"
        "Check: Pay bill by check and print it from Odoo.\n"
        "Batch Deposit: Encase several customer checks at once by generating a batch deposit to \n"
        "submit to your bank. When encoding the bank statement in Odoo, you are suggested to \n"
        "reconcile the transaction with the batch deposit.To enable batch deposit,module \n"
        "account_batch_deposit must be installed.\n"
        "SEPA Credit Transfer: Pay bill from a SEPA Credit Transfer file you submit to your bank.\n"
        "To enable sepa credit transfer, module account_sepa must be installed ")

    closing_date = fields.Date(string='Closing Date', copy=False)

    closing_payment_id = fields.Many2one(
        'account.payment',
        string="Payment", copy=False, readonly=True,
        help='used for custody purpose')

    # restriction purposes
    request_type = fields.Selection(string='Request Type', default='from_budget', selection=[(
        'from_budget', 'From Budget'), ('restriction', 'Form Restriction'), ])

    @api.onchange('department_id')
    def _onchange_department(self):
        for rec in self:
            if rec.department_id:
                if rec.department_id.analytic_account_id:
                    rec.analytic_account_id = rec.department_id.analytic_account_id.id
                else:
                    rec.analytic_account_id = False
            else:
                rec.analytic_account_id = False

    @api.onchange('closing_journal_id')
    def _onchange_journal(self):
        if self.closing_journal_id:
            # Set default payment method (we consider the first to be the default one)
            payment_methods = self.closing_journal_id.inbound_payment_method_ids
            self.closing_payment_method_id = payment_methods and payment_methods[0] or False
            # Set payment method domain (restrict to methods enabled for the journal and to
            #  selected payment type)
            payment_type = 'inbound'
            return {'domain': {'closing_payment_method_id': [('payment_type', '=', payment_type),
                                                             ('id', 'in', payment_methods.ids)]}}

        return {'domain': {'closing_payment_method_id': [('payment_type', '=', ''),
                                                         ('id', '=', 0)]}}

    @api.multi
    @api.constrains('total_amount', 'lines_ids', 'state')
    def _check_amount(self):
        for obj in self:
            if self._context.get('not_check_in_draft', False) and obj.state == 'draft':
                continue
            if obj.total_amount <= 0:
                raise ValidationError(_('''Total amount must be greater than zero'''))
            if obj.custody_total_amount > obj.custody_amount:
                raise ValidationError(
                    _('''custody lines amount can not be greater than custody total amount'''))

    @api.onchange('purpose')
    def _onchange_purpose(self):
        self.lines_ids = False

    @api.one
    @api.depends(
        'lines_ids.amount', 'state', 'custody_amount')
    def _compute_total(self):
        if self.purpose == 'expense':
            self.total_amount = sum(x.amount for x in self.lines_ids)
        if self.purpose == 'custodies':
            self.custody_total_amount = sum(x.amount for x in self.lines_ids)
            self.total_amount = self.custody_amount
            self.custody_residual_amount = self.custody_amount - self.custody_total_amount

    @api.multi
    def copy(self, default=None):
        return super(
            RequisitionRequest, self.with_context(
                {'not_check_in_draft': True})).copy(default)

    @api.multi
    def unlink(self):
        ''' delete request but they must be in draft or cancel state .
        '''
        for rec in self:
            if rec.state not in ['draft', 'cancel']:
                raise ValidationError(
                    _('You cannot delete a requisition request not in draft or cancel state.'))
        return super(RequisitionRequest, self).unlink()

    @api.multi
    def request(self):
        """
        change state to request
        """
        self.ensure_one()
        if self.purpose == 'expense':
            msg = _("waiting for service officer.")
        if self.purpose == 'custodies':
            msg = _("waiting for financial controller.")

        self.write({'state': 'requested'})
        self.message_post(body=msg)

    @api.multi
    def approve(self):
        """
        change state to approved
        """
        msg = _("waiting for department manager.")
        self.write({'state': 'approved'})
        self.message_post(body=msg)

    @api.multi
    def running(self):
        """
        change state to running
        """

        self.write({'state': 'running'})

    @api.multi
    def done(self):
        """
        change state to done and create budget confirmation
        """
        self.ensure_one()

        if not self.lines_ids:
            raise ValidationError(
                _(''' you have to enter details first '''))

        if self.purpose == 'custodies':
            if self.payment_id:
                if self.payment_id.state != 'posted':
                    raise ValidationError(
                        _(''' payment have to be confirmed first '''))

        if self.purpose == 'expense' and self.request_type == 'restriction':
            for line in self.lines_ids:
                if not line.restriction:
                    raise ValidationError(
                        _(''' you have to enter restriction for each line in the details '''))
            return self.post()

        for line in self.lines_ids:
            line.sudo().check_budget()

        budget_confirmation_obj = self.env['budget.confirmation']
        data = {
            'name': self.name,
            'date': self.date,
            'beneficiary_id': self.beneficiary_id.id,
            'department_id': self.department_id.id,
            'analytic_account_id': self.analytic_account_id.id,
            'user_id': self.user_id.id,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            'type': 'requisition.request',
            'ref': self.name,
            'res_model': 'requisition.request',
            'res_id': self.id,
            'description': self.description,
            'total_amount': sum(x.amount for x in self.lines_ids),
            'lines_ids': []
        }
        for line in self.lines_ids:
            date = self.date

            date = fields.Date.from_string(date)

            budget_lines = line.analytic_account_id.crossovered_budget_line.filtered(
                lambda x: x.service_id.id == line.service_id.id and
                x.crossovered_budget_id.state == 'done' and
                fields.Date.from_string(x.date_from) <= date and
                fields.Date.from_string(x.date_to) >= date)

            if budget_lines:
                budget_line_id = budget_lines[0].id
                remain = budget_lines[0].remain
                new_balance = remain - line.amount
                data['lines_ids'].append((0, 0, {
                    'service_id': line.service_id.id,
                    'amount': line.amount,
                    'analytic_account_id': line.analytic_account_id.id,
                    'description': line.description,
                    'budget_line_id': budget_line_id,
                    'remain': remain,
                    'new_balance': new_balance,
                }))
            else:
                raise ValidationError(
                    _(''' no budget for this service ''' + str(line.service_id.name)))

        self.budget_confirmation_id = budget_confirmation_obj.create(data)

        msg = _("waiting for budget confirmation to be approved.")
        self.write({'state': 'done'})
        self.message_post(body=msg)

    @api.multi
    def first_move_line_get(self, move_id, company_currency, current_currency):
        debit = credit = 0.0
        credit = self.custody_total_amount

        sign = debit - credit < 0 and -1 or 1

        if not self.company_id.default_custody_journal_id:
            raise ValidationError(_(''' please set expenses journal in settings '''))

        journal_id = self.company_id.default_custody_journal_id

        # set the first line
        move_line = {
            'name': self.name or '/',
            'debit': debit,
            'credit': credit,
            'account_id': self.custody_id.property_account_expense_id.id,
            'move_id': move_id,
            'journal_id': journal_id.id,
            'partner_id': self.beneficiary_id.commercial_partner_id.id,
            'currency_id': company_currency != current_currency and current_currency or False,
            'amount_currency': (sign * abs(self.custody_total_amount)  # amount < 0 for refunds
                                if company_currency != current_currency else 0.0),
            'date': self.date,
            'date_maturity': self.date,
            # 'payment_id': self.payment_id.id,
        }
        return move_line

    @api.multi
    def move_line_create(self, line_total, move_id, company_currency, current_currency):
        if not self.company_id.default_custody_journal_id:
            raise ValidationError(_(''' please set expenses journal in settings '''))

        journal_id = self.company_id.default_custody_journal_id

        for line in self.lines_ids:
            # create one move line per custody line where amount is not 0.0
            if not line.amount:
                continue
            line_subtotal = line.amount

            amount = line_subtotal
            move_line = {
                'journal_id': journal_id.id,
                'name': (line.service_id.name or '/') + ' ' + (line.description or '/'),
                'account_id': line.service_id.property_account_expense_id.id,
                'move_id': move_id,
                'partner_id': line.beneficiary_id.commercial_partner_id.id,
                'analytic_account_id': line.analytic_account_id and line.analytic_account_id.id or False,
                'quantity': 1,
                'credit': 0.0,
                'debit': abs(amount),
                'date': self.date,
                'amount_currency': line_subtotal if current_currency != company_currency else 0.0,
                'currency_id': company_currency != current_currency and current_currency or False,
                # 'payment_id': self.payment_id.id,
            }

            self.env['account.move.line'].create(move_line)

        return line_total

    @api.multi
    def account_move_get(self):

        if not self.company_id.default_custody_journal_id:
            raise ValidationError(_(''' please set expenses journal in settings '''))

        journal_id = self.company_id.default_custody_journal_id

        if self.name:
            name = self.name
        elif journal_id.sequence_id:
            if not journal_id.sequence_id.active:
                raise UserError(_('Please activate the sequence of selected journal !'))
            name = journal_id.sequence_id.with_context(ir_sequence_date=self.date).next_by_id()
        else:
            raise UserError(_('Please define a sequence on the journal.'))

        move = {
            'name': name,
            'journal_id': journal_id.id,
            'narration': self.description,
            'date': self.date,
            'ref': self.name,
        }
        return move

    @api.multi
    def create_move(self):
        '''
        done for the custody to create move and change custody state to done
        '''
        self.ensure_one()

        if self.purpose != 'custodies':
            return

        if not self.company_id.default_custody_journal_id:
            raise ValidationError(_(''' please set expenses journal in settings '''))

        journal_id = self.company_id.default_custody_journal_id

        local_context = dict(self._context, force_company=journal_id.company_id.id)

        ctx = local_context.copy()
        ctx['date'] = self.date
        ctx['check_move_validity'] = False

        company_currency = journal_id.company_id.currency_id.id
        current_currency = self.currency_id.id or company_currency

        # self.payment_id.write({'state': 'reconciled'})

        move = self.env['account.move'].create(self.account_move_get())

        move_line = self.env['account.move.line'].with_context(ctx).create(
            self.with_context(ctx).first_move_line_get(
                move.id, company_currency, current_currency))
        line_total = move_line.debit - move_line.credit

        # Create one move line per self line where amount is not 0.0
        line_total = self.with_context(ctx).move_line_create(
            line_total, move.id, company_currency, current_currency)

        self.write({'move_id': move.id, 'state': 'done'})

        move.post()

    @api.multi
    def budget_confirmed(self):
        """
        change state to budget_confirmed
        """
        self.write({'state': 'budget_confirmed'})
        self.post()

    @api.multi
    def post(self):
        """
        change state to posted and create invoice/move
        """
        self.ensure_one()
        if self.purpose == 'expense':
            self.create_invoice()
        if self.purpose == 'custodies':
            self.create_move()

        self.write({'state': 'posted'})

    @api.multi
    def re_request(self):
        """
        create new custody request with the amount of money used
        """
        self.ensure_one()
        new_id = self.copy(
            {'state': 'draft', 'custody_amount': self.custody_total_amount,
             'date': str(fields.date.today())})
        return new_id

    @api.multi
    def close_all(self):
        self.close(all_amount=True)

    @api.multi
    def close(self, all_amount=False):
        """
        create payment if there is a residual and change state to closed
        """
        self.ensure_one()

        if self.purpose == 'custodies':
            if self.payment_id:
                if self.payment_id.state != 'posted':
                    raise ValidationError(
                        _(''' payment have to be confirmed first '''))

        residual_amount = self.custody_residual_amount
        if all_amount:
            residual_amount = self.custody_amount

        if residual_amount > 0.0:
            payment_type = 'inbound'
            partner_type = 'customer'
            sequence_code = 'account.payment.customer.invoice'

            if not self.closing_payment_method_id:
                raise ValidationError(
                    _(''' you have to be enter payment method type first '''))

            if not self.closing_date:
                raise ValidationError(
                    _(''' you have to be enter closing date first '''))

            if not self.closing_journal_id:
                raise ValidationError(
                    _(''' you have to be enter closing journal first '''))

            name = self.env['ir.sequence'].with_context(
                ir_sequence_date=self.date).next_by_code(sequence_code)
            data = {
                'name': self.name,
                'payment_type': payment_type,
                'payment_method_id': self.closing_payment_method_id.id,
                'partner_type': partner_type,
                'partner_id': self.beneficiary_id.commercial_partner_id.id,
                'amount': residual_amount,
                'currency_id': self.currency_id.id,
                'payment_date': self.closing_date,
                'journal_id': self.closing_journal_id.id,
                'company_id': self.company_id.id,
                'communication': self.name,
                'custody_id': self.custody_id.id,
            }

            payment_id = self.env['account.payment'].create(data)
            payment_id.post()

            self.closing_payment_id = payment_id.id

        self.write({'state': 'closed'})

    @api.multi
    def get_invoice_lines(self):
        """
        prepare invoice lines from details lines
        for invoice creation
        """
        self.ensure_one()
        lines = self.lines_ids

        lines = []
        for x in self.lines_ids:
            account_id = x.service_id.property_account_expense_id.id
            if self.request_type == 'restriction' and x.restriction:
                if not x.service_id.account_restricted_expense_id:
                    raise ValidationError(
                        _(''' please set restricted expense account in settings '''))
                account_id = x.service_id.account_restricted_expense_id.id

            lines.append({
                'name': x.description,
                'product_id': x.service_id.id,
                'service_id': x.service_id.id,
                'account_id': account_id,
                'price_unit': x.amount,
                'quantity': 1,  # only one service
                'account_analytic_id': x.analytic_account_id.id,
            })

        lines = [(0, 0, x) for x in lines]
        return lines

    @api.multi
    def create_invoice(self):
        """
        create invoice for the current request
        """
        self.ensure_one()
        lines = self.get_invoice_lines()

        journal_id = False

        if self.purpose == 'expense':
            if not self.company_id.default_expense_journal_id:
                raise ValidationError(_(''' please set expenses journal in settings '''))
            journal_id = self.company_id.default_expense_journal_id.id

        company_id = self.company_id.id
        p = self.beneficiary_id if not company_id else self.beneficiary_id.with_context(
            force_company=company_id)

        rec_account = p.property_account_receivable_id
        pay_account = p.property_account_payable_id
        if not rec_account and not pay_account:
            raise ValidationError(
                _(''' please set Beneficiary's payable and receivable accounts first '''))

        restriction = self.request_type == 'restriction'
        data = {'name': self.name, 'reference': self.name, 'type': 'in_invoice',
                'default_type': 'in_invoice', 'journal_type': 'purchase', 'date': self.date,
                'date_invoice': self.date, 'date_due': self.date, 'narration': self.description,
                'company_id': self.company_id.id, 'currency_id': self.currency_id.id,
                'partner_id': self.beneficiary_id.id, 'journal_id': journal_id,
                'account_id': self.beneficiary_id.property_account_payable_id.id,
                'invoice_line_ids': lines, 'res_model': 'requisition.request', 'res_id': self.id,
                'restricted': restriction}
        self.invoice_id = self.env['account.invoice'].create(data).id

    @api.multi
    def cancel(self):
        """
        change state to cancel
        """
        self.write({'state': 'cancel'})

    @api.multi
    def to_draft(self):
        """
        change state to draft
        """
        self.write({'state': 'draft'})


class RequisitionRequestLine(models.Model):
    _name = 'requisition.request.line'
    _description = 'requisition request details'

    request_id = fields.Many2one('requisition.request', string='Requisition Request',
                                 ondelete='cascade', index=True)

    beneficiary_id = fields.Many2one(comodel_name='res.partner',
                                     string='Beneficiary')

    purpose = fields.Selection(string='Purpose', selection=[(
        'expense', 'Expense'), ('custodies', 'Custodies'), ])

    department_id = fields.Many2one(
        comodel_name='hr.department', required=True, string='Requesting Party')

    initiative_id = fields.Many2one(related='service_id.initiative_id',
                                    comodel_name='initiative',
                                    string='initiative',
                                    store=True)

    service_id = fields.Many2one(
        comodel_name='product.product', string='Service',
        required=True,
        domain=[('type', '=', 'service'),
                ('nature', 'in', ['expense', 'custody'])])

    amount = fields.Float(string='Amount',
                          digits=dp.get_precision('Product Price'),
                          help="Total amount in services request line",
                          required=True)

    analytic_account_id = fields.Many2one('account.analytic.account',
                                          'Analytic Account',
                                          required=True)

    company_id = fields.Many2one(
        'res.company', string='Company', related='request_id.company_id', store=True, readonly=True,
        related_sudo=False)

    currency_id = fields.Many2one(
        'res.currency', related='request_id.currency_id', store=True, related_sudo=False)

    description = fields.Text(string='Description')

    restriction = fields.Many2one(comodel_name='donation.request',
                                  string='Restriction', domain=[('state', '=', 'done')])

    # @api.multi
    # @api.constrains('service_id', 'department_id')
    # def _check_service_department(self):
    #     for obj in self:
    #         exist = []
    #         print("..................obj.request_id.lines_ids", obj.request_id.lines_ids)
    #         for sib in obj.request_id.lines_ids:
    #             if (sib.service_id.id, sib.department_id.id) in exist:
    #                 raise ValidationError(
    #                     _('''services can not be duplicated for this Requesting Party'''))
    #             else:
    #                 exist.append((sib.service_id.id, sib.department_id.id))

    @api.multi
    @api.constrains('amount')
    def _check_amount(self):
        for obj in self:
            if obj.amount <= 0:
                raise ValidationError(
                    _('''amount must be greater than zero for service : ''' + obj.service_id.name))

    @api.onchange('analytic_account_id')
    def _onchange_analytic_account_id(self):
        for line in self:
            line.service_id = False

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

    @api.multi
    def check_budget(self):
        '''
        check the available budget for given service and analytic amount
        in defined period of time
        '''
        self.ensure_one()
        service_id = self.service_id.id
        analytic_account_id = self.analytic_account_id
        date = self.request_id.date

        date = fields.Date.from_string(date)

        budget_lines = analytic_account_id.crossovered_budget_line.filtered(
            lambda x: x.service_id.id == service_id and
            x.crossovered_budget_id.state == 'done' and
            fields.Date.from_string(x.date_from) <= date and
            fields.Date.from_string(x.date_to) >= date)

        if budget_lines:
            remain = budget_lines[0].remain
            if remain >= self.amount:
                return True

        raise ValidationError(_(''' no enough budget ''' + str(self.service_id.name)))
