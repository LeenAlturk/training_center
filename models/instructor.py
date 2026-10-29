from odoo import api, fields, models



class Instructor(models.Model):
    _name = 'instructor'
    _description = 'Instructor'
    _inherit=['mail.thread', 'mail.activity.mixin']
    _rec_name='name'
    name = fields.Char(required=True)
    gender=fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ])
    age=fields.Integer(string='Age')
    active= fields.Boolean(default=True)
    hiring_date =fields.Date()
    note =fields.Text(string='Note')
    email=fields.Char(string='Email')
    years_exp=fields.Integer(string='Years Exp')
    educational_Level=fields.Selection([
        ("bachelor","Bachelor"),
        ("master","Master")
    ])
    instructor_state = fields.Selection([
        ('interview', 'Interview'),
        ('hired', 'Hired'),
        ('active','Active'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
    ], string='Status', default='interview',tracking = True)
    course_ids=fields.One2many(
        comodel_name='training.course',
        inverse_name='instructor_id',
        string='Course',
    )
    default_rate = fields.Float(string='Default Rate')
    confirmed_courses = fields.Integer(string='Number of confirmed courses' , compute='_compute_confirmed_courses')
    your_revenue = fields.Float(string='Revenue',compute='_compute_your_revenue')
    my_courses =fields.Integer(string='Number of my courses' , compute='_compute_your_courses')
    max_class_size = fields.Integer(string='Max Class Size')

    def action_change_hired(self):
        for instructor in self:
            if instructor.instructor_state == 'interview':
                instructor.instructor_state = 'hired'
    def action_change_active(self):
        for instructor in self:
            if instructor.instructor_state == 'hired' or instructor.instructor_state == 'terminated' or instructor.instructor_state == 'on_leave':
                instructor.instructor_state = 'active'
    def action_change_on_leave(self):
        for instructor in self:
            if instructor.instructor_state == 'active':
                instructor.instructor_state = 'on_leave'
    def action_change_terminated(self):
        for instructor in self:
            if instructor.instructor_state == 'on_leave' or instructor.instructor_state == 'active':
                instructor.instructor_state = 'terminated'

    @api.depends('course_ids')
    def _compute_your_courses(self):
        for instructor in self:
            instructor.my_courses = len(instructor.course_ids)

    def action_view_related_courses_records(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'courses',
            'res_model': 'training.course',
            'view_mode': 'list,form',
            'domain': [('instructor_id', '=', self.id)],
        }

    @api.depends('course_ids.total_revenue')
    def _compute_your_revenue(self):
        for instructor in self:
            instructor.your_revenue = 0
            for course in instructor.course_ids:
                if course.state == 'confirmed':
                    instructor.your_revenue +=course.total_revenue

    @api.depends()
    def _compute_confirmed_courses(self):
        for instructor in self:
            instructor.confirmed_courses = self.env['training.course'].search_count(
                [('instructor_id', '=', instructor.id),
                 ('state', '=', 'confirmed'),
                 ]
            )




