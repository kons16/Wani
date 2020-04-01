"""
ユーザーの認証周りの処理

bcryptでのハッシュ化
password = b"super secret password"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
"""
import bcrypt
import sqlite3


class Auth:
    def __init__(self):
        pass

    def create_user(self, **kwargs):
        """ ユーザーをハッシュ化したパスワードで登録する"""
        pass

    def session_new(self):
        """ 新しいセッションのページ(ログイン) """
        pass

    def session_create(self):
        """ 新しいセッションの作成(ログイン) """
        pass

    def session_destory(self):
        """ セッションの削除(ログアウト) """
        pass
