from odoo import api, fields, models
class TagsCourse(models.Model):
    _name = 'tags.course'
    _description = 'Tags Course'
    name = fields.Char(string='Name')
    color = fields.Integer(string='Color')
