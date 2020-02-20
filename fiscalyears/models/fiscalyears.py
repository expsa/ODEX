# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class fiscalyears(models.Model):
    _name = 'fiscalyears'
    _description = "Fiscal Year"

    name = fields.Char(string='Name')

    code = fields.Char(compute="_get_code", store=True, string='Code',
                       help='''The code of the fiscalyear like
     start date - end date - state ''')

    start_date = fields.Date(string='Start Date', required=True, help='''the start of the
     fiscalyear''')
    end_date = fields.Date(string='End Date', required=True,
                           help='the end of the fiscalyear')
    state = fields.Selection(selection=[('draft', 'Draft'), ('open', 'Open'),
                                        ('closed', 'Closed'),
                                        ('cancel', 'Cancel')],
                             string='State', default='draft',
                             help='''the state of the current
                             fiscalyear where \n draft is the new created \n
                             open is the current runing fiscalyear \n
                             closed is means you can not assign any operation
                             in this fiscalyear \n this ficalyear has been
                              canceled ''')
    type = fields.Selection(selection=[('monthly', 'Monthly'),
                                       ('quarterly', 'Quarterly'),
                                       ('biannual', 'Biannual'),
                                       ('annual', 'Annual')],
                            string='Type', default='monthly',
                            help='''the type of the fiscalyear \n
                            monthly : per month \n
                            quarterly : every three months\n
                            biannual : every six months\n
                            annual : every twelve months''')
    periods_ids = fields.One2many(comodel_name='fiscalyears.periods',
                                  inverse_name='fiscalyear_id',
                                  string='Periods', help='''the date periods
     used to assign operations''')

    @api.multi
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        ''' check start date and end date to see if :
            start date come after end date or the range of
            the given fiscalyear is corrosing another fiscalyear
        '''
        for obj in self:
            if fields.Date.from_string(obj.start_date) > \
                    fields.Date.from_string(self.end_date):
                raise ValidationError(
                    _('start date must be before end date'))
            if in_range(self, fields.Date.from_string(obj.start_date)) or \
                    in_range(self, fields.Date.from_string(obj.end_date)):
                raise ValidationError(
                    _('dates range can not cross with another fiscalyear'))

    @api.multi
    @api.depends('start_date', 'end_date')
    def _get_code(self):
        ''' make the code of the record from start date and end date.
        '''
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.code = ('%s') % (
                    str(fields.Date.from_string(rec.start_date).year))

    @api.multi
    def create_periods(self):
        ''' create fiscalyear periods accoring to configuration.

            returns: boolean
                * true if the periods has created sucssesfly,
                * exception if any error happend.
        '''
        for rec in self:
            if not rec.type:
                raise ValidationError(
                    _('you must enter the fiscalyear type to create periods'))
            type_dict = {'monthly': 1, 'quarterly': 3,
                         'biannual': 6, 'annual': 12}
            interval = type_dict.get(rec.type, False)

            if not interval:
                raise ValidationError(
                    _('you must enter the fiscalyear type to create periods'))

            periods_obj = self.env['fiscalyears.periods']

            rec.periods_ids.unlink()
            all_periods = self.get_periods(interval)

            periods_obj.create({
                'fiscalyear_id': rec.id,
                'start_date': rec.start_date,
                'end_date': rec.start_date,
                'state': 'open',
                'opening': True,
            })

            while True:
                try:
                    period = next(all_periods)
                    periods_obj.create({
                        'fiscalyear_id': rec.id,
                        'start_date': period[0],
                        'end_date': period[1],
                    })
                    flag = True
                except:
                    break

    def get_periods(self, interval):
        ''' get all periods start dates and end dates pairs
            acorrding to the configuration of fiscalyear .

            param interval: the length of the period in months

            returns: boolean
                * list of tuples containing start and end dates of each period
        '''
        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)
        while True:
            delta = start_date + relativedelta(months=interval)
            delta = delta - relativedelta(days=1)

            if delta >= end_date:
                delta = end_date

            yield (start_date, delta)

            start_date = delta + relativedelta(days=1)
            if start_date >= end_date:
                break

    @api.multi
    def open(self):
        ''' make sure periods have been created for each
            fiscalyear and change state to open .
        '''
        for rec in self:
            if not rec.periods_ids:
                raise ValidationError(
                    _('you must create periods for this fiscal year'))
            rec.state = 'open'
            #rec.periods_ids.write({'state': 'open'})

    @api.multi
    def close(self):
        ''' change state of the fiscalyears and there periods
            to close .
        '''
        for rec in self:
            if not all(x == 'closed' for x in
                       rec.mapped('periods_ids.state')):
                raise ValidationError(
                    _('you must close every period of this fiscal year'))
            rec.state = 'closed'

    @api.multi
    def cancel(self):
        ''' change state to cancel .
        '''
        for rec in self:
            rec.periods_ids.cancel()
            rec.state = 'cancel'

    @api.multi
    def draft(self):
        ''' change state to draft .
        '''
        for rec in self:
            rec.periods_ids.draft()
            rec.state = 'draft'

    @api.multi
    def unlink(self):
        ''' delete fiscal years but they must be in draft state .
        '''
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    _('You cannot delete a fiscal year not in draft state.'))
            rec.periods_ids.unlink()
        return super(fiscalyears, self).unlink()


