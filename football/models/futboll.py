import base64
import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)


class Lojtari(models.Model):
    _name = "lojtari"

    # id = fields.Integer(required=True)
    name = fields.Char(required=True)
    vlera_e_lojtarit = fields.Integer()
    mbiemri = fields.Char(required=True)
    ekipi_nga_i_cili_ka_ardhur_id = fields.Many2one(comodel_name='ekipet', string='Ekipi From',
                                                    required=False)  # many2one
    ekipi_aktual_id = fields.Many2one(comodel_name='ekipet', string='Ekipi From', required=True)  # many2one
    paga = fields.Integer(required=True)
    golat = fields.Integer(required=True)
    kombesia_id = fields.Many2one(comodel_name='kombesia', string='Kombesia', required=False)  # many2one


class Ekipi(models.Model):
    _name = "ekipet"

    # id = fields.Integer(required=True)
    name = fields.Char(required=True)
    buxheti = fields.Integer()
    vlera_e_ekpit = fields.Integer(default_value=False)

    def llogarit_vlera_e_ekipit(self):
        # lojtaret = self.env['lojtari'].search(['&', '|', ('ekipi_nga_i_cili_ka_ardhur_id', '=', self.id),('ekipi_nga_i_cili_ka_ardhur_id', '=', self.id),('ekipi_nga_i_cili_ka_ardhur_id', '=', self.id)])
        # sum = 0
        # for lojtar in lojtaret:
        #     sum += lojtar.vlera_e_lojtarit
        # self.vlera_e_ekpit = self.buxheti + sum
        self.vlera_e_ekpit = self.buxheti + sum(
            self.env['lojtari'].search([('ekipi_nga_i_cili_ka_ardhur_id', '=', self.id)]).mapped('vlera_e_lojtarit'))


class Sezon_ekip(models.Model):
    _name = "sezonekip"

    # id_ekipit = fields.Integer(required=True)
    ekipit_id = fields.Many2one(comodel_name='ekipet', string='Ekipi', required=False)
    sezonit_id = fields.Many2one(comodel_name='sezone', string='Sezonet', required=False)
    fitore = fields.Integer(required=True)
    humbje = fields.Integer(required=True)
    barazime = fields.Integer(required=True)
    piket = fields.Integer()

    def llogarit_piket_nga_rezultatet(self):
        ndeshje = self.env["ndeshje"].search(
            ['|',("ekipi_home_id", "=", self.ekipit_id.id), ('ekipi_away_id', '=', self.ekipit_id.id)])
        for nd in ndeshje:
            if nd.ekipi_home_id.id == self.ekipit_id.id:
                if nd.gola_home > nd.gola_away:
                    self.fitore += 1
                elif nd.gola_home == nd.gola_away:
                    self.barazime += 1
                else:
                    self.humbje += 1
            else:
                if nd.gola_home < nd.gola_away:
                    self.fitore += 1
                elif nd.gola_home == nd.gola_away:
                    self.barazime += 1
                else:
                    self.humbje += 1

    def llogarit_piket(self):
        self.piket = 3 * self.fitore + self.barazime


class Ndeshje(models.Model):
    _name = "ndeshje"

    ekipi_home_id = fields.Many2one(comodel_name='ekipet', string='Ekipi home', required=False)  # many2one
    gola_home = fields.Integer(required=True)
    ekipi_away_id = fields.Many2one(comodel_name='ekipet', string='Ekipi away', required=False)  # many2one
    gola_away = fields.Integer(required=True)
    sezonekip_id = fields.Many2one(comodel_name='sezonekip', string='Sezoni', required=False)
    java = fields.Integer(required=True)

    def perditeso_piket(self):
        flag = self.env["sezonekip"].search(
            ['|',("ekipit_id", "=", self.ekipi_home_id.id), ("ekipit_id", '=',self.ekipi_away_id.id)])
        if self.gola_home > self.gola_away:
            flag.fitore += 1
        elif self.gola_home == self.gola_away:
            flag.barazime += 1
        else:
            flag.humbje += 1

    # ekipi_a_id = fields.Many2one(comodel_name='ekipet')


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
