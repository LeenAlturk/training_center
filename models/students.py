from odoo import api,fields,models
class Students(models.Model):
    _inherit = 'res.partner'
    is_student = fields.Boolean(string='Is Student', default=True)
    join_date = fields.Datetime(string='Join Date')
    student_degree = fields.Selection(
    [('bachelors' , 'Bachelors'),
    ('masters', 'Masters')] ,string='Student Degree')
