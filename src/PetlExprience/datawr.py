#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, create_engine
import psycopg2
import petl as etl

conn = None
engine = None


def getEngine ():
    global engine
    if engine is None:
        # engine = create_engine('mysql+mysqldb://root@localhost:3306/blog?charset=utf8')
        # engine = create_engine('sqlite:///:memory:', echo=True)
        engine = create_engine('postgresql://test:test@127.0.0.1:5432/test', echo=True)
        # print (engine)
        # print (engine.table_names())
    return conn


def getConnect ():
    global conn
    if conn is None:
        conn = psycopg2.connect(database="test", user="test", password="test", host="127.0.0.1", port="5432")
    return conn


def createTabele():
    conn = getConnect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''create table user_table(
                id integer not null primary key,
                name varchar(32) not null,
                password varchar(32) not null,
                singal varchar(128)
            )'''
        )
        conn.commit()
    except Exception as e:
        print (e.message)


def freeConnection():
    global conn
    if conn is None:
        return
    conn.close()
    conn = None


def insertOperate():
    print ('insert records into table')
    conn = getConnect()
    cursor = conn.cursor()
    cursor.execute("insert into user_table(id,name,password,singal)\
values(1,'name','pd','s1')")
    conn.commit()
    print ('insert records into table successfully')


def insertOperate2():
    print ('insert records into table')
    conn = getConnect()
    cursor = conn.cursor()
    # cursor.execute("insert into user_table(id,name,password,singal) values(%s,%s,%s,%s)", (5, "m5", "p5", "s5"))


    data= [(6, "m6", "p6", "s6"),
           (7, "m7", "p7", "s7")]
    cursor.executemany("insert into user_table(id,name,password,singal) values(%s,%s,%s,%s)",
                  data)

    conn.commit()


def selectOperate():
    print ("query table")
    conn = getConnect()
    cursor = conn.cursor()
    cursor.execute("select id,name,password,singal from public.user_table where id>2")
    rows = cursor.fetchall()
    for row in rows:
        print( 'id=', row[0], ',name=', row[1], ',pwd=', row[2], ',singal=', row[3], '\n')


def updateOperate():
    conn = getConnect()
    cursor = conn.cursor()
    cursor.execute("update user_table set name='update ...' where id=2")
    conn.commit()
    print ("Total records of rows updated :", cursor.rowcount)


def deleteOperate():
    conn = getConnect()
    cursor = conn.cursor()
    print ('begin delete')
    cursor.execute("delete from user_table where id=2")
    conn.commit()
    print ('end delete')
    print ("Total records of rows deleted :", cursor.rowcount)

def isTableExists(tablename):
    conn = getConnect()
    cursor = conn.cursor()
    try:
        cursor.execute("select *  from {}".format(tablename))
        conn.commit()
        return True
    except Exception as e:
        return False



def petlQeury():
    conn = getConnect()
    cursor = conn.cursor()

    table = etl.fromdb(conn, 'SELECT * FROM test_table')
    print (etl.lookall(table))

    # No handlers could be found for logger "petl.io.db"
    # table = etl.fromdb(cursor, 'SELECT * FROM test_table')
    # print (table)


def petlInsert():
    conn = getConnect()
    cursor = conn.cursor()
    engine  = getEngine()
    tablename = "test_table"
    create = False
    if isTableExists(tablename):
        create = False
    else:
        create = True
    table = [
        ["id", "name", "password", "singal"],
        [1, "m6", "p6", "s6"],
        [2, "m6", "p6", "s6"],
        [3, "m6", "p6", "s6"],
        [4, "m6", "p6", "s6"],
        [5, "m6", "p6", "s6"]]

    """
        Note that the database table will be truncated

        If create=True this function will attempt to automatically create a database table before loading the data.
        This functionality requires SQLAlchemy to be installed.

        dbo : database object
            DB-API 2.0 connection, callable returning a DB-API 2.0 cursor, or
            SQLAlchemy connection, engine or session

    """

    # etl.todb(table, conn, tablename=tablename, create=create)
    # etl.todb(table, cursor, tablename=tablename, create=create)

    # etl.todb(table, engine, tablename=tablename)

    ""

    table2 = [
        ["id", "name", "password", "singal"],
        [11, "m6", "p6", "s6"],
        [12, "m6", "p6", "s6"],
        [13, "m6", "p6", "s6"],
        [14, "m6", "p6", "s6"],
        [15, "m6", "p6", "s6"]]
    etl.appenddb(table2, engine,tablename=tablename)
    table3 = [
        ["id", "name", "password", "singal"],
        [111, "m6", "p6", "s6"],
        [121, "m6", "p6", "s6"],
        [131, "m6", "p6", "s6"],
        [141, "m6", "p6", "s6"],
        [151, "m6", "p6", "s6"]]
    etl.appenddb(table3, engine,tablename=tablename)

if __name__ == "__main__":
    # createTabele()
    # insertOperate()
    # insertOperate2()
    # selectOperate()
    petlInsert()
    petlQeury()

    freeConnection()
    pass