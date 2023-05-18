# -*- coding: utf-8 -*-

import datetime
import logging
import json
import pytz
from odoo import api, fields, models, tools
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


def timezone_converter(input_dt, current_tz='UTC', target_tz='UTC'):
    # input_dt = input_dt.replace(tzinfo=None)
    current_tz = pytz.timezone(current_tz)
    target_tz = pytz.timezone(target_tz)
    target_dt = current_tz.localize(input_dt).astimezone(target_tz)
    return target_tz.normalize(target_dt).replace(tzinfo=None)

# class nvx_hms(models.Model):
#     _name = 'nvx_hms.nvx_hms'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class ResourceResource(models.Model):
    _inherit = 'resource.resource'

    procedure_ids = fields.Many2many('nvx_hms.procedure', string='Procedimientos del recurso')


class AbsDateTime(fields.Char):
    desc = fields.Char()


class Procedure(models.Model):
    _name = "nvx_hms.procedure"

    name = fields.Char()
    product_id = fields.Many2one('product.template', string='Producto')
    type = fields.Selection([('1RAVEZ', '1ra Vez'), ('CONTROL', 'Control'), ('OTRO', 'Otro')]
                            , string='Tipo', default='1RAVEZ')
    duration = fields.Integer(string='Duración', default=15)
    status = fields.Boolean('Activo', default=True)
    resource_ids = fields.Many2many('resource.resource', string='Recursos del Procedimiento')


class AppointmentCheck(models.TransientModel):
    _name = 'nvx_hms.appointment.check'
    _description = 'Appointment Check-IN'

    appointment_id = fields.Many2one('nvx_hms.appointment', string='ID Cita'
                                  , default=lambda self: self._get_default_appointment_id())
    resource_id = fields.Many2one('resource.resource', string='Profesional'
                                  , default=lambda self: self._get_default_resource_id())
    product_id = fields.Many2one('product.product', string='Producto'
                                 , domain="[('categ_id', 'in', ('Plan', 'Control', 'Terapia'))]"
                                 , default=lambda self: self._get_default_product_id())
    l10n_co_document_type = fields.Selection([('rut', 'NIT'),
                                            ('id_document', 'Cédula'),
                                            ('id_card', 'Tarjeta de Identidad'),
                                            ('passport', 'Pasaporte'),
                                            ('foreign_id_card', 'Cédula Extranjera'),
                                            ('external_id', 'ID del Exterior'),
                                            ('diplomatic_card', 'Carné Diplomatico'),
                                            ('residence_document', 'Salvoconducto de Permanencia'),
                                            ('civil_registration', 'Registro Civil'),
                                            ('national_citizen_id', 'Cédula de ciudadanía'),
                                            ('rfc', 'RFC')], string='Tipo de Documento',
                                            help='Tipo de Documento de identidad', default=lambda self: self._get_default_l10n_co_document_type())
    vat = fields.Char(string='Documento de identidad', default=lambda self: self._get_default_vat())
    contact_address = fields.Char(string='Dirección de Contacto')
    companion_name = fields.Char(string='Nombre del Acompañante')
    companion_phone = fields.Char(string='Teléfono del Acompañante')
    guardian_name = fields.Char(string='Nombre del Responsable')
    guardian_phone = fields.Char(string='Teléfono del Responsable')    
    guardian_relationship = fields.Char(string='Parentesco del Responsable')
    health_insurance = fields.Char(string='Seguro Médico')
    insurance_type = fields.Selection([('contributivo', 'Contributivo'), ('subsidiado', 'Subsidiado'), ('otro', 'Otro')], string='Tipo de Vinculación')

    def action_checkin(self):
        try:
            vals_partner_update = {'l10n_co_document_type': self.l10n_co_document_type, 'vat': self.vat}
            vals_partner_create = {'name': self.appointment_id.lead_id.name, 'mobile': self.appointment_id.lead_id.phone, **vals_partner_update}
            if not self.appointment_id.lead_id.partner_id.id:
                x_partner_obj = self.env['res.partner'].sudo().create(vals_partner_create)
                _logger.debug(' action_checkin 1 >>>>>>>>>>>>>> partner creado ' + str(x_partner_obj))
                for lead1 in self.appointment_id.lead_id:
                    lead1.partner_id = x_partner_obj.id
            else:
                x_partner_obj = self.appointment_id.lead_id.partner_id
                _logger.debug(' action_checkin 1 >>>>>>>>>>>>>> partner existente actualizado 2 ' + str(x_partner_obj))
                x_partner_obj.sudo().write(vals_partner_update)
            extra_data = {
                    'contact_address': self.contact_address
                    ,'companion_name': self.companion_name
                    ,'companion_phone': self.companion_phone
                    ,'guardian_name': self.guardian_name
                    ,'guardian_phone': self.guardian_phone
                    ,'guardian_relationship': self.guardian_relationship
                    ,'health_insurance': self.health_insurance
                    ,'insurance_type': self.insurance_type
            }
            self.appointment_id.write({'resource_id': self.resource_id
                            , 'product_id': self.product_id
                            , 'extra_data': json.dumps(extra_data)
                            })
        except Exception as e:
            msg = f'ERROR: No fue posible actualizar datos del paciente, revise los datos.  {e}'
            raise UserError(msg)
        return self.appointment_id._action_checkin()

    @api.model
    def _get_default_appointment_id(self):
        return self.env['nvx_hms.appointment'].browse(self.env.context.get('default_appointment_id'))

    @api.model
    def _get_default_resource_id(self):
        return self.env['nvx_hms.appointment'].browse(self.env.context.get('default_appointment_id')).resource_id

    @api.model
    def _get_default_product_id(self):
        return self.env['nvx_hms.appointment'].browse(self.env.context.get('default_appointment_id')).product_id

    @api.model
    def _get_default_l10n_co_document_type(self):
        try:
            return self.env['nvx_hms.appointment'].browse(self.env.context.get('default_appointment_id')).lead_id.partner_id.l10n_co_document_type
        except:
            return None

    @api.model
    def _get_default_vat(self):
        try:
            return self.env['nvx_hms.appointment'].browse(self.env.context.get('default_appointment_id')).lead_id.partner_id.vat
        except:
            return None


