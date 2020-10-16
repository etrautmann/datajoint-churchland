import datajoint as dj
from churchland_pipeline_python import acquisition, equipment
import os, re, inspect
from datetime import datetime

# create virtual module (creates a schema with originally defined tables)
# first argument: package name, not relevant
# second argument: schema name, most important
# lab = dj.create_virtual_module('shan_costa_lab', 'shan_costa_lab') 
# lab.__name__
# lab.schema.drop()

def schema_drop_order():
    return [
        'churchland_analyses_pacman_processing',
        'churchland_analyses_pacman_acquisition',
        'churchland_analyses_processing',
        'churchland_common_acquisition',
        'churchland_common_action',
        'churchland_common_reference',
        'churchland_common_lab',
        'churchland_common_equipment'
    ]

def fill_sessions():
    """
    Fill remaining session data
    """

    for session_key in acquisition.Session.fetch('KEY'):

        # add users
        acquisition.Session.User.insert1(dict(user='njm2149', **session_key), skip_duplicates=True)
        if session_key['session_date'] >= datetime.strptime('2019-11-01','%Y-%m-%d').date():
            acquisition.Session.User.insert1(dict(user='emt2177', **session_key), skip_duplicates=True)

        # add load cell
        acquisition.Session.Hardware.insert1(dict(
            **session_key,
            **(equipment.Hardware & {'hardware': '5lb Load Cell'}).fetch1('KEY')
            ), skip_duplicates=True)