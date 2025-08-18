# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime
import base64
import io
import xlrd

class PortalComplaint(models.Model):
    _description = "Portal Complaint"
    _name = 'portal.complaint'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    name = fields.Char(string='Code', required=True, readonly=True, copy=False, index=True,
            default=lambda self: self.env['ir.sequence'].next_by_code('portal.complaint'))
    title = fields.Char('Title', required=True, help="Enter the Title")
    description = fields.Text('Description', help="Enter the Description")
    user_id = fields.Many2one('res.users', 'User', required=True, help="Select the user who is taking the complaint", default=lambda self: self.env.user.id)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, help="Status of the complaint request")


    def action_request(self):
        """Action to request complaint"""
        self.state = 'requested'
        self.message_post(body=_("Complaint request has been submitted."))

    def action_to_draft(self):
        """Action to revert complaint to draft state"""
        self.state = 'draft'
        self.message_post(body=_("Complaint request has been reverted to draft."))

    def action_approve(self):
        """Action to approve complaint"""
        self.state = 'approved'
        self.message_post(body=_("Complaint request has been approved."))

    def action_decline(self):
        """Action to decline complaint"""
        self.state = 'rejected'
        self.message_post(body=_("Complaint request has been rejected."))