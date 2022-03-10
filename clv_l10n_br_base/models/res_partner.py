# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from erpbrasil.base import misc
except ImportError:
    _logger.error("Biblioteca erpbrasil.base não instalada")


class Partner(models.Model):
    _inherit = "res.partner"

    # def _display_address(self, without_company=False):
    #     country_code = self.country_id.code or ""
    #     if self.country_id and country_code.upper() != "BR":
    #         # this ensure other localizations could do what they want
    #         return super(Partner, self)._display_address(without_company=False)
    #     else:
    #         address_format = (
    #             self.country_id
    #             and self.country_id.address_format
    #             or "%(street_name)s, %(street_number)s %(street2)s\n%(district)s"
    #             "\n%(zip)s - %(city)s-%(state_code)s\n%(country_name)s"
    #         )
    #         args = {
    #             "city_name": self.city_id and self.city_id.name or "",
    #             "state_code": self.state_id and self.state_id.code or "",
    #             "state_name": self.state_id and self.state_id.name or "",
    #             "country_code": self.country_id and self.country_id.code or "",
    #             "country_name": self.country_id and self.country_id.name or "",
    #             "company_name": self.parent_id and self.parent_id.name or "",
    #         }

    #         address_field = [
    #             "title",
    #             "street_name",
    #             "street2",
    #             "zip",
    #             "city",
    #             "street_number",
    #             "district",
    #         ]
    #         for field in address_field:
    #             args[field] = getattr(self, field) or ""
    #         if without_company:
    #             args["company_name"] = ""
    #         elif self.parent_id:
    #             address_format = "%(company_name)s\n" + address_format
    #         return address_format % args

    # city_id = fields.Many2one(domain="[('state_id', '=', state_id)]")

    country_id = fields.Many2one(default=lambda self: self.env.ref("base.br"))

    district = fields.Char(string="District", size=32)
    # street2 = fields.Char(string="District")

    # @api.model
    # def _address_fields(self):
    #     """Returns the list of address
    #     fields that are synced from the parent."""
    #     return super(Partner, self)._address_fields() + ["district"]

    # def get_street_fields(self):
    #     """Returns the fields that can be used in a street format.
    #     Overwrite this function if you want to add your own fields."""
    #     return super(Partner, self).get_street_fields() + ["street_name"]

    # def _set_street(self):
    #     company_country = self.env.user.company_id.country_id
    #     if company_country.code:
    #         if company_country.code.upper() != "BR":
    #             return super(Partner, self)._set_street()

    @api.onchange("zip")
    def _onchange_zip(self):
        self.zip = misc.format_zipcode(self.zip, self.country_id.code)

    @api.onchange("city_id")
    def _onchange_city_id(self):
        self.city = self.city_id.name

    def _inverse_street_data(self):
        """Updates the street field.
        Writes the `street` field on the partners when one of the sub-fields in STREET_FIELDS
        has been touched"""
        street_fields = self._get_street_fields()
        for partner in self:
            street_format = (
                partner.country_id.street_format or '%(street_name)s, %(street_number)s/%(street_number2)s')
            previous_field = None
            previous_pos = 0
            street_value = ""
            separator = ""
            # iter on fields in street_format, detected as '%(<field_name>)s'
            for re_match in re.finditer(r'%\(\w+\)s', street_format):
                # [2:-2] is used to remove the extra chars '%(' and ')s'
                field_name = re_match.group()[2:-2]
                field_pos = re_match.start()
                if field_name not in street_fields:
                    raise UserError(_("Unrecognized field %s in street format.", field_name))
                if not previous_field:
                    # first iteration: add heading chars in street_format
                    if partner[field_name]:
                        street_value += street_format[0:field_pos] + partner[field_name]
                else:
                    # get the substring between 2 fields, to be used as separator
                    separator = street_format[previous_pos:field_pos]
                    if street_value and partner[field_name]:
                        street_value += separator
                    if partner[field_name]:
                        street_value += partner[field_name]
                previous_field = field_name
                previous_pos = re_match.end()

            # add trailing chars in street_format
            street_value += street_format[previous_pos:]
            partner.street = street_value

    @api.depends('street')
    def _compute_street_data(self):
        """Splits street value into sub-fields.
        Recomputes the fields of STREET_FIELDS when `street` of a partner is updated"""
        street_fields = self._get_street_fields()
        for partner in self:
            if not partner.street:
                for field in street_fields:
                    partner[field] = None
                continue

            street_format = (
                partner.country_id.street_format or '%(street_name)s, %(street_number)s/%(street_number2)s')
            street_raw = partner.street
            vals = self._split_street_with_params(street_raw, street_format)
            # assign the values to the fields
            for k, v in vals.items():
                partner[k] = v
            for k in set(street_fields) - set(vals):
                partner[k] = None
