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


class Auth:
    def __init__(self, table_name):
        self.table = table_name
        pass

    def create_user(self, **kwargs):
        """ ユーザーをハッシュ化したパスワードでテーブルに追加する"""
        kwargs["password"] = bcrypt.hashpw(kwargs["password"], bcrypt.gensalt())

        conn = sqlite3.connect("db/development.sqlite3")
        c = conn.cursor()
        c.executescript("INSERT INTO %s VALUES (%s)" % (self.table, kwargs))
        conn.commit()
        conn.close()

    def session_new(self):
        """ 新しいセッションのページ(ログイン) """
        pass

    def session_create(self):
        """ 新しいセッションの作成(ログイン) """
        pass

    def session_destory(self):
        """ セッションの削除(ログアウト) """
        pass
