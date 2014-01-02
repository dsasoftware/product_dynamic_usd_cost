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

class product_product(osv.osv):
    """ Product Product """
    _name = "product.product"
    _inherit = "product.product"

    def _update_usd_cost(self,cr,uid,ids=None,context=None):

	currency_obj = self.pool.get('res.currency')
	product_obj = self.pool.get('product.product')
	order_obj = self.pool.get('purchase.order')
	order_line_obj = self.pool.get('purchase.order.line')
	product_ids = product_obj.search(cr,uid,['|',('cost_method','=','usd_cost'),('cost_method','=','usd_30_cost')])

	for product in product_obj.browse(cr,uid,product_ids):
		max_date = 0	
		order_line_ids = order_line_obj.search(cr,uid,[('product_id','=',product.id)])
		for order_line in order_line_obj.browse(cr,uid,order_line_ids):
			if order_line.order_id.state in ('sent','confirmed','approved','done') \
				and order_line.order_id.date_order > max_date: 

				currency_id = currency_obj.search(cr,uid,[('name','=','USD')])
				if product.cost_method == 'usd_cost':
					data_currency = currency_obj.read(cr,uid,currency_id)		
					price_unit_other_currency = order_line.product_usd_cost * data_currency[0]['rate']
				else:
					future_id = self.pool.get('res.currency.future').search(cr,uid,[('currency_id','=',currency_id[0]),\
						('days','=',30)])
					if future_id:
                                        	data_future = self.pool.get('res.currency.future').read(cr,uid,future_id)
                                                rate = data_future[0]['rate']
						price_unit_other_currency = order_line.product_usd_cost * rate

				vals_product = {
					'standard_price': price_unit_other_currency
					}
				return_id = product_obj.write(cr,uid,product.id,vals_product)
				max_date = order_line.order_id.date_order
				_logger.debug("Updated product " + product.name)
			
	return None

    _columns = {
	        'cost_method': fields.selection([('standard','Standard Price'), 
						('average','Average Price'),
						('last_purchase','Last Purchase'),
						('usd_30_cost','30 days USD Cost'),
						('usd_cost','USD Cost')],
						 'Costing Method', required=True,
						help="Standard Price: The cost price is manually updated at the end of a specific period (usually every year). \nAverage Price: The cost price is recomputed at each incoming shipment."),
		}

product_product()

