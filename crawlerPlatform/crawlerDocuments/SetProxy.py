import pymysql


class Ss():

    def getOne(self, ty):
        db = pymysql.connect("192.168.1.68", "root", "123456", "mytest", charset='utf8')
        sql = "select * from proxy where " + ty + "='1' and http_='http' ORDER BY RAND() limit 1"
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        prox = cursor.fetchone()
        cursor.close()
        db.commit()
        db.close()
        return prox

    def getOnes(self, ty):
        db = pymysql.connect("192.168.1.68", "root", "123456", "mytest", charset='utf8')
        sql = "select * from proxy where " + ty + "=1 and http_='https' ORDER BY RAND() limit 1"
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        prox = cursor.fetchone()
        cursor.close()
        db.commit()
        db.close()
        return prox

    def setFalse(self, ip,port, ty):
        db = pymysql.connect("192.168.1.68", "root", "123456", "mytest", charset='utf8')
        sql = "update proxy set " + ty + "='0' where ip='" + ip+"' and port='"+port+"'"
        print("进入修改proxy数据库")
        print(sql)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        print("处理完成")


if __name__ == '__main__':
    s = Ss()
    print(s.getOne('gxst'))
