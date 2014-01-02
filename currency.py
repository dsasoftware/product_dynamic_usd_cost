# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class res_currency_future(osv.osv):
    """ Res Currency Future """
    _name = "res.currency.future"
    _description = "Currency future"

    _columns = {
	'currency_id' : fields.many2one('res.currency','Currency'),
	'days': fields.selection([('30','30 days'),
				 ('60','60 days'),
				 ('90','90 days'),
				 ('120','120 days'),
				 ('150','150 days'),
				 ('180','180 days'),
				 ('210','210 days'),
				 ('240','240 days'),
				 ('270','270 days'),
				 ('300','300 days'),
				 ('330','330 days'),
				 ('360','360 days')],'Day Window'),
	'rate': fields.float('Currency Rate'),
	}

    _sql_constraints = [
        ('unique_currency_future', 'unique (currency_id,days)', 'The document currency and days must be unique!')
    ]


res_currency_future()

class res_currency(osv.osv):
    """ Res Currency """
    _name = "res.currency"
    _inherit = "res.currency"

    _columns = {
	'future_id': fields.one2many('res.currency.future','currency_id','Currency Future'),
	}

res_currency()
