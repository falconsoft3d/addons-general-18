# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime
import base64
import io
import xlrd

class PortalVacation(models.Model):
    _description = "Portal Vacation"
    _name = 'portal.vacation'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    name = fields.Char(string='Code', required=True, readonly=True, copy=False, index=True,
            default=lambda self: self.env['ir.sequence'].next_by_code('portal.photo'))
    date_from = fields.Date('Date From', required=True, help="Enter the start date of the vacation")
    date_to = fields.Date('Date To', required=True, help="Enter the end date of the vacation")
    reason = fields.Text('Reason', required=True, help="Enter the reason for the vacation")
    user_id = fields.Many2one('res.users', 'User', required=True, help="Select the user who is taking the vacation", default=lambda self: self.env.user.id)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, help="Status of the vacation request")


    def action_request(self):
        """Action to request vacation"""
        self.state = 'requested'
        self.message_post(body=_("Vacation request has been submitted."))

    def action_to_draft(self):
        """Action to revert vacation to draft state"""
        self.state = 'draft'
        self.message_post(body=_("Vacation request has been reverted to draft."))

    def action_approve(self):
        """Action to approve vacation"""
        self.state = 'approved'
        self.message_post(body=_("Vacation request has been approved."))

    def action_decline(self):
        """Action to decline vacation"""
        self.state = 'rejected'
        self.message_post(body=_("Vacation request has been rejected."))