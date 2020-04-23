"""
ユーザーの認証周りの処理

bcryptでのハッシュ化
password = b"super secret password"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

パスワードチェック
bcrypt.checkpw(b"super secret password", hashed)): boolean
"""
import bcrypt
import sqlite3
import uuid
import OpenSSL
from http import cookies


class Auth:
    def __init__(self, table_name):
        self.table_name = table_name
        pass

    def create_user(self, user_data: dict):
        """ ユーザーをハッシュ化したパスワードでテーブルに追加する """
        user_data["password"] = bcrypt.hashpw(user_data["password"].encode("utf-8"),
                                              bcrypt.gensalt()).decode("UTF-8")

        conn = sqlite3.connect("db/development.sqlite3")
        c = conn.cursor()
        create_user_sql = "INSERT INTO {} VALUES ".format(self.table_name)
        s = self.__TupleMake(user_data)
        create_user_sql += s

        try:
            print(create_user_sql)
            c.execute(create_user_sql)
        except sqlite3.Error as e:
            print(e)

        conn.commit()
        conn.close()

    def session_new(self, **kwargs):
        """ 新しいセッションのページ(ログイン) """
        pass

    def session_create(self, **kwargs) -> bool:
        """ 新しいセッションの作成(ログイン) """
        # セッションIDの作成
        session_id = uuid.UUID(bytes=OpenSSL.rand.bytes(16))
        cookie = cookies.SimpleCookie()
        cookie['SESSION_ID'] = session_id

    def session_destory(self):
        """ セッションの削除(ログアウト) """
        pass

    def __TupleMake(self, user_data: dict) -> str:
        """ 辞書型のデータを文字列に変換する """
        # time = self.__CreateTimeStamp()
        s = "(null, "
        for i, (k, v) in enumerate(user_data.items()):
            if i == 0:
                s += "'{}'".format(v)
            else:
                s += ", '{}'".format(v)
        s += ")"
        return s
