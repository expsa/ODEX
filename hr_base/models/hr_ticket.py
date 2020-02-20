
from odoo import models, fields, api

class HRTicket(models.Model):
    _name = 'hr.ticket'

    name = fields.Many2one(comodel_name='hr.employee', string="Employee Name", required=True)
    emp_no = fields.Char("Employee No", required=True)
    leave_from = fields.Char("Leave From", required=True)
    leave_to = fields.Char("Leave To", required=True)
    status = fields.Selection(selection=[(
        'bachelor', 'Bachelor'),
        ('family', 'Family')], required=True, string='Status')

    dependent = fields.Selection(selection=[(
        '1', '1+1 '),
        ('2', '1+2 '),
        ('3', '1+3 '),
        ('all', 'All ')], required=True, string='Dependent')
    fn = fields.Char("First Name", )
    mn = fields.Char("Middle Name", )
    ln = fields.Char("Last Name", )
    gender = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Gender", required=True)
    dob = fields.Date("DOB", required=True)
    mobile = fields.Char("Mobile No", required=True)
    contact_no = fields.Char("Contact No", required=True)
    nationality = fields.Many2one(comodel_name='res.country',string= "Nationality", required=True)
    passport = fields.Many2one(comodel_name='hr.employee.document',string= "Passport No", required=True)
    issue = fields.Date("Issue Date", required=True)
    expiry = fields.Date("Expiry Date", required=True)
    departure = fields.Char("Departure Air Port", required=True)
    destination = fields.Char("Destination Air Port", required=True)
    departure_date = fields.Date("Departure Date", required=True)
    return_date = fields.Date("Return Date", required=True)
    priority = fields.Selection(selection=[(
        'critical', 'Critical'),
        ('high', 'High'),
        ('normal', 'Normal')], required=True, string='Priority')
    #remarks = fields.Char("Remarks", required=True)

    dependent_id = fields.One2many('hr.ticket.dependent', 'dependent_ticket', string="Dependent")
    reissue_ticket = fields.One2many('hr.ticket.reissue', 'reissue_ticket', string="Re issue")

    create_book = fields.Boolean("Create Booking")
    conf_book = fields.Boolean("Confirm Booking")
    re_issue = fields.Boolean("Re Issue")
    cancel_ticket = fields.Boolean("Cancel Ticket")

    req_no = fields.Char("Request No", required=True)
    agent = fields.Char("Travel Agent", required=True)
    book_date = fields.Date("Booking Date", required=True)
    book_by = fields.Char("Booked By", required=True)
    piad_amt = fields.Float("Paid Amount", required=True)

    break_jun = fields.Selection(selection=[(
        'yes', 'Yes'),
        ('no', 'No'), ], string="Break Journey", required=True)

    receive = fields.Selection(selection=[(
        'yes', 'Yes'),
        ('no', 'No'), ], string="Booking Received", required=True)

    receive_date = fields.Date("Received Date", required=True)
    cutt_date = fields.Date("Cutt Off Date", required=True)
    desc = fields.Char("Description", required=True)
    attach = fields.Binary("Attach", required=True)
    sent_by = fields.Char("Sent for confirmation By", required=True)
    sent_by_date = fields.Char("Sent for confirmation Date", required=True)

    cancellation = fields.Selection(selection=[(
        'full', 'Full Ticket'),
        ('part', 'Part Ticket'), ], string="Cancel Ticket", required=True)

    refund = fields.Selection(selection=[(
        'yes', 'Yes'),
        ('no', 'No'), ], string="Refundable", required=True)
    cnr = fields.Char("Credit Note Number")

    @api.onchange('conf_book')
    def _onchange_conf_book(self):
        if self.conf_book == True:
            self.create_book = False

    @api.onchange('create_book')
    def _onchange_create_book(self):
        if self.create_book == True:
            self.conf_book = False

    @api.onchange('name')
    def _onchange_name(self):

        dent = self.env['hr.contract'].search([('employee_id', '=', self.name.id)])

        self.dependent = dent.dependent
        self.status = dent.status

        self.emp_no = self.name.employee_code
        self.fn = self.name.fn
        self.mn = self.name.mn
        self.ln = self.name.ln
        self.gender = self.name.gender
        self.dob = self.name.birthday
        self.mobile = self.name.mobile_phone
        self.contact_no = self.name.work_phone
        self.nationality = self.name.country_id
        self.passport = self.name.passport_id
        self.issue = self.name.iqama_num.issue_date
        self.expiry = self.name.iqama_num.expiry_date
        #self.remarks = self.name.e_remark

        if self.name.dependent_id:
            dependent_list = []
            for x in self.name.dependent_id:
                dependent_list.append({
                    'passport': x.d_passport,
                    'dob': x.dob,
                    'fn': x.fn,
                    'mn': x.mn,
                    'ln': x.ln,
                    'ticket_req': 'yes',
                    'name': x.name,
                })
            self.dependent_id = dependent_list

            dependent_list = []