class fiscalyears_periods(models.Model):
    _name = 'fiscalyears.periods'
    _description = "Fiscal Year Period"
    name = fields.Char(compute="_get_name", store=True,
                       string='Name', help='''The name of the period like
     start date - end date - state ''')

    opening = fields.Boolean(string='Opening', help='is it an opening period')

    start_date = fields.Date(string='Start Date', help='''the start of the
     period''')
    end_date = fields.Date(string='End Date', help='the end of the period')
    state = fields.Selection(selection=[('draft', 'Draft'), ('open', 'Open'),
                                        ('closed', 'Closed'),
                                        ('cancel', 'Cancel')],
                             default='draft',
                             string='State', help='''the state of the current
                             period where \n draft is the new created \n
                             open is the current runing period \n
                             closed is means you can not assign any operation
                             in this period \n this ficalyear has been
                              canceled ''')
    fiscalyear_id = fields.Many2one(comodel_name='fiscalyears',
                                    string='Fiscalyear')

    @api.multi
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        ''' check start date and end date to see if :
            start date come after end date or the range of
            the given period is corrosing another period
            or corrossing the fiscalyear date range
        '''
        for obj in self:
            start_date = fields.Date.from_string(obj.start_date)
            end_date = fields.Date.from_string(obj.end_date)

            fiscalyear_start_date = fields.Date.from_string(
                obj.fiscalyear_id.start_date)

            fiscalyear_end_date = fields.Date.from_string(
                obj.fiscalyear_id.end_date)

            if start_date > end_date:
                raise ValidationError(
                    _('start date must be before end date'))

            if start_date < fiscalyear_start_date \
                    or end_date > fiscalyear_end_date:
                raise ValidationError(
                    _('period range must be in the fiscalyear range'))

            if not obj.opening and (
                in_range(self, start_date) or in_range(self, end_date)
            ):
                raise ValidationError(
                    _('dates range can not cross with another period'))

    @api.multi
    @api.depends('start_date', 'end_date', 'state')
    def _get_name(self):
        ''' make the name of the record from start date and end date and state.
        '''
        for rec in self:
            if rec.start_date and rec.end_date:
                # for translation purpose
                opening_str = _('opening')

                name = ('%s-%s') % (
                    str(fields.Date.from_string(rec.start_date).year),
                    str(fields.Date.from_string(rec.start_date).month))

                if rec.opening:
                    name = ('%s-%s') % (
                        str(fields.Date.from_string(rec.start_date).year),
                        opening_str)
                rec.name = name

    @api.multi
    def cancel(self):
        ''' change state to cancel .
        '''
        for rec in self:
            # operations code goes here
            rec.state = 'cancel'

    @api.multi
    def close(self):
        ''' change state of the  period
            to close after make sure every linked operation is reached
            last state.
        '''
        for rec in self:
            # operations code goes here
            rec.state = 'closed'

    @api.multi
    def draft(self):
        ''' change state to draft .
        '''
        for rec in self:
            rec.state = 'draft'

    @api.multi
    def unlink(self):
        ''' delete fiscal years but they must be in draft state .
        '''
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    _('You cannot delete a period not in draft state.'))
        return super(fiscalyears_periods, self).unlink()

    @api.multi
    def open(self):
        '''
        change state to open .
        '''
        for rec in self:
            if rec.fiscalyear_id.state not in ['open']:
                raise UserError(
                    _('''You cannot open a period where the fiscalyear not in
                     open state.'''))
            rec.state = 'open'


def in_range(self, dt):
    ''' check a date in all fiscalyear/period date ranges.

        param td: date to check

        returns: boolean
            * true if the date hase occurred in previous fiscalyear/period,
            * False if the date hase not occurred in previous
            fiscalyear/period.
    '''
    domain = [('id', '!=', self.id),
              ('state', '!=', 'cancel')]

    if dir(self).__contains__('opening'):
        domain += [('opening', '!=', True)]
    date_ranges = self.search(domain)

    for year in date_ranges:
        if dt == fields.Date.from_string(year.start_date):
            return True
        elif dt == fields.Date.from_string(year.end_date):
            return True
        elif dt > fields.Date.from_string(year.start_date) \
                and dt < fields.Date.from_string(year.end_date):
            return True

    return False
