#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = '夜雨涟'

'''
orm
'''

import asyncio
import logging
import aiomysql


def log(sql, arfs=()):
    logging.info('SQL:%s' % sql)


async def create_pool(loop, **kw):
    logging.info('创建数据库链接池...')
    #用于创建链接池
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),       #默认定义host为localhost
        port=kw.get('port', 3306),              #默认定义mysql的端口号为3306
        user=kw['user'],                        #user是通过关键字参数传递进来
        password=kw['password'],                #password是通过关键字参数传递进来
        db=kw['db'],                            #数据库名字
        charset=kw.get('charset', 'utf8mb4'),   #默认数据库字符集为utf8mb4
        autocommit=kw.get('autocommit', True),  #默认自动提交事务
        maxsize=kw.get('maxsize', 10),          #连接池最多同时处理10个请求
        minsize=kw.get('minsize', 1),           #链接池最少1个请求
        loop=loop                               #传递消息循环对象loop用于异步执行
    )


#用于SQL的select语句。对应select方法，传入sql语句和参数
async def select(sql, args, size=None):
    log(sql, args)
    global __pool
    #异步等待连接池对象返回可以连接线程，with语句封装了清理\关闭conn和处理异常
    async with __pool.get() as conn:
        #等待连接对象返回DictCursor可以通过dice的方式取得数据库对象，需要通过游标对象执行SQL
        async with conn.cursor(aiomysql.DictCursor) as cur:
            #将sql中的'?'替换为'%s'，因为mysql语句中的占位符为%s
            await cur.execute(sql.replace('?', '%s'), args or ())
            #如果传入size
            if size:
                #从数据库获取指定的行数
                rs = await cur.fetchmany(size)
            else:
                #返回所有的结果集
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs))
        return rs

async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected