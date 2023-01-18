from odoo import models, fields, api


class Registraduria(models.Model):
    _name = 'registraduria.listas'
    _description = 'Lista de votantes en la Registraduria de Valledupar'


    departamento = fields.Char(string="DEPARTAMENTO")
    minicipio= fields.Char(string="MUNICIPIO")
    puesto = fields.Char(string="PUESTO")
    direccion = fields.Char(string="DIRECCION")
    mesa = fields.Char(string="MESA")