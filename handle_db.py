# -*- coding: utf-8 -*-
# @Author : Pupper
# @Email  : pupper.cheng@gmail.com
import json
import os

import pymysql
import configparser

from dotenv import load_dotenv

load_dotenv(verbose=True)

conf = configparser.ConfigParser()
conn = pymysql.connect(host=os.getenv("VIEW_SQL_HOST"),  # host属性
                       user=os.getenv("VIEW_SQL_USER"),  # 用户名
                       password=os.getenv("VIEW_SQL_PASSWORD"),  # 此处填登录数据库的密码
                       db=os.getenv("VIEW_SQL_DB"),  # 数据库名
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

    def result_view(self, article_id, ip):
        find_sql = f'''select CAST(sum(view1) AS SIGNED ) as view1,CAST(sum(view2) AS SIGNED ) as view2,
                    CAST(sum(view3) AS SIGNED ) as view3,CAST(sum(view4) AS SIGNED ) as view4,
                    CAST(sum(view5) AS SIGNED ) as view5,CAST(sum(view6) AS SIGNED ) as view6,
                    CAST(sum(view7) AS SIGNED ) as view7,CAST(sum(view8) AS SIGNED ) as view8,
                    CAST(sum(view9) AS SIGNED ) as view9 from hv_user
                    where id = {article_id};'''
        self.db.execute(find_sql)
        view_data = self.db.fetchall()
        desc = self.db.description
        result_dict = {}
        if view_data[0][0] is None:
            for i in range(len(view_data[0])):
                result_dict[desc[i][0]] = 0
        else:
            for i in range(len(view_data[0])):
                result_dict[desc[i][0]] = view_data[0][i]
            find_view_sql = f'''select * from hv_user where id = {article_id} and ip = '{ip}';'''
            self.db.execute(find_view_sql)
            user_view = self.db.fetchall()
            if user_view != ():
                for i in range(2, len(user_view[0])):
                    if user_view[0][i] == 1:
                        result_dict["my_view"] = i-1
        return result_dict

    def find_view(self, view_data):
        if type(view_data) != dict:
            view_data = json.loads(view_data)

        article_data = self.find_article(view_data["address"])
        if article_data == ():
            insert_sql = f'''insert into hv_article(address) values ('{view_data["address"]}');'''
            self.db.execute(insert_sql)
            conn.commit()
            return {"view1": 0, "view2": 0, "view3": 0, "view4": 0, "view5": 0, "view6": 0, "view7": 0, "view8": 0,
                    "view9": 0}

        return self.result_view(article_data[0][0], view_data["ip"])

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

        return self.result_view(article_id, view_data["ip"])


if __name__ == '__main__':
    sh = SqliteHandle()
    # a = sh.find_view({"address": "https://pupper.cn/posts/b99aaa.html", "ip": "127.0.0.12"})
    a = sh.insert_view({"address": "https://pupper.cn/posts/b99aaa.html", "ip": "127.0.0.32", "view": "view5"})
    print(a)