class Appointment(models.Model):
    _name = "nvx_hms.appointment"
    _inherit = 'mail.thread'

    slot_id = fields.Many2one('nvx_hms.slot', string='Espacio', store=False )
    name = fields.Char(string='Código')
    start = fields.Char('Inicio', index=True)
    start_cmp = fields.Char('Inicio')
    resource_id = fields.Many2one('resource.resource', string='Profesional')
    resource_cmp = fields.Char('Profesional')
    duration = fields.Integer('Duración', default=15)
    duration_cmp = fields.Char('Duración')

    procedure_id = fields.Many2one('nvx_hms.procedure', string='Procedimiento', domain="[('status', '=', True)]")
    lead_id = fields.Many2one('crm.lead', string='Prospecto')
    status = fields.Selection([('AGENDADA', 'Agendada'), ('PREPAGADA', 'Prepagada')
                                  , ('CANCELADA', 'Cancelada') , ('CHEQUEADA', 'Chequeada')
                                  , ('ASISTIDA', 'Asistida'), ('DESERTADA', 'Desertada')]
                              , string='Estado', default='AGENDADA')
    campaign_id = fields.Many2one('utm.campaign', string='Campaña')
    comments = fields.Text('Comentarios')
    old_data = fields.Text('Datos Antiguos')
    company_id = fields.Many2one('res.company', string='Sede')
    mobile = fields.Char(related='lead_id.phone', readonly=True, store=False)
    temp_resource_ids = fields.Many2many('resource.resource', store=False)
    start_date = fields.Char('Dia Inicio', compute='_get_start_date', store=True)
    #stop_date = fields.Char('Fecha Fin', compute='_get_start_date', store=True)
    product_id = fields.Many2one('product.product', string='Producto', domain="[('categ_id', 'in', ('Plan', 'Control'))]")
    attending_status = fields.Char(string='Estado Asistencia')
    extra_data = fields.Text('Extra Data')

    @api.model
    def update_status(self, days_after=10000, batch_size=1000):
        x_from = fields.Date.today() - datetime.timedelta(days=days_after) 
        x_to = fields.Date.today() - datetime.timedelta(hours=8)
        appo_list = self.env['nvx_hms.appointment'].sudo().search([
                                                         [u'start', '>', str(x_from)], [u'start', '<', str(x_to)]
                                                        ], limit=batch_size, order='start desc')
        for appo in appo_list:
            x_appo_date = datetime.datetime.strptime(appo.start.split('+')[0], '%Y-%m-%d %H:%M:%S')
            x_invoice_from = x_appo_date - datetime.timedelta(hours=18)
            x_invoice_to = x_appo_date + datetime.timedelta(hours=18)
            partners = []
            partner_ids = []
            x_phone = '0' * 7
            x_name = 'X' * 20
            if appo.lead_id.phone:
                x_phone = appo.lead_id.phone[-7:]
            if appo.lead_id.name:
                x_name = appo.lead_id.name[:20]
            _logger.debug(f'Appointments - update_status - {appo.name} {x_phone}  {x_name} >>>>>>>>>>>>>> ')
            partners = self.env['res.partner'].sudo().search([
                                            '|' 
                                                , '|', (u'mobile', u'like', x_phone)
                                                    , (u'phone', u'like', x_phone)
                                                , (u'name', u'like', x_name)
                                            ])
            if appo.lead_id.partner_id:
                partner_ids += [appo.lead_id.partner_id.id] 
            if len(partners) > 0:    
                partner_ids += partners.ids
            invoice_count = self.env['account.move'].sudo().search_count([
                                                        [u'partner_id', u'in', partner_ids]
                                                        , [u'date', '>', x_invoice_from], [u'date', '<', x_invoice_to]
                                                        , [u'state', '=', 'posted'], ['type', 'in', ['out_invoice'] ]
                                                        ])
            pos_orders_count = self.env['pos.order'].sudo().search_count([
                                            [u'partner_id', u'in', partner_ids]
                                            , [u'date_order', '>', x_invoice_from], [u'date_order', '<', x_invoice_to]
                                            , [u'state', 'in', ['posted', 'done' ]]
                                            ])
            new_attending_status = 'DESERTADA'
            if invoice_count + pos_orders_count > 0 or appo.status in ['CHEQUEADA', 'ASISTIDA', 'PREPAGADA']:
                new_attending_status = 'ASISTIDA'

            appo.attending_status = new_attending_status
            _logger.debug(f'Appointments - update_status - {new_attending_status} - {appo.name}  {str(partner_ids)}  >>>>>>>>>>>>>> ')
                
    def validate_appointment(self, vals):
        #procedure = self.env['nvx_hms.procedure'].sudo().browse([vals['procedure_id']])
        sede = vals['company_id']
        resource = self.env['resource.resource'].sudo().browse([vals['resource_id']])
        start = vals['start']
        _logger.debug(f' validate_appointment create >>>>>>>>>>>>>> {str(vals)}  {resource.company_id.id}')
        if sede != resource.company_id.id:
            msg = f'ERROR: El profesional {resource.name} no tiene agenda creada en la sede {str(sede)}.'
            raise UserError(msg)
        concurrent_appointments = self.env['nvx_hms.appointment'].sudo().search_count([
                                                [u'start', u'=', start]
                                                , [u'resource_id', '=', resource.id]
                                                , [u'status', '!=', 'CANCELADA']
                                                ])
        if concurrent_appointments > 0:
            msg = f'ERROR: El profesional {resource.name} ya tiene ocupado el horario {start}.'
            raise UserError(msg)
        return True

    @api.model
    def create(self, vals):
        _logger.debug(' vals appointment create >>>>>>>>>>>>>> ' + str(vals))
        if 'minutos' in vals['duration_cmp']:
            try:
                cleaned = vals['duration_cmp'].replace('dias','').replace('horas','').replace('minutos','').replace(' ','')
                splitted = cleaned.split('=')
                blocking_duration = int(splitted[1])*24*60 + int(splitted[2])*60 + int(splitted[3])
                vals['duration'] = blocking_duration
            except:
                msg = f'''ERROR: Duración del BLOQUEO debe ser de la forma "dias=0 horas=0 minutos=0".  
                                    Ejemplo para 2 horas y media: dias=0 horas=2 minutos=30
                                    Ejemplo para 1 dias y 5 horas: dias=1 horas=5 minutos=0
                        '''
                raise UserError(msg)
        else:
            self.validate_appointment(vals)
        #vals['name'] = "A-" + vals['id'].zfill(8)
        result = super(Appointment, self).create(vals)

        result.write({'name': "A" + str(result.id).zfill(10)})
        result.message_post(body=f'Cita {result.name} creada.')
        # result.name = "A-" + result.id.zfill(8)
        mc_config1 = self.env['mass_chat.config'].sudo().search([[u'company_id', u'=', result.company_id.id]], limit=1)
        for cfg in mc_config1:
            if cfg.appointment_sequence_id:
                try:
                    extra_data = {'#SEDE': result.company_id.name}
                    x_phone = result.lead_id.phone.replace(' ', '').replace('+', '')
                    contact_number = f'{x_phone}@c.us'
                except AttributeError:
                    msg = f'ERROR: Prospecto no tiene celular registrado, revise los datos'
                    raise UserError(msg)
                try:
                    mail_channel = self.env['mail.channel'].sudo().search([[u'name', u'=', contact_number]], order='id desc', limit=1)
                    mass_chat_account = self.env['mass_chat.account'].sudo().search([[u'im_livechat_channel_id', u'=', mail_channel.livechat_channel_id.id]], order='id desc', limit=1)
                    result.lead_id.sequence_reverse_by_ids(result.lead_id.phone
                                                            , [cfg.appointment_sequence_id.id]
                                                            , result.start, extra_data=extra_data
                                                            , override_mc_account_id=mass_chat_account.id)
                except:
                    _logger.info(f' Error en configuración de secuencia agendamiento cita. | {str(result)} | {str(mail_channel)} | {str(mass_chat_account)}')
                result.message_post(body=f'Secuencia Agendó Cita programada - {mass_chat_account.name} - {cfg.appointment_sequence_id.name}')
                    #Company 1 = mc_account 11,   Company 5 = mc_account 12
                """
                override_mc_account_id=None
                extra_data = None
                if not('-' in result.company_id.name):
                    if result.company_id.id == 1:
                        override_mc_account_id = 11
                    if result.company_id.id == 5:
                        override_mc_account_id = 12
                    extra_data = {'#SEDE': result.company_id.name}
                    result.lead_id.sequence_reverse_by_ids(result.lead_id.phone, [cfg.appointment_sequence_id.id]
                                                    , result.start, extra_data=extra_data, override_mc_account_id=override_mc_account_id)
                
                """


        return result

    def get_changes(self, vals):
        obj = self.read()[0]
        #raise UserError(str(obj) + '-------------------' +  str(dict_new))
        #dict_old = dict(obj[0])
        changes = ""
        for key, value in vals.items():
            changes += f"\n {key} : {obj[key]} > {value}"
        #raise UserError(str(dict_changes))
        return changes

    def write(self, vals):
        for item in self:
            #item.validate_appointment(vals)
            old_data = {}
            vals_changed = item.get_changes(vals)
            if len(set(['name', 'resource_id', 'start', 'company_id', 'lead_id', 'status', 'mobile', 'product_id' ]).intersection(vals.keys())) > 0:
                _logger.debug(' vals appointment write >>>>>>>>>>>>>> ' + str(vals))
                old_data = {'Profesional': item.resource_id.name, 'Fecha cita': item.start
                            , 'Sede': item.company_id.name, 'Prospecto': item.lead_id.name
                            , 'Estado': item.status, 'Celular': item.mobile, 'Producto': item.product_id.product_tmpl_id.name}
                item.message_post(body=f'Cita modificada. ----- Datos anteriores {str(old_data)}')
            result = super().write(vals)
            mc_config1 = item.env['mass_chat.config'].sudo().search([[u'id', u'>', 0]], limit=1)
            for cfg in mc_config1:
                if 1 == 0 and cfg.appointment_sequence_id:
                    item.lead_id.sequence_deactivate_by_ids(result.lead_id.phone, [cfg.appointment_sequence_id.id])
                    item.lead_id.sequence_reverse_by_ids(result.lead_id.phone, [cfg.appointment_sequence_id.id]
                                                        , result.start)
            return result

    def _get_computes(self):
        pass

    @api.depends("start")
    def _get_start_date(self):
        for i in self:
            try: 
                i.start_date = i.start.split(' ')[0]
            except:
                #_logger.debug(' ERROR NVX Appointment _get_start_date convirtiendo a fecha >>>>>>>>>>> ' + str(i.start_date))
                i.start_date = None

    @api.onchange('company_id')
    def onchange_company_id(self):
        for i in self:
            i.slot_id = None
            i.procedure_id = None
            domain = [('company_id', '=', i.company_id.id)]
            if i.procedure_id:
                domain = [('company_id', '=', i.company_id.id), ('resource_id', 'in', i.procedure_id.resource_ids.ids)]
            _logger.debug(f' DEBUG Appointment onchange_company_id domain  >>>>>>>>>>> {domain} ')                             
            return {'domain': {'slot_id': domain}}

    @api.onchange('procedure_id')
    def onchange_procedure_id(self):
        for i in self:
            i.duration = i.procedure_id.duration
            i.temp_resource_ids = i.procedure_id.resource_ids
            i.slot_id = None
            if i.procedure_id.name == 'BLOQUEO':
                i.duration_cmp = "dias=0 horas=0 minutos=" + str(i.procedure_id.duration)
                domain = [('company_id', '=', i.company_id.id)]
            else:
                i.duration_cmp = str(i.procedure_id.duration)
                domain = [('company_id', '=', i.company_id.id), ('resource_id', 'in', i.procedure_id.resource_ids.ids)]
            _logger.debug(f' DEBUG Appointment onchange_procedure_id domain  >>>>>>>>>>> {domain} ')                             
            return {'domain': {'slot_id': domain}}

    @api.onchange('slot_id')
    def onchange_slot_id(self):
        for i in self:
            i.start = i.slot_id.start
            i.start_date2 = i.slot_id.start 
            _logger.debug(f' DEBUG Appointment onchange_slot_id  >>>>>>>>>>> {i.start}  {i.start_date2}')
            i.resource_id = i.slot_id.resource_id
            # self.duration = self.slot_id.duration
            i.start_cmp = str(i.start)
            i.resource_cmp = str(i.resource_id.user_id.name)
            if i.procedure_id.name == 'BLOQUEO':
                i.duration_cmp = "dias=0 horas=0 minutos=" + str(i.procedure_id.duration)
            else:
                i.duration_cmp = str(i.duration)

    def action_cancel(self):
        for app1 in self:
            if app1.status in ['AGENDADA']:
                app1.status = 'CANCELADA'

    def action_prepay(self):
        for app1 in self:
            if app1.status in ['AGENDADA']:
                app1.status = 'PREPAGADA'

    def _action_checkin(self):
        msg1 = '\n'
        chq1 = 0
        estado_historia = ''
        # if app1.status in ['AGENDADA', 'CHEQUEADA']
        for app1 in self:
            lead_id = self.env['crm.lead'].sudo().browse(app1.lead_id.id)
            if app1.status in ['AGENDADA', 'CHEQUEADA', 'PREPAGADA']:
                vals_partner = {'name': app1.lead_id.name, 'mobile': app1.lead_id.phone}
                if not app1.lead_id.partner_id.id:
                    x_partner_obj = self.env['res.partner'].sudo().create(vals_partner)
                    _logger.debug(' action_checkin >>>>>>>>>>>>>> partner creado ' + str(x_partner_obj))
                    for lead1 in lead_id:
                        lead1.partner_id = x_partner_obj.id
                    '''                    
                    partner1 = self.env['res.partner'].sudo().search([[u'mobile', u'like', lead_id.phone[-10:]]], limit=1)
                    if len(partner1) == 0:
                        x_partner_obj = self.env['res.partner'].sudo().create(vals_partner)
                        _logger.debug(' action_checkin >>>>>>>>>>>>>> partner creado ' + str(x_partner_obj))
                        # new_partner_id = x_partner_obj.id
                    else:
                        _logger.debug(' action_checkin >>>>>>>>>>>>>> partner existente actualizado 1 ' + str(partner1))
                        partner1.sudo().write(vals_partner)
                        x_partner_obj = partner1

                    for lead1 in lead_id:
                        lead1.partner_id = x_partner_obj.id
                    '''
                else:
                    x_partner_obj = app1.lead_id.partner_id
                    _logger.debug(' action_checkin >>>>>>>>>>>>>> partner existente actualizado 2 ' + str(x_partner_obj))
                    x_partner_obj.sudo().write(vals_partner)
                #Consultas anteriores
                old_patient_obj = self.env['medical.patient'].search([[u'patient_id', u'=', x_partner_obj.id],
                                                    [u'appointment_id', u'<', app1.id]
                                                    ])
                date_of_birth = None
                sex = None
                age = None
                marital_status = None
                for old_pat1 in old_patient_obj:
                    date_of_birth = old_pat1.date_of_birth or date_of_birth
                    sex = old_pat1.sex or sex
                    age = old_pat1.age or age
                    marital_status = old_pat1.marital_status or marital_status
                old_patient_obj.sudo().write({'status': 'CERRADA'
                                                , 'history_user_id': app1.resource_id.user_id.id
                                                })
                #

                x_patient_obj = self.env['medical.patient'].search([[u'patient_id', u'=', x_partner_obj.id],
                                                                    [u'appointment_id', u'=', app1.id]
                                                                    ])
                extra_data = json.loads(app1.extra_data)
                if not x_patient_obj.id:
                    vals_patient = {'name': app1.name, 'status': 'ABIERTA'
                        , 'patient_id': x_partner_obj.id
                        , 'user_id': app1.resource_id.user_id.id
                        , 'history_user_id': app1.resource_id.user_id.id
                        , 'appointment_id': app1.id
                        , 'date_of_birth': date_of_birth
                        , 'sex': sex
                        , 'age': age
                        , 'marital_status':marital_status
                        , 'contact_address': extra_data.get('contact_address')
                        , 'companion_name': extra_data.get('companion_name')
                        , 'companion_phone': extra_data.get('companion_phone')
                        , 'guardian_name': extra_data.get('guardian_name')
                        , 'guardian_phone': extra_data.get('guardian_phone')
                        , 'guardian_relationship': extra_data.get('guardian_relationship')
                        , 'health_insurance': extra_data.get('health_insurance')
                        , 'insurance_type': extra_data.get('insurance_type')
                        }
                    self.env['medical.patient'].sudo().create(vals_patient)
                    estado_historia = 'ABIERTA'
                else:
                    for pat1 in x_patient_obj:
                        if pat1.status == 'ABIERTA' or 1 == 1:
                            pat1.user_id = app1.resource_id.user_id.id
                            pat1.history_user_id = app1.resource_id.user_id.id
                            estado_historia = 'ABIERTA'
                        pat1.appointment_id = app1.id



                if estado_historia == 'ABIERTA':
                    chq1 += 1
                    app1.status = 'CHEQUEADA'
                    msg1 += '\n ' + app1.name \
                            + ' > Paciente: ' + app1.lead_id.partner_id.name \
                            + ' > Profesional: ' + app1.resource_id.name
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = str(chq1) + '  Cita(s) chequeada(s) con éxito! ' + msg1
        return {
            'name': 'Proceso Chequeo.',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view_id,
            'target': 'new',
            'context': context,
        }
        # return {'warning': {'title': 'Check-in', 'message': 'Cita(s) chequeada(s) con éxito!'}}


class Slot(models.Model):
    _name = "nvx_hms.slot"
    _auto = False
    _order = "name"

    name = fields.Char()
    start = fields.Char()
    resource_id = fields.Many2one('resource.resource', string='Profesional')
    duration = fields.Integer()
    company_id = fields.Many2one('res.company', string='Sede')
    durations = fields.Char()

    def search(self, args, **kwargs):
        _logger.debug(f' SLOT_appointment domain >>>>>>>>>>>>>> {args}    xxxxxxxxxxxxxxxxxx   {kwargs}')
        #domain = [('company_id', '=', 1), ('durations', 'like', '30')]
        domain = args
        return super(Slot, self).search(domain, **kwargs)

    # @api.model_cr
    def init(self):
        _logger.debug(' slot init >>>>>>>>>>>>')
        if 1 == 0:
            tools.drop_view_if_exists(self._cr, 'nvx_hms_slot')
            self._cr.execute(""" 
CREATE OR REPLACE VIEW public.nvx_hms_slot_20220529
AS SELECT concat((10 * rr.company_id)::text, (100 * avalability.resource_id)::text, to_char(avalability.start, 'MMDDHHMI'::text))::bigint AS id,
    concat("substring"(avalability.start::text, 1, 29), ', ', rr.name) AS name,
    "substring"(avalability.start::text, 1, 29) AS start,
    avalability.resource_id,
    30 AS duration,
    rr.company_id,
    ((((((('D30'::text ||
        CASE avalability.start - lead(avalability.start, 1) OVER (PARTITION BY avalability.resource_id, (avalability.start::date) ORDER BY avalability.start)
            WHEN '-00:30:00'::interval THEN 'D60'::text
            ELSE ''::text
        END) ||
        CASE avalability.start - lead(avalability.start, 2) OVER (PARTITION BY avalability.resource_id, (avalability.start::date) ORDER BY avalability.start)
            WHEN '-01:00:00'::interval THEN 'D90'::text
            ELSE ''::text
        END) ||
        CASE avalability.start - lead(avalability.start, 3) OVER (PARTITION BY avalability.resource_id, (avalability.start::date) ORDER BY avalability.start)
            WHEN '-01:30:00'::interval THEN 'D120'::text
            ELSE ''::text
        END) ||
        CASE avalability.start - lead(avalability.start, 4) OVER (PARTITION BY avalability.resource_id, (avalability.start::date) ORDER BY avalability.start)
            WHEN '-02:00:00'::interval THEN 'D150'::text
            ELSE ''::text
        END) ||
        CASE avalability.start - lead(avalability.start, 5) OVER (PARTITION BY avalability.resource_id, (avalability.start::date) ORDER BY avalability.start)
            WHEN '-02:30:00'::interval THEN 'D180'::text
            ELSE ''::text
        END) ||
        CASE avalability.start - lead(avalability.start, 6) OVER (PARTITION BY avalability.resource_id, (avalability.start::date) ORDER BY avalability.start)
            WHEN '-03:00:00'::interval THEN 'D210'::text
            ELSE ''::text
        END) ||
        CASE avalability.start - lead(avalability.start, 7) OVER (PARTITION BY avalability.resource_id, (avalability.start::date) ORDER BY avalability.start)
            WHEN '-03:30:00'::interval THEN 'D240'::text
            ELSE ''::text
        END) ||
        CASE avalability.start - lead(avalability.start, 8) OVER (PARTITION BY avalability.resource_id, (avalability.start::date) ORDER BY avalability.start)
            WHEN '-04:00:00'::interval THEN 'D270'::text
            ELSE ''::text
        END AS durations
   FROM ( SELECT fecha.fecha AS start,
            a.id AS resource_id
           FROM resource_resource a
             JOIN resource_calendar_attendance b ON a.calendar_id = b.calendar_id
             JOIN generate_series(CURRENT_DATE::timestamp with time zone, (CURRENT_DATE + 30)::timestamp with time zone, '00:30:00'::interval) fecha(fecha) ON (date_part('isodow'::text, fecha.fecha) - 1::double precision) = b.dayofweek::integer::double precision AND date_part('hour'::text, fecha.fecha) >= b.hour_from AND date_part('hour'::text, fecha.fecha) <= (b.hour_to - 1::double precision) AND a.active = true
        EXCEPT
         SELECT generate_series(to_timestamp(ce.start::text, 'YYYY-MM-DD HH24:MI:SS'::text), to_timestamp(ce.start::text, 'YYYY-MM-DD HH24:MI:SS'::text) + '00:01:00'::interval * (ce.duration - 1)::double precision, '00:20:00'::interval) AS busy_slot,
            ce.resource_id
           FROM nvx_hms_appointment ce
          WHERE ce.start::text >= to_char(CURRENT_DATE::timestamp with time zone, 'YYYY-MM-DD HH24:MI:SS'::text) AND ce.status::text <> 'CANCELADA'::text) avalability
     LEFT JOIN resource_resource rr ON avalability.resource_id = rr.id
  WHERE concat("substring"(avalability.start::text, 1, 29), ', ', rr.name) !~~ '%:30:00+00, Respaldo%'::text;
            """)
