# -*- coding: utf-8 -*-
# Part of Marlon Falcon. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
import random

class ProjectProject(models.Model):
    _inherit = 'project.project'

    use_geolocation = fields.Boolean('Use Geolocation', default=True)
    latitude = fields.Float('Latitude', digits=(16, 15))
    longitude = fields.Float('Longitude', digits=(16, 15))


    # portal.documentation
    portal_documentation_ids = fields.Many2many('portal.documentation', copy=False)
    portal_documentation_count = fields.Integer(compute='_compute_portal_documentation_count', string='Documentation Count')

    @api.depends('portal_documentation_ids')
    def _compute_portal_documentation_count(self):
        for project in self:
            project.portal_documentation_count = self.env['portal.documentation'].search_count([('project_id', '=', project.id)])



    def action_view_portal_documentation(self):
        action = self.env.ref('mfh_employee_portal.action_portal_documentation').sudo().read()[0]
        action['domain'] = [('project_id', '=', self.id)]
        action['context'] = {
                              'default_project_id': self.id,
                            }
        return action


    # portal.photo
    portal_photo_ids = fields.One2many('portal.photo', 'project_id', copy=False)
    portal_photo_count = fields.Integer(compute='_compute_portal_photo_count', string='Photo Count')

    @api.depends('portal_photo_ids')
    def _compute_portal_photo_count(self):
        for project in self:
            project.portal_photo_count = self.env['portal.photo'].search_count([('project_id', '=', project.id)])

    def action_view_portal_photo(self):
        action = self.env.ref('mfh_employee_portal.action_portal_photo').sudo().read()[0]
        action['domain'] = [('project_id', '=', self.id)]
        action['context'] = {
                              'default_project_id': self.id,
                            }
        return action

    # portal.improvement
    portal_improvement_ids = fields.One2many('portal.improvement', 'project_id', copy=False)
    portal_improvement_count = fields.Integer(compute='_compute_portal_improvement_count', string='Improvement Count')
    @api.depends('portal_improvement_ids')
    def _compute_portal_improvement_count(self):
        for project in self:
            project.portal_improvement_count = self.env['portal.improvement'].search_count([('project_id', '=', project.id)])


    def action_view_portal_improvement(self):
        action = self.env.ref('mfh_employee_portal.action_portal_improvement').sudo().read()[0]
        action['domain'] = [('project_id', '=', self.id)]
        action['context'] = {
                              'default_project_id': self.id,
                            }
        return action
