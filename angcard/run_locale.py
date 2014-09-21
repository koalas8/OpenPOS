#-*- coding=utf-8 -*-
# ╔══╗╔╗═══════╔╗╔╗
# ╚╗╔╝║║╔═╦╦╦═╗║╚╝╠═╦╦╗
# ╔╝╚╗║╚╣║║║║╩╣╚╗╔╣║║║║
# ╚══╝╚═╩═╩═╩═╝═╚╝╚═╩═╝
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from juke import app

app.run(host='0.0.0.0', port=80)
