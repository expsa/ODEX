# -*- coding: utf-8 -*-

import logging
from datetime import timedelta, datetime, date

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class TaskRunStop(models.Model):
    _inherit = ['project.task']
    
    task_run = fields.Boolean(default=False, index=True, copy=False)
    task_run_user = fields.Many2one('res.users', index=True, copy=False)
    task_run_time = fields.Datetime(index=True, copy=False)
    
    task_pause = fields.Boolean(default=False, index=True, copy=False)
    task_run_sum = fields.Float(default=0.0, index=True, copy=False)
    task_pause_last_time = fields.Datetime(index=True, copy=False)
    
    def run_task(self):
        if self.env['account.analytic.line'].search([('user_id','=',self.env.uid),('running','=',True)]):
            raise UserError(_('You have a fast Timesheet.')) 
        if self.task_run_time:
            raise UserError(_('Task already started.')) 
        if not self.env.user.employee_ids:
            raise UserError(_('You can not start the task, because you are not an employee.')) 
        if (self.user_id.id != self.env.uid) and (not self.env.user.has_group('project.group_project_manager')):
            raise UserError(_('This task is not assigned to you, but %s\nYou must be a Manager to run this task' % self.user_id.name))    
        run_user_tasks = self.env['project.task'].search([('task_run_user','=',self.env.uid),('task_run','=',True),('task_pause','=',False)], limit=1)
        if run_user_tasks:
            action = {
                "name": _("You are have running task"),
                "type": "ir.actions.act_window",
                "res_model": "project_task_run_stop.pause_wizard",
                "views": [[False, "form"]],
                "target": "new",
                "context": {'run_user_tasks': run_user_tasks.id, 'task': self.id, 'run': True, 'pause': False}
            }
            return action
        if not self.user_id:
            self.write({'user_id': self.env.uid})
        self.write({'task_run': True, 'task_run_user': self.env.uid, 'task_run_time': datetime.now()})
        self.env['bus.bus'].sendone('need_refresh_tasks', {'model': 'project.task', 'uid': self.env.user.id})
    
    def pause_task(self):
        if self.env['account.analytic.line'].search([('user_id','=',self.env.uid),('running','=',True)]):
            raise UserError(_('You have a fast Timesheet.')) 
        if not self.task_run_time:
            raise UserError(_("Task don't started."))
        if not self.env.user.employee_ids:
            raise UserError(_('You can not pause the task, because you are not an employee.')) 
        if (self.user_id.id != self.env.uid) and (not self.env.user.has_group('project.group_project_manager')):
            raise UserError(_('This task is not assigned to you, but %s\nYou must be a Manager to pause this task' % self.user_id.name))      
        if not self.task_pause:
            if self.task_pause_last_time:
                hours = self.task_run_sum + ((datetime.now() - datetime.strptime(self.task_pause_last_time, '%Y-%m-%d %H:%M:%S')).total_seconds() / 3600.0)
            else:
                hours = (datetime.now() - datetime.strptime(self.task_run_time, '%Y-%m-%d %H:%M:%S')).total_seconds() / 3600.0
            self.write({'task_pause': True, 'task_run_sum': hours})
        else:
            run_user_tasks = self.env['project.task'].search([('task_run_user','=',self.env.uid),('task_run','=',True),('task_pause','=',False)], limit=1)
            if run_user_tasks:
                action = {
                    "name": _("You are have running task"),
                    "type": "ir.actions.act_window",
                    "res_model": "project_task_run_stop.pause_wizard",
                    "views": [[False, "form"]],
                    "target": "new",
                    "context": {'run_user_tasks': run_user_tasks.id, 'task': self.id, 'pause': True, 'run': False}
                }
                return action
            else:  
                self.write({'task_pause': False, 'task_pause_last_time': datetime.now()})
            
    def stop_task(self):
        if self.env['account.analytic.line'].search([('user_id','=',self.env.uid),('running','=',True)]):
            raise UserError(_('You have a fast Timesheet.')) 
        name = _("Description of work")
        if not self.task_run_time:
            raise UserError(_('Task already stopped.')) 
        if not self.env.user.employee_ids:
            raise UserError(_('You can not complete the task, because you are not an employee.')) 
        if (self.task_run_user.id != self.env.uid) and (not self.env.user.has_group('project.group_project_manager')):
            raise UserError(_('This task was launched not by you, but by %s\nYou must be a Manager to complete this task' % self.task_run_user.name))
        action = {
          "name": name,
          "type": "ir.actions.act_window",
          "res_model": "project_task_run_stop.stop_wizard",
          "views": [[False, "form"]],
          "target": "new",
          }
        return action

  
