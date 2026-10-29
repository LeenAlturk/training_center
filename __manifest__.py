# -*- coding: utf-8 -*-
{
    "name" : "Training Center",
    "version" : "1.0",
    "author" : "leen",
    "depends": ["base","sale","mail"],
    "summary" : "Training Center is a moduel that elp you to mange your work",
    "application" : True,
    'data' : [
        'security/ir.model.access.csv',
        'data/course_sequanse.xml',
        "views/course.xml",
        "views/instructor.xml",
        "views/tags.xml",
        "views/partner.xml",
        "views/sale.xml",
        "views/product.xml",
        "views/account_move_line.xml"
    ]
}