from odoo import api, fields, models
class Product(models.Model):
    _inherit = "product.template"
    _description = "Product"
    state = fields.Selection([
        ("draft", "Draft"),
        ('confirmed', 'Confirmed'),
        ("done", "Done"),
        ("cancel", "Cancel"),
    ],string="Status", readonly=True, default="draft")
    seat=fields.Integer(string="Seat",readonly=True,default="0")
    registered_seat = fields.Integer(
        string="Registered Seats",
        default=0,
    )
    remaining_course_seat=fields.Integer(string="Remaining Course Seat", compute="_compute_seat",store=True)

    @api.depends(
       "seat",
       "registered_seat",
    )
    def _compute_seat(self):
        for product in self:
                product.remaining_course_seat = product.seat- product.registered_seat


