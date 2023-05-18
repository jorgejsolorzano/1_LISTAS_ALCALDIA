# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

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
                                              ('rfc', 'RFC')], string='Document Type',
                                             help='Indicates to what document the information in here belongs to.')


