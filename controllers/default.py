# -*- coding: utf-8 -*-

def user():
    return dict(form=auth())

def index():
    if len(request.args):
        page=int(request.args[0])
    else: 
        page=0
    items_per_page=5
    limitby=((page)*items_per_page,(page+1)*items_per_page+1)
    x = db().select(db.post.ALL,limitby=limitby,orderby=~db.post.created_on)
    return dict(x=x,page=page,items_per_page=items_per_page)

@auth.requires_login()
def upload():
    post=SQLFORM(db.post).process()
    if post.accepts(request.vars):
        response.flash='Uploaded Successfully'
        session.prompt='Your profile updated.View '
        redirect(URL('index'))
    elif post.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return locals()

def myrecepies():
    rec = db((db.post.created_by==auth.user_id)).select(orderby=~db.post.created_on)
    return dict(rec=rec)

def edit():
        this_recipe = db.post(request.args(0,cast=int)) or redirect(URL('index'))
        form = SQLFORM(db.post,this_recipe).process(next = URL('show',args=request.args))
        return dict(form=form)

@auth.requires_membership('manager')
def manage():
    grid= SQLFORM.grid(db.post)
    return locals()

def show(): 
    curr=db.post(request.args(0,cast=int))
    db.comments.postid.default=curr.id
    form=SQLFORM(db.comments,submit_button='Upload').process()
    com=db(db.comments.postid==curr.id).select()
    if session.sent:
        curr.update_record(votes=session.new)
        session.sent=''
    voting=SQLFORM(db.dummy,submit_button='Like/Unlike').process()
    if voting.accepted:
        redirect(URL('second',args=[curr.id]))
    return locals()

def second():
    currpost=db.post(request.args(0,cast=int))
    existing=db(db.likes.userid==auth.user_id).select(db.likes.ALL)
    session.sent=1
    session.new=1
    session.flag =0
    for row in existing:
        if row.postid == request.args(0,cast=int):
            session.flag = session.get('flag')+1
            if row.status==2:
                session.new= currpost.votes-1
                row.update_record(status=1)
            elif row.status==1:
                session.new= currpost.votes+1
                row.update_record(status=2)
    if session.flag!=0:
        return locals()
    else:
        session.new= currpost.votes+1
        db.likes.insert(userid=auth.user_id,postid=request.args(0),status=2)
        return locals()






























def add():
    form=SQLFORM(db.item).process()
    if form.accepts(request.vars):
        response.flash='Uploaded Successfully'
        session.prompt='Your profile updated.Click below to view'
        redirect(URL('index'))
    elif post.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return locals()

def session_counter():
    session.counter = session.get('counter',1)+1
    session.counter2 = session.get('counter2',1)+1
    redirect(URL('first',args=['hips2','dont2','lie2']))
    return dict(message=T("Hello MyApp"), count=session.counter)

def first():
    x=request.args
    v1=request.function
    session.a=session.a or 1
    form1=FORM(INPUT(_type='submit')).process()
    if form1.accepted:
        redirect(URL('second'))
    return dict(rform=form1,x=x,v1=v1)

def download():
    return response.download(request, db)

def call():
    return service()

@auth.requires_signature()
def data():
    return dict(form=crud())
