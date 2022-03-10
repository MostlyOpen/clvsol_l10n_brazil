# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CountryState(models.Model):
    _inherit = "res.country.state"

    ibge_code = fields.Char(string="IBGE Code", size=2)
