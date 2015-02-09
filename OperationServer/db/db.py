#!/usr/bin/env python
# coding=utf-8

import MySQLdb

con = MySQLdb.connect(host="localhost", user="root", passwd="123123", db="qiniustream", port=3306, charset="utf8")

cur = con.cursor()

"""
mysql> desc stream;
+---------------+-------------+------+-----+---------+----------------+
| Field         | Type        | Null | Key | Default | Extra          |
+---------------+-------------+------+-----+---------+----------------+
| id            | int(2)      | NO   | PRI | NULL    | auto_increment |
| classid       | int(2)      | YES  |     | NULL    |                |
| direction     | varchar(10) | YES  |     | NULL    |                |
| streamcontent | text        | YES  |     | NULL    |                |
+---------------+-------------+------+-----+---------+----------------+

"""

#insert row into table.
def insert_stream(classid, direction, stream_content):
    sql_insert = "insert into stream (classid, direction, streamcontent) values (%s, %s, %s)"
    cur.execute(sql_insert, (classid, direction, stream_content))
    con.commit()

#select the row from table
def select_row(classid):
    try:
        sql_select = "select * from stream where classid=%s"
        cur.execute(sql_select,(classid))
        result = cur.fetchall()
        return result
    except:
        return False
