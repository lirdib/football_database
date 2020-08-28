import base64
import logging
from datetime import datetime

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError, UserError
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
    ekipi_aktual_id = fields.Many2one(comodel_name='ekipet', string='Ekipi aktual', required=True)  # many2one
    paga = fields.Integer(required=True)
    golat = fields.Integer(required=True)
    kombesia_id = fields.Many2one(comodel_name='kombesia', string='Kombesia', required=False)  # many2one


class Ekipi(models.Model):
    _name = "ekipet"

    # id = fields.Integer(required=True)
    name = fields.Char(required=True)
    buxheti = fields.Integer()
    vlera_e_ekpit = fields.Integer(default_value=False)
    lojtaret_ids = fields.One2many(comodel_name='lojtari', inverse_name='ekipi_aktual_id', string='')
    lojtaret_prone_ids = fields.One2many(comodel_name='lojtari', inverse_name='ekipi_nga_i_cili_ka_ardhur_id',
                                         string='')

    def llogarit_vlera_e_ekipit(self):
        for lojtar in self.lojtaret_ids:
            lojtar.paga *= 1.1
        for lojtar in self.lojtaret_ids.filtered(lambda l: l.paga < 50000):
            lojtar.paga *= 1.2
        # lojtaret = self.env['lojtari'].search(['&', '|', ('ekipi_nga_i_cili_ka_ardhur_id', '=', self.id),('ekipi_nga_i_cili_ka_ardhur_id', '=', self.id),('ekipi_nga_i_cili_ka_ardhur_id', '=', self.id)])
        # sum = 0
        # for lojtar in lojtaret:
        #     sum += lojtar.vlera_e_lojtarit
        # self.vlera_e_ekpit = self.buxheti + sum
        self.vlera_e_ekpit = self.buxheti + sum(
            self.env['lojtari'].search([('ekipi_nga_i_cili_ka_ardhur_id', '=', self.id)]).mapped('vlera_e_lojtarit'))

        self.vlera_e_ekpit = self.buxheti + sum(self.lojtaret_prone_ids.mapped('vlera_e_lojtarit'))


class Sezon_ekip(models.Model):
    _name = "sezonekip"


    # id_ekipit = fields.Integer(required=True)
    ekipit_id = fields.Many2one(comodel_name='ekipet', string='Ekipi', required=False)
    sezonit_id = fields.Many2one(comodel_name='sezone', string='Sezonet', required=False)
    fitore = fields.Integer(required=True)
    humbje = fields.Integer(required=True)
    barazime = fields.Integer(required=True)
    piket = fields.Integer(compute='llogarit_piket')

    #ef llogarit_piket_nga_rezultatet(self):
    #   ndeshje = self.env["ndeshje"].search(
    #       ['|', ("ekipi_home_id", "=", self.ekipit_id.id), ('ekipi_away_id', '=', self.ekipit_id.id)])
    #   for nd in ndeshje:
    #       if nd.ekipi_home_id.id == self.ekipit_id.id:
    #           if nd.gola_home > nd.gola_away:
    #               self.fitore += 1
    #           elif nd.gola_home == nd.gola_away:
    #               self.barazime += 1
    #           else:
    #               self.humbje += 1
    #       else:
    #           if nd.gola_home < nd.gola_away:
    #               self.fitore += 1
    #           elif nd.gola_home == nd.gola_away:
    #               self.barazime += 1
    #           else:
    #               self.humbje += 1


   #def kryej_veprimet(self):
   #    flag = self.env['ndeshje'].search([('status', '=', 'kane_laujtur')])
   #    for ndeshje in flag:
   #        if ndeshje.gola_home > ndeshje.gola_away:
   #            self.fitore +=1
   #        elif ndeshje.gola_home == ndeshje.gola_away:
   #            self.barazime +=1
   #        else:
   #            self.humbje += 1

    @api.multi
    @api.depends('fitore', 'barazime')
    def llogarit_piket(self):
        for record in self:
            record.piket = 3 * record.fitore + record.barazime


