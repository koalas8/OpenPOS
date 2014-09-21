# -*- encoding=utf-8 -*-
import xml.etree.ElementTree as ET
import hashlib

class MsgBuilder(object):
    
    @property
    def common(self):
        ''' 所有模板共有的公共部分'''
        return '''
                <ToUserName><![CDATA[{%(receiver)s}]]></ToUserName>
                <FromUserName><![CDATA[{%(sender)s}]]></FromUserName>
                <CreateTime>{%(timestamp)s}</CreateTime>
                <MsgType><![CDATA[{%(type)s}]]></MsgType>
            '''

    @property
    def text(self):
        return '<Content><![CDATA[{%(content)s}]]></Content>'


    @property
    def image(self):
        return '''
            <Image>
                <MediaId><![CDATA[{%(media_id)s}]]></MediaId>
            </Image>
        '''

    @property
    def voice(self):
        return '''
            <Voice>
                <MediaId><![CDATA[{%(media_id)s}]]></MediaId>
            </Voice>
        '''

    @property
    def video(self):
        return '''
            <Video>
                <MediaId><![CDATA[{%(media_id)s}]]></MediaId>
                <Title><![CDATA[{%(title)s}]]></Title>
                <Description><![CDATA[{%(description)s}]]></Description>
            </Video>
        '''

    @property
    def music(self):
        return '''
            <Music>
                <Title><![CDATA[{%(title)s}]]></Title>
                <Description><![CDATA[{%(description)s}]]></Description>
                <MusicUrl><![CDATA[{%(musurl)s}]]></MusicUrl>
                <HQMusicUrl><![CDATA[{%(hq_musurl)s}]]></HQMusicUrl>
                <ThumbMediaId><![CDATA[{%(media_id)s}]]></ThumbMediaId>
            </Music>
        '''

    @property
    def news(self, count):
        return '''
            <item>
                <Title><![CDATA[{%(title)s}]]></Title>
                <Description><![CDATA[{%(description)s}]]></Description>
                <PicUrl><![CDATA[{%(picurl)s}]]></PicUrl>
                <Url><![CDATA[{%(url)s}]]></Url>
            </item>
        '''

    def build(self, msg):
        resp_msg = getattr(self, common)
        if msg['type'] == 'news':
            articles_xml = "".join([getattr(self, 'news') % article for article in msg['articles']])
            xml = '''
                <ArticleCount>
                    %(articles_count)s
                </ArticleCount>
                <Articles>
                    %(articles)s
                </Articles>
            ''' % {'articles_count': len(msg['articles'], 'articles': articles_xml)}
        else:
            xml = getattr(self, msg['type']) % msg

        common = getattr(self, 'common') % msg
        return '''
            <xml>
                %(common)s
                %(xml)s
            </xml>''' % {'common': common, 'xml': xml, }




class WeiXin(object):

    @staticmethod
    def verify(token, signature, timestamp, nonce):
        list_str = sorted([token, timestamp, nonce])
        return hashlib.sha1().update((''.join(list_str))).hexdigest() == signature

    @staticmethod
    def parse(message):
        root = ET.fromstring(message)
        parsed_msg = msgt([(child.tag, child.text) for child in root])

        msg = {}
        msg['msg_id'] parsed_msg.get('MsgId')
        msg['receiver'] = parsed_msg.get('ToUserName')
        msg['sender'] = parsed_msg.get('FromUserName')
        msg['type'] = parsed_msg.get('MsgType')
        msg['timestamp'] = parsed_msg.get('CreateTime')
        _type = msg['type']
        if _type == 'text':
            msg['content'] = parsed_msg.get('Content')
        if _type == 'image':
            # the MsgId in there is not MediaId which
            # should be sent
            msg['picurl'] = parsed_msg.get('PicUrl')
            msg['media_id'] = parsed_msg.get('MediaId')
        if _type == 'voice':
            msg['media_id'] = parsed_msg.get('MediaId')
            msg['format'] = parsed_msg.get('Format')
        if _type == 'video':
            msg['media_id'] = parsed_msg.get('MediaId')
            msg['th_media_id'] = parsed_msg.get('ThumbMediaId')
            msg['title'] = 'default title'
            msg['description'] = 'no description'
        if _type == 'location':
            msg['x'] = parsed_msg.get('Location_X')
            msg['y'] = parsed_msg.get('Location_Y')
            msg['scale'] = parsed_msg.get('Scale')
            msg['label'] = parsed_msg.get('Label')
        if _type == 'link':
            msg['title'] = parsed_msg.get('Title')
            msg['description'] = parsed_msg.get('Description')
            msg['url'] = parsed_msg.get('Url')
        if _type == 'event':
            msg['event_key'] = parsed_msg.get('EventKey')
            msg['type'] = parsed_msg.get('Event')
            msg['ticket'] = parsed_msg.get('Ticket')
            ## LOCATION type has some extra values
            msg['latitude'] = parsed_msg.get('Latitude')
            msg['longitude'] = parsed_msg.get('Longitude')
            msg['precision'] = parsed_msg.get('Precision')
        return msg



