from datetime import datetime as dt
from dateutil import relativedelta
from datetime import datetime, timedelta
from odoo import models, fields, api, exceptions
from odoo.tools.translate import _
from odoo.exceptions import ValidationError
from num2words import num2words
from hijri_converter import convert


# Hr_Employee
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # iqama fields in employee view
    iqama_creat_date = fields.Date(related='iqama_number.issue_date', readonly=True, default=fields.date.today())
    iqama_expiy_date = fields.Date(related='iqama_number.expiry_date', readonly=True)
    name_as_pass = fields.Char('Name(As in Passport)')
    employee_code = fields.Char()
    arabic_name = fields.Char()
    work_fax = fields.Char('Work Fax')
    serial_num = fields.Char('Serial No.')
    grade = fields.Char()
    is_head = fields.Boolean('Is Head  of Function')
    is_line_man = fields.Boolean('Is Line Manager')

    is_calender = fields.Boolean(default=False)
    spouse_no = fields.Char('Spouse Phone No.')
    joining_date = fields.Date('Joining Date')
    leaving_date = fields.Date()
    serv_year = fields.Char('Total Service Year', store=True, force_save=True)
    vendor_no = fields.Char("Vendor No")
    mol_no = fields.Char("MOL No")
    # iban = fields.Char("IBAN")
    bank_code = fields.Char("Bank Code", related="bank_account_id.bank_id.name")
    bank_account_id = fields.Many2one(
        'res.partner.bank', 'Bank Account Number',
        domain="[('partner_id', '=', address_home_id)]",
        groups="hr.group_hr_user",
        help='Employee bank salary account')
    issue = fields.Date("Issue Date")
    expiry = fields.Date("Expiry Date", )
    # passport fields to private information page
    date_issuance_passport = fields.Date(related="passport_id.issue_date", readonly=True, default=fields.date.today())
    expiration_date_passport = fields.Date(related="passport_id.expiry_date", readonly=True,
                                           default=fields.date.today())
    place_issuance_passport = fields.Char(related="passport_id.place_issue_id", readonly=True,
                                          default=fields.date.today())

    # related fields if employee is saudi
    date_issuance_saudi_id = fields.Date(related="saudi_number.issue_date", readonly=True, default=fields.date.today())
    expiration_date_saudi_id = fields.Date(related="saudi_number.expiry_date", readonly=True,
                                           default=fields.date.today())
    place_issuance_saudi_id = fields.Char(related="saudi_number.place_issue_id", readonly=True,
                                          default=fields.date.today())

    own_license = fields.Boolean()

    depend = fields.Boolean("Have Dependent")
    fn = fields.Char("First Name")
    mn = fields.Char("Middle Name")
    ln = fields.Char("Last Name")
    bg = fields.Char("Blood Group")
    a_email = fields.Char("Alternate Email ID")
    airport = fields.Char("Nearest Airport")

    first_hiring_date = fields.Date(string='Start Hiring Date')
    # duration_in_months = fields.Float(compute='_get_months_no')
    contact_no = fields.Char("Contact No")
    reason = fields.Char(string="Reason")
    r_name = fields.Char("Name")

    # fields of page work infrmation in note book in employees view
    emp_no = fields.Char(string="Employee number", track_visibility='always')
    english_name = fields.Char(string="English Name")
    home_no = fields.Char()
    present_address = fields.Char()
    work_location = fields.Char()
    direct_emp = fields.Selection(selection=[('yes', 'direct employee'), ('no', 'not direct employee')], default="yes")
    is_marketer = fields.Boolean(string='marketer?')

    finger_print = fields.Boolean()

    payment_method = fields.Selection(selection=[('cash', 'cash'), ('bank', 'bank')], default="cash")

    # fields of page private information in notebook in employees view
    religion = fields.Selection(selection=[('muslim', 'Muslim'), ('christian', 'Christian'), ('other', 'Other')])
    blood_type = fields.Selection(
        [('o-', 'O-'), ('o+', 'O+'), ('A-', 'A-'), ('A+', 'A+'), ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'),
         ('AB+', 'AB+')])
    employee_from = fields.Selection(selection=[('citizen', 'Citizen'), ('other', 'Other')], default="citizen")
    entry_date_ksa = fields.Date(attrs="{'invisible':[('employee_from','=','citizen)]'}")
    visa_number = fields.Char()
    number_child = fields.Integer()
    place_birth = fields.Char()
    state = fields.Selection(selection=[('draft', _('Draft')),
                                        ('complete', _('Complete Data')),
                                        ('open', _('Create Contract')),
                                        ('out_of_service', _('Out of service'))],
                             default="draft", track_visibility='always')

    # fields of hr settings page in notebook
    vihcle = fields.Char()
    vihcle_distance = fields.Integer()
    attendance = fields.Selection(selection=[('present', 'Present'), ('Apsent', 'Apsent')], default="present")
    active = fields.Boolean(default=True)
    Employee_type = fields.Selection(
        selection=[('employee', 'Employee'), ('worker', 'worker'), ('sales person', 'Sales Person')],
        default='employee')
    medical_exam_check = fields.Boolean()
    is_cordinator = fields.Boolean()
    is_revisor = fields.Boolean()
    is_evaluation_manager = fields.Boolean()
    evaluator_membership_no = fields.Char()

    # Fields of iqama and health
    medical_insuranc = fields.Boolean()
    medical_class = fields.Selection(selection=[('vip', 'vip'), ('a', 'A'), ('b', 'B'), ('c_senior', 'C senior')])
    medical_membership_no = fields.Char()
    medical_membership_exp = fields.Date()
    medical_exam_file = fields.Binary()
    filename = fields.Char()

    # Relational fields
    address_home_id = fields.Many2one('res.partner', 'Private Address', help='',
                                      groups="hr.group_hr_user")  # private partner
    # sick leaves page
    saudi_number = fields.Many2one('hr.employee.document', domain=[('document_type', '=', 'saudi')],
                                   track_visibility='always')
    passport_id = fields.Many2one('hr.employee.document', domain=[('document_type', '=', 'passport')],
                                  track_visibility='always')
    p_state_id = fields.Many2one(comodel_name='res.country.state', string="Fed. State")
    r_manager = fields.Many2one(comodel_name='hr.employee', string="Reporting Manager")
    dependent_id = fields.One2many('hr.dependent', 'dependent_relation', string="Dependent")
    qualifiction_id = fields.One2many('hr.qualification', 'qualification_relation_name', string="Qualifications")
    certification_id = fields.One2many('hr.certification', 'certification_relation', string="Certification")
    insurance_id = fields.One2many('hr.insurance', 'insurance_relation', string="Insurance")
    trainings_id = fields.One2many('hr.trainings', 'employee_id', string="Trainings")
    other_asset = fields.Many2many('maintenance.equipment', string='Other Assets')
    project = fields.Many2one(comodel_name='projects.projects')
    employment_history_ids = fields.One2many(comodel_name='hr.employee.history', inverse_name='employement_history')
    attachment_ids = fields.One2many('ir.attachment', 'employee_attaches_id')
    head = fields.Many2one(comodel_name='hr.employee', string='Head of Function')
    line_man = fields.Many2one(comodel_name='hr.employee', string='Line Manager')
    performence_manager = fields.Many2one(comodel_name='hr.employee', string='Performance Manager')
    office = fields.Many2one(comodel_name='office.office')
    iqama_number = fields.Many2one(comodel_name='hr.employee.document', domain=[('document_type', '=', 'Iqama')],
                                   track_visibility='always')

    country_id = fields.Many2one('res.country', 'Nationality (Country)',
                                 groups="base.group_user")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], groups="base.group_user", default="male")
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="base.group_user", default='single')

    base_salary = fields.Float(compute='compute_base_salary')
    salary_in_words = fields.Char(compute='get_salary_amount')
    payslip_lines = fields.One2many(comodel_name='hr.payslip.line', compute='compute_base_salary')

    @api.multi
    def change_current_date_hijri(self):
        year = datetime.now().year
        day = datetime.now().day
        month = datetime.now().month
        hijri_date = convert.Gregorian(year, month, day).to_hijri()
        return hijri_date

    @api.depends('base_salary')
    def get_salary_amount(self):
        for item in self:
            item.salary_in_words = num2words(item.base_salary, lang=self.env.user.lang)

    @api.multi
    def compute_base_salary(self):
        for item in self:
            last_day_of_prev_month = datetime.now().date().replace(day=1) - timedelta(days=1)
            start_day_of_prev_month = datetime.now().date().replace(day=1) - timedelta(days=last_day_of_prev_month.day)

            payroll = item.env['hr.payslip'].search(
                [('employee_id', '=', item.name), ('date_from', '<=', datetime.now().date()),
                 ('date_to', '>=', datetime.now().date()), ('contract_id', '=', item.contract_id.id)])
            if not payroll:
                payroll = item.env['hr.payslip'].search(
                    [('employee_id', '=', item.name), ('date_from', '<=', start_day_of_prev_month),
                     ('date_to', '>=', last_day_of_prev_month), ('contract_id', '=', item.contract_id.id)])

            item.base_salary = payroll.total_allowances
            item.payslip_lines = payroll.allowance_ids.filtered(
                lambda r: r.salary_rule_id.rules_type in ('salary', 'house')).sorted(lambda b: b.name)

    ### National address ###
    addres_city = fields.Many2one('addres.city')
    addres_region = fields.Many2one('addres.region')
    street = fields.Char()
    building_number = fields.Char()
    postal_code = fields.Char()
    extra_number = fields.Char()
    property_type = fields.Char()
    drug_type = fields.Selection([('property', 'Property'), ('rent', 'Rent')], default="rent")
    apartment_number = fields.Char()

    @api.model
    def create(self, vals):
        new_record = super(HrEmployee, self).create(vals)
        update_list = []
        if vals.get('passport_id', False):
            update_list.append(vals.get('passport_id', False))

        if vals.get('iqama_number', False):
            update_list.append(vals.get('iqama_number', False))

        if vals.get('saudi_number', False):
            update_list.append(vals.get('saudi_number', False))

        if vals.get('license_number_id', False):
            update_list.append(vals.get('license_number_id', False))

        if vals.get('copy_examination_file', False):
            update_list.append(vals.get('copy_examination_file', False))

        if update_list:
            documents_ids = self.env['hr.employee.document'].browse(update_list)
            documents_ids.write({'employee_ref': new_record.id})
        return new_record

    @api.constrains('emp_no')
    def e_unique_field_name_constrains(self):
        for item in self:
            items = self.search([('emp_no', '=', item.emp_no)])
            if len(items) > 1:  # return more than one item with the same value
                  raise ValidationError(_('You cannot create Employee with the same employee number'))

    @api.onchange('department_id')
    def onchange_department_id(self):
        if self.department_id:
            self.department = self.department_id

    @api.onchange('line_man')
    def onchange_line_man(self):
        self.r_manager = self.line_man

    @api.multi
    @api.depends('first_hiring_date', 'leaving_date')
    def _get_months_no(self):
        for employee in self:
            try:
                join_date = datetime.datetime.strptime(employee.first_hiring_date, "%Y-%m-%d")
                to_date = datetime.datetime.strptime(employee.leaving_date, '%Y-%m-%d')
                # current_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
                employee.duration_in_months = (to_date.year - join_date.year) * 12 + to_date.month - join_date.month
            except:
                employee.duration_in_months = 0.0

    @api.multi
    def draft_state(self):
        for item in self:
            state = item.state

            # Check if the employee contract is End
            if state == 'out_of_service':
                if item.contract_id:
                    if item.contract_id.state == 'end_contract':
                        raise exceptions.Warning(_('Please Re-contract ,because the contract in End contract state'))

            item.state = "draft"

    @api.multi
    def complete_state(self):
        self.state = "complete"

    # create contract
    @api.multi
    def create_contract(self):
        if self.contract_id:
            raise exceptions.Warning(_('You have already a contract'))
        else:
            seq = self.env['ir.sequence'].next_by_code('hr.contract') or '/'
            action = self.env.ref('hr_contract.action_hr_contract')
            result = action.read()[0]
            result['views'] = [(self.env.ref('hr_contract.hr_contract_view_form').id, 'form')]
            # override the context to get rid of the default filtering
            result['context'] = {'default_name': seq, 'default_employee_id': self.id}
            result.update({'view_type': 'form',
                           'view_mode': 'form',
                           'target': 'current'})

        self.state = "open"
        return result

    # Change state to open if there is a contract
    @api.multi
    def open_sate(self):
        for item in self:
            if item.contract_id:
                item.state = 'open'
            else:
                raise exceptions.Warning(_('Employee %s has no contract') % item.name)

    @api.onchange('first_hiring_date', 'leaving_date')
    def onchange_dates(self):
        if self.first_hiring_date:
            if self.leaving_date:
                start_date_1 = dt.strptime(self.first_hiring_date, "%Y-%m-%d")
                end_date_1 = dt.strptime(self.leaving_date, "%Y-%m-%d")
                if end_date_1 > start_date_1:
                    r = relativedelta.relativedelta(end_date_1, start_date_1)
                    if r.years > 0:
                        years = r.years
                        months = r.months
                        self.serv_year = "%s Years %s Months" % (years, months)
                    else:
                        years = r.years
                        months = r.months
                        self.serv_year = "%s Months" % months
                else:
                    raise exceptions.Warning(
                        _('Leaving Date  must be greater than First Hiring Date'))

            elif not self.leaving_date:
                start_date_1 = dt.strptime(self.first_hiring_date, "%Y-%m-%d")
                end_date_1 = datetime.now().date()

                if start_date_1:
                    r = relativedelta.relativedelta(end_date_1, start_date_1)
                    if r.years > 0:
                        years = r.years
                        months = r.months
                        self.serv_year = "%s Years %s Months" % (years, months)
                    else:
                        years = r.years
                        months = r.months
                        self.serv_year = "%s Months" % months

    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))
        return super(HrEmployee, self).unlink()


