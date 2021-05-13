#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'AmamiyaRen'

'''
导入 logging 模块并使用';'对其全局配置
logging 模块用法：参考自 https://zhuanlan.zhihu.com/p/56968001
basicConfig 配置了 level 信息，level 配置为 INFO 信息，即只输出 INFO 级别的信息
logging 日志的级别可参考下面的官方文档
https://docs.python.org/zh-cn/3.8/library/logging.html?highlight=logging#logging-levels
'''

import logging;logging.basicConfig(level=logging.INFO)
import asyncio
from aiohttp import web

async def index(request):
    # 请求---》web---》响应
    # request         response
    return web.Response(body=b'<h1>Awesome</h1>', headers={'content-type': 'text/html'})


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), '192.168.10.40', 9000)
    logging.info('server started at http://192.168.10.40:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
