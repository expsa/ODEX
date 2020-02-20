from odoo import models, fields, api, _, exceptions
import datetime
from datetime import timedelta
from dateutil import relativedelta
from datetime import datetime as dt
from textblob import TextBlob
from hijri_converter import convert



# Contract
class Contract(models.Model):
    _inherit = 'hr.contract'

    state = fields.Selection(selection=[('draft', _('Draft')),
                                        ('employeed_aproval', _('Employeed Approval')),
                                        ('hr_head_approval', _('Hr Head Approval')),
                                        ('program_directory', _('Program Directory')),
                                        ('end_contract', _('End Contract'))], default="draft")

    active = fields.Boolean(default=True)
    employee_name = fields.Char(related="employee_id.name", readonly=True)
    employee_type = fields.Selection(selection=[('saudi', _('Saudi')),('foreign', _('Foreign')), 
                                    ('external', _('Outsource1')),('external2', _('Outsource2'))], default='saudi',track_visibility='always')
    contract_status = fields.Selection(selection=[('single', _('single contract')),
                                                  ('marriage', _('marriage contract'))], default='single',track_visibility='always')
    contract_duration = fields.Selection( selection=[('none', _('None')),
                                                     ('12_months', _('12 Months')),
                                                     ('24_months', _('24 Months'))], default='12_months')
    experience_year = fields.Integer()
    has_end_service_benefit = fields.Boolean(string='Has end service benefits')

    # fields on salary information page
    suspended = fields.Boolean(string='Suspended')
    social_insurance = fields.Boolean(string='Social Insurance')
    salary = fields.Float(string='Base Salary',track_visibility='always')

    # fields of information page
    wage = fields.Float()
    advatages = fields.Text()
    trial_date_start = fields.Date(track_visibility='always')
    trial_date_end = fields.Date(track_visibility='always')
    date_start = fields.Date(track_visibility='always')
    date_end = fields.Date(track_visibility='always')
    note = fields.Text()
    # fields of dependent page
    wife_husband = fields.Char()
    employee_code = fields.Char()
    allow_mbl = fields.Boolean(string='Allow Mobile Allowance')
    sign_bonous = fields.Boolean(string='Sign on Bounus')
    loan_allow = fields.Boolean(string='Allow Loan Allowance')
    air_allow = fields.Boolean(string='Air Allowance')
    adults = fields.Integer(string='Adult(s)')
    # children = fields.Integer()
    infants = fields.Integer()
    package = fields.Float()
    gosi = fields.Boolean(string='GOSI')
    #vehicle_attendance = fields.Integer(string='Vehicle Attendance')
    #system_attendance = fields.Integer(string='System Attendance')
    #line_manager_attendance = fields.Integer(string='Line Manager Attendance')
    #expense_claim = fields.Float(string='Expense Claim')
    #hr_visa_ticket = fields.Float(string='HR Visa/Ticket')
    #other_allowances = fields.Float(string='Other Allowances')
    #advance_salary = fields.Float(string='Advance AGT Salary')
    hr_expense = fields.Float(string='Hr Expense')
    cash_sales = fields.Float(string='Cash Sales')
    traffic_fine = fields.Float(string='Traffic Fine')
    bk_balance = fields.Float(string='Bank Balance')
    other_deductions = fields.Float(string='Other Deductions')

    fn = fields.Char(string="First Name")
    ln = fields.Char(string="Last Name")
    dn = fields.Char(string="Display Name")
    e_date = fields.Date(string="Effective Date")

    status = fields.Selection(selection=[('bachelor', 'Bachelor'), ('family', 'family')], string='Status')
    hra = fields.Char("HRA")
    t_allow = fields.Float(string="Transport Allowance")
    f_allow = fields.Float(string="Food Allowance")
    f_ot = fields.Float(string="Fixed OT")
    departure = fields.Char(string="Departure Air Port")
    destination = fields.Char(string="Destination Air Port")
    medical = fields.Selection(selection=[('yes', 'Yes'), ('no', 'No')], string='Medical')

    c_accommodation = fields.Selection(selection=[(
        'yes', 'Yes'),
        ('no', 'No')], string='Company Accommodation')

    c_vehicle = fields.Selection(selection=[(
        'yes', 'Yes'),
        ('no', 'No')], string='Company Vehicle')

    c_vacation = fields.Selection(selection=[(
        '12', '12 Months'),
        ('18', '18 Months'),
        ('24', '24 Months')], string='Contractual Vacation')

    nod = fields.Selection(selection=[(
        '12', '12 Months'),
        ('18', '18 Months'),
        ('24', '24 Months')], string='Number of days')

    probation = fields.Selection(selection=[(
        '3', '3 Months'),
        ('6', '6 Months')], string='Probation')

    dependent = fields.Selection(selection=[(
        '1', '1+1 '),
        ('2', '1+2 '),
        ('3', '1+3 '),
        ('all', 'All ')], string='Dependent')

    incentive = fields.Selection(selection=[(
        'yes', 'Yes'),
        ('no', 'No')], string='Incentive')

    monthly_salary = fields.Float(string='Monthly Salary', compute='_compute_monthly_salary')
    saudi_emp_type = fields.Selection([('saudi-contract', _('Saudi Contracting')),
                                       ('saudi-non', _('Saudi Non-Contracting'))], _('Saudi Employee Type'),
                                      default='saudi-contract')

    contract_type = fields.Selection([('local', _('Local')), ('international', _('International'))], _('Contract Type'))

    contract_description = fields.Selection([('locum', _('LOCUM')), ('permanent', _('Permanent'))],
                                            _('Contract Description'), default='locum')

    house_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                            _('House Allowance Type'), default='none')
    house_allowance = fields.Float(_('House Allowance'))
    salary_insurnce = fields.Float(string='Salary Insurnce')
    overtime_eligible = fields.Selection([('yes', _('Yes')), ('no', _('No'))],
                                         _('Overtime Eligibility'), default='no')
    overtime_eligible_float = fields.Float(_('Overtime Eligibility Amount'))
    exit_and_return = fields.Selection([('yes', _('Yes')), ('no', _('No'))], _('Exit and Return'), default='no')
    exit_and_return_amount = fields.Float(_('Exit and Return Amount'), default=200)

    air_ticket_eligible = fields.Selection([('yes', _('Yes')), ('no', _('No'))],
                                           _('Air Ticket Eligible'), default='no')
    annual_leave = fields.Selection([('yes', 'Yes'),
                                     ('no', 'No'),
                                     ], string='Annual Leave', default="no")

    annual_leave_days = fields.Float(string='Annual Leave In Days')

    transport_allowance_type = fields.Selection(
        [('none', _('None')), ('perc', _('Percentage')), ('num', _('Number')), ('company', 'By Company')],
        _('Transportation Allowance Type'), default='none')
    transport_allowance = fields.Float(_('Transportation Allowance'))

    transport_allowance_temp = fields.Float(string='Transportation Allowance', compute='_get_amount')

    field_allowance_type = fields.Selection(
        [('none', _('None')), ('perc', _('Percentage')), ('num', _('Number')), ('company', 'By Company')],
        _('Field Allowance Type'), default='none')
    field_allowance = fields.Float(_('Field Allowance'))

    field_allowance_temp = fields.Float(string='Field Allowance', compute='_get_amount')

    special_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                              _('Special Allowance Type'), default='none')
    special_allowance = fields.Float(_('Special Allowance'))
    special_allowance_temp = fields.Float(_('Special Allowance'), compute='_get_amount')

    other_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                            _('Other Allowances Type'), default='none')
    other_allowance = fields.Float(_('Other Allowances'))
    other_allowance_temp = fields.Float(_('Other Allowances'), compute='_get_amount')

    travel_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                             _('Travel Allowance Type'), default='none')
    travel_allowance = fields.Float(_('Travel Allowance'))
    travel_allowance_temp = fields.Float(_('Travel Allowance'), compute='_get_amount')
    education_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                                _('Education Allowance Type'), default='none')
    education_allowance = fields.Float(_('Education Allowance'))
    education_allowance_temp = fields.Float(_('Education Allowance'), compute='_get_amount')

    food_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                           _('Food Allowance Type'), default='none')
    food_allowance2 = fields.Float(_('Food Allowance'))
    food_allowance2_temp = fields.Float(_('Food Allowance'), compute='_get_amount')

    security_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                               _('Security Allowance Type'), default='none')
    security_allowance = fields.Float(_('Security Allowance'))
    security_allowance_temp = fields.Float(_('Security Allowance'), compute='_get_amount')
    communication_allowance_type = fields.Selection(
        [('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
        _('Communication Allowance Type'), default='none')
    communication_allowance = fields.Float(_('Communication Allowance'))
    communication_allowance_temp = fields.Float(_('Communication Allowance'), compute='_get_amount')

    retire_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                             _('Retire Allowance Type'), default='none')
    retire_allowance = fields.Float(_('Retirement Allowance'))

    infect_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                             _('Infection Allowance Type'), default='none')
    infect_allowance = fields.Float(_('Infection Allowance'))
    supervision_allowance_type = fields.Selection(
        [('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
        _('Supervision Allowance Type'), default='none')
    supervision_allowance = fields.Float(_('Supervision Allowance'))
    insurance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                      _('Insurance Type'), default='none')
    insurance = fields.Float(_('Insurance'))
    other_deduction_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                            _('Other Deductions Type'), default='none')
    other_deduction = fields.Float(_('Other Deductions'))
    gosi_deduction = fields.Float(compute="_calculate_gosi", string='Gosi (Employee Percentage)')
    gosi_employer_deduction = fields.Float(compute="_calculate_gosi", string='Gosi (Employer Percentage)')
    total_gosi = fields.Float(compute="_calculate_gosi", string='Total')
    is_gosi_deducted = fields.Selection([('yes', _('Yes')), ('no', _('No'))], default='yes')
    blood_type = fields.Selection(
        [('O-', 'O−'), ('O+', 'O+'), ('A-', 'A−'), ('A+', 'A+'), ('B-', 'B−'), ('B+', 'B+'), ('AB-', 'AB−'),
         ('AB+', 'AB+')], 'Blood Type')

    religion = fields.Selection([('muslim', _('Muslim')), ('christian', _('Christian')), ('other', _('Other'))],
                                _('Religion'))
    gender = fields.Selection([('male', _('Male')), ('female', _('Female'))],
                              _('Gender'))

    birth_place = fields.Char(_('Birth Place'))

    point_of_hire = fields.Char(_('Point of hire'))
    city = fields.Char(_('City Hired From'))
    country = fields.Char(_('Country Hired From'))
    contact_address = fields.Char(_('Contact address'), size=512)

    date_of_birth = fields.Date(_('Date Of Birth'))
    marital = fields.Selection(
        [('single', _('Single')), ('married', _('Married')), ('widower', _('Widower')), ('divorced', _('Divorced'))],
        _('Marital Status'), default='single')
    mobile_no = fields.Char(_('Mobile No'))
    p_o_box_no = fields.Char(_('P. O. Box'))
    zip_code = fields.Char(_('Zip Code'))
    saudi_id_iqama = fields.Char(_('Saudi ID / Iqama Number'))
    saudi_id_iqama_date = fields.Date(_('Saudi ID / Iqama Issue Date'))
    saudi_id_iqama_expiry = fields.Date(_('Saudi ID / Iqama Expiry Date'))
    passport_number = fields.Char(_('Passport number'))
    passport_issue_date = fields.Date(_('Passport Issue Date'))
    passport_expiry_date = fields.Date(_('Passport Expiry Date'))
    passport_issue_place = fields.Char(_('Passport Issue Place'))
    saudi_com_number = fields.Char(_('Saudi Commission Number'))
    saudi_com_date = fields.Date(_('Saudi Commission Issue Date'))
    saudi_com_expiry_date = fields.Date(_('Saudi Commission Expiry Date'))
    bls_date = fields.Date(_('BLS Date'))
    acls_date = fields.Date(_('ACLS Date'))
    insurance_date = fields.Date(_('Insurance Date'))
    specialty = fields.Char(_('Specialty'))
    category = fields.Char(_('Category'))
    effective_from = fields.Date(_('Effective From'))
    to_contact = fields.Text(_('To contact in case of Emergency'))
    emp_type = fields.Selection([('saudi', _('Saudi')), ('other', _('Foreign')), 
                                ('external', _('Outsource1')),('external2', _('Outsource2'))], _('Employee Type'))
    appraisal = fields.Boolean(_('Appraisal'))
    re_contract = fields.Boolean(_('re contract'))
    contract_draft = fields.Boolean(_('Contract Draft'))
    breakdown_allowance = fields.Float(compute="_cal_allowance", string='Breakdown Allowance')
    car_allowance = fields.Float(_('Car Allowance'))
    ticket_allowance = fields.Float(_('Ticket Allowance'))
    medical_ins_allowance = fields.Float(_('Medical Insurance Allowance'))
    medical_ins_issue_date = fields.Date(_('Medical Insurance Issue Date'))
    medical_ins_exp_date = fields.Date(_('Medical Insurance Expiry Date'))
    join_date = fields.Date(_('Join Date'))
    driving_lic_issue_date = fields.Date(_('Driving License Issue Date'))
    driving_lic_exp_date = fields.Date(_('Driving License Expiry Date'))
    driving_lic_issue_place = fields.Char(_('Driving License Issue Place'))
    dependants_ticket_amount = fields.Float(string='Dependants Ticket Amount', compute='_get_dependants_ticket_amount')
    air_ticket_amount = fields.Float(string='Air Ticket Amount')
    air_ticket_number = fields.Integer(string='Air Ticket No.')
    total_air_ticket_amount = fields.Float(string='Total Air Ticket Amount', compute='_get_total_ticket_amount')
    trial_duration = fields.Float(string='Trail Duration', compute='_compute_contract_duration')
    contract_duration_cal = fields.Float(string='Contract Duration', compute='_compute_contract_duration')

    # Relational fields
    job_id = fields.Many2one(related="employee_id.job_id", readonly=True)
    working_hours = fields.Many2one(related='employee_id.resource_calendar_id')
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account')
    journal_id = fields.Many2one(comodel_name='account.journal')
    vac_des = fields.Many2one(comodel_name='hr.vacation.dest', string='Vacation Destination')
    employee_dependent_ids = fields.One2many(comodel_name='hr.employee.dependent', inverse_name='contract_id')
    employee_dependant = fields.One2many('hr.employee.dependent', 'contract_id', _('Employee Dependants'))
    children_allowance = fields.One2many('hr.children.allowance', 'contract_id', _('Children Allowance'))
    nationality = fields.Many2one('res.country', related='employee_id.country_id', readonly=True)
    type_id = fields.Many2one('hr.contract.type', _('Type'))
    employee_id = fields.Many2one('hr.employee')
    department_id = fields.Many2one('hr.department', _('Department Name'), related='employee_id.department_id',
                                    readonly=True)

    @api.multi
    def change_current_date_hijri(self,date):
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        year = date.year
        day = date.day
        month = date.month
        hijri_date = convert.Gregorian(year, month, day).to_hijri()
        return hijri_date

    def translate_to_eng(self,text):
        if text:
            eng_text = text
            text = TextBlob(text)
            ln = text.detect_language()
            if ln != 'en':
                eng_text = text.translate(to='en')
            if eng_text == 'Space technology':
                eng_text = 'TAQNIA Space'
            return eng_text
        else:
            return ' '

    ###############>>send email end contract and trial peroid<<<##########
    @api.model
    def contract_mail_reminder(self):
        now = dt.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([('state', '=', 'program_directory')])
        trial_days_send_email=5
        for i in match:
            if i.date_end:
                exp_date = fields.Date.from_string(i.date_end) - timedelta(days=30)
                if date_now >= exp_date:
                    mail_content = "Hello ,<br>The Contract ", i.employee_id.name, "is going to expire on ", \
                                   str(i.date_end), ". Please renew the Contract or end it before expiry date"
                    main_content = {
                        'subject': _('Contract -%s Expired End Period On %s') % (i.name, i.date_end),
                        'author_id': self.env.user.company_id.partner_id.id,
                        'body': mail_content,
                        'email_to': self.env.user.company_id.email,
                        'email_cc': self.env.user.company_id.hr_email,
                        'model': self._name,
                    }
                    self.env['mail.mail'].create(main_content).send()

            if i.trial_date_end:
                exp_date = fields.Date.from_string(i.trial_date_end)
                exp_date1 = fields.Date.from_string(i.trial_date_end)  - timedelta(days=trial_days_send_email)
                #if date_now >= exp_date :
                if exp_date >= date_now and date_now >= exp_date1:
                    mail_content = "Hello ,<br>The Contract trial period",i.employee_id.name, "is going to expire on ", \
                                   str(i.trial_date_end),".Please renew the trial Contract period or Contracting is Done it before expiry date"
                    main_content = {
                        'subject': _('Contract-%s Expired Trial Period On %s') % (i.name, i.trial_date_end),
                        'author_id': self.env.user.company_id.partner_id.id,
                        'body': mail_content,
                        'email_to': self.env.user.company_id.email,
                        'email_cc': self.env.user.company_id.hr_email,
                        'model': self._name,
                    }
                    self.env['mail.mail'].create(main_content).send()
    ##########################################################################
    @api.onchange('contract_duration')
    def get_contract_end_date(self):
        date_start = datetime.datetime.strptime(self.date_start, '%Y-%m-%d')
        if self.contract_duration == '12_months':
            self.date_end = date_start + relativedelta.relativedelta(months=12)
        elif self.contract_duration == '24_months':
            self.date_end = date_start + relativedelta.relativedelta(months=24)
        else:
            self.date_end = False

    @api.onchange('salary_degree')
    def onchange_base_salary(self):
        if self.salary_degree:
            self.salary = self.salary_degree.base_salary

    # update  to control on date constrains
    @api.onchange('trial_date_start', 'trial_date_end', 'date_start', 'date_end')
    def onchange_dates(self):
        if self.trial_date_start:
            if self.trial_date_end:
                if self.date_start:
                    if self.date_end:
                        start_date_1 = dt.strptime(self.date_start, "%Y-%m-%d")
                        end_date_1 = dt.strptime(self.date_end, "%Y-%m-%d")
                        trial_start_date_1 = dt.strptime(self.trial_date_start, "%Y-%m-%d")
                        trial_end_date_1 = dt.strptime(self.trial_date_end, "%Y-%m-%d")

                        if trial_end_date_1 < trial_start_date_1:
                            raise exceptions.Warning(
                                _('trial End Date  must be greater than Trial Start date'))
                        if end_date_1 < start_date_1:
                            raise exceptions.Warning(
                                _('End  date must be greater than Start date'))


    @api.onchange('contract_description')
    def _contract_duration_change_state(self):
        if self.contract_description == 'locum':
            self.contract_duration = 'none'
            self.date_end = ''

    @api.one
    @api.depends('wage', 'house_allowance', 'transport_allowance', 'communication_allowance')
    def _compute_monthly_salary(self):
        self.monthly_salary = self.wage + self.house_allowance_temp + self.transport_allowance_temp + \
                              self.communication_allowance_temp + self.field_allowance_temp + \
                              self.special_allowance_temp + self.other_allowance_temp

    @api.depends()
    def _cal_allowance(self):
        allowance = 0.0
        if self.employee_id.country_id.code == 'SA':
            allowance = self.salary * 1 / 100
        self.breakdown_allowance = allowance

    @api.one
    @api.depends()
    def _calculate_gosi(self):
        if self.emp_type == 'saudi' and self.is_gosi_deducted == "yes":
            employee_gosi = (self.salary_insurnce + self.house_allowance_temp) * 10 / 100
            employer_gosi = (self.salary_insurnce + self.house_allowance_temp) * 12 / 100
            self.gosi_deduction = employee_gosi
            self.gosi_employer_deduction = employer_gosi
            self.total_gosi = employee_gosi + employer_gosi

        elif self.emp_type == 'saudi' and self.is_gosi_deducted == "no":

            employee_gosi = (self.salary_insurnce + self.house_allowance_temp) * 10 / 100
            employer_gosi = (self.salary_insurnce + self.house_allowance_temp) * 12 / 100

            self.gosi_deduction = 0.0
            self.gosi_employer_deduction = employee_gosi + employer_gosi
            self.total_gosi = employee_gosi + employer_gosi
        else:
            # pass
            employer_gosi = (self.salary_insurnce + self.house_allowance_temp) * 2 / 100

            self.gosi_deduction = 0.0
            self.gosi_employer_deduction = employer_gosi
            self.total_gosi = employer_gosi

        if self.emp_type == 'saudi' and self.saudi_emp_type == 'saudi-non':
            self.gosi_deduction = 0.0
            self.gosi_employer_deduction = 0.0
            self.total_gosi = 0.0


    @api.one
    @api.depends('date_start', 'date_end', 'trial_date_start', 'trial_date_end')
    def _compute_contract_duration(self):
        if self.date_start and self.date_end:
            date_start = datetime.datetime.strptime(self.date_start, '%Y-%m-%d').date()
            date_end = datetime.datetime.strptime(self.date_end, '%Y-%m-%d').date()
            self.contract_duration_cal = relativedelta.relativedelta(date_end, date_start).years
        if self.trial_date_start and self.trial_date_end:
            date_start = datetime.datetime.strptime(self.trial_date_start, '%Y-%m-%d').date()
            date_end = datetime.datetime.strptime(self.trial_date_end, '%Y-%m-%d').date()
            self.trial_duration = relativedelta.relativedelta(date_end, date_start).months

    @api.one
    @api.depends('air_ticket_amount')
    def _get_total_ticket_amount(self):
        self.total_air_ticket_amount = self.air_ticket_amount * self.air_ticket_number

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.job_id = self.employee_id.job_id
            self.department_id = self.employee_id.department_id
            self.employee_code = self.employee_id.employee_code
            self.fn = self.employee_id.fn
            self.mn = self.employee_id.mn
            self.ln = self.employee_id.ln
            self.dn = self.employee_id.name

    @api.multi
    def draft_state(self):
        self.state = "draft"

    @api.multi
    def employeed_aproval(self):
        self.state = "employeed_aproval"

    @api.multi
    def hr_head_approval(self):
        self.state = "hr_head_approval"

    @api.multi
    def end_contract_state(self):
        self.state = "end_contract"

    @api.multi
    def program_directory(self):
        self.state = "program_directory"

    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))
        return super(Contract, self).unlink()

    @api.onchange('working_hours')
    def _onchange_working_hours(self):
        if self.employee_id.contract_id.id == self._origin.id:
            self.env['resource.resource'].browse([self.employee_id.resource_id.id]).write({'calendar_id': self.working_hours.id})

class VacationDest(models.Model):
    _name = 'hr.vacation.dest'
    _rec_name = 'name'
    name = fields.Char(required=True)

VacationDest()


class EmployeeChildAllowance(models.Model):
    _name = 'hr.children.allowance'

    name = fields.Char(_('Children Name'))
    age = fields.Integer(_('Age'))
    fees = fields.Float(_('Educational Fees'))
    remarks = fields.Text(_('Remarks'))

    # Relational fields
    contract_id = fields.Many2one('hr.contract', _('Contract'))


EmployeeChildAllowance()


class HrContractType(models.Model):
    _inherit = 'hr.contract.type'

    salary_type = fields.Selection([('amount', _('Amount')),
                                    ('scale', _('Scale'))], string='Salary Type')
    #permission_hours = fields.Integer()
    #permission_number = fields.Integer()
    #work_days = fields.Integer()
    #work_hour = fields.Integer()
    #overtime_factor_daily = fields.Float(string='Overtime Factor Daily')
    #overtime_factor_holiday = fields.Float(string='Overtime Factor Holiday')
