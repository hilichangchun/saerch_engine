import pymysql
import time

connection = pymysql.connect("dbforedinburgh.cqpftfdbw3kd.eu-west-2.rds.amazonaws.com", "admin", "ttds2020", "TTDS_onlineCrawler")
# connection = pymysql.connect("127.0.0.1", "root", "", "ttds")


# target是一个list
# fetchWordPosition和fetchKeywordValue函数里面存的是word[String格式] -> target = ['tifanaire', 'chelly']
# fetchIDAndDate存的是ID[数字] -> target = [1,2,3]
# 类似上面的格式传进去就没问题，我测试过了
# 现在只fetchIDAndDate这个函数能用，剩下两个要等黄宸宇那边更新

def fetchWordPosition(target):
    # 取wordPosition中内容并存为字典
    target = list(target)
    result={}
    select_str = 'SELECT WORD, ID, POSITION FROM `wordPosition` WHERE WORD in (%s)' % ','.join(['%s'] * len(target))
    with connection.cursor() as cursor:
        for i in target:
            result[i]={}
        cursor.execute(select_str, target)
        sulin = cursor.fetchall()
        for k in sulin:
            tempList = k[2].split(",")
            tempList = list(map(int, tempList))
            result[k[0]][k[1]]=tempList
    return result

def fetchKeywordValue(target):
    # 取TFIDF / BM25的内容存入字典
    target = list(target)
    result={}
    select_str = 'SELECT WORD, ID, TFIDF, BM25 FROM `keywordValue` where WORD in (%s)' % ','.join(['%s'] * len(target))
    with connection.cursor() as cursor:
        for i in target:
            result[i]={}
        cursor.execute(select_str, target)
        sulin = cursor.fetchall()
        for k in sulin:
            temp = []
            temp.append(k[2])
            temp.append(k[3])
            result[k[0]][k[1]]=tuple(temp)
    return result

def fetchIDAndDate(target):
    # 取 ID和DATE内容存进字典
    target = list(target)
    select_str = 'SELECT ID, DATE FROM `docIDTime` where ID in (%s)' % ','.join(['%s'] * len(target))
    # print("ID_TIME")
    with connection.cursor() as cursor:
        cursor.execute(select_str, target)
        sulin = dict(cursor.fetchall())
        # print(sulin)
    return sulin