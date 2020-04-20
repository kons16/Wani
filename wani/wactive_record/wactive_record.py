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
        c = self.conn.cursor()
        c.execute(insert)
        self.conn.commit()
        self.conn.close()

    def all(self):
        """ 全レコードを配列として取得 """
        c = self.conn.cursor()
        c.execute('SELECT * FROM %s' % self.table_name)
        all_result = c.fetchall()
        c.close()
        return all_result

    def first(self):
        """ idが一番小さいレコードを取得 """

    def last(self):
        """ idが一番大きいレコードを取得 """

    def find(self, id: int):
        """ idのレコードを取得し, Persistanceのオブジェクトとして返す """
        c = self.conn.cursor()
        c.execute("SELECT * FROM {} WHERE id = {}".format(self.table_name, id))
        fetchone = c.fetchone()

        # カラム名: レコードのデータ で保存
        name_record = {}
        result = []
        for i, d in enumerate(c.description):
            name_record[d[0]] = fetchone[i]

        result.append(name_record)

        self.conn.close()
        persist = Persistance(self.table_name, id, result)
        return persist

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
        """ リストのデータを文字列に変換する """
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
    def __init__(self, table_name, id, fetch_data):
        super().__init__(table_name)
        self.data = fetch_data
        self.id = id

    def update(self, **kwargs):
        """
        レコードの更新
        obj.update(name="tom", year="32")のときnameカラムとyearカラムを変更
        """
        c = self.conn.cursor()
        update_sql = "UPDATE {} SET ".format(self.table_name)
        # update_sqlにSETパラーメタを書き込んでいく
        for i, (k, v) in enumerate(kwargs.items()):
            if i != len(kwargs)-1:
                # TODO: ""で囲むのを直す(int型などに対応させる)
                update_sql += "{}=\"{}\", ".format(k, v)
            else:
                update_sql += "{}=\"{}\" ".format(k, v)

        update_sql += "WHERE id={}".format(self.id)

        try:
            c.execute(update_sql)
        except sqlite3.Error as e:
            print(e)

        self.conn.commit()
        self.conn.close()
