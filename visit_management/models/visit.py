# -*- coding: utf-8 -*-

from lxml import etree

from odoo import fields, models, api
from odoo.exceptions import Warning
from odoo.osv.orm import setup_modifiers
from odoo.tools.translate import _
from datetime import datetime

ToDay = str(datetime.now().date())


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # @api.model
    # def _get_area_domain(self):

    #     target_ids = self.env['sales.visit.target'].search([('salesperson_user_id', '=', self.env.user.id)])
    #     area_ids = []
    #     for target in target_ids:
    #         if target:
    #             if target.area_customer == 'by_area':
    #                 area_ids.append(target.area_id.id)
    #     if area_ids:
    #         return [('id', 'in', area_ids)]
    #     else:
    #         return [('id', 'in', [])]

    area_id = fields.Many2one(comodel_name='res.country.area', string='Area')

    meeting_count = fields.Integer(
        compute='_compute_meeting_count_commercial_partner')

    @api.multi
    def _compute_meeting_count_commercial_partner(self):
        att_model = self.env['calendar.event']
        for partner in self:
            domain = [('customer_id', '=', partner.id)]
            attendees = att_model.search_count(domain
                                               )
            partner.meeting_count = attendees

    @api.multi
    def schedule_meeting_calendar(self):
        partner_ids = self.ids
        partner_ids.append(self.env.user.partner_id.id)
        action = self.env.ref('visit_management.action_calendar_event_visit').read()[0]
        action['domain'] = [('customer_id', '=', self.id)]
        action['context'] = {
            'default_partner_ids': partner_ids,
            'default_customer_id': self.id,
        }
        return action


ResPartner()


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    record_type = fields.Selection(selection=[('normal', 'Calender Meeting'), ('visit', 'Visit')], string='Record Type',
                                   default='normal')

    @api.model
    def _get_customer_domain(self):
        target_ids = self.env['sales.visit.target'].search(
            [('salesperson_user_id', '=', self.env.user.id), ('date_from', '<=', ToDay),
             ('date_to', '>=', ToDay)])
        customer_ids = []
        if target_ids:
            for target_id in target_ids:
                if target_id.area_customer == 'by_area':
                    print('+++++++++++++++++++++++++++area')
                    for id in self.env['res.partner'].sudo().search([('area_id', '=', target_id.area_id.id)])._ids:
                        customer_ids.append(id)
                else:
                    print('+++++++++++++++++++++++++++custom')
                    for id in target_id.partner_ids._ids:
                        customer_ids.append(id)
            print('+++++++++++++++++++++++++++customer_ids',customer_ids)
        # else:
        #     print('+++++++++++++++++++++++++++else')
        #     customer_ids = self.env['res.partner'].sudo().search(
        #         ['|', ('user_id', '=', self.env.user.id), ('user_id', '=', False)])._ids
        return [('id', 'in', customer_ids)]

    state = fields.Selection(
        selection=[('draft', 'Draft'), ('progress', 'In progress'), ('approve', 'To Approve'), ('approved', 'Approved'),
                   ('cancel', 'Canceled')],
        string='State', default='draft', track_visibility='onchange')

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customers",
                                  domain=lambda item: item._get_customer_domain())
    feedback = fields.Html(string='Feedback')
    area_id = fields.Many2one(comodel_name='res.country.area', string='Area', related='customer_id.area_id')
    cancel_reason = fields.Html(string='Return Reason')

    @api.multi
    def set_to_approve(self):
        manager = self.env['crm.team'].sudo().search([('member_ids', 'in', [self.user_id.id])])
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>manager',manager.name)
        if manager.user_id and manager.user_id.partner_id:
            self.message_subscribe([manager.user_id.partner_id.id])
            values = {
                'body': _('A new Visit need your approval %s ') % (manager.name),
                'model': self._name,
                'message_type': 'comment',
                'no_auto_thread': False,
                'res_id': self.id,
                'partner_ids': [(6, 0, [manager.user_id.partner_id.id])]
            }
            self.env['mail.message'].create(values)
        self.state = 'approve'

    @api.multi
    def set_to_approved(self):
        self.state = 'approved'

    @api.multi
    def set_to_progress(self):
        self.state = 'progress'

    @api.multi
    def set_to_cancel(self):
        dummy, view_id = self.env['ir.model.data'].get_object_reference('visit_management',
                                                                        'wizard_cancel_visit_form_view')
        return {
            'name': _("Cancel Visit : %s" % (self.name)),
            'view_id': view_id,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cancel.visit.reason',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'context': self._context,
        }

    @api.multi
    def unlink(self):
        for item in self:
            if item.state != 'draft':
                raise Warning(_("You can't remove visit in state %s") % (item.state))

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):

        res = super(CalendarEvent, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                         submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field"):
                if node.get('name', False) not in ('state', 'id', 'start_date', 'stop_date', 'state_datetime'):
                    if self.env.user.has_group('visit_management.group_visit_manager'):
                        node.set('attrs', "{'readonly': [('state', 'in', ('approved','cancel'))]}")
                    elif self.env.user.has_group('visit_management.group_visit_user'):
                        node.set('attrs', "{'readonly': [('state', 'in', ('approve','approved','cancel'))]}")
                node_name = node.get('name')
                setup_modifiers(node, res['fields'][node_name])
            res['arch'] = etree.tostring(doc)

        return res


CalendarEvent()


class AreaCode(models.Model):
    _name = 'res.country.area'
    _rec_name = 'name'
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)


