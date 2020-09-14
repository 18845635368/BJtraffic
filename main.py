import pandas as pd
import numpy as np
import pymysql

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

if __name__ == '__main__':
    FILEPATH = 'rawdata.xlsx'
    read_data_xlsxTodb()