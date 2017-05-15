#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/15 下午2:45
# @Author  : allenwu
# @File    : config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

