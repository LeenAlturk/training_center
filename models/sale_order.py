from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "Sale Order"

    def action_confirm(self):
        res = super().action_confirm()
        for line in self.order_line:
            if line.product_uom_qty > line.product_template_id.remaining_course_seat:
                raise ValidationError(_(f"there is no enough seat in this course {line.product_id.name} there is {line.product_template_id.remaining_course_seat} seat"))
            else:
                line.product_template_id.write({
                    "registered_seat": line.product_template_id.registered_seat + line.product_uom_qty,
                })
        return res


