# -*- coding: utf-8 -*-

#: Database backend
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
#: Secret key
SECRET_KEY = 'make this something random'
#: Timezone
TIMEZONE = 'Asia/Calcutta'

#: Node types that are going to be used
NODULES = ('PAGE', 'FOLDER', )

#: Theme for each node type
# PAGE_THEME = 'templates/themes/mytheme/'  # path to directory where `page/{edit.html,show.html,...}' exists

#:
# PAGE_BASEPATH = '/pages'
# FOLDER_BASEPATH = '/folders'
# FOLDER_URLPATH = '/'
