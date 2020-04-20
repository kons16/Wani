"""
sqliteへテーブルの作成やカラムの追加をできる.
具体的な実行方法は各docstringを参考

テーブル作成
$ python manage_db.py create [table_name] [カラム名]:[型] ...

既存テーブルへのカラム追加
$ python manage_db.py add [table_name] [カラム名]:[型]

既存カラムへインデックス付与
インデックス名はデフォルトで "カラム名index" になる
$ python manage_db.py index [table_name] [カラム名]
"""
import sys
import sqlite3
import os
from typing import List


def wactive(create_type: str, table_name: str, column: List):
    """
    AUTOINCREMENTありのid付きでusersテーブルを作成する場合
    python manage_db.py create users "name:text" "year:int"
    """
    # dbディレクトリがなければ作成
    if not os.path.exists("db"):
        os.makedirs("db")

    if create_type == "create":
        """ テーブルの作成 """
        table_column_type = "id integer PRIMARY KEY AUTOINCREMENT, "

        for i, c in enumerate(column):
            info = c.split(":")
            if i != len(column)-1:
                table_column_type += info[0] + " " + info[1] + ", "
            else:
                table_column_type += info[0] + " " + info[1]

        conn = sqlite3.connect("db/development.sqlite3")
        c = conn.cursor()

        try:
            c.executescript("CREATE TABLE %s(%s)" % (table_name, table_column_type))
        except sqlite3.Error as e:
            print('sqlite3.Error occurred:', e.args[0])

        conn.commit()
        conn.close()

    elif create_type == "add":
        """ カラムの追加 """
        info = column[0].split(":")
        table_column_type = info[0] + " " + info[1]

        conn = sqlite3.connect("db/development.sqlite3")
        c = conn.cursor()
        c.executescript("ALTER TABLE %s add column %s" % (table_name, table_column_type))
        conn.commit()
        conn.close()

    elif create_type == "see":
        conn = sqlite3.connect("db/development.sqlite3")
        c = conn.cursor()
        c.executescript('select * from %s' % (table_name))
        data = c.fetchall()
        print(data)
        conn.close()

    elif create_type == "index":
        """ 
        カラムにインデックスを付与
        SQL : create index nameindex on user(name);
        python manage_db.py index users name
        """
        conn = sqlite3.connect("db/development.sqlite3")
        c = conn.cursor()
        index_sql = "CREATE INDEX {} on {}({})".format(column[0]+"index",
                                                       table_name,
                                                       column[0])
        try:
            c.execute(index_sql)
        except sqlite3.Error as e:
            print(e)

        conn.close()

    else:
        print("no")


if __name__ == "__main__":
    args = sys.argv
    create_type = args[1]
    table_name = args[2]
    column = args[3:]
    wactive(create_type, table_name, column)
