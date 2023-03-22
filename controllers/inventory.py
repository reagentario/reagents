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

@auth.requires_login()
def sub_locations_content_list():
    query = (db.sublocations.id > 0)
    db.inventory.sub_location.requires = IS_IN_DB(db(query), db.sublocations.sub_location_short, '%(sub_location_short)s - %(sub_location)s')

    form = SQLFORM.factory(
                Field("sub_location", label=(T("Location")), requires=IS_EMPTY_OR(IS_IN_DB(db(query), db.sublocations.sub_location_short, '%(sub_location_short)s - %(sub_location)s',multiple=False))),
                formstyle='divs',
                submit_button="Search",
                )

    if form.accepts(request.vars,session):
        sub_location = form.vars.sub_location
        sub_location_exp = db(db.sublocations.sub_location_short==sub_location).select(db.sublocations.sub_location)
        rows = db(db.inventory.sub_location==sub_location).select(orderby=db.inventory.item) #,groupby=db.inventory.item)
        title = T('Sub Location: %s') % sub_location_exp[0].sub_location
    elif form.errors:
        session.flash=T('there are errors in submitted form')
        response.flash=form.errors
    else:
        response.flash=T('please fill out the form')
        title = ""
        rows = []

    headers = [T("Name"), T("Amount"), T("Item Size")]
    fields = ['item', 'amount_closed', 'unit_size']

    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
                  TBODY(*[TR(*[TD(row[field]) for field in fields]) \
                        for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"

    return dict(title=title, form=form, table=table)



@auth.requires_login()
def list():
    import datetime
    query = (db.sublocations.id > 0)

    form = SQLFORM.factory(
                Field("item", label=(T("Item Name"))),
                Field("sub_location", label=(T("Location")), requires=IS_EMPTY_OR(IS_IN_DB(db(query), db.sublocations.sub_location_short, '%(sub_location_short)s - %(sub_location)s',multiple=False))),
                #Field("idnumber", label=(T("ID Number"))),
                formstyle='divs',
                submit_button="Search",
                )

    # The base query to fetch all records
    query = db.inventory.id > 0

    # testing if the form was accepted
    if form.process().accepted:
        # gathering form submitted values
        item = form.vars.item
        #idnumber = form.vars.idnumber
        sub_location = form.vars.sub_location
        # more dynamic conditions in to query
        if item:
            query &= db.inventory.item.like("%%%s%%" % item)
        if sub_location:
            query &= db.inventory.sub_location==sub_location

    type = request.args[0]
    if (type == '0'):
        records = db((db.inventory.id>0) & (query)).select(orderby=db.inventory.item)
        title = T('Laboratory Inventory')

    if not response.flash:
        response.flash = T('Number of items: %s') % len(records)
    return dict(form=form, title=title, list=records)


@auth.requires_membership("manager")
def list_low():
    import datetime

    # The base query to fetch all records
    query = db.inventory.id > 0

    records = db((db.inventory.id>0) & (query)).select(orderby=db.inventory.item)
    rows = []
    for r in records:
        if r.amount_closed3<r.amount_limit3 or r.amount_closed<r.amount_limit1:
            rows.append(r)


    title = T('Laboratory Inventory')

    if not response.flash:
        response.flash = T('Number of items: %s') % len(rows)
    return dict(title=title, list=rows)


@auth.requires_login()
def show():
    record = db.inventory[request.args[0]]
    if not record:
        redirect(URL(r=request, f='index'))

    rows = []
    for f in db.inventory.fields:
        if record[f] == None:
            pass
            #rows.append(TR(TD(db.inventory[f].label, _id="nowrap"), TD((""), _align="middle")))
        else:
            rows.append(TR(TD(db.inventory[f].label, _id="nowrap"), TD(record[f], _align="middle")))

    body = TBODY(*rows)
    table = TABLE(*[body], _class='table-1')

    return dict(title=T("Item details"), table=table, record=record)

@auth.requires_login()
def plus():
    # not used, see move instead
    record = db.inventory[request.args[0]]
    db(db.inventory.id==request.args[0]).update(amount_closed=db.inventory.amount_closed +1)
    logger.info('%s has added 1 unit of id %s -- name: %s' % (user_alias_name,
                request.args[0], record['item']))
    add_log(itemid='%s' % request.args[0], record=record,
                    event_details='added 1 unit', category='A')
    session.flash = T('Item amount closed increased by 1 unit')
    redirect(URL(r=request, f='show', args=request.args[0]))
    return


@auth.requires_login()
def minus():
    record = db.inventory[request.args[0]]
    if record['amount_closed'] == 0:
        session.flash = T('Error - no more available')
        redirect(URL(r=request, f='show', args=request.args[0]))
        return
    db(db.inventory.id==request.args[0]).update(amount_closed=db.inventory.amount_closed -1)
    logger.info('%s has removed 1 unit of id %s -- name: %s' % (user_alias_name,
                request.args[0], record['item']))
    add_log(itemid='%s' % request.args[0], record=record,
                    event_details='removed 1 unit from lab', category='A')
    session.flash = T('Item amount decreased by 1 unit')
    redirect(URL(r=request, f='show', args=request.args[0]))
    return


@auth.requires_login()
def move():
    record = db.inventory[request.args[0]]
    if record['amount_closed3'] == 0:
        session.flash = T('Error - no more available')
        redirect(URL(r=request, f='show', args=request.args[0]))
        return
    db(db.inventory.id==request.args[0]).update(amount_closed=db.inventory.amount_closed +1)
    db(db.inventory.id==request.args[0]).update(amount_closed3=db.inventory.amount_closed3 -1)
    logger.info('%s has moved from warehouse 1 unit of id %s -- name: %s' % (user_alias_name,
                request.args[0], record['item']))
    add_log(itemid='%s' % request.args[0], record=record,
                    event_details='moved 1 unit from warehouse to lab', category='A')
    session.flash = T('Moved 1 unit from warehouse to lab')
    redirect(URL(r=request, f='show', args=request.args[0]))
    return


@auth.requires_login()
def add():
    record = db.inventory[request.args[0]]
    db(db.inventory.id==request.args[0]).update(amount_closed3=db.inventory.amount_closed3 +1)
    logger.info('%s has added to warehouse 1 unit of id %s -- name: %s' % (user_alias_name,
                request.args[0], record['item']))
    add_log(itemid='%s' % request.args[0], record=record,
                    event_details='added 1 unit to warehouse', category='A')
    session.flash = T('Added 1 unit to warehouse')
    redirect(URL(r=request, f='show', args=request.args[0]))
    return


@auth.requires_login()
def order():
    record = db.inventory[request.args[0]]
    db(db.inventory.id==request.args[0]).update(to_be_ordered=db.inventory.to_be_ordered +1)
    logger.info('%s has requested 1 unit of id %s -- name: %s' % \
                (user_alias_name, request.args[0], record['item']))
    add_log(itemid='%s' % request.args[0], record=record,
                    event_details='1 unit requested', category='R')
    session.flash = T('1 unit requested')
    redirect(URL(r=request, f='show', args=request.args[0]))
    return


@auth.requires_login()
def log_note():
    record = db.inventory[request.args[0]]
    form = SQLFORM.factory(
            Field('note', type='text', requires=IS_NOT_EMPTY()),
            formstyle='bootstrap',
            submit_button="OK",
            )
    if form.process().accepted:
        add_log(itemid='%s' % request.args[0], record=record,
                    event_details=form.vars.note, category='N')
        redirect(URL(r=request, f='show', args=request.args[0]))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(title=T('Add note'), form=form, record=record)


@auth.requires_membership("manager")
def delete():
    record = db.inventory[request.args[0]]
    item_id = request.args(0) or redirect(URL(c='inventory', r=request, f='list', args="0"))
    form = SQLFORM(db.inventory, item_id, deletable=True, fields = ['item'])
    if form.process().accepted:
        logger.info('%s has deleted item number %s -- Name: %s' % \
            (user_alias_name, request.args[0], form.vars.item))
        add_log(itemid='%s' % request.args[0], record=record,
                    event_details="deleted", category='D')
        session.flash = 'form accepted'
        redirect(URL(c='inventory', r=request, f='list', args="0"))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(title=T('Deleting Item'), form=form)


def add_log(itemid, record, event_details, category):
    db.applog.insert(event_time=now,
                        username='%s' % user_alias_name, itemid=itemid,
                        item='%s' % record.item,
                        event_details=event_details, category=category)

