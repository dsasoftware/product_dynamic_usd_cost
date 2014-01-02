# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

class purchase_order_line(osv.osv):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'

    _columns = {
	'product_usd_cost': fields.float('US Dollar Cost'),
	}


	
    def create(self, cr, uid, vals, context=None):

	data = vals

	data_order = self.pool.get('purchase.order').read(cr,uid,data['order_id'])
	if data_order['state'] == 'draft':
		if type(data['order_id']) == 'list':
			data_order = data_order[0]
		if 'price_unit' in vals.keys():
			price_unit = vals['price_unit']
		else:
			price_unit = data['price_unit']
		if data_order['currency_id'][1] == 'ARS':
			currency_id = self.pool.get('res.currency').search(cr,uid,[('name','=','USD')])
			if currency_id:
				rate = self.pool.get('res.currency').read(cr,uid,currency_id)[0]['rate_silent']
				vals['product_usd_cost'] = price_unit / rate
        return super(purchase_order_line, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):

	data = self.read(cr,uid,ids)
	data = data[0]

	data_order = self.pool.get('purchase.order').read(cr,uid,data['order_id'][0])
	if data_order['state'] == 'draft':
		if type(data['order_id']) == 'list':
			data_order = data_order[0]
		if 'price_unit' in vals.keys():
			price_unit = vals['price_unit']
		else:
			price_unit = data['price_unit']
		if data_order['currency_id'][1] == 'ARS':
			currency_id = self.pool.get('res.currency').search(cr,uid,[('name','=','USD')])
			if currency_id:
				rate = self.pool.get('res.currency').read(cr,uid,currency_id)[0]['rate_silent']
				vals['product_usd_cost'] = price_unit / rate
        return super(purchase_order_line, self).write(cr, uid, ids, vals, context=context)

purchase_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
