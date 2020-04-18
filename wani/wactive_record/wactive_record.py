"""
WactiveRecordでDB操作

・WactiveRecordクラス

・Persistanceクラス
モデルから得たレコードが持つ処理
    - update
"""
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from typing import List


class WactiveRecord:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.conn = sqlite3.connect("db/development.sqlite3")

    def create(self, data: List):
        """ テーブルにレコードを追加 """
        insert = "INSERT INTO {} VALUES ".format(self.table_name)
        s = self.__TupleMake(data)
        insert += s
        self.c.execute(insert)
        self.conn.commit()
        self.conn.close()

    def all(self):
        """ 全レコードを配列として取得 """
        self.c.execute('SELECT * FROM %s' % self.table_name)
        all_result = self.c.fetchall()
        self.c.close()
        return all_result

    def first(self):
        """ idが一番小さいレコードを取得 """

    def last(self):
        """ idが一番大きいレコードを取得 """

    def find(self, id: int):
        """ idのレコードを取得し, Persistanceのオブジェクトとして返す """
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM {} WHERE id = {}".format(self.table_name, id))
        fetchone = self.c.fetchone()

        # カラム名: レコードのデータ で保存
        name_record = {}
        result = []
        for i, d in enumerate(self.c.description):
            name_record[d[0]] = fetchone[i]

        result.append(name_record)

        self.c.close()
        return Persistance(self.table_name, result).data

    def find_by(self, column_name, search_word: str):
        """ column_nameのsearch_wordの中で最初にヒットした1件のレコードを取得 """

    def where(self, column_name, search_word: str):
        """ 該当するレコード全件を取得 """

    def __CreateTimeStamp(self):
        """ タイムスタンプの作成 """
        now = time.time()
        jst = timezone(timedelta(hours=+9), 'JST')
        loc = datetime.fromtimestamp(now, jst).timestamp()
        return loc

    def __TupleMake(self, data: List) -> str:
        """ リストのデータを()に変換する """
        # time = self.__CreateTimeStamp()
        s = "(null, "
        for i, item in enumerate(data):
            if i == 0:
                s += "'{}'".format(item)
            else:
                s += ", '{}'".format(item)
        s += ")"
        return s


class Persistance(WactiveRecord):
    def __init__(self, table_name, fetch_data):
        super().__init__(table_name)
        self.data = fetch_data

    def update(self, **kwargs):
        """ レコードの更新 """
        print(kwargs)
        """
        try:
            self.c.execute("INSERT INTO {} VALUES ({})".format(self.table,
                                                               ))
        except sqlite3.Error as e:
            print(e)

        self.conn.commit()
        self.c.close()
        """