AreaCode()


class SalesVisit(models.Model):
    _name = "sales.visit.target"
    _rec_name = 'salesperson_user_id'
    _inherit = ['mail.thread']
    salesperson_user_id = fields.Many2one(comodel_name="res.users", string="Sales Engineer", required=True,
                                          track_visibility='onchange')
    tag_ids = fields.Many2many('calendar.event.type', 'sales_visit_category_rel', 'visit_id', 'type_id', 'Tags')

    area_customer = fields.Selection(selection=[('by_area', 'Area'), ('by_customer', 'By Customers')],
                                     default='by_area', required=True,
                                     string='Customer Filter')

    partner_ids = fields.Many2many(comodel_name="res.partner", string="Customers", domain=[('customer', '=', True)])
    date_from = fields.Date(string="Date From", required=True, track_visibility='onchange')
    date_to = fields.Date(string="Date to", required=True, track_visibility='onchange')
    target_no = fields.Integer(string='Visit Targets No.')
    area_id = fields.Many2one(comodel_name='res.country.area', string='Area')
    meeting_count = fields.Integer(compute='_compute_target')

    @api.multi
    def get_meetings(self):
        date_from = self.date_from + " 00:00:01"
        date_to = self.date_to + " 23:59:00"
        return self.env['calendar.event'].sudo().search([('start', '>=', date_from),
                                                         ('start', '<=', date_to),
                                                         ('user_id', '=',
                                                          self.salesperson_user_id.id),
                                                         ('area_id', '=', self.area_id.id)])

    @api.model
    def create(self, vals):
        res = super(SalesVisit, self).create(vals)
        res.message_subscribe([res.salesperson_user_id.partner_id.id])
        values = {
            'body': _('A new Visit Target has been created fro you %s ') % (res.salesperson_user_id.name),
            'model': self._name,
            'message_type': 'comment',
            'no_auto_thread': False,
            'res_id': res.id,
            'partner_ids': [(6, 0, [res.salesperson_user_id.partner_id.id])]
        }
        self.env['mail.message'].create(values)
        return res

    @api.multi
    def _compute_target(self):
        for item in self:
            date_from = item.date_from + " 00:00:01"
            date_to = item.date_to + " 23:59:00"
            if item.area_customer == 'by_area':
                item.meeting_count = self.env['calendar.event'].sudo().search_count([('start', '>=', date_from),
                                                                                     ('start', '<=', date_to),
                                                                                     ('user_id', '=',
                                                                                      item.salesperson_user_id.id),
                                                                                     ('area_id', '=', item.area_id.id)])
            else:
                item.meeting_count = self.env['calendar.event'].sudo().search_count([('start', '>=', date_from),
                                                                                     ('start', '<=', date_to),
                                                                                     ('user_id', '=',
                                                                                      item.salesperson_user_id.id),
                                                                                     ('customer_id', 'in',
                                                                                      item.partner_ids.ids)])

    @api.multi
    def current_meeting_calendar(self):
        item = self
        date_from = item.date_from + " 00:00:01"
        date_to = item.date_to + " 23:59:00"
        if item.area_customer == 'by_area':
            meeting_ids = self.env['calendar.event'].sudo().search([('start', '>=', date_from),
                                                                    ('start', '<=', date_to),
                                                                    ('user_id', '=',
                                                                     item.salesperson_user_id.id),
                                                                    ('area_id', '=', item.area_id.id)]).ids
        else:
            meeting_ids = self.env['calendar.event'].sudo().search([('start', '>=', date_from),
                                                                    ('start', '<=', date_to),
                                                                    ('user_id', '=',
                                                                     item.salesperson_user_id.id),
                                                                    ('customer_id', 'in',
                                                                     item.partner_ids.ids)]).ids
        action = self.env.ref('visit_management.action_calendar_event_visit').read()[0]
        action['domain'] = [('id', 'in', meeting_ids)]
        return action

    @api.multi
    @api.constrains('date_to', 'date_from')
    def constraint_overlap(self):
        item_same_period = self.search_count([('date_from', '<=', self.date_to),
                                              ('date_to', '>=', self.date_from),
                                              ('salesperson_user_id', '=', self.salesperson_user_id.id),
                                              ('area_id', '=', self.area_id.id)])
        if item_same_period > 1:
            raise Warning(_('Overlap .. This Engineer has a similar target before'))


SalesVisit()
