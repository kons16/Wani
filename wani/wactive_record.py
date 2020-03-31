"""
WactiveRecordでDB操作
"""


class WactiveRecord:
    def __init__(self, table_name):
        self.model = table_name

    def all(self):
        """ 全レコードを配列として取得 """

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

    def save(self):
        """ 変更を保存(commit) """
