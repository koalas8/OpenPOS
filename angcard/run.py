#-*- coding=utf-8 -*-
# ╔══╗╔╗═══════╔╗╔╗
# ╚╗╔╝║║╔═╦╦╦═╗║╚╝╠═╦╦╗
# ╔╝╚╗║╚╣║║║║╩╣╚╗╔╣║║║║
# ╚══╝╚═╩═╩═╩═╝═╚╝╚═╩═╝
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from juke import app

