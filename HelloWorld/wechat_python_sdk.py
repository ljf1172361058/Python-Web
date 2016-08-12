# -*- coding: utf-8 -*-

' 使用Python进行微信公众号开发 '

__author__ = 'Zhihui Li'

from wechat_sdk import WechatConf
WECHAT_TOKEN = 'zhimeng'
AppID = 'wx41f672045025645d'
AppSecret = '9476f135cf6534cebaacb946df89794c'
# 实例化 WechatConf 微信配置类
conf = WechatConf(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret,
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='MAue8W7ftSTzYo98lHFK1x6HWtNRgAY0jpChUaBkGQZ'  # 如果传入此值则必须保证同时传入 token, appid
)

from wechat_sdk import WechatBasic
# 实例化 WechatBasic 官方接口类
wechat = WechatBasic(conf=conf)

from django.http import HttpResponse, HttpResponseBadRequest
from wechat_sdk.messages import *
from django.views.decorators.csrf import csrf_exempt
from HelloWorld.switch import Switch
from HelloWorld.record_query import getData

@csrf_exempt
def checkout(request):
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        # 验证服务器请求有效性
        if not wechat.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        # 验证成功
        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")

    # POST
    elif request.method == 'POST':
        # 解析本次请求的 XML 数据
        try:
            wechat.parse_data(data=request.body)
        except ParseError:
            return HttpResponseBadRequest('Invalid XML Data')

        # 获取解析好的微信请求信息
        message = wechat.get_message()

        # 回复类型,默认为文本,于reply_dict中的key对应
        reply_type = 'reply_text'

        # 关注事件以及不匹配时的默认回复
        reply_text = '感谢米娜桑的关注^_^！\n' \
                     '回复括号内的关键字可获取相关信息哦：\n' \
                     '【功能】查看目前支持的功能\n' \
                     '【战绩 角色名】查看300战绩'

        # 定义一个回复消息字典,所有回复类型及回复信息均按照微信回复规则定义
        reply_dict = {'reply_text': reply_text,
                      'reply_image': '',
                      'reply_voice': '',
                      'reply_video': [],
                      'reply_music': '',
                      'reply_news': [{'title': '', 'description': '', 'picurl': '', 'url': ''}]
                      }

        # 是否是文本消息
        if isinstance(message, TextMessage):
            # 当前会话内容
            content = message.content.strip()  # 对应于 XML 中的 Content

            if content == '功能':
                reply_dict[reply_type] = (
                    '目前支持的功能：\n\n'
                    '1.300英雄战绩查询\n'
                    '2.装逼卖萌/:8-)'
                    '\n\n觉得功能不够多,没关系!\n'
                    '还有更多功能正在开发中哦！'
                    '敬请期待^_^'
                )
            if content.startswith('战绩'):
                if content == '战绩':  # 用户查战绩但没有输入角色名
                    # 提示ta输入角色名
                    reply_dict[reply_type] = (
                        '想查战绩?/::$\n小伙子你可不按套路出牌呐/:dig\n'
                        '角色名都没得让我咋查?/:P-(/快哭了'
                    )
                else:
                    # 获取角色名
                    content = content[2:]
                    reply_dict[reply_type] = getData(content.strip())

        # 是否是图片消息
        elif isinstance(message, ImageMessage):
            picurl = message.picurl  # 对应于 XML 中的 PicUrl
            media_id = message.media_id  # 对应于 XML 中的 MediaId
            reply_dict[reply_type] = '您发送的是图片：图片链接为:' + picurl

        # 是否是录音消息
        elif isinstance(message, VoiceMessage):
            media_id = message.media_id  # 对应于 XML 中的 MediaId
            format = message.format  # 对应于 XML 中的 Format
            recognition = message.recognition  # 对应于 XML 中的 Recognition
            reply_dict[reply_type] = '您发送的是一段语音'

        # 是否是小视频消息
        elif isinstance(message, ShortVideoMessage):
            media_id = message.media_id  # 对应于 XML 中的 MediaId
            thumb_media_id = message.thumb_media_id  # 对应于 XML 中的 ThumbMediaId
            reply_dict[reply_type] = '您发送的是一段小视频'

        # 是否是视频消息
        elif isinstance(message, VideoMessage):
            media_id = message.media_id  # 对应于 XML 中的 MediaId
            thumb_media_id = message.thumb_media_id  # 对应于 XML 中的 ThumbMediaId
            reply_dict[reply_type] = '您发送的是一段视频'

        # 是否是地理位置消息
        elif isinstance(message, LocationMessage):
            location = message.location  # Tuple(X, Y)，对应于 XML 中的 (Location_X, Location_Y)
            scale = message.scale  # 对应于 XML 中的 Scale
            label = message.label  # 对应于 XML 中的 Label
            reply_dict[reply_type] = '您发送的是一段地理位置'

        # 是否是链接消息
        elif isinstance(message, LinkMessage):
            title = message.title  # 对应于 XML 中的 Title
            description = message.description  # 对应于 XML 中的 Description
            url = message.url  # 对应于 XML 中的 Url
            reply_dict[reply_type] = '您发送的是一段链接,链接地址为:'+url

        # 是否是事件消息
        elif isinstance(message, EventMessage):
            if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                key = message.key  # 对应于 XML 中的 EventKey (普通关注事件时此值为 None)
                ticket = message.ticket  # 对应于 XML 中的 Ticket (普通关注事件时此值为 None)
                reply_dict[reply_type] = '感谢米娜桑的关注^_^！\n' \
                             '回复括号内的关键字可获取相关信息哦：\n' \
                             '【功能】查看目前支持的功能\n' \
                             '【战绩 角色名】查看300战绩'

            elif message.type == 'unsubscribe':  # 取消关注事件（无可用私有信息）
                pass
            elif message.type == 'scan':  # 用户已关注时的二维码扫描事件
                key = message.key  # 对应于 XML 中的 EventKey
                ticket = message.ticket  # 对应于 XML 中的 Ticket
            elif message.type == 'location':  # 上报地理位置事件
                latitude = message.latitude  # 对应于 XML 中的 Latitude
                longitude = message.longitude  # 对应于 XML 中的 Longitude
                precision = message.precision  # 对应于 XML 中的 Precision
            elif message.type == 'click':  # 自定义菜单点击事件
                key = message.key  # 对应于 XML 中的 EventKey
            elif message.type == 'view':  # 自定义菜单跳转链接事件
                key = message.key  # 对应于 XML 中的 EventKey
            elif message.type == 'templatesendjobfinish':  # 模板消息事件
                status = message.status  # 对应于 XML 中的 Status
            elif message.type in ['scancode_push', 'scancode_waitmsg', 'pic_sysphoto',
                                  'pic_photo_or_album', 'pic_weixin', 'location_select']:  # 其他事件
                key = message.key  # 对应于 XML 中的 EventKey
                reply_dict[reply_type] = '感谢您的关注'

        # 自定义一个 switch类 来实现其他语言中switch的功能【当然Python中也可以用字典代替switch】
        for case in Switch(reply_type):
            if case('reply_text'):  # 回复文本消息
                response = wechat.response_text(content=reply_dict.get(reply_type))
                break
            if case('reply_image'):  # 回复图片消息
                response = wechat.response_image(media_id=reply_dict.get(reply_type))
                break
            if case('reply_voice'):  # 回复语音消息
                response = wechat.response_voice(media_id=reply_dict.get(reply_type))
                break
            if case('reply_video'):  # 回复视频消息
                response = wechat.response_video(media_id=reply_dict.get(reply_type)[0], title=None, description=None)
                break
            if case('reply_music'):  # 回复音乐消息
                response = wechat.response_music(music_url=reply_dict.get(reply_type)[0], title=None, description=None,
                                                 hq_music_url=None, thumb_media_id=None)
                break
            if case('reply_news'):  # 回复图文消息(这里还有问题,需完善后方可使用)
                # response = wechat.response_news(articles=reply_dict.get(reply_type)[0])
                pass
            if case():  # default, could also just omit condition or 'if True'
                print("something else!")
                response = wechat.response_text(content=reply_dict.get(reply_type))
                # No need to break here, it'll stop anyway

    return HttpResponse(response, content_type="application/xml")