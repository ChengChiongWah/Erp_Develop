# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.http import request
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_reject(self):
        self.ensure_one()
        head_reject = self.env['sale.reject']
        values = {
            'name': 'Reject_' + self.name,
            'sale_order_name': self.name,
            'partner_id': self.partner_id.id,
            'confirmation_date': fields.Datetime.now(),
            'payment_term_id': self.partner_id.property_payment_term_id.id,
            'date_order': fields.Datetime.now(),
            'validity_date': fields.Datetime.now(),
            'company_id': self.env.user.company_id.id,
        }
        head = head_reject.create(values)
        lines_reject = self.env['sale.reject.line']
        for t in self.order_line:
            values_lines = {
                'order_id': head.id,
                'name': t.name,
                'price_unit': t.price_unit,
                'product_id': t.product_id.id,
                'product_uom_qty': t.product_uom_qty,
                'product_uom': t.product_uom.id,
                'qty_delivered': t.qty_delivered,
                'salesman_id': t.salesman_id.id,
                'company_id': t.company_id.id,
                'order_partner_id': t.order_partner_id.id,
                'customer_lead': t.customer_lead,
                'procurement_ids': t.procurement_ids.id,
            }
            lines_reject.create(values_lines)
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.reject',
            'res_id': head.id,
            'type': 'ir.actions.act_window',
            'target': 'main',
        }


class SaleReject(models.Model):
    _name = 'sale.reject'

    name = fields.Char('Name', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    sale_order_name = fields.Char('Sale_Order_Name')
    partner_id = fields.Many2one('res.partner', string='Customer')
    confirmation_date = fields.Datetime(string='Confirmation Date', index=True,
                                        help="Date on which the sale order is confirmed.", oldname="date_confirm")
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term')
    date_order = fields.Datetime(string='Order Date', required=True, index=True, copy=False,
                                 default=fields.Datetime.now)
    validity_date = fields.Date(string='Expiration Date',
                                help="Manually set the expiration date of your quotation (offer), or it will set the date automatically based on the template if online quotation is installed.")
    reject_line = fields.One2many('sale.reject.line', 'order_id', string='Order Lines', copy=True)
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company']._company_default_get('sale.order'))
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange',
                              default=lambda self: self.env.user)
    product_id = fields.Many2one('product.product', related='reject_line.product_id', string='Product')


class SaleRejectLine(models.Model):
    _name = 'sale.reject.line'

    order_id = fields.Many2one('sale.reject', string='Order Reference', required=True, ondelete='cascade', index=True,
                               copy=False)
    name = fields.Text(string='Description', required=True)
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0)
    product_id = fields.Many2one('product.product', string='Product', change_default=True, ondelete='restrict',
                                 required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True,
                                   default=1.0)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True)
    qty_delivered = fields.Float(string='Delivered', copy=False, digits=dp.get_precision('Product Unit of Measure'),
                                 default=0.0)
    salesman_id = fields.Many2one(related='order_id.user_id', store=True, string='Salesperson', readonly=True)
    company_id = fields.Many2one(related='order_id.company_id', string='Company', store=True, readonly=True)
    order_partner_id = fields.Many2one(related='order_id.partner_id', store=True, string='Customer')
    customer_lead = fields.Float(
        'Delivery Lead Time', required=True, default=0.0,
        help="Number of days between the order confirmation and the shipping of the products to the customer",
        oldname="delay")
    procurement_ids = fields.One2many('procurement.order', 'sale_line_id', string='Procurements')

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if self.product_id:
            product = self.product_id
            self.name = product.name

