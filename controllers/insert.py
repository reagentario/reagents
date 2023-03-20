# coding: utf8
import datetime
import string
import os,sys

now = datetime.datetime.now()

@auth.requires_membership("manager")
def insert():
    # form to insert a new item
    query = (db.sublocations.id > 0)
    db.inventory.sub_location.requires = IS_IN_DB(db(query), db.sublocations.sub_location_short, '%(sub_location_short)s - %(sub_location)s')
    db.inventory.sub_location2.requires = IS_IN_DB(db(query), db.sublocations.sub_location_short, '%(sub_location_short)s - %(sub_location)s')

    db.inventory.to_be_ordered.readable = db.inventory.to_be_ordered.writable = False

    form=SQLFORM(db.inventory,formstyle='table3cols', _class='string')

    if form.accepts(request.vars,session):
        text = dict2txt(form)
        logger.info('%s has created item number %s: %s' % (user_alias_name, form.vars.id, text))
        add_log(itemid='%s' % form.vars.id, item='%s' % form.vars.item, lot='%s' % form.vars.lot,
                event_details='added %s units' % form.vars.amount_closed, category='C')
        session.flash=T('form accepted')
        redirect(URL(c='inventory', r=request, f='show', args=form.vars.id))
    elif form.errors:
        session.flash=T('there are errors in submitted form')
        response.flash=form.errors
    else:
        response.flash=T('please fill out the form')
    return dict(title=T("New item addition"), form=form)

@auth.requires_membership("manager")
def copy():
    # create a new item starting from an existing ones
    row=db(db.inventory.id==request.args[0]).select()[0]

    query = (db.sublocations.id > 0)

    db.inventory.to_be_ordered.readable = db.inventory.to_be_ordered.writable = False

    # set the default for all fields by ID
    for fieldname in db.inventory.fields:
        if fieldname!='id': db.inventory[fieldname].default=row[fieldname]

    db.inventory.sub_location.requires = IS_IN_DB(db(query), db.sublocations.sub_location_short, '%(sub_location_short)s - %(sub_location)s')

    form=SQLFORM(db.inventory,formstyle='table3cols', _class='string')
    form.vars.to_be_ordered = 0
    form.vars.amount_closed = False
    if form.accepts(request.vars,session):
        text = dict2txt(form)
        logger.info('%s has created item number %s (copy from %s): %s' % (user_alias_name, form.vars.id, request.args[0], text))
        add_log(itemid='%s' % form.vars.id, item='%s' % form.vars.item,
                event_details='added %s units' % form.vars.amount_closed, category='C')
        session.flash=T('accepted form')
        redirect(URL(c='inventory', r=request, f='show', args=form.vars.id))
    elif form.errors:
        session.flash=T('there are errors in submitted form')
        response.flash=form.errors
    else:
        response.flash=T('please fill out the form')
    response.view='insert/insert.html'
    return dict(title=T("New Item"), form=form)

def add_log(itemid, item, lot, event_details, category):
    db.applog.insert(event_time=now,
                        username='%s' % user_alias_name, itemid=itemid,
                        item=item,
                        event_details=event_details,
                        category=category)


def row2txt(row):
    text = ""
    for key, val in row.iteritems():
        text += ' -- '+key+': '+'"'+str(val)+'"'
    return text

def dict2txt(dict):
    text = ""
    for key, val in dict.vars.items():
        session.flash=('key, val = %s - %s') % (key, val)
        text += ' -- '+key+': '+'"'+str(val)+'"'
    return text

