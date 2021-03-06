"""
WactiveRecordでDB操作

・WactiveRecordクラス

・Persistanceクラス
モデルから得たレコードが個々に持つ処理
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

    def all(self) -> List:
        """ 全レコードを配列として取得

        :result [{'id': 1, 'name': 'yay', 'email': None, 'password': None}, {'id': 2 ...}]
        """
        c = self.conn.cursor()
        c.execute('SELECT * FROM %s' % self.table_name)
        all_record = c.fetchall()
        c.close()

        result = []
        for record in all_record:
            name_record = self.__makeFetchColumnData(record, c.description)
            result.append(name_record)

        return result

    def first(self) -> List:
        """ idが一番小さいレコードを取得

        :persist [{'id': 1, 'name': 'tom'}]
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM {} ORDER BY ASC LIMIT 1".format(self.table_name))
        fetchone = c.fetchone()

        result = []
        name_record = self.__makeFetchColumnData(fetchone, c.description)
        result.append(name_record)

        self.conn.close()
        persist = Persistance(self.table_name, result[0]["id"], result)
        return persist

    def last(self) -> List:
        """ idが一番大きいレコードを取得

        :persist [{'id': 1, 'name': 'tom'}]
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM {} ORDER BY DESC LIMIT 1".format(self.table_name))
        fetchone = c.fetchone()

        result = []
        name_record = self.__makeFetchColumnData(fetchone, c.description)
        result.append(name_record)

        self.conn.close()
        persist = Persistance(self.table_name, result[0]["id"], result)
        return persist

    def find(self, id: int) -> List:
        """ idのレコードを取得し, Persistanceのオブジェクトとして返す

        :persist [{'id': 1, 'name': 'tom'}]
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM {} WHERE id = {}".format(self.table_name, id))
        fetchone = c.fetchone()

        result = []
        name_record = self.__makeFetchColumnData(fetchone, c.description)
        result.append(name_record)

        self.conn.close()
        persist = Persistance(self.table_name, id, result)
        return persist

    def find_by(self, **kwargs) -> List:
        """ column_nameのsearch_wordの中で最初にヒットした1件のレコードを取得

        :param kwargs: {"name": "tom"}
        :persist [{'id': 1, 'name': 'tom'}]
        """
        key = list(kwargs.keys())[0]
        value = list(kwargs.values())[0]
        c = self.conn.cursor()
        # valueがint型のときエスケープシーケンスさせない
        if type(value) is int:
            c.execute("SELECT * FROM {} WHERE {}={} ORDER BY id DESC LIMIT 1".format(self.table_name,
                                                                                     key,
                                                                                     value))
        else:
            c.execute("SELECT * FROM {} WHERE {}=\"{}\" ORDER BY id DESC LIMIT 1".format(self.table_name,
                                                                                         key,
                                                                                         value))
        fetchone = c.fetchone()

        result = []
        name_record = self.__makeFetchColumnData(fetchone, c.description)
        result.append(name_record)

        self.conn.close()
        persist = Persistance(self.table_name, result[0]["id"], result)
        return persist

    def where(self, rule: str) -> List:
        """ 該当するレコード全件を取得
        :ruleの演算子前後はスペース1つ空ける
        "id >= 10" や　"name = tom" など

        :param rule: SQLに書く条件文 例 "id > 10"
        :persist [{'id': 1, 'name': 'tom'}]
        """
        pre_var = rule.split(" ")[0]
        ope = rule.split(" ")[1]
        aft_var = rule.split(" ")[2]

        c = self.conn.cursor()
        if type(aft_var) is int:
            c.execute("SELECT * FROM {} WHERE {}{}{}".format(self.table_name,
                                                             pre_var,
                                                             ope,
                                                             aft_var))
        else:
            c.execute("SELECT * FROM {} WHERE {}{}\"{}\"".format(self.table_name,
                                                                 pre_var,
                                                                 ope,
                                                                 aft_var))
        all_record = c.fetchall()
        c.close()

        result = []
        for record in all_record:
            name_record = self.__makeFetchColumnData(record, c.description)
            result.append(name_record)

        print(result)
        return result

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

    def __makeFetchColumnData(self, fetchone: tuple, description: tuple) -> dict:
        """ fetchしたレコード(fetchone)をカラム名(description)を付けて辞書型として返すようにする。
        カラム名: レコードのデータ で保存する

        :name_record [{'id': 1, 'name': 'tom'}]
        """
        name_record = {}
        for i, d in enumerate(description):
            name_record[d[0]] = fetchone[i]

        return name_record


class Persistance(WactiveRecord):
    def __init__(self, table_name: str, id: int, fetch_data: List):
        super().__init__(table_name)
        self.data = fetch_data
        self.id = id

    def update(self, **kwargs):
        """ レコードの更新

        obj.update(name="tom", year="32")のときnameカラムとyearカラムを変更
        """
        c = self.conn.cursor()
        update_sql = "UPDATE {} SET ".format(self.table_name)
        # update_sqlにSETパラーメタを書き込んでいく
        for i, (k, v) in enumerate(kwargs.items()):
            if i != len(kwargs)-1:
                if type(v) is int:
                    update_sql += "{}={}, ".format(k, v)
                else:
                    update_sql += "{}=\"{}\", ".format(k, v)

            else:
                if type(v) is int:
                    update_sql += "{}={}, ".format(k, v)
                else:
                    update_sql += "{}=\"{}\", ".format(k, v)

        update_sql += "WHERE id={}".format(self.id)

        try:
            c.execute(update_sql)
        except sqlite3.Error as e:
            print(e)

        self.conn.commit()
        self.conn.close()
