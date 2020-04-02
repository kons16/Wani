"""
WactiveRecordでDB操作
"""
import sqlite3
import time
from datetime import datetime, timedelta, timezone


class WactiveRecord:
    def __init__(self, table_name):
        self.table = table_name
        self.conn = sqlite3.connect("db/development.sqlite3")
        self.c = self.conn.cursor()

    def create(self, data):
        """ テーブルにレコードを追加 """
        insert = "INSERT INTO {} VALUES ".format(self.table)
        s = self.__TupleMake(data)
        insert += s
        self.c.execute(insert)
        self.conn.commit()
        self.conn.close()

    def update(self):
        """ テーブルのレコードをアップデート """

    def all(self):
        """ 全レコードを配列として取得 """
        self.c.execute('SELECT * FROM %s' % self.table)
        all_result = self.c.fetchall()
        self.c.close()
        return all_result

    def first(self):
        """ idが一番小さいレコードを取得 """

    def last(self):
        """ idが一番大きいレコードを取得 """

    def find(self, id):
        """ idのレコードを取得 """

    def find_by(self, column_name, search_word):
        """ column_nameのsearch_wordの中で最初にヒットした1件のレコードを取得 """

    def where(self, column_name, search_word):
        """ 該当するレコード全件を取得 """

    def __CreateTimeStamp(self):
        """ タイムスタンプの作成 """
        now = time.time()
        jst = timezone(timedelta(hours=+9), 'JST')
        loc = datetime.fromtimestamp(now, jst).timestamp()
        return loc

    def __TupleMake(self, data):
        """ リストのデータを()に変換する """
        # time = self.__CreateTimeStamp()
        s = "("
        for i, item in enumerate(data):
            if i == 0:
                s += "'{}'".format(item)
            else:
                s += ", '{}'".format(item)
        s += ")"
        return s
