# -*- coding: utf-8 -*-
{
    'name': 'Import Metadata',
    'description' : """Allow you to import metadata on every record. The metadata are the create_uid, create_date, 
        write_uid, write_date. You need to call create or write (or load method) 
        as admin with the following value in the context: {'write_metadata': True}.
        
        Note that write_date and write_uid may not be set as you want since other write can be trigger directly after yours in the same transaction.
        Like on res.partner. Those two value will change soon anyway. 
    """,
    'version': '1.0',
    "category": 'Extra Tools',
    'author': 'Thibault Francois',
    'depends': ['base'],
    'website': 'https://github.com/tfrancoi/easier_import',
    'data': [],
    'installable': True,
    'application': False,
}


