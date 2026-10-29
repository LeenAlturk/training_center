from odoo import api, fields, models
class SaleLineOrder(models.Model):
    _inherit = "sale.order.line"
    _description = "Sale Line Order"
    course_id = fields.Many2one(
        comodel_name="training.course",
        string="Course",
        domain="[('state', '=','confirmed'),('product_id.product_tmpl_id.remaining_course_seat','>',0)]",
    )
    instructor_id = fields.Many2one(string="Instructor",related="course_id.instructor_id",readonly=True)




    @api.onchange("product_template_id")
    def change_course_name(self):
        if self.product_template_id:
            self.course_id = self.env['training.course'].search([
                ('product_id.product_tmpl_id', '=', self.product_template_id.id)
            ], limit=1)


    @api.onchange("course_id")
    def change_product_template(self):
        if self.course_id:
            self.product_id = self.course_id.product_id
            self.price_unit = self.course_id.price

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res['course_id'] = self.course_id.id
        return res


