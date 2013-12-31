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

class account_invoice_line(osv.osv):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    _columns = {
	'product_usd_cost': fields.float('US Dollar Cost'),
	}


    def create(self, cr, uid, vals, context=None):

	data = vals

	data_invoice = self.pool.get('account.invoice').read(cr,uid,data['invoice_id'])
	if data_invoice['state'] == 'draft' and data_invoice['type'] == 'in_invoice':
		if type(data['invoice_id']) == 'list':
			data_invoice = data_invoice[0]
		if 'price_unit' in vals.keys():
			price_unit = vals['price_unit']
		else:
			price_unit = data['price_unit']
		if data_invoice['currency_id'][1] == 'ARS':
			currency_id = self.pool.get('res.currency').search(cr,uid,[('name','=','USD')])
			if currency_id:
				rate = self.pool.get('res.currency').read(cr,uid,currency_id)[0]['rate_silent']
				vals['product_usd_cost'] = price_unit / rate
        return super(account_invoice_line, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):

	data = self.read(cr,uid,ids)
	data = data[0]

	data_invoice = self.pool.get('account.invoice').read(cr,uid,data['invoice_id'][0])
	if data_invoice['state'] == 'draft' and data_invoice['type'] == 'in_invoice':
		if type(data['invoice_id']) == 'list':
			data_invoice = data_invoice[0]
		if 'price_unit' in vals.keys():
			price_unit = vals['price_unit']
		else:
			price_unit = data['price_unit']
		if data_invoice['currency_id'][1] == 'ARS':
			currency_id = self.pool.get('res.currency').search(cr,uid,[('name','=','USD')])
			if currency_id:
				rate = self.pool.get('res.currency').read(cr,uid,currency_id)[0]['rate_silent']
				vals['product_usd_cost'] = price_unit / rate
        return super(account_invoice_line, self).write(cr, uid, ids, vals, context=context)

account_invoice_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
