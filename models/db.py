# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

db.define_table('sublocations',
    SQLField('sub_location', label=(T('Location'))),
    SQLField('sub_location_short', label=(T('Location abbreviation'))),
    fake_migrate=False,
    migrate=True,
    )

db.define_table('inventory',
    SQLField('item', label=(T('Name')), requires=IS_NOT_EMPTY()),
    SQLField('sub_location', label=(T('Primary Location')), requires=IS_IN_DB(db, db.sublocations.sub_location_short, '%(sub_location_short)s')),
    SQLField('sub_location2', label=(T('Secondary Location')), requires=IS_EMPTY_OR(IS_IN_DB(db, db.sublocations.sub_location_short, '%(sub_location_short)s'))),
    SQLField('amount_open', type='integer', label=(T('Item amount open')), requires=IS_INT_IN_RANGE(0, None), default=0),
    SQLField('amount_closed', type='integer', label=(T('Item amount closed')), requires=IS_INT_IN_RANGE(0, None), default=0),
    SQLField('amount_open2', type='integer', label=(T('Item amount open in secondary location')), requires=IS_INT_IN_RANGE(0, None), default=0),
    SQLField('amount_closed3', type='integer', label=(T('Item amount in tertiary location')), requires=IS_INT_IN_RANGE(0, None), default=0),
    SQLField('amount_limit1', type='integer', label=(T('Alert for item amount in primary location')), requires=IS_INT_IN_RANGE(0, None), default=0),
    SQLField('amount_limit3', type='integer', label=(T('Alert for item amount in tertiary location')), requires=IS_INT_IN_RANGE(0, None), default=0),
    SQLField('unit_size', label=(T('Item Size')), requires=IS_NOT_EMPTY()),
    SQLField('notes', label=(T('Note'))),
    SQLField('to_be_ordered', type='integer', label=(T('To be ordered')), requires=IS_INT_IN_RANGE(0, None), default=0),
    fake_migrate=False,
    migrate=True,
    )


db.define_table('log_types',
    SQLField('category', label=(T('Type'))),
    SQLField('description', label=(T('Description'))),
    fake_migrate=False,
    migrate=True,
    )

db.define_table('applog',
    SQLField('event_time', 'datetime'),
    SQLField('username', label=(T('User Alias Name'))),
    SQLField('itemid', label=(T('ID'))),
    SQLField('item', label=(T('Item name'))),
    SQLField('event_details', 'text', label=(T('Event details'))),
    SQLField('category', label=(T('Type')), requires=IS_IN_DB(db, db.log_types.category)),
    fake_migrate=False,
    migrate=True,
    )


# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user']= [
    Field('alias_name', label=(T('Alias Name')))
    ]

auth.define_tables(username=False, signature=False)

if auth.is_logged_in():
    user_id = auth.user.id
    user_alias_name = auth.user.alias_name
else:
    user_id = None
    user_alias_name = None


auth.settings.actions_disabled.append('register')
auth.settings.actions_disabled.append('retrieve_password')

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
