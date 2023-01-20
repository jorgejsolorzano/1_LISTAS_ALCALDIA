
from odoo import models, fields, api


class milistado(models.Model):
     _name = 'milistado.listas'
     _description = 'Creacion listado alcaldia de Valledupar'

     
     cedula = fields.Char(string="CEDULA", required=True, size=10)
     nombres = fields.Char(string="NOMBRES")
     apellidos = fields.Char(string="APELLIDOS")
     sexo = fields.Selection([('M','Masculino'),('F','Femenino'), ('O','LGTBIQ+')], string="SEXO")
     movil = fields.Char(string="MOVIL", size=9)
     email = fields.Char(string="E-MAIL")

     departamento = fields.Char(string="DEPARTAMENTO", default='Cesar')
     municipio = fields.Char(string="MUNICIPIO", default='Valledupar')
     comuna = fields.Selection([('1','Comuna 1'),('2','Comuna 2'), ('3','Comuna 3'), ('4','Comuna 4'), ('5','Comuna 5'), ('6','Comuna 6')], string="COMUNA")
     zona = fields.Char(string="ZONA")
     barrio = fields.Char(string="BARRIO")
     corregimiento = fields.Char(string="CORREGIMIENTO")
     vereda = fields.Char(string="VEREDA")
     direccion = fields.Char(string="DIRECCION")
     oficio = fields.Char(string="PROFESION - OFICIO")
     
     puesto_votacion  = fields.Char(string="PUESTO DE VOTACION")
     mesa_votacion  = fields.Char(string="MESA VOTACION")
     tipo_voto  = fields.Selection([('D','Duro'),('S','Seguro'), ('P','Posible')],string="TIPO DE VOTO")

