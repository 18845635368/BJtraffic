import copy

#   用于计算平均度数,统计各种度数的节点
#   @params:stations:站点信息表
#   @return:avg_degree:图的平均度数
#           degree_distribution:图的度数分布[1,2,3...]
def get_degree(stations):
    print("开始计算各个节点的度数，并且统计各种度数的节点的个数")
    sum_degree = 0
    degree_distribution = [0]
    for item in stations:
        t = len(item[1])
        item.append(t)
        #   这是给coreness,cluster coefficient准备的空位
        item.append(0)
        item.append(0)

        sum_degree = sum_degree + t
        while t > len(degree_distribution) - 1:
            degree_distribution.append(0)
        degree_distribution[t] = degree_distribution[t] + 1
    avg_degree = sum_degree / len(stations)
    return stations,avg_degree, degree_distribution


#   用来算阶乘的
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)


#   用于生成所有点之间的最短路径
#   @params:stations,shortest_path
#   @return:station,shortest_path
def findshortestpath(stations,shortest_path):
    print("开始寻找所有节点之间的最短路径")
    s_size = len(stations)
    for i in range(s_size):
        for j in range(s_size):
            if i == j:
                continue
            for k in range(s_size):
                if k == j or k == i:
                    continue
                if shortest_path[i][j] == 1:
                    break
                if shortest_path[i][j] < (shortest_path[i][k] + shortest_path[j][k]) and shortest_path[i][
                    k] != 10000 and shortest_path[j][k] != 10000:
                    shortest_path[i][j] = shortest_path[i][k] + shortest_path[j][k]
                    shortest_path[j][i] = shortest_path[i][k] + shortest_path[j][k]
            print("%d和%d的最短路径查找完毕" % (i, j))
    return stations,shortest_path


#   计算平均路径
#   @return 平均路径长度
def getavgpath(stations,shortest_path):
    s_size = len(stations)
    sum_pathlen = 0
    sum_path = factorial(s_size) / (2 * factorial(s_size - 2))
    for i in range(s_size):
        for j in range(i + 1, s_size):
            sum_pathlen = sum_pathlen + shortest_path[i][j]
    return sum_pathlen / sum_path


#   用于计算corness
#   @return stations：更新了cornness
def calculateCorness(stations):
    print("开始计算的corness.")
    stations_copy = copy.deepcopy(stations)
    k = 1
    s_size = len(stations_copy)
    total_out = 0
    while 1:
        for i in range(s_size):
            if stations[i][4] == 0 and k >= stations_copy[i][2] :
                stations[i][4] = k
                total_out = total_out + 1
                for j in stations_copy[i][1]:
                    stations_copy[j][2] = stations_copy[j][2] - 1
        k = k + 1
        if total_out==s_size:
            break
    return stations

#   用于计算一个的节点的cluster coefficient
def calculateclustercoefficient(node_id):
    print("开始计算%d的clustercoefficient" % node_id)
    connect = stations[node_id][1]
    connect_size = len(connect)
    if connect_size < 2:
        return 0
    triplet_all = factorial(connect_size) / (factorial(2) * factorial(connect_size - 2))
    triplet_closed = 0
    #   method1
    for i in range(0, connect_size - 1):
        for j in range(i + 1, connect_size):
            lista = stations[i][1]
            len_lista = len(lista)
            for k in range(len_lista):
                if lista[k] == connect[j]:
                    triplet_closed = triplet_closed + 1
    #   method2
    # for i in range(0, connect_size - 1):
    #     for j in range(i + 1, connect_size):
    #         if shortest_path[connect[i]][connect[j]]==1:
    #             triplet_closed = triplet_closed + 1

    return triplet_closed / triplet_all


#   计算平均的cluster coefficient finished
def getavgcc():
    s_size = len(stations)
    sum_cc = 0
    for item in range(s_size):
        sum_cc = sum_cc + calculateclustercoefficient(item)
    return sum_cc / s_size


#   随机攻击任何节点，切断任何与其相连的边
def attackrandomly():
    print()


#   有意的攻击，可以攻击度数大的，也可以攻击cluster coefficient大的
def attackintendly():
    print()


# if __name__ == '__main__':
#     data1, data2 = ini()
#     data2stations(data1, data2)
#     get_degree()
#     # stations[0][1].append(2)
#     # stations[2][1].append(0)
#     print(stations)
#     # for i in range(10):
#     #     print(calculateclustercoefficient(i))
#     # print(getavgcc())
#     findshortestpath()
#     #calculateCorness()
#     print(stations)

# print('总节点数为%d' % len(stations))
# print('平均度数为%f' % float(sum_degree / len(stations)))
# print('输出分布程度列表')
# print(degree_distribution)