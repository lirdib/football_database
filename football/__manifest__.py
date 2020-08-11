# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Football',
    'version': '1.1',
    'category': 'Football',
    'sequence': 1,
    'summary': 'Jobs, Departments, Employees Details',
    'description': "",
    'website': 'https://www.odoo.com/page/employees',
    'images': [
    ],
    'depends': [
        'base_setup',
        'mail',
        'resource',
        'web',
    ],
    'data': [
        'views/sezone_view.xml',
        'views/ekipi_view.xml',
        'views/lojtari_view.xml',
        'views/kombesia_view.xml',
        'views/ndeshje_view.xml',
        'views/transferime_view.xml',
        'views/sezon_ekip_view.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
