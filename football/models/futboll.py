import base64
import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)


class Ekipi(models.Model):
    _name = "ekipet"

    # id = fields.Integer(required=True)
    name = fields.Char(required=True)
    buxheti = fields.Integer()
    # sezon_ekip = fields.Many2one(comodel_name='sezonekip',string='sezonekip')


class Sezon_ekip(models.Model):
    _name = "sezonekip"

    # id_ekipit = fields.Integer(required=True)
    ekipit_id = fields.Many2one(comodel_name='ekipet', string='Ekipi', required=False)
    sezonit_id = fields.Many2one(comodel_name='sezone', string='Sezonet', required=False)
    fitore = fields.Integer(required=True)
    humbje = fields.Integer(required=True)
    barazime = fields.Integer(required=True)


class Ndeshje(models.Model):
    _name = "ndeshje"

    ekipi_home_id = fields.Many2one(comodel_name='ekipet', string='Ekipi home', required=False)  # many2one
    gola_home = fields.Integer(required=True)
    ekipi_away_id = fields.Many2one(comodel_name='ekipet', string='Ekipi away', required=False)  # many2one
    gola_away = fields.Integer(required=True)
    java = fields.Integer(required=True)
    ekipi_a_id = fields.Many2one(comodel_name='ekipet')


class Lojari(models.Model):
    _name = "lojtari"

    # id = fields.Integer(required=True)
    name = fields.Char(required=True)
    mbiemri = fields.Char(required=True)
    ekipi_nga_i_cili_ka_ardhur_id = fields.Integer(required=True)  # many2one
    ekipi_aktual_id = fields.Integer(required=True)  # many2one
    paga = fields.Integer(required=True)
    golat = fields.Integer(required=True)
    kombesia_id = fields.Many2one(comodel_name='kombesia', string='Kombesia', required=False)  # many2one


class Transferime(models.Model):
    _name = "transferime"

    # id = fields.Integer()
    id_lojtarit_id = fields.Many2one(comodel_name='lojtari', string='Transferimi', required=False)
    ekipi_from_id = fields.Many2one(comodel_name='ekipet', string='Ekipifrom', required=False)
    ekipi_to_id = fields.Many2one(comodel_name='ekipet', string='Ekipito', required=False)
    lloji_kontrate = fields.Boolean(string="Kontrate huazimi",
                                    description="uncheck kontrate blerje, check kontrate huazimi", default=False)
    kohezgjatja_e_kontrates = fields.Date()
    data_e_nenshkrimit = fields.Date()


class Sezone(models.Model):
    _name = "sezone"

    # id_sezonit = fields.Integer()
    sezoni = fields.Char()
    data_e_fillimit = fields.Date()
    data_e_mbarimit = fields.Date()
    numri_i_ekipeve = fields.Integer()
    cmimiVendiPare = fields.Integer()
    cimiVendiDyte = fields.Integer()
    cmimiVendiTrete = fields.Integer()
    cimiVendiKatert = fields.Integer()


class Kombesia(models.Model):
    _name = "kombesia"

    name = fields.Char()
    long_name = fields.Char()
