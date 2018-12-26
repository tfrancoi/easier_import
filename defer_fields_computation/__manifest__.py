# -*- coding: utf-8 -*-
{
    'name': 'Defer Fields Computation',
    'description': """Allow to load data into a model by deferring the computation of the computed fields at the end of the load. 
    All the computations are then processed in batch on all the records created in one transaction.
    This can significantly decrease the import time on a model with transaction size > 1.
    This functionality is active if {'defer_fields_computation': True} is set in the context.
    """,
    'version': '1.0',
    "category": 'Extra Tools',
    'author': 'Jean Adam',
    'depends': ['base'],
    'website': 'https://github.com/tfrancoi/easier_import',
    'data': [],
    'installable': True,
    'application': False,
}