class Attachment(models.Model):
    _inherit = 'ir.attachment'
    employee_attaches_id = fields.Many2one(comodel_name='hr.employee')


class Trainings(models.Model):
    _name = 'hr.trainings'
    _rec_name = 'training_sum'

    training_sum = fields.Char('Training Summary')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    type_training = fields.Char('Type of Training')
    training_company = fields.Char('Training Company')
    training_place = fields.Char('Training Place')
    status = fields.Char()
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Training Relation')


class Religion(models.Model):
    _name = 'hr.religion.religion'
    _rec_name = 'name'
    name = fields.Char(required=True)


class Relation(models.Model):
    _name = 'hr.relation.relation'
    _rec_name = 'name'
    name = fields.Char(required=True)


class college(models.Model):
    _name = 'hr.college'
    _rec_name = 'name'
    name = fields.Char(required=True)


class Qualification(models.Model):
    _name = 'hr.qualification'
    _rec_name = 'uni_name'

    uni_name = fields.Many2one(comodel_name='office.office', string='University Name', required=True)
    col_name = fields.Many2one(comodel_name='hr.college', string='College Name')
    prg_status = fields.Char('Program Status')
    comp_date = fields.Date('Completion Date')
    contact_name = fields.Char('Contact Name')
    contact_phn = fields.Char('Contact Phone No')
    contact_email = fields.Char('Contact Email')
    country_name = fields.Many2one(comodel_name='res.country')
    qualification_degree = fields.Selection(
        [('weak', _('Weak')), ('good', _('Good')), ('very_good', _('Very Good')), ('excellent', _('Excellent'))])
    qualification_specification_id = fields.Many2one(comodel_name='qualification.specification')

    # relation field
    qualification_relation_name = fields.Many2one(comodel_name='hr.employee')


