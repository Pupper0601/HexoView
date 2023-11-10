# -*- coding: utf-8 -*-
# @Author : Pupper
# @Email  : pupper.cheng@gmail.com
import json
import sqlite3
from loguru import logger


def join_sqlite():
    """
    连接数据库
    :return: 数据库对象、游标
    """
    conn = sqlite3.connect('./db.sqlite3')  # 连接数据库,如果不存在则自动创建
    cur = conn.cursor()  # 获取游标
    logger.info(f"数据库连接成功: {conn}")
    # 创建数据库
    create_hv_article = """create table IF NOT EXISTS `hv_article` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `address` 
    text);"""
    create_hv_user = """CREATE TABLE IF NOT EXISTS `hv_user` (
      `ip` varchar(60) NOT NULL,
      `id` int(11) NOT NULL primary key,
      `view1` int(11) NOT NULL DEFAULT '0',
      `view2` int(11) NOT NULL DEFAULT '0',
      `view3` int(11) NOT NULL DEFAULT '0',
      `view4` int(11) NOT NULL DEFAULT '0',
      `view5` int(11) NOT NULL DEFAULT '0',
      `view6` int(11) NOT NULL DEFAULT '0',
      `view7` int(11) NOT NULL DEFAULT '0',
      `view8` int(11) NOT NULL DEFAULT '0',
      `view9` int(11) NOT NULL DEFAULT '0'
    );"""
    # 执行 sql 语言
    cur.execute(create_hv_article)
    cur.execute(create_hv_user)
    return conn, cur


class SqliteHandle:
    def __init__(self):
        # 连接数据库
        self.conn, self.cur = join_sqlite()

    @staticmethod
    def dict_factory(cursor, row):
        # 将游标获取的数据处理成字典返回
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def find_article(self, site, article_id=False):
        """
        查询文章
        :param site: 文章地址
        :param article_id: 文章 id
        :return:
        """
        find_sql = f'''select * from hv_article where address = '{site}';'''
        self.cur.execute(find_sql)
        article_data = self.cur.fetchall()
        if len(article_data) != 0:
            if article_id:
                return article_data[0][0]
            else:
                return article_data
        else:
            insert_sql = f'''insert into hv_article(address) values ('{site}');'''
            self.cur.execute(insert_sql)
            self.conn.commit()
            find_sql = f'''select * from hv_article where address = '{site}';'''
            self.cur.execute(find_sql)
            article_data = self.cur.fetchall()
            if article_data != ():
                if article_id:
                    return article_data[0][0]
                else:
                    return article_data

    def result_view(self, article_id, ip):
        """

        :param article_id: 文章 id
        :param ip:ip 地址
        :return:
        """
        find_sql = f'''select CAST(sum(view1) AS SIGNED ) as view1,CAST(sum(view2) AS SIGNED ) as view2,
                    CAST(sum(view3) AS SIGNED ) as view3,CAST(sum(view4) AS SIGNED ) as view4,
                    CAST(sum(view5) AS SIGNED ) as view5,CAST(sum(view6) AS SIGNED ) as view6,
                    CAST(sum(view7) AS SIGNED ) as view7,CAST(sum(view8) AS SIGNED ) as view8,
                    CAST(sum(view9) AS SIGNED ) as view9 from hv_user
                    where id = {article_id};'''
        self.cur.execute(find_sql)
        view_data = self.cur.fetchall()
        desc = self.cur.description
        result_dict = {}
        if view_data[0][0] is None:
            for i in range(len(view_data[0])):
                result_dict[desc[i][0]] = 0
        else:
            for i in range(len(view_data[0])):
                result_dict[desc[i][0]] = view_data[0][i]
            find_view_sql = f'''select * from hv_user where id = {article_id} and ip = '{ip}';'''
            self.cur.execute(find_view_sql)
            user_view = self.cur.fetchall()
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
            self.cur.execute(insert_sql)
            self.conn.commit()
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
        self.cur.execute(find_view_sql)
        find_view = self.cur.fetchall()

        if find_view != ():
            insert_view_sql = f'''delete from hv_user where id = {article_id} and ip = '{view_data["ip"]}';'''
            self.cur.execute(insert_view_sql)
            self.conn.commit()

        # # 插入 hexo_user 数据
        insert_view_sql = f'''insert into hv_user(ip, id, {view_data["view"]})
                        values('{view_data["ip"]}','{article_id}',1);'''
        self.cur.execute(insert_view_sql)
        self.conn.commit()

        return self.result_view(article_id, view_data["ip"])


if __name__ == '__main__':
    sh = SqliteHandle()
    # a = sh.find_view({"address": "https://pupper.cn/posts/b99aaa.html", "ip": "127.0.0.12"})
    a = sh.insert_view({"address": "https://pupper.cn/posts/b99bbb.html", "ip": "127.0.0.33", "view": "view3"})
    print(a)
