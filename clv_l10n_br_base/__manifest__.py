# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Brazilian Localization Base',
    'summary': 'Brazilian Localization Base Module used by CLVsol Solutions.',
    'version': '15.0.6.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    "depends": [
        "base",
        "base_setup",
        "base_address_city",
        "base_address_extended"
    ],
    "data": [
        "data/res.city.csv",
        "data/res.country.state.csv",
        "data/res_country_data.xml",
        "views/res_city_view.xml",
        "views/res_country_state_view.xml",
        "views/res_partner_view.xml",
    ],
    "demo": [
    ],
    "installable": True,
    "external_dependencies": {"python": ["num2words", "erpbrasil.base"]},
}
