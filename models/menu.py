# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(B('web', SPAN(2), 'py'), XML('&trade;&nbsp;'),
                  _class="navbar-brand", _href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = T('Laboratory inventory management')

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('Items'), False, URL(c='inventory', r=request, f='list', args=['0']), []),
]

if auth.has_membership(auth.id_group('manager')):
    response.menu += [
        (T('Management'), False, '#', [
            (T('Add Item'), False, URL('insert','insert'), []),
            (T('Sublocations List'), False, URL('management','list_sublocations'), []),
            (T('View Sublocation content'), False, URL(c='inventory', r=request, f='sub_locations_content_list', args=[]), []),
            (T('Sublocation Add'), False, URL('management','add_sublocation'), []),
            (T('View low quantity'), False, URL('inventory','list_low'), []),
            (T('View Orders'), False, URL('management','view_orders'), []),
            (T('Show item logs'), False, URL(c='logs', r=request, f='show_logs', args="0"), []),
            (T('Search item logs'), False, URL(c='logs', r=request, f='search_logs', args="0"), []),
        ]),
    ]

if auth.has_membership(auth.id_group('supermanager')):
    response.menu += [
        (T('SuperManagement'), False, '#', [
            (T('User List'), False, URL('management','list_users'), []),
            (T('User Add'), False, URL('management','add_user'), []),
            (T('Edit inventory logs'), False, URL(c='management', r=request, f='edit_logs'), []),
            (T('Edit inventory'), False, URL(c='management', r=request, f='edit'), []),
        ]),
    ]

DEVELOPMENT_MENU = False

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources
    # ------------------------------------------------------------------------------------------------------------------
    if auth.has_membership(auth.id_group('admin')):
        response.menu += [
            (T('This App'), False, '#', [
                (T('Edit inventory'), False, URL(c='management', r=request, f='edit_all'), []),
                (T('Design'), False, URL('admin', 'default', 'design/%s' % app)),
                (T('Controller'), False, URL( 'admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
                (T('View'), False, URL( 'admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
                (T('DB Model'), False, URL( 'admin', 'default', 'edit/%s/models/db.py' % app)),
                (T('Menu Model'), False, URL( 'admin', 'default', 'edit/%s/models/menu.py' % app)),
                (T('Config.ini'), False, URL( 'admin', 'default', 'edit/%s/private/appconfig.ini' % app)),
                (T('Layout'), False, URL( 'admin', 'default', 'edit/%s/views/layout.html' % app)),
                (T('Stylesheet'), False, URL( 'admin', 'default', 'edit/%s/static/css/web2py-bootstrap3.css' % app)),
                (T('Database'), False, URL(app, 'appadmin', 'index')),
                (T('Errors'), False, URL( 'admin', 'default', 'errors/' + app)),
                (T('About'), False, URL( 'admin', 'default', 'about/' + app)),
            ]),
        ]


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('This App'), False, '#', [
            (T('Design'), False, URL('admin', 'default', 'design/%s' % _app)),
            (T('Controller'), False,
             URL(
                 'admin', 'default', 'edit/%s/controllers/%s.py' % (_app, request.controller))),
            (T('View'), False,
             URL(
                 'admin', 'default', 'edit/%s/views/%s' % (_app, response.view))),
            (T('DB Model'), False,
             URL(
                 'admin', 'default', 'edit/%s/models/db.py' % _app)),
            (T('Menu Model'), False,
             URL(
                 'admin', 'default', 'edit/%s/models/menu.py' % _app)),
            (T('Config.ini'), False,
             URL(
                 'admin', 'default', 'edit/%s/private/appconfig.ini' % _app)),
            (T('Layout'), False,
             URL(
                 'admin', 'default', 'edit/%s/views/layout.html' % _app)),
            (T('Stylesheet'), False,
             URL(
                 'admin', 'default', 'edit/%s/static/css/web2py-bootstrap3.css' % _app)),
            (T('Database'), False, URL(_app, 'appadmin', 'index')),
            (T('Errors'), False, URL(
                'admin', 'default', 'errors/' + _app)),
            (T('About'), False, URL(
                'admin', 'default', 'about/' + _app)),
        ]),
        ('web2py.com', False, '#', [
            (T('Download'), False,
             'http://www.web2py.com/examples/default/download'),
            (T('Support'), False,
             'http://www.web2py.com/examples/default/support'),
            (T('Demo'), False, 'http://web2py.com/demo_admin'),
            (T('Quick Examples'), False,
             'http://web2py.com/examples/default/examples'),
            (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
            (T('Videos'), False,
             'http://www.web2py.com/examples/default/videos/'),
            (T('Free Applications'),
             False, 'http://web2py.com/appliances'),
            (T('Plugins'), False, 'http://web2py.com/plugins'),
            (T('Recipes'), False, 'http://web2pyslices.com/'),
        ]),
        (T('Documentation'), False, '#', [
            (T('Online book'), False, 'http://www.web2py.com/book'),
            (T('Preface'), False,
             'http://www.web2py.com/book/default/chapter/00'),
            (T('Introduction'), False,
             'http://www.web2py.com/book/default/chapter/01'),
            (T('Python'), False,
             'http://www.web2py.com/book/default/chapter/02'),
            (T('Overview'), False,
             'http://www.web2py.com/book/default/chapter/03'),
            (T('The Core'), False,
             'http://www.web2py.com/book/default/chapter/04'),
            (T('The Views'), False,
             'http://www.web2py.com/book/default/chapter/05'),
            (T('Database'), False,
             'http://www.web2py.com/book/default/chapter/06'),
            (T('Forms and Validators'), False,
             'http://www.web2py.com/book/default/chapter/07'),
            (T('Email and SMS'), False,
             'http://www.web2py.com/book/default/chapter/08'),
            (T('Access Control'), False,
             'http://www.web2py.com/book/default/chapter/09'),
            (T('Services'), False,
             'http://www.web2py.com/book/default/chapter/10'),
            (T('Ajax Recipes'), False,
             'http://www.web2py.com/book/default/chapter/11'),
            (T('Components and Plugins'), False,
             'http://www.web2py.com/book/default/chapter/12'),
            (T('Deployment Recipes'), False,
             'http://www.web2py.com/book/default/chapter/13'),
            (T('Other Recipes'), False,
             'http://www.web2py.com/book/default/chapter/14'),
            (T('Helping web2py'), False,
             'http://www.web2py.com/book/default/chapter/15'),
            (T("Buy web2py's book"), False,
             'http://stores.lulu.com/web2py'),
        ]),
        (T('Community'), False, None, [
            (T('Groups'), False,
             'http://www.web2py.com/examples/default/usergroups'),
            (T('Twitter'), False, 'http://twitter.com/web2py'),
            (T('Live Chat'), False,
             'http://webchat.freenode.net/?channels=web2py'),
        ]),
    ]

