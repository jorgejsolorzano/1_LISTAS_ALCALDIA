
from odoo import models, fields, api


class milistado(models.Model):
     _name = 'milistado.listas'
     _description = 'Creacion listado alcaldia de Valledupar'

     user_id = fields.Many2one('res.users',string="USUARIO", default=lambda self: self.env.user)
     cedula = fields.Char(string="CEDULA", required=True, size=10)
     nombres = fields.Char(string="NOMBRES")
     apellidos = fields.Char(string="APELLIDOS")
     sexo = fields.Selection([('M','Masculino'),('F','Femenino'), ('O','Otro')], string="SEXO")
     movil = fields.Char(string="MOVIL", size=9)
     email = fields.Char(string="E-MAIL")

     departamento = fields.Char(string="DEPARTAMENTO", default='Cesar')
     municipio = fields.Char(string="MUNICIPIO", default='Valledupar')
     comuna = fields.Selection([('1','Comuna 1'),('2','Comuna 2'), ('3','Comuna 3'), ('4','Comuna 4'), ('5','Comuna 5'), ('6','Comuna 6')], string="COMUNA")
     zona = fields.Char(string="ZONA")
     barrio = fields.Char(string="BARRIO")
     corregimiento = fields.Selection([('Aguas Blancas','Aguas Blancas'),('Atanquez','Atanquez'),('Azucar Buena','Azucar Buena'),('Badillo','Badillo'),('Caracoli','Caracoli'),('Chemesquemena','Chemesquemena'),('El Alto de La Vuelta','El Alto de La Vuelta'),('El Jabo','El Jabo'),('El Perro','El Perro'),('Guacoche','Guacoche'),('Guacochito','Guacochito'),('Guatapuri','Guatapuri'),('Guaymaral','Guaymaral'),('La Mina','La Mina'),('La Vega Arriba','La Vega Arriba'),('Las Raices','Las Raices'),('Los Corazones','Los Corazones'),('Los Haticos','Los Haticos'),('Los Venados','Los Venados'),('Mariangola','Mariangola'),('Patillal','Patillal'),('Rio Seco','Rio Seco'),('Sabana Crespo','Sabana Crespo'),('Valencia de Jesus','Valencia de Jesus'),('Villa Germania','Villa Germania')],string="CORREGIMIENTO")
     vereda = fields.Selection([('Avinche','Avinche'),('Las Flores','Las Flores'),('Nueva Idea','Nueva Idea'),('El Potrero','El Potrero'),('El Mojao','El Mojao'),('Guingueca','Guingueca'),('Las Dos Bocas','Las Dos Bocas'),('Kaminticua','Kaminticua'),('El Poder','El Poder'),('La Macana','La Macana'),('Yosagaca','Yosagaca'),('San Pablo','San Pablo'),('La Montana','La Montana'),('Los Hoyos','Los Hoyos'),('Ramalito','Ramalito'),('Rancho de Goya','Rancho de Goya'),('Ponton','Ponton'),('El Cerro','El Cerro'),('Juaneta','Juaneta'),('Platanita','Platanita'),('El Chorro','El Chorro'),('Surimena','Surimena'),('Cherua','Cherua'),('Puerto Leticia','Puerto Leticia'),('Santa Marta','Santa Marta'),('El Mecedor','El Mecedor'),('Pueblo Hernandez','Pueblo Hernandez'),('Cheducua','Cheducua'),('Maruamake','Maruamake'),('Sinka','Sinka'),('Bernaka,','Bernaka,'),('Conchurua','Conchurua'),('Rongoy','Rongoy'),('Piedra Lisa','Piedra Lisa'),('Las Mercedes','Las Mercedes'),('La Subia','La Subia'),('Nuevo Mundo','Nuevo Mundo'),('El Cercao','El Cercao'),('Murillo','Murillo'),('El Callao','El Callao'),('Los Calabazos','Los Calabazos'),('Montecristo','Montecristo'),('Sierra Mariangola','Sierra Mariangola'),('Trocha de Angostura','Trocha de Angostura'),('Las Gallinetas','Las Gallinetas'),('El Oasis','El Oasis'),('Las Mariposas','Las Mariposas'),('La Gran Via','La Gran Via'),('Canta rana','Canta rana'),('Los Aringibles','Los Aringibles'),('El Diluvio','El Diluvio'),('Nueva Idea','Nueva Idea'),('La Sierrita','La Sierrita'),('El Arca','El Arca'),('El Tunel','El Tunel'),('La Guitarra','La Guitarra'),('Casablanca','Casablanca'),('El Silencio','El Silencio'),('La Sierra','La Sierra'),('Las Palmas I','Las Palmas I'),('Las Palmas II','Las Palmas II'),('Descanso','Descanso'),('Sicarare','Sicarare'),('El Mono','El Mono'),('Nuevo Mundo','Nuevo Mundo'),('Las Nubes','Las Nubes'),('Penimike','Penimike'),('Sabana de Jordan','Sabana de Jordan'),('Izrua','Izrua'),('Yugaka','Yugaka'),('La Estrella','La Estrella'),('Virua','Virua'),('Donachui','Donachui'),('Garupal','Garupal'),('El Morrocollo','El Morrocollo'),('Carrera Larga','Carrera Larga'),('La Feria','La Feria'),('Contrabando','Contrabando'),('El Rosario','El Rosario'),('Nuevo Rumbo','Nuevo Rumbo'),('El Balsamo','El Balsamo'),('Playon de Goya','Playon de Goya'),('Camperucho','Camperucho'),('Las Mercedes','Las Mercedes'),('La Sierrita','La Sierrita'),('El Mangon','El Mangon'),('Campo Alegre','Campo Alegre'),('Buenos Aires','Buenos Aires'),('Las Cumbres','Las Cumbres'),('Nueva Lucia','Nueva Lucia'),('Praderas de Camperucho','Praderas de Camperucho'),('Nueva Lucha','Nueva Lucha'),('Las Mercedes','Las Mercedes'),('Los Laureles','Los Laureles'),('La Colombia','La Colombia'),('El Mamon','El Mamon'),('La Cuba','La Cuba'),('Putumayo','Putumayo'),('Tierras Nuevas','Tierras Nuevas'),('La Montanita','La Montanita'),('Los Ceibotes','Los Ceibotes'),('Los Cominos de Tamacal','Los Cominos de Tamacal'),('Seinimi','Seinimi'),('Sogrone','Sogrone'),('Sabanitas','Sabanitas'),('El Palmar','El Palmar'),('La Montana','La Montana')],string="VEREDA")
     direccion = fields.Char(string="DIRECCION")
     oficio = fields.Char(string="PROFESION - OFICIO")
     
     puesto_votacion  = fields.Char(string="PUESTO DE VOTACION")
     mesa_votacion  = fields.Char(string="MESA VOTACION")
     tipo_voto  = fields.Selection([('D','Duro'),('S','Seguro'), ('P','Posible')],string="TIPO DE VOTO")

