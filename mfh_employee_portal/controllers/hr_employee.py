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
from odoo import SUPERUSER_ID

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


    @http.route('/portal/dashboard/<token>', methods=['GET'], auth='none')
    def entrar_endpoint(self, **kwargs):
        _logger.info("=entrar_endpoint=")
        _logger.info("kwargs: %s", kwargs)


        token = kwargs.get('token')
        latitude = kwargs.get('latitude')
        longitude = kwargs.get('longitude')


        employee = http.request.env['hr.employee'].with_user(SUPERUSER_ID).search([
            ('token', '=', token),
            ('active_login', '=', True)
        ], limit=1)



        company = http.request.env['res.company'].sudo().search([], limit=1)




        if not employee:
            return env.get_template('login_portal.html').render({
                'csrf_token': http.request.csrf_token(),
            })
        else:
            company_id = employee.company_id

            # Proyectos abiertos
            projects_not_use_geolocation_ids = http.request.env['project.project'].sudo().search([
                ('use_geolocation', '=', False),
            ])

            projects_use_geolocation_ids = http.request.env['project.project'].sudo().search([
                ('use_geolocation', '=', True),
            ])

            # recorremos los proyectos para quitar los que no esten dentro del rango de distancia
            if latitude and longitude:
                latitude = float(latitude)
                longitude = float(longitude)

                portal_parameter_distance_km = http.request.env['ir.config_parameter'].sudo().get_param('mfh_employee_portal.portal_parameter_distance_km', default=1)

                projects_use_geolocation_ids = projects_use_geolocation_ids.filtered(
                    lambda p: math.sqrt((p.latitude - latitude) ** 2 + (p.longitude - longitude) ** 2) <= portal_parameter_distance_km)



            projects = projects_not_use_geolocation_ids + projects_use_geolocation_ids

            # comprobamos si hay una asistencia abierta
            hr_attendance_id = http.request.env['hr.attendance'].sudo().search([
                ('employee_id', '=', employee.id),
                ('check_out', '=', False)
            ], limit=1)

            return env.get_template('dashboard_portal.html').render({
                'csrf_token': http.request.csrf_token(),
                'token': token,
                'projects': projects,
                'employee' : employee,
                'hr_attendance_id': hr_attendance_id,
            })


    # register in
    @http.route('/portal/post/register', type='json', auth='public', cors='*')
    def portal_post_register(self, **kwargs):
        _logger.info("== portal_post_register ==")
        token = kwargs.get('token')
        project = kwargs.get('project')

        employee_id = http.request.env['hr.employee'].sudo().search([('token', '=', token),
                                                                  ('active_login', '=', True)], limit=1)
        project_id = http.request.env['project.project'].sudo().search([('id', '=', project)], limit=1)

        if not employee_id or not project_id:
            return {
                    'status': 'error',
                    'error': 'Token Incorrecto',
                }
        else:
            # Creamos una asistencia

            vals = {
                'employee_id': employee_id.id,
                'check_in': fields.Datetime.now(),
                'project_id': project_id.id,
            }

            _logger.info(vals)

            hr_attendance = http.request.env['hr.attendance'].sudo().create(vals)

            return {
                    'status': 'ok',
                    'user': employee_id.name,
                    'token': token,
                }

    # register out
    @http.route('/portal/post/exit', type='json', auth='public', cors='*')
    def portal_post_register_out(self, **kwargs):
        _logger.info("== portal_post_register_out ==")
        token = kwargs.get('token')

        employee_id = http.request.env['hr.employee'].sudo().search([('token', '=', token),
                                                                  ('active_login', '=', True)], limit=1)

        if not employee_id:
            return {
                    'status': 'error',
                    'error': 'Token Incorrecto',
                }
        else:
            # Comprobamos si hay una asistencia abierta
            hr_attendance = http.request.env['hr.attendance'].sudo().search([
                ('employee_id', '=', employee_id.id),
                ('check_out', '=', False)
            ], limit=1)

            if not hr_attendance:
                return {
                    'status': 'error',
                    'error': 'No hay una asistencia abierta',
                }

            # Cerramos la asistencia
            hr_attendance.check_out = fields.Datetime.now()

            return {
                    'status': 'ok',
                    'user': employee_id.name,
                    'token': token,
                }