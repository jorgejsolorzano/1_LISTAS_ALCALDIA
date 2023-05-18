# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
import logging

_logger = logging.getLogger(__name__)
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

# class medical_patient(models.Model):
#     _inherit = 'medical.patient'
#
#     user_id = fields.Many2one('res.users', 'Physician', index=True)


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


class Appointment(models.Model):
    _name = "nvx_hms.appointment"

    slot_id = fields.Many2one('nvx_hms.slot', string='Espacio', store=False)
    name = fields.Char(string='Código')
    start = fields.Char('Inicio')
    start_cmp = fields.Char('Inicio', compute='_get_computes')
    resource_id = fields.Many2one('resource.resource', string='Profesional')
    resource_cmp = fields.Char('Profesional', compute='_get_computes')
    duration = fields.Integer('Duración', default=15)
    duration_cmp = fields.Char('Duración', compute='_get_computes')

    procedure_id = fields.Many2one('nvx_hms.procedure', string='Procedimiento', domain="[('status', '=', True)]")
    lead_id = fields.Many2one('crm.lead', string='Prospecto')
    status = fields.Selection([('AGENDADA', 'Agendada'), ('CANCELADA', 'Cancelada'), ('CHEQUEADA', 'Chequeada')
                              , ('ASISTIDA', 'Asistida'), ('DESERTADA', 'Desertada')]
                              , string='Estado', default='AGENDADA')
    campaign_id = fields.Many2one('utm.campaign', string='Campaña')
    comments = fields.Text('Comentarios')
    old_data = fields.Text('Datos Antiguos')
    company_id = fields.Many2one('res.company', string='Sede')
    mobile = fields.Char(related='lead_id.phone', readonly=True, store=False)

    @api.model
    def create(self, vals):
        _logger.debug(' vals appointment create >>>>>>>>>>>>>> ' + str(vals))
        #vals['name'] = "A-" + vals['id'].zfill(8)
        result = super(Appointment, self).create(vals)
        result.write({'name': "A" + str(result.id).zfill(10)})
        #result.name = "A-" + result.id.zfill(8)
        return result

    def _get_computes(self):
        for i in self:
            i.start_cmp = str(i.start)
            i.resource_cmp = str(i.resource_id.user_id.name)
            i.duration_cmp = str(i.duration)

    @api.onchange('slot_id')
    def onchange_slot(self):
        self.start = self.slot_id.start
        self.resource_id = self.slot_id.resource_id
        self.duration = self.slot_id.duration
        self._get_computes()

    def action_cancel(self):
        for app1 in self:
            if app1.status in ['AGENDADA']:
                app1.status = 'CANCELADA'

    def action_checkin(self):
        msg1 = '\n'
        chq1 = 0
        estado_historia = ''
        #if app1.status in ['AGENDADA', 'CHEQUEADA']
        for app1 in self:
            if app1.status in ['AGENDADA', 'CHEQUEADA']:
                if not app1.lead_id.partner_id.id:
                    vals_partner = {'name': app1.lead_id.name
                                    , 'mobile': app1.lead_id.phone}
                    x_partner_obj = self.env['res.partner'].sudo().create(vals_partner)
                    _logger.debug(' action_checkin >>>>>>>>>>>>>> partner creado ' + str(x_partner_obj))
                    lead_id = self.env['crm.lead'].sudo().browse(app1.lead_id.id)
                    for lead1 in lead_id:
                        lead1.partner_id = x_partner_obj.id
                else:
                    x_partner_obj = app1.lead_id.partner_id
                    _logger.debug(' action_checkin >>>>>>>>>>>>>> partner existente ' + str(x_partner_obj) + '---' + str(x_partner_obj.id))

                x_patient_obj = self.env['medical.patient'].search([[u'patient_id', u'=', x_partner_obj.id]], limit=1)
                if not x_patient_obj.id:
                    vals_patient = {'name': app1.name, 'status': 'ABIERTA'
                                    , 'patient_id': x_partner_obj.id, 'user_id': app1.resource_id.user_id.id
                                    , 'appointment_id': app1.id}
                    self.env['medical.patient'].sudo().create(vals_patient)
                    estado_historia = 'ABIERTA'
                else:
                    for pat1 in x_patient_obj:
                        if pat1.status == 'ABIERTA':
                            pat1.user_id = app1.resource_id.user_id.id
                            estado_historia = 'ABIERTA'
                if estado_historia == 'ABIERTA':
                    chq1 += 1
                    app1.status = 'CHEQUEADA'
                    msg1 += '\n ' + app1.name \
                            + ' > Paciente: ' + app1.lead_id.partner_id.name \
                            + ' > Profesional: ' + app1.resource_id.user_id.name
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
        #return {'warning': {'title': 'Check-in', 'message': 'Cita(s) chequeada(s) con éxito!'}}





class Slot(models.Model):
    _name = "nvx_hms.slot"
    _auto = False

    name = fields.Char()
    start = fields.Char()
    resource_id = fields.Many2one('resource.resource', string='Profesional')
    duration = fields.Integer()
    company_id = fields.Many2one('res.company', string='Sede')


    #@api.model_cr
    def init(self):
        _logger.debug(' slot init >>>>>>>>>>>>')
        tools.drop_view_if_exists(self._cr, 'nvx_hms_slot')
        self._cr.execute(""" CREATE VIEW nvx_hms_slot AS (            					
                select row_number() OVER (ORDER BY start) AS id
                , concat(start::text , ', '  , rr.name  ) as name
                , start
                , resource_id
                , 20 as duration  
                , company_id
                from (   		
                            SELECT   
                                 substring(fecha::text from 1 for 19) as start
                                , a.id  as resource_id
                                FROM resource_resource a 
                                inner join resource_calendar_attendance b 
                                    on a.calendar_id = b.calendar_id
                                inner join generate_series(CURRENT_DATE, CURRENT_DATE + 30, '20 min'::interval) fecha
                                    on extract(isodow from  fecha) - 1 = dayofweek::int
                                    and extract(hour from  fecha) between hour_from and hour_to - 1
                                    and a.active = 'true'
                                    except
                                    
                                 SELECT start,
                                    ce.resource_id
                                   FROM nvx_hms_appointment ce
                                   where status not in ('CANCELADA')
                        ) avalability left join resource_resource rr on avalability.resource_id = rr.id 

        )""")