class TaskPauseWizard(models.TransientModel):
    _name = 'project_task_run_stop.pause_wizard'
    
    @api.multi
    def action_pause_task(self):
        task = self.env['project.task'].browse(self.env.context.get('task'))
        run_user_tasks = self.env['project.task'].browse(self.env.context.get('run_user_tasks'))
        if task and run_user_tasks and self.env.context.get('run'):
            run_user_tasks.pause_task()
            task.run_task()
        if task and run_user_tasks and self.env.context.get('pause'):
            run_user_tasks.pause_task()
            task.pause_task()   
        self.env['bus.bus'].sendone('need_refresh_tasks', {'model': 'project.task', 'uid': self.env.user.id})  
        
    
class TaskStopDescription(models.TransientModel):
    _name = 'project_task_run_stop.stop_wizard'

    description = fields.Char(string = 'Description of work')
  
    @api.multi
    def action_stop_task(self):
        task = self.env['project.task'].browse(self.env.context.get('active_id'))
        datetime_run_time = datetime.strptime(task.task_run_time, '%Y-%m-%d %H:%M:%S')
        project = task.project_id
        if task.task_run_sum:
            if task.task_pause:
                unit_amount = task.task_run_sum
            else:
                unit_amount = task.task_run_sum + ((datetime.now() - datetime.strptime(task.task_pause_last_time, '%Y-%m-%d %H:%M:%S')).total_seconds() / 3600.0)
        else:
            unit_amount = (datetime.now() - datetime.strptime(task.task_run_time, '%Y-%m-%d %H:%M:%S')).total_seconds() / 3600.0
        timesheet = {'date': fields.Date.context_today(self),
                     'task_id': task.id,
                     'project_id': project.id,
                     'account_id': project.analytic_account_id.id,
                     'user_id': self.env.uid,
                     'name': self.description,
                     'run_time': datetime_run_time,
                     'stop_time': datetime.now(),
                     'unit_amount': unit_amount,
                     }
        task.sudo().write({'timesheet_ids': [(0, _, timesheet)],
                    'task_run': False, 
                    'task_run_user': None, 
                    'task_run_time': None,
                    'task_pause': False,
                    'task_run_sum': 0.0, 
                    'task_pause_last_time':  None,       
                   })
        final_stage = project.type_ids.search([('final_stage','=',True)], limit=1)
        if final_stage:
            task.update({'stage_id': final_stage.id})
        self.env['bus.bus'].sendone('need_refresh_tasks', {'model': 'project.task', 'uid': self.env.user.id})
      
      
