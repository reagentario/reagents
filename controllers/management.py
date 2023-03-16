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

@auth.requires_membership("admin")
def edit_all():
    grid = SQLFORM.grid(db.inventory, paginate=25)
    return dict(grid=grid)

@auth.requires_membership("supermanager")
def edit():
     grid = SQLFORM.grid(db.inventory.id>0, paginate=25)
     return dict(grid=grid)

@auth.requires_membership("supermanager")
def edit_logs():
    grid = SQLFORM.grid(db.applog.id>0, paginate=25)
    return dict(grid=grid)

def list_users():
    btn = lambda row: A("Edit", _href=URL('manage_user', args=row.auth_user.id))
    db.auth_user.edit = Field.Virtual(btn)
    rows = db(db.auth_user).select()
    headers = ["ID", T("Name"), T("Last Name"), T("Alias"), "Email", "Edit"]
    fields = ['id', 'first_name', 'last_name', "alias_name", "email", "edit"]
    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
                  TBODY(*[TR(*[TD(row[field]) for field in fields]) \
                        for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"
    title = T('User List')
    return dict(title=title, table=table)

@auth.requires_membership("manager")
def add_user():
    form = SQLFORM(db.auth_user)
    if form.accepts(request.vars,session):
        logger.info('%s has added the user %s' % (user_alias_name, form.vars.id))
        session.flash=T('accepted form')
        redirect(URL(c='management', r=request, f='list_users'))
    elif form.errors:
        session.flash=T('there are errors in submitted form')
        response.flash=form.errors
    else:
        response.flash=T('please fill out the form')

    return dict(form=form)

@auth.requires_membership("supermanager")
def manage_user():
    user_id = request.args(0) or redirect(URL('list_users'))
    form = SQLFORM(db.auth_user, user_id, readonly=False)
    membership_panel = LOAD(request.controller,
                            'manage_membership.html',
                            args=[user_id],
                            ajax=True)

    if form.accepts(request.vars,session):
        logger.info('%s has modified the user %s' % (user_alias_name, form.vars.id))
        session.flash=T('accepted form')
        redirect(URL(c='management', r=request, f='list_users'))
    elif form.errors:
        session.flash=T('there are errors in submitted form')
        response.flash=form.errors
    else:
        response.flash=T('please fill out the form')

    return dict(form=form,membership_panel=membership_panel)

@auth.requires_membership("supermanager")
def manage_membership():
    user_id = request.args(0) or redirect(URL('list_users'))
    db.auth_membership.user_id.default = int(user_id)
    db.auth_membership.user_id.writable = False
    form = SQLFORM.grid(db.auth_membership.user_id == user_id,
                       args=[user_id],
                       searchable=False,
                       deletable=False,
                       details=False,
                       selectable=False,
                       csv=False)
    return form

@auth.requires_membership("manager")
def list_sublocations():
    btn = lambda row: A("Edit", _href=URL('manage_sublocation', args=row.sublocations.id))
    db.sublocations.edit = Field.Virtual(btn)
    rows = db(db.sublocations).select()
    headers = ["ID", T("Sub Location"), T("Short"), "Edit"]
    fields = ['id', 'sub_location', 'sub_location_short', 'edit']
    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
                  TBODY(*[TR(*[TD(row[field]) for field in fields]) for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"
    return dict(table=table)

@auth.requires_membership("manager")
def manage_sublocation():
    sub_id = request.args(0) or redirect(URL('list_sublocations'))
    form = SQLFORM(db.sublocations, sub_id, deletable=True)
    #if form.process().accepted:
    if form.accepts(request.vars,session):
        logger.info('%s has modified a sublocation %s' % (user_alias_name, form.vars.id))
        session.flash = T('form accepted')
        redirect(URL(c='management', r=request, f='list_sublocations'))
    elif form.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill out the form')
    return dict(form=form)

@auth.requires_membership("manager")
def add_sublocation():
    form = SQLFORM(db.sublocations,  fields = ['sub_location', 'sub_location_short'])
    if form.accepts(request.vars,session):
        logger.info('%s has added the sub location %s' % (user_alias_name, form.vars.id))
        session.flash=T('form accepted')
        redirect(URL(c='management', r=request, f='list_sublocations'))
    elif form.errors:
        session.flash=T('there are errors in submitted form')
        response.flash=form.errors
    else:
        response.flash=T('please fill out the form')

    return dict(form=form)

@auth.requires_membership("manager")
def view_orders():
    btn = lambda row: A("Reset", _href=URL('reset_order', args=row.inventory.id))
    db.inventory.reset_order = Field.Virtual(btn)
    rows = db((db.inventory.to_be_ordered>0)).select()
    headers = [T("Name"), T("Item Size"), T("Quantity"), "Reset"]
    fields = ['item', 'unit_size', 'to_be_ordered', 'reset_order']
    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
                  TBODY(*[TR(*[TD(row[field]) for field in fields]) for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"

    return dict(table=table)

@auth.requires_membership("manager")
def reset_order():
    record = db.inventory[request.args[0]]
    db((db.inventory.id==request.args[0])).update(to_be_ordered=0)
    logger.info('%s has reset orders for id %s -- name: %s' % \
        (user_alias_name, request.args[0], record['item']))
    add_log(itemid='%s' % request.args[0], record=record,
            event_details='order reset', category='R')
    session.flash = T('orders resetted for item %s') % record['item']
    redirect(URL(r=request, f='view_orders'))
    return

@auth.requires_login()
def update():
    # update an existing item
    record = db.inventory(request.args(0)) or redirect(URL('index'))
    r = record.as_dict()

    query = (db.sublocations.id > 0)
    db.inventory.sub_location.requires = IS_IN_DB(db(query), db.sublocations.sub_location_short, '%(sub_location_short)s - %(sub_location)s')

    form = SQLFORM(db.inventory, record)
    if form.accepts(request.vars, session):
        d1 = r
        d2 = db.inventory(request.args(0)).as_dict()
        k1 = set(d1.keys())
        k2 = set(d2.keys())
        common_keys = set(k1).intersection(set(k2))

        for key in common_keys:
            if d1[key] != d2[key] :
                logger.info('%s has updated item number %s: %s: value changed from "%s" to "%s"' % (user_alias_name, request.args[0], key, str(d1[key]), str(d2[key])))
                add_log(itemid=record.id, record=record,
                        event_details='%s has updated item number %s: %s: value changed from "%s" to "%s"' % \
                              (user_alias_name, request.args[0], key, str(d1[key]), str(d2[key])),
                        category='M')

        session.flash = T('accepted form')
        redirect(URL(c='inventory', r=request, f='show', args=form.vars.id))
    elif form.errors:
        session.flash=T('there are errors in submitted form')
        response.flash=form.errors
    else:
        response.flash=T('please fill out the form')
    response.view='insert/insert.html'
    return dict(title="Item modification", form=form)

def add_log(itemid, record, event_details, category):
    db.applog.insert(event_time=now,
                        username='%s' % user_alias_name, itemid=itemid,
                        item='%s' % record.item,
                        event_details=event_details, category=category)

def add_std_log(std_id, record, event_details, category):
    db.applogstd.insert(event_time=now,
                        username='%s' % user_alias_name, std_id=std_id,
                        item='%s' % record.item,
                        event_details=event_details, category=category)

def row2txt(row):
    text = ""
    for key, val in row.iteritems():
        text += ' -- '+key+': '+'"'+str(val)+'"'
    return text

def dict2txt(dict):
    text = ""
    for key, val in dict.vars.iteritems():
        text += ' -- '+key+': '+'"'+str(val)+'"'
    return text
