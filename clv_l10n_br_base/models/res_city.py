# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class City(models.Model):
    _inherit = "res.city"

    ibge_code = fields.Char(string="IBGE Code", size=7, index=True)