class hr_employee_history(models.Model):
    _name = 'hr.employee.history'
    employement_history = fields.Many2one(comodel_name='hr.employee')
    name = fields.Char(required=True)
    position = fields.Char(required=True)
    employeer = fields.Char(required=True)
    salary = fields.Float(required=True)
    address = fields.Char(required=True)
    date_from = fields.Date()
    date_to = fields.Date()
    country = fields.Many2one(comodel_name='res.country')


class Payslip(models.Model):
    _name = 'employee.payslip'

    payslip = fields.Char()
    date = fields.Date()


class Project(models.Model):
    _name = 'projects.projects'
    _rec_name = 'name'
    name = fields.Char()


class Qualification_Specification(models.Model):
    _name = 'qualification.specification'
    name = fields.Char()


# Hr_job
class HrJob(models.Model):
    _inherit = 'hr.job'

    employee_ids = fields.One2many('hr.employee', 'job_id', string='Employees', domain=[('state', '=', 'open')])
    department_ids = fields.Many2many('hr.department', string='Departments')


# Hr_Department
class HrDepartment(models.Model):
    _inherit = 'hr.department'

    employee_ids = fields.One2many('hr.employee', 'department_id', string='Employees', domain=[('state', '=', 'open')])

    job_ids = fields.Many2many('hr.job', string='Jobs')
    email_manager = fields.Char(string='Email Manager', related='manager_id.work_email')


class addres_city(models.Model):
    _name = 'addres.city'
    name = fields.Char()


class addres_region(models.Model):
    _name = 'addres.region'
    name = fields.Char()

class HrAttendances(models.Model):
    _inherit = 'resource.calendar'

    permission_hours = fields.Integer()
    permission_number = fields.Integer()
    work_days = fields.Integer()
    work_hour = fields.Integer()
    overtime_factor_daily = fields.Float(string='Overtime Factor Daily')
    overtime_factor_holiday = fields.Float(string='Overtime Factor Holiday')
    max_overtime_hour = fields.Integer()


