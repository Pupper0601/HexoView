# -*- coding: utf-8 -*-
# @Author : Pupper
# @Email  : pupper.cheng@gmail.com
import json
import sqlite3


class SqliteHandle:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.conn.row_factory = SqliteHandle.dict_factory
        self.cs = self.conn.cursor()
        self.__create_table()

    @staticmethod
    def dict_factory(cursor, row):
        # 将游标获取的数据处理成字典返回
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __create_table(self):
        find_hexo_article = "select * from sqlite_master where tbl_name = 'hexo_article';"
        if not self.cs.execute(find_hexo_article).fetchall():
            hexo_article = """CREATE TABLE hexo_article(
                id integer default 0,
                address varchar(255) primary key);"""
            self.cs.execute(hexo_article)

        find_hexo_user = "select * from sqlite_master where tbl_name = 'hexo_user';"
        if not self.cs.execute(find_hexo_user).fetchall():
            hexo_user = """CREATE TABLE hexo_user(
                ip varchar(60) not null,
                id int not null,
                view1 int not null default 0,
                view2 int not null default 0,
                view3 int not null default 0,
                view4 int not null default 0,
                view5 int not null default 0,
                view6 int not null default 0,
                view7 int not null default 0,
                view8 int not null default 0,
                view9 int not null default 0);"""
            self.cs.execute(hexo_user)

    def find_view(self, view_data):
        if type(view_data) != dict:
            view_data = json.loads(view_data)

        find_sql = f'''select sum(view1) as v1,sum(view2) as v2,sum(view3) as v3,sum(view4) as v4,sum(view5) as v5,
            sum(view6) as v6,sum(view7) as v7,sum(view8) as v8,sum(view9) as v9 from hexo_user 
            where id = (select id from hexo_article where address = '{view_data["address"]}');'''
        view = self.cs.execute(find_sql).fetchall()
        if view[0]["v1"] is None:
            return {"v1": 0, "v2": 0, "v3": 0, "v4": 1, "v5": 0, "v6": 0, "v7": 0, "v8": 0, "v9": 0}
        return view[0]

    def insert_view(self, view_data):
        """
        插入数据库
        :param view_data: 插入数据 字典
        :return:
        """
        if type(view_data) != dict:
            view_data = json.loads(view_data)

        find_article_sql = f'''select * from hexo_article where address = '{view_data["address"]}';'''
        article_data = self.cs.execute(find_article_sql).fetchall()
        if not article_data:
            # 写入 hexo_article 表
            insert_sql = f'''insert into hexo_article(id, address) 
                values ((select ifnull(Max(id), 0) +1 from hexo_article),'{view_data["address"]}')'''
            self.cs.execute(insert_sql)
            self.conn.commit()
        # 插入成功后重修查询
        view_id = self.cs.execute(find_article_sql).fetchall()[0]["id"]

        find_view_sql = f'''select * from hexo_user where id = {view_id} and ip = '{view_data["ip"]}';'''
        find_view = self.cs.execute(find_view_sql).fetchall()
        # 删除 hexo_user 数据
        if find_view:
            delete_sql = f'''delete from hexo_user where id = {view_id} and ip = '{view_data["ip"]}';'''
            self.cs.execute(delete_sql)
            self.conn.commit()
        # 插入 hexo_user 数据
        insert_view_sql = f'''insert into hexo_user(ip, id, {view_data["view"]})
            values('{view_data["ip"]}','{view_id}',1);'''
        self.cs.execute(insert_view_sql)
        self.conn.commit()
        return self.find_view({"address": view_data["address"]})


if __name__ == '__main__':
    sh = SqliteHandle()
    # sh.find_view({"address": "https://pupper.cn/posts/b9926ccb.html"})
    a = sh.insert_view({"address": "https://pupper.cn/posts/b3426ccb.html", "ip": "127.0.0.12", "view": "view4"})
    print(a)