class Ndeshje(models.Model):
    _name = "ndeshje"

    sezonekip_home_id = fields.Many2one(comodel_name='sezonekip', string='Ekipi home', required=False, compute='_gjej_sezonekip_home_id')  # many2one
    gola_home = fields.Integer()
    sezonekip_away_id = fields.Many2one(comodel_name='sezonekip', string='Ekipi away', required=False, compute='_gjej_sezonekip_away_id')  # many2one
    gola_away = fields.Integer()
    sezon_id = fields.Many2one(comodel_name='sezone', string='Sezoni', required=False)
    ekipi_home_id = fields.Many2one(comodel_name="ekipet")
    ekipi_away_id = fields.Many2one(comodel_name="ekipet")
    java = fields.Integer(required=True)
    state = fields.Selection(string='Statusi', default='nuk_kane_luajur',
                             selection=[('nuk_kane_luajur', 'Nuk kane luajtur'),
                                        ('kane_luajtur', 'Kane Luajtur')])



    @api.onchange('ekipi_home_id', 'ekipi_away_id', 'sezon_id')
    def kontrollo_ndeshjet(self):
        if self.sezon_id and self.ekipi_home_id and self.ekipi_away_id:
            if self.env['ndeshje'].search(
                    [('ekipi_home_id', '=', self.ekipi_home_id.id), ('ekipi_away_id', '=', self.ekipi_away_id.id),
                     ('sezon_id', '=', self.sezon_id.id)]):
                raise UserError('Kjo ndeshje eshte luajtur nje here')


            elif self.ekipi_home_id.id == self.ekipi_away_id.id:
                raise UserError('Dy ekipet nuk mund te jene te njejta')

    @api.multi
    @api.depends('ekipi_home_id', 'sezon_id')
    def _gjej_sezonekip_home_id(self):
        if self.sezon_id and self.ekipi_home_id:
            self.sezonekip_home_id = self.env['sezonekip'].search([('sezonit_id', '=', self.sezon_id.id), ('ekipit_id', '=', self.ekipi_home_id.id)], limit=1)

    @api.multi
    @api.depends('ekipi_away_id', 'sezon_id')
    def _gjej_sezonekip_away_id(self):
        if self.sezon_id and self.ekipi_home_id:
            self.sezonekip_away_id = self.env['sezonekip'].search(
                [('sezonit_id', '=', self.sezon_id.id), ('ekipit_id', '=', self.ekipi_away_id.id)], limit=1)

    def nderro_gjendje(self):
        self.state = 'kane_luajtur'
        if self.gola_home > self.gola_away:
            self.sezonekip_home_id.fitore += 1
            self.sezonekip_away_id.humbje +=1
        elif self.gola_home == self.gola_away:
            self.sezonekip_home_id.barazime += 1
            self.sezonekip_away_id.barazime +=1
        else:
            self.sezonekip_home_id.humbje += 1
            self.sezonekip_away_id.fitore += 1

        #lojtaret = self.env['lojtari'].search(['&', '|', ('ekipi_nga_i_cili_ka_ardhur_id', '=', self.id),('ekipi_nga_i_cili_ka_ardhur_id', '=', self.id),('ekipi_nga_i_cili_ka_ardhur_id', '=', self.id)])

    def anulo_ndeshje(self):
        self.state = 'nuk_kane_luajur'

        if self.gola_home > self.gola_away:
            self.sezonekip_home_id.fitore -= 1
            self.sezonekip_away_id.humbje -=1
        elif self.gola_home == self.gola_away:
            self.sezonekip_home_id.barazime -= 1
            self.sezonekip_away_id.barazime -=1
        else:
            self.sezonekip_home_id.humbje -= 1
            self.sezonekip_away_id.fitore -= 1



class Transferime(models.Model):
    _name = "transferime"

    # id = fields.Integer()
    id_lojtarit_id = fields.Many2one(comodel_name='lojtari', string='Transferimi', required=False)
    ekipi_from_id = fields.Many2one(comodel_name='ekipet', string='Ekipifrom', required=False)  # ekipi me te cilin luan
    ekipi_to_id = fields.Many2one(comodel_name='ekipet', string='Ekipito',
                                  required=False)  # ekipi tek i cili do te transferohet
    lloji_kontrate = fields.Boolean(string="Kontrate huazimi",
                                    description="uncheck kontrate blerje, check kontrate huazimi", default=False)
    kohezgjatja_e_kontrates = fields.Date()
    data_e_nenshkrimit = fields.Date()
    vite_kontrate = fields.Float(string='Kohezgjatja ne vite', compute='llogarit_kohezgjatje')
    state = fields.Selection(string='Statusi', default="draft",
                             selection=[('draft', 'Draft'),
                                        ('ne_ekzekutim', 'Ne ekzekutim'),
                                        ('ekzekutuar', 'Ekzekutuar')])

    @api.multi
    @api.depends('data_e_nenshkrimit', 'kohezgjatja_e_kontrates')
    def llogarit_kohezgjatje(self):
        for record in self:
            if record.kohezgjatja_e_kontrates and record.data_e_nenshkrimit:
                kohezgjatja_e_kontrates = record.kohezgjatja_e_kontrates if type(
                    record.kohezgjatja_e_kontrates) is not str else datetime.strptime(record.kohezgjatja_e_kontrates,
                                                                                      '%Y-%m-%d')
                data_e_nenshkrimit = record.data_e_nenshkrimit if type(
                    record.data_e_nenshkrimit) is not str else datetime.strptime(record.data_e_nenshkrimit, '%Y-%m-%d')
                dite_kontrate = (kohezgjatja_e_kontrates - data_e_nenshkrimit)
                record.vite_kontrate = dite_kontrate.days / 365.0

    @api.onchange('id_lojtarit_id')
    def percakto_automatikisht_ekipin_me_te_cilin_luan(self):
        if self.id_lojtarit_id.ekipi_aktual_id.id:
            self.ekipi_from_id = self.id_lojtarit_id.ekipi_aktual_id.id

    def kalo_ekzekutim(self):
        self.state = 'ne_ekzekutim'

    def kalo_ekzekutuar(self):
        self.state = 'ekzekutuar'
        self.id_lojtarit_id.ekipi_aktual_id = self.ekipi_to_id.id


class Sezone(models.Model):
    _name = "sezone"


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
