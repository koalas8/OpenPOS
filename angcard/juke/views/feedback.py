#-*- coding=utf-8 -*-
from flask import session, request, Blueprint
from flask.json import jsonify
from flask.views import MethodView
from sqlalchemy import or_, and_, desc
from sqlalchemy.orm import aliased
from juke.modules import *
from juke import rspmsg
from juke import app
from juke import authority


class FeedbackList(MethodView):
	def get(self):
		i = request
		page = int(i.get('page', '1'))
		limit = int(i.get('limit', '10'))

		q = db_session.query(FeedbackInfo)
		total = q.count()
		q = q.order_by(FeedbackInfo.create_datetime.desc())
		suggestions = q.limit(limit).offset((page - 1) * limit).all()

		return jsonify(success=True, total=total, page=page, limit=limit,
					   data=[{'titls': s.title} for s in suggestions])


	def post(self):
		unit_no = session['unit_no']
		shop_no = session['shop_no'] or ''
		creator = session['user_no']
		title = request.json.get('title', '').strip()
		content = request.json.get('content', '').strip()
		if not title:
			return jsonify(success=False, msg=u'请填写标题', show_msg=True)

		feedback = FeedbackInfo(unit_no=unit_no, shop_no=shop_no, creator=creator, title=title, content=content)
		db_session.add(feedback)
		db_session.commit()
		return jsonify(success=True, msg=u'您的反馈我们已经收到，如有需要，我们会及时与您联系。', show_msg=True)

