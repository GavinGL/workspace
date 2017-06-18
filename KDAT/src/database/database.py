# -*- coding: UTF-8 -*-

import sys
import sqlite3
from modules.myClass import *

DEBUG = False
#数据库文件路径
DB_FILE_PATH = '..\\data\\data.db'
#是否打印sql
SHOW_SQL = False

def init(table):
    if DEBUG:
        print('show_sql : {}'.format(SHOW_SQL))
    #如果存在数据库表，则删除表
    drop_table_test(table)
    #创建数据库表
    create_table_system(table)

def get_conn(path):
    '''获取到数据库的连接对象，参数为数据库文件的绝对路径'''
    try:
        conn = sqlite3.connect(path)
        if DEBUG:
            print '#'*5,'Connecting to',path,'...','#'*5
        return conn
    except IOError:
        print 'Error:can not read data'

def get_cursor(conn):
    '''获取数据库的游标对象，参数为数据库的连接对象'''
    try:
        return conn.cursor()
    except IOError:
        print 'Error in get_cursor()'

def close_all(conn, cu):
    '''关闭数据库游标对象和数据库连接对象'''
    if cu is not None:
        cu.close()
    if conn is not None:
        conn.close()

def drop_table(conn, table):
    '''如果表存在,则删除表'''
    if table is not None and table != '':
        sql = 'drop table if exists ' + table
        if SHOW_SQL:
            print('sql:[{}]'.format(sql))
        cu = get_cursor(conn)
        cu.execute(sql)
        conn.commit()
        if DEBUG:
            print('Delete tables [{}] successfully!'.format(table))
        close_all(conn,cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))

def drop_table_test(table):
    '''删除数据库表'''
    try:
        if DEBUG:
            print('Deleting tables...')
        conn = get_conn(DB_FILE_PATH)
        drop_table(conn, table)
    except IOError:
        print 'Delete table [{}] fail'.format(table)

def create_table(conn, sql,table):
    '''创建数据库表：table'''
    if sql is not None and sql != '':
        cu = get_cursor(conn)
        if SHOW_SQL:
            print('sql:[{}]'.format(sql))
        cu.execute(sql)
        conn.commit()
        if DEBUG:
            print('Create table [{}] successfully!'.format(table))
        conn.close()
    else:
        print('the [{}] is empty or equal None!'.format(sql))

def create_table_system(table):
    '''创建数据库表'''
    if DEBUG:
        print('Creating table...')
    create_table_sql = '''CREATE TABLE {} (
                          `id`      int(11)     NOT NULL,
                          `name`    char(20)  DEFAULT NULL,
                          `info`    char(500) DEFAULT NULL,
                           PRIMARY KEY (`id`)
                        )'''.format(table)
    conn = get_conn(DB_FILE_PATH)
    create_table(conn, create_table_sql,table)

def save(conn, sql, data):
    '''插入数据'''
    if sql is not None and sql != '':
        if data is not None:
            cu = get_cursor(conn)
            for d in data:
                if SHOW_SQL:
                    print('sql:[{}],values:[{}]'.format(sql, d))
                cu.execute(sql, d)
                conn.commit()
            close_all(conn, cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))
"""
def save_test():
    '''保存数据...'''
    if DEBUG:
        print('Saving data...')
    save_sql = '''INSERT INTO [{}] values (?, ?, ?, ?, ?, ?)'''.format(TABLE_NAME)
    data = [(1, 920048, 341372, 0, 8480, 41928),
            (2, 920080, 341340, 0, 8480, 41928),
            (3, 920080, 341340, 0, 8480, 41928)]
    conn = get_conn(DB_FILE_PATH)
    save(conn, save_sql, data)
"""
def insert_system(table,data):
    '''保存数据...'''
    if DEBUG:
        print('Saving data...')
    save_sql = '''INSERT INTO [{}] VALUES (? , ? , ? )'''.format(table)
    conn = get_conn(DB_FILE_PATH)
    save(conn, save_sql, data)

def fetchall(conn, sql):
    '''查询所有数据'''
    if sql is not None and sql != '':
        cu = get_cursor(conn)
        if SHOW_SQL:
            print('sql:[{}]'.format(sql))
        cu.execute(sql)
        r = cu.fetchall()
        if len(r) > 0:
            for e in range(len(r)):
                print(r[e])
    else:
        print('the [{}] is empty or equal None!'.format(sql)) 

def fetchone(conn, sql, data):
    '''查询一条数据'''
    if sql is not None and sql != '':
        if data is not None:
            #Do this instead
            d = (data,) 
            cu = get_cursor(conn)
            if SHOW_SQL:
                print('sql:[{}],values:[{}]'.format(sql, data))
            cu.execute(sql, d)
            r = cu.fetchall()
            if len(r) > 0:
                for e in range(len(r)):
                    print(r[e])
        else:
            if DEBUG:
                print('the [{}] equal None!'.format(data))
    else:
        print('the [{}] is empty or equal None!'.format(sql))

def fetchall_test(table):
    '''查询所有数据...'''
    if DEBUG:
        print('fetch all data...')
    fetchall_sql = '''SELECT * FROM [{}]'''.format(table)
    conn = get_conn(DB_FILE_PATH)
    fetchall(conn, fetchall_sql)
    conn.close()

def fetchone_test(table):
    '''查询一条数据...'''
    if DEBUG:
        print('fetch one data...')
    fetchone_sql = 'SELECT * FROM [{}] WHERE ID = ? '.format(table)
    data = 1
    conn = get_conn(DB_FILE_PATH)
    fetchone(conn, fetchone_sql, data)
    conn.close()

def getavg(table):
    '''求平均值'''
    if DEBUG:
        print 'getting avg ...'
    getavg_sql = 'select avg(used) from [{}]'.format(table)
    conn = get_conn(DB_FILE_PATH)
    cu = conn.execute(getavg_sql)
    conn.commit()
    r = cu.fetchall()
    if DEBUG:
        print '##### avg is :%.2f'%(r[0][0])
    close_all(conn,cu)

def DataInsert(module,table,data):
    #向数据库表中插入数据
    for case in switch(module):
        if case('system'):
            insert_system(table,data)
            break
        if case():
            print u"===>>>传入模块异常"
    
