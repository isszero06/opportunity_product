from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.addons import decimal_precision as dp

class DimensionSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    item_partner_no = fields.Char('partner Item NO' ,states={'done': [('readonly', True)]})
    item_partner_sub_no = fields.Char('SN' ,states={'done': [('readonly', True)]})
    cust_desc = fields.Char('Cust.Desc' ,states={'done': [('readonly', True)]})
    
class CrmLeadProduct(models.Model):
    _name = 'crm.lead.product'

    item_partner_no = fields.Char('partner Item NO', copy=True)
    item_partner_sub_no = fields.Char('SN', copy=True)
    cust_desc = fields.Char('Cust.Desc', copy=True)
    product_id = fields.Many2one('product.product',string='Items', copy=True)
    description = fields.Text(string='Description', copy=True)
    price_unit = fields.Float(string='Standard Unit Price', related='product_id.lst_price' readonly=True ,store=True, copy=True)
    #tax_id = fields.Many2many('account.tax', string='Taxes')
    #is_dimension = fields.Boolean('Use Dimensions..?',related="product_id.is_dimension")
    #height = fields.Float('Height (cm)')
    #width = fields.Float('Width (cm)')
    #pcs1 = fields.Float('PCs' , default=1)
    #m2 = fields.Float('m2/PC',default=False, readonly=True)
    #total_m2 = fields.Float('Total(m2)',default=False , readonly=True)
    #height1 = fields.Float('Actual Height (cm)')
    #width1 = fields.Float('Actual Width (cm)')
    #di_batch = fields.Char('Dimension Batch', readonly=True)
    product_uom_qty = fields.Float('Ordered Qty', copy=True)
    product_uom_id = fields.Many2one('uom.uom', related='product_id.uom_id', readonly=True)
    lead_id = fields.Many2one('crm.lead')
    line_subtotal = fields.Float('SubTotal', compute='_calculate_line_subtotal',store=True)

    
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            #self.price_unit = self.product_id.lst_price
            self.product_uom_id = self.product_id.uom_id.id
            #self.tax_id = self.product_id.taxes_id.ids
    

    #@api.onchange('height', 'width')
    #def calculate_m2(self):
        #for each in self:
            #if each.height and each.width:
                #each.m2 = (each.height * each.width) / 10000
    

    @api.depends('price_unit', 'product_uom_qty')
    def _calculate_line_subtotal(self):
        for each in self:
            each.line_subtotal = (each.price_unit * each.product_uom_qty)

    #@api.onchange('m2','pcs1')
    #def compute_total_m2(self):
        #for each in self:
            #each.total_m2 = (each.m2 * each.pcs1)
           # each.product_uom_qty = each.total_m2
        
class CrmLead(models.Model):
    _inherit = 'crm.lead'

    lead_product_ids = fields.One2many('crm.lead.product','lead_id',string='Products For Quotation')
    lead_total = fields.Float('Total',compute='get_lead_total')

    @api.depends('lead_product_ids.line_subtotal','lead_total')
    def get_lead_total(self):
        for lead in self:
            total = 0.0
            for line in lead.lead_product_ids:
                total += line.line_subtotal

            lead.lead_total = total
            lead.write({'planned_revenue':lead.lead_total})

    
    def action_create_quotation(self):
        sale_obj=self.env['sale.order']
        sale_line_obj=self.env['sale.order.line']
        order_lines = []
        for line in self.lead_product_ids:
            order_lines.append((0,0,{'product_id': line.product_id.id,
                'name': line.description,
                'product_uom_qty':line.product_uom_qty,
                #'price_unit': line.price_unit,
                 'item_partner_sub_no': line.item_partner_sub_no,
                 'cust_desc': line.cust_desc,
                 #'height' : line.height,
                 #'width' : line.width,
                 #'pcs1' : line.pcs1,
                 #'m2' : line.m2,
                 #'total_m2' : line.total_m2,
                 #'di_batch': line.di_batch
                #'tax_id':[(6, 0, line.tax_id.ids)]

            }))
        if self.partner_id:
            sale_id = sale_obj.create({
                'partner_id':self.partner_id.id,
                'team_id': self.team_id.id,
                'campaign_id': self.campaign_id.id,
                'medium_id': self.medium_id.id,
                'source_id': self.source_id.id,
                'opportunity_id': self.id,
                'order_line':order_lines,
            })
        else:
            raise UserError('In order to create sale order, Customer field should not be empty !!!')
        return True
    
   
