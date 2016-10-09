# -*- coding: utf-8 -*-
db = DAL('sqlite://storage.sqlite')

db.define_table(auth.settings.table_user_name,
        Field('first_name', length=128, default=''),
        Field('last_name', length=128, default=''),
        Field('username', length=128, default='',unique=True),
        Field('email', length=128, default='', unique=True),
        Field('password', 'password', length=512,readable=False, label='Password'),
        Field('registration_key', length=512,writable=False, readable=False, default=''),
        Field('reset_password_key', length=512,writable=False, readable=False, default=''),
        Field('registration_id', length=512,writable=False, readable=False, default=''))

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires = \
IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires = \
IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [IS_STRONG(min=8,upper=1,lower=1,special=1), CRYPT()]
custom_auth_table.username.requires = [IS_NOT_EMPTY(),IS_NOT_IN_DB(db,custom_auth_table.username)]
custom_auth_table.email.requires = [IS_EMAIL(error_message=auth.messages.invalid_email),IS_NOT_IN_DB(db, custom_auth_table.email)]
auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table


from gluon.tools import Auth, Service, PluginManager
auth = Auth(db)
service = Service()
plugins = PluginManager()
auth.define_tables(username=False, signature=False)
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')

auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

db.define_table('post',
        Field('title','string',requires=IS_NOT_EMPTY() and IS_NOT_IN_DB(db,'post.title') and IS_LENGTH(maxsize=10)),
        Field('about','text',requires=IS_NOT_EMPTY() and IS_NOT_IN_DB(db,'post.about')),
        Field('file','upload',requires=IS_NOT_EMPTY()),
        Field('votes', 'integer',default=0,writable=False,readable=False),
        Field('userid',writable=False,readable=False),
        auth.signature)

db.define_table('comments',
        Field('postid','reference post',readable=False,writable=False),
        Field('body','text',requires=IS_NOT_EMPTY()),
        auth.signature,
        )
db.define_table('likes',
        Field('userid','reference auth_user',readable=False,writable=False),
        Field('postid','reference post',readable=False,writable=False),
        Field('status','integer',default=1)
        )
db.define_table('dummy')
auth.enable_record_versioning(db)
