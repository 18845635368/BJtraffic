import pandas as pd
import numpy as np
import pymysql
import netprocess

def read_data_xlsxTodb(PATH):
    data = pd.read_excel(PATH)
    data1 = np.array(data)
    i = 0
    current = -1
    laststation = -1
    name = []
    stationname = []
    namemap = {'?': -1}
    edge = []
    for temp in data1:
        if temp[1] != 0:
            continue
        else:
            if temp[0] == current:
                current = temp[0]
                if temp[3] not in name:
                    name.append(temp[3])
                    namemap[temp[3]] = i
                    stationname.append([i, temp[3]])
                    edge.append([laststation, i])
                    laststation = i
                    i = i + 1
                else:
                    edge.append([laststation, namemap[temp[3]]])
                    laststation = namemap[temp[3]]
            else:
                current = temp[0]
                if temp[3] not in name:
                    name.append(temp[3])
                    namemap[temp[3]] = i
                    stationname.append([i, temp[3]])
                    laststation = i
                    i = i + 1
                else:
                    laststation = namemap[temp[3]]
    print("已读取表格数据")
    edges = []
    for i in edge:
        if i not in edges:
            if [i[1], i[0]] not in edges:
                edges.append(i)
    print("已去除重复数据,正在写入数据库...")
    mysql_server = 'localhost'
    name = 'root'
    password = '123p123p'
    mysql_db = 'BJtraffic'
    db = pymysql.connect(mysql_server, name, password, mysql_db)
    j = -1
    for item in edges:
        cursor = db.cursor()
        j = j + 1
        print(j)
        sql = "insert into edges (id,start,end) values(%d,%d,%d)" % (j, item[0], item[1])
        cursor.execute(sql)
        db.commit()
    print ("已写入数据库。")

#   初始化最短路径表
def table_ini():
    #   一开始先将最短路径表初始化一下
    for i in range(1300):
        for j in range(1300):
            if i == j:
                shortest_path[i][j] = 0
            else:
                shortest_path[i][j] = 10000

#   用于将数据库读取出来的数据转化为stations
#   @param:data1:raw data from stations
#          data2:raw data from edges
#          stations:stations
def data2stations(data1, data2,stations,shortest_path):

    for row in data1:
        stations.append([row[1], []])

    for row in data2:
        s = row[1]
        e = row[2]
        stations[s][1].append(e)
        stations[e][1].append(s)
        shortest_path[s][e] = 1
        shortest_path[e][s] = 1
    return stations,shortest_path

#   初始化全部数据
#   @return :节点信息[[name，[相连的边的另一端]]..]
#             data2:边表  [[id,start,end]...]
def ini(stations,shortest_path):
    # 开始的时候初始化最短路径表
    table_ini()
    #   连接database
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password = '123p123p',
        database= 'BJtraffic',
        charset="utf8")

    #   得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    #   得到一个可以执行SQL语句并且将结果作为字典返回的游标
    #   cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    #   定义要执行的SQL语句
    sql1 = "select id,name from stationname"
    sql2 = "select id,start,end from edges"

    #   执行SQL语句
    #   data1存放从节点表读出来的数据，data2存放的是从节点表读出来的数据
    cursor.execute(sql1)
    data1 = cursor.fetchall()
    cursor.execute(sql2)
    data2 = cursor.fetchall()
    cursor.close()

    stations,shortest_path=data2stations(data1,data2,stations,shortest_path)

    return stations,shortest_path

def writestations(stations):
    mysql_server = 'localhost'
    name = 'root'
    password = '123p123p'
    mysql_db = 'BJtraffic'
    db = pymysql.connect(mysql_server, name, password, mysql_db)
    for item in stations:
        cursor = db.cursor()

        sql = "update stationname set degree=%d,cluster=%d,coreness=%d where name = '%s'" % (item[2], item[3], item[4],item[0])
        print(sql)
        cursor.execute(sql)
        db.commit()
    print ("已写入数据库。")

def writeshortpath(data):
    size=len(data)
    mysql_server = 'localhost'
    name = 'root'
    password = '123p123p'
    mysql_db = 'BJtraffic'
    db = pymysql.connect(mysql_server, name, password, mysql_db)
    for i in range(1,size):
        for j in range(i):
            cursor = db.cursor()

            sql = "insert into shortestpath (start,end,value ) values (%d,%d,%d)" % (i,j,data[i][j])
            print(sql)
            cursor.execute(sql)
            db.commit()


#   读取数据库中的数据
#   @params:tablename:string,
#           cols:string array eg.["id","name"...]/['*']
#   @return:raw data from database
def readdb(tablename,cols):
    mysql_server = 'localhost'
    name = 'root'
    password = '123p123p'
    mysql_db = 'BJtraffic'
    db = pymysql.connect(mysql_server, name, password, mysql_db)
    cursor = db.cursor()
    col=""
    if cols[0]=='*':
        col=cols[0]
    else:
        for i in cols:
            col=col+i+','
        col=col[:-1]
    sql = "select %s from %s" % (col,tablename,)
    cursor.execute(sql)
    data=cursor.fetchall()
    db.commit()
    cursor.close()

    return data


if __name__ == '__main__':
    FILEPATH = 'rawdata.xlsx'

    #read_data_xlsxTodb()

    #stations存放的是处理过后的节点数据，0 for name，1 for 相连接的节点 ，2 for 度数， 3 for cluster coefficient, 4 for coreness
    stations = []
    shortest_path = np.zeros((1300, 1300))

    stations,shortest_path=ini(stations,shortest_path)
    stations,_,_=netprocess.get_degree(stations)
    stations=netprocess.calculateCorness(stations)
    stations,shortest_path=netprocess.findshortestpath(stations,shortest_path)
    writestations(stations)
    writeshortpath(shortest_path)

