import sqlite3 as sql
import hexdump
import os
import subprocess

def db_connect(dbname):
    #sqlite3 connections
    try:
        conn = sql.connect(dbname)
        cur = conn.cursor()
        return (conn, cur)
    except:
        return 'error in connecting'

def commit_and_close(conn_cur):
    conn_cur[0].commit()
    conn_cur[0].close()

def insert_image(tablename, row_details, dbname, dbcolumn, conn_cur):
    filepath = [ None for i in range(len(dbcolumn))] 
    for column, value in row_details.items():
        for i in range(len(dbcolumn)):
            if column == dbcolumn[i]:
                dump_value = subprocess.Popen("""hexdump -ve '1/1 "%%0.2X"' %s"""%value, shell=True, stdout=subprocess.PIPE, )
                dump_value= dump_value.communicate()[0]
                dump_value = "x'" + dump_value + "'" 
                row_details[column] = "%s"%dump_value

    query_column_details =', '.join(row_details.keys())
    query_value_details ='"'+'","' .join(row_details.values())+'"'
    query = "insert into spidy (%s) values(%s);"%(query_column_details,query_value_details)
    
    #now I need to perform insert operation
    conn_cur[1].execute(query)
       
    conn_cur[0].commit()

def retrive_image(self, db, tablename, pk_column, pk, image_column, imagename):  
  
    #retrive image as blob
    #query for execution 
    query = "select quote(%s) from %s where %s='%s' limit 1 offset 0;"%(image_column,tablename,pk_column,pk)   
    #command 
    command = ''' echo "%s" | sqlite3 '%s' | tr -d "X'" | xxd -r -p > %s ''' %(query,db,imagename)
    print command
    
    #execute command 
    os.system(command) 


if __name__=='__main__' :
    row_details = {"name":"yoman","img":"cheetah_chat.png","profile":"logo.png"}
    tablename="spidy"
    dbname = 'db'
    dbcolumn = ['img','profile']

    conn_cur = db_connect(dbname)
    #insert_image(tablename, row_details, dbname, dbcolumn, conn_cur)
    retrive_image(dbname, tablename, 'name', 'yoman', 'img', 'cheetah_chat.png', conn_cur)



