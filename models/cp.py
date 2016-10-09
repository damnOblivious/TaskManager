# -*- coding: utf-8 -*-
db = DAL('sqlite://storage.sqlite')

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
auth.enable_record_versioning(db)
