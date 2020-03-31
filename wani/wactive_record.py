"""
WactiveRecordでDB操作
"""
import sqlite3


class WactiveRecord:
    def __init__(self, table_name):
        self.model = table_name
        self.conn = sqlite3.connect("db/development.sqlite3")
        self.c = self.conn.cursor()

    def create(self):
        """ テーブルにレコードを追加 """
        self.c.executescript("INSERT INTO %s VALUES (%s)" % (self.model, ))
        self.c.commit()
        self.c.close()

    def update(self):
        """ テーブルのレコードをアップデート """

    def all(self):
        """ 全レコードを配列として取得 """
        self.c.executescript("SELECT * FROM (%s)" % self.model)
        return self.c.fetchall()

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