class AnalyticAccountRunStop(models.Model):
    _inherit = ['account.analytic.line']      

    run_time = fields.Datetime(string="Run time")
    stop_time = fields.Datetime(string="Stop time") 
    running = fields.Boolean(default=False, index=True, copy=False)
    task_paused = fields.Many2one('project.task', copy=False)
    
    @api.multi
    def init_fast_timesheet(self):
        res = self.search([('user_id','=',self.env.uid),('running','=',True)], limit=1)
        if res:
            run = fields.Datetime.from_string(res.run_time)
            now = datetime.now()
            sec = (now - run).seconds
            return sec
        else:
            return False
          
    @api.multi
    def start_stop_fast_timesheet(self):
        res = self.search([('user_id','=',self.env.uid),('running','=',True)], limit=1)
        if res:
            if res.task_paused:
                return res.task_paused.name
            else:
                return -1
        else:
            return False
    
    @api.multi
    def start_fast_timesheet(self):
        project = self.env['project.project'].browse(int(self.env['ir.config_parameter'].sudo().get_param('project_task_run_stop.project_fast_timesheet')))
        if not project:
            return False
        run_user_task = self.env['project.task'].search([('task_run_user','=',self.env.uid),('task_run','=',True),('task_pause','=',False)], limit=1)
        if run_user_task:
            run_user_task.pause_task()
        
        datetime_run_time = datetime.now()
        timesheet = {'date': fields.Date.context_today(self),
                     'name': self.env.user.name + ': ' + _('Fast timesheet in progress'),
                     'project_id': project.id,
                     'account_id': project.analytic_account_id.id,
                     'user_id': self.env.uid,
                     'run_time': datetime_run_time,
                     'running': True,
                     'task_paused': run_user_task.id or None,
                     }
        self.create(timesheet)
        self.env['bus.bus'].sendone('need_refresh_tasks', {'model': 'project.task', 'uid': self.env.user.id})
        return True
            
    @api.multi
    def save_fast_timesheet(self, description, project, unpause):
        res = self.search([('user_id','=',self.env.uid),('running','=',True)], limit=1)
        task_unpause = res.task_paused
        run = fields.Datetime.from_string(res.run_time)
        now = datetime.now()
        unit_amount = (now - run).seconds / 3600
        if project:
            timesheet = {'stop_time': now,
                         'name': description,
                         'project_id': project.id,
                         'unit_amount': unit_amount,
                         'running': False,
                         'task_paused': None,
                         }
        else:
            timesheet = {'stop_time': now,
                         'name': description,
                         'unit_amount': unit_amount,
                         'running': False,
                         'task_paused': None,
                         }  
        res.write(timesheet)
        if unpause:
            task_unpause.pause_task()
        self.env['bus.bus'].sendone('need_refresh_tasks', {'model': 'project.task', 'uid': self.env.user.id})    
    
    
class ProjectTaskTypeInheritPTRS(models.Model):
    _inherit = 'project.task.type'
    
    final_stage = fields.Boolean(string='Final Stage', default=False,
                                 help='The final stage. The task is automatically transferred to this stage after pressing the Stop button.')    
    
    
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    project_fast_timesheet = fields.Many2one('project.project', string="Project for fast timesheet")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update({
            'project_fast_timesheet': int(self.env['ir.config_parameter'].sudo().get_param('project_task_run_stop.project_fast_timesheet')),
           })
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('project_task_run_stop.project_fast_timesheet', self.project_fast_timesheet.id)
        
        
class RunStopWizardStopFastTimesheet(models.TransientModel):
    _name = 'project_task_run_stop.wizard_stop_fast_timesheet'

    def _default_unpause_flag(self):
        res = self.env['account.analytic.line'].search([('user_id','=',self.env.uid),('running','=',True)], limit=1)
        if res.task_paused:
            return True
    
    description = fields.Char(string = 'Description of work')
    project_id = fields.Many2one('project.project', string='Select project')
    unpause_flag = fields.Boolean(default=_default_unpause_flag)
    unpause = fields.Boolean(default=_default_unpause_flag)
    
    def stop_fast_timesheet(self):
        fast_timesheet = self.env['account.analytic.line']
        res = fast_timesheet.search([('user_id','=',self.env.uid),('running','=',True)], limit=1)
        res.save_fast_timesheet(self.description, self.project_id, self.unpause)
        self.env['bus.bus'].sendone('need_refresh_fast_timesheet', 'need_refresh_fast_timesheet')
  