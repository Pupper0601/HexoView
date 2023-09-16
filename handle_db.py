# -*- coding: utf-8 -*-
# @Author : Pupper
# @Email  : pupper.cheng@gmail.com
import json
import pymysql
import configparser

conf = configparser.ConfigParser()
conf.read("config.ini", encoding="utf8")
conn = pymysql.connect(host=conf["mysql"]["HOST"],  # host属性
                       user=conf["mysql"]["USER"],  # 用户名
                       password=conf["mysql"]["PASSWORD"],  # 此处填登录数据库的密码
                       db=conf["mysql"]["DB"],  # 数据库名
                       charset="utf8")


class SqliteHandle:
    def __init__(self):
        # 创建游标
        conn.row_factory = SqliteHandle.dict_factory
        self.db = conn.cursor()

    @staticmethod
    def dict_factory(cursor, row):
        # 将游标获取的数据处理成字典返回
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def find_article(self, address, article_id=False):
        find_sql = f'''select * from hv_article where address = '{address}';'''
        self.db.execute(find_sql)
        article_data = self.db.fetchall()
        if article_data != ():
            if article_id:
                return article_data[0][0]
            else:
                return article_data
        else:
            insert_sql = f'''insert into hv_article(address) values ('{address}');'''
            self.db.execute(insert_sql)
            conn.commit()
            find_sql = f'''select * from hv_article where address = '{address}';'''
            self.db.execute(find_sql)
            article_data = self.db.fetchall()
            if article_data != ():
                if article_id:
                    return article_data[0][0]
                else:
                    return article_data


    def result_view(self, article_id):
        find_sql = f'''select CAST(sum(view1) AS SIGNED ) as v1,CAST(sum(view2) AS SIGNED ) as v2,
                    CAST(sum(view3) AS SIGNED ) as v3,CAST(sum(view4) AS SIGNED ) as v4,
                    CAST(sum(view5) AS SIGNED ) as v5,CAST(sum(view6) AS SIGNED ) as v6,
                    CAST(sum(view7) AS SIGNED ) as v7,CAST(sum(view8) AS SIGNED ) as v8,
                    CAST(sum(view9) AS SIGNED ) as v9 from hv_user
                    where id = {article_id};'''
        self.db.execute(find_sql)
        view_data = self.db.fetchall()
        desc = self.db.description
        result_dict = {}
        for i in range(len(view_data[0])):
            if view_data[0][i] is None:
                result_dict[desc[i][0]] = 0
            else:
                result_dict[desc[i][0]] = view_data[0][i]
        return result_dict

    def find_view(self, view_data):
        if type(view_data) != dict:
            view_data = json.loads(view_data)

        article_data = self.find_article(view_data["address"])

        if article_data == ():
            insert_sql = f'''insert into hv_article(address) values ('{view_data["address"]}');'''
            self.db.execute(insert_sql)
            conn.commit()
            return {"v1": 0, "v2": 0, "v3": 0, "v4": 0, "v5": 0, "v6": 0, "v7": 0, "v8": 0, "v9": 0}

        return self.result_view(article_data[0][0])

    def insert_view(self, view_data):
        """
        插入数据库
        :param view_data: 插入数据 字典
        :return:
        """
        if type(view_data) != dict:
            view_data = json.loads(view_data)

        article_id = self.find_article(view_data["address"], article_id=True)

        find_view_sql = f'''select * from hv_user where id = {article_id} and ip = '{view_data["ip"]}';'''
        self.db.execute(find_view_sql)
        find_view = self.db.fetchall()

        if find_view != ():
            insert_view_sql = f'''delete from hv_user where id = {article_id} and ip = '{view_data["ip"]}';'''
            self.db.execute(insert_view_sql)
            conn.commit()

        # # 插入 hexo_user 数据
        insert_view_sql = f'''insert into hv_user(ip, id, {view_data["view"]})
                        values('{view_data["ip"]}','{article_id}',1);'''
        self.db.execute(insert_view_sql)
        conn.commit()

        return self.result_view(article_id)


if __name__ == '__main__':
    sh = SqliteHandle()
    a = sh.find_view({"address": "https://pupper.cn/posts/b9926ccb.html"})
    # a = sh.insert_view({"address": "https://pupper.cn/posts/b99aaa.html", "ip": "127.0.0.12", "view": "view4"})
    print(a)
