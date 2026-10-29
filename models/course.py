from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
class Course(models.Model):
    _name = 'training.course'
    _description = 'Training Center'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    course_Number = fields.Char(
        string="Course Number",
        required=True,
        readonly=True,
        copy=False,
        default="New",
    )
    name = fields.Char(string='Course Name')
    description = fields.Text(string='Course Description')
    price = fields.Float(string='Course Price')
    start_date = fields.Datetime(string='Course Start Date')
    seats = fields.Integer(string='Course Seats')
    end_date = fields.Datetime(string='Course End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ],default='draft',string='Course State',tracking = True)
    instructor_id = fields.Many2one(
        comodel_name='instructor',
        string='Instructor',
    )

    tags_ids = fields.Many2many(
        comodel_name='tags.course',
        string='Tags',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Related Product',
        readonly=True,
        copy=False,

    )
    email_instructor = fields.Char(string='Email Instructor', related='instructor_id.email')

    total_revenue = fields.Integer(string='Total Revenue' , compute='_compute_total_revenue' )

    @api.onchange('instructor_id')
    def warning_number_of_courses(self):
        if self.instructor_id.my_courses > 3 :
                return {
                    'warning':{
                        'title':'Course Warning',
                        'message':'this instructor has more than 3 courses',
                    },
                }


    @api.onchange('instructor_id')
    def help_user_with_price(self):
            if self.instructor_id:
                self.price = self.instructor_id.default_rate
            else:
                self.price = 0


    @api.depends('price','seats')
    def _compute_total_revenue(self):
        total_revenue = 0
        for course in self:
            total_revenue += course.price * course.seats
            course.total_revenue = total_revenue

    @api.constrains('start_date','end_date')
    def check_course_start_date(self):
        for course in self:
            if course.start_date and course.start_date > course.end_date:
                raise ValidationError('Course Start Date must be before Course End Date')

    @api.constrains('seats')
    def check_course_seats(self):
     for course in self:
         if course.seats <= 0 :
             raise ValidationError('Course seats must be greater than 0')


    @api.constrains('instructor_id','seats')
    def check_max_class_size(self):
        for course in self:
            if course.seats > course.instructor_id.max_class_size:
                raise ValidationError('Course seats more than max class size of instructor')




    def action_confirm_course(self):
        for course in self:
               course.state = 'confirmed'
               product=self.env['product.product'].create({
                   'name' : course.name,
                   'seat' :course.seats,
                   'state' : course.state,
                   'list_price' : course.price,
                   'type' : 'service',
               })
               course.product_id = product.id
        return True

    def action_see_related_product(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'product.product',
            'res_id': self.product_id.id,
            'domain': [('name','=',self.name)],

        }

    def write(self, vals):
        res = super().write(vals)
        for course in self:
            if course.product_id:
                if 'price' in vals:
                        if course.price:
                            course.product_id.list_price = course.price
                if 'name' in vals:
                    if course.name:
                        course.product_id.name = course.name
                if 'state' in vals:
                    if course.state:
                        course.product_id.state = course.state
        return res





    def action_make_done_course(self):
        for course in self:
            if course.state == 'confirmed':
                course.state = 'done'
            elif course.state == 'draft':
             raise UserError('You cannot make course as Done in  in Draft state')



    def action_cancel_course(self):
        for course in self:
            course.state = 'cancel'

    def unlink(self):
        for course in self:
            if course.state != 'draft':
                raise UserError('You cannot delete course not in Draft state')
        return super().unlink()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("course_Number", "New") == "New":
                vals["course_Number"] = self.env["ir.sequence"].next_by_code(
                    "training_course"
                ) or "New"
        return super().create(vals_list)



