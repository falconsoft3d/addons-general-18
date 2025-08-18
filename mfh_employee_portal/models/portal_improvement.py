# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime
import base64
import io
import xlrd

class PortalImprovement(models.Model):
    _description = "Portal Improvement"
    _name = 'portal.improvement'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    name = fields.Char(string='Code', required=True, readonly=True, copy=False, index=True,
            default=lambda self: self.env['ir.sequence'].next_by_code('portal.improvement'))
    project_id = fields.Many2one('project.project', 'Project', ondelete="cascade")
    title = fields.Char('Title', required=True, help="Enter the Title")
    description = fields.Text('Description', help="Enter the Description")