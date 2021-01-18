# -*- encoding: utf-8 -*-
{
	"name": "Opportunity Product",
	"version": "0.4.0",
        "author": 'Zero Systems',
        "company": 'Zero for Information Systems',
         "website": "https://www.erpzero.com",
        "email": "sales@erpzero.com",
	"sequence": 0,
	"depends": [
		'base','sale_crm','sale','product'
	],
	"category": "crm",
        'summary': """ Add Products to CRM opportunity """,
	"description": """
	This module allow to add normal products on opportunity and create muti quote 
	to help sales department . 
	""",
	"data": [
		'security/ir.model.access.csv',
		'views/opportunity_product.xml',
		'reports/crm_report.xml',
	],
	"auto_install": False,
	"installable": True,
	"application": False,
    'images': ['static/description/logo.PNG'],
	'license': 'LGPL-3',
}
