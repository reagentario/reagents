# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import datetime
now = datetime.datetime.now()

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


@auth.requires_login()
def show_logs():

    if not request.vars.page:
        redirect(URL(args=request.args[0], vars={'page':1}))
    else:
        page = int(request.vars.page)

    start = (page-1)*50
    end = page*50

    type = request.args[0]
    if (type == '0'):
        query = db.applog.id > 0
        count = db(query).count()
        rows = db(query).select(limitby=(start,end), orderby=~db.applog.event_time)
        pager = 1
        title = T('All Logs')
    else:
        query = db.applog.id > 0
        query &= db.applog.itemid==request.args[0]
        count = db(query).count()
        rows = db(query).select(orderby=~db.applog.event_time)
        pager = 0
        title = T('Item Logs')

    response.flash = T('Number of results: %s') % count

    return dict(title=title, rows=rows, pager=pager)


@auth.requires_login()
def search_logs():
    form = SQLFORM.factory(
                Field("item", label=(T('Item Name'))),
                Field("username", label=(T('User Alias Name'))),
                Field('itemid', label=(T('ID'))),
                Field('category', label=(T('Category')), requires=IS_EMPTY_OR(IS_IN_DB(db, db.log_types.category, '%(description)s',multiple=True))),
                formstyle='divs',
                submit_button="Search",
                )

    # The base query to fetch no records
    query = db.applog.id<1
    query2 = db.applog.id>1
    # testing if the form was accepted
    if form.process().accepted:
        query = db.applog.id > 0
        # gathering form submitted values
        itemid = form.vars.itemid
        item = form.vars.item
        username = form.vars.username
        category = form.vars.category
        # more dynamic conditions in to query
        if itemid:
            query &= db.applog.itemid == itemid
        if item:
            query &= db.applog.item.like("%%%s%%" % item)
        if username:
            query &= db.applog.username.like("%%%s%%" % username)
        if category:
            for i,st in enumerate(category):
                subquery = db.applog.category.like("%%%s%%" % st)
                query2=query2|subquery if i else subquery
                #see https://web2py.wordpress.com/tag/select/
    elif form.errors:
        session.flash=T('there are errors in submitted form')
        response.flash=form.errors
    else:
        response.flash = 'please fill out the form'


    count = db(query&query2).count()
    rows = db(query&query2).select(orderby=~db.applog.id)
    response.flash = T('Number of results: %s') % count
    return dict(form=form, rows=rows)
