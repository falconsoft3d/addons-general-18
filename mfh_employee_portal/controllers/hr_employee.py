import jinja2
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo import models, fields, _
import math
import logging
_logger = logging.getLogger(__name__)
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.fields import Datetime


loader = jinja2.PackageLoader('odoo.addons.mfh_employee_portal', 'web')
env = jinja2.Environment(loader=loader, autoescape=True)


class PortalHrEmployee(http.Controller):

    @http.route('/portal', methods=['GET'], auth='none')
    def login_endpoint(self, **kwargs):
        _logger.info("=login_endpoint=")
        company = http.request.env['res.company'].sudo().search([], limit=1)
        return env.get_template('login_portal.html').render({
            'csrf_token': http.request.csrf_token(),
            'company': company,
        })



    @http.route('/portal/login/check', type='json', auth='public', cors='*')
    def login_response(self, **kwargs):
        password = kwargs.get('password')
        employee = http.request.env['hr.employee'].sudo().search([('attendance_password', '=', password),
                                                                  ('active_login', '=', True)
                                                                 ], limit=1)

        if employee:
            if employee.attendance_password == password:
                # Creamos un token para el usuario
                employee.generate_token()
                token = employee.token
                request.session['my_current_url'] = kwargs.get('url')

                # Revisamo si hay una asistencia
                hr_attendance = http.request.env['hr.attendance'].sudo().search([
                                                                  ('employee_id', '=', employee.id),
                                                                  ('check_out', '=', False)], limit=1)

                if hr_attendance:
                    login = '0'
                else:
                    login = '1'

                return {
                    'status': 'ok',
                    'user': employee.name,
                    'password': password,
                    'token': token,
                    'login' : login,
                }
            else:
                return {
                    'status': 'error',
                    'error': 'Codigo Incorrecto',
                    'user': 0
                }
        else:
            return {
                'status': 'error',
                'error': 'Contraseña Incorrecta',
                'user': 0
            }