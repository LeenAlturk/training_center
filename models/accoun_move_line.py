from odoo import api, fields, models
class AccounMoveLine(models.Model):
    _inherit = 'account.move.line'
    course_id = fields.Many2one(
        comodel_name= 'training.course',
        string='course',

    )

