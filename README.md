# Wani
WSGIの仕様に沿ったWebフレームワークです。  

## Wani サンプル
```Python
from wani import Wani, Response

app = Wani()


@app.route("/", ["GET"])
def hello(request):
    return Response("Hello, Wani")


if __name__ == "__main__":
    app.run()
```
ブラウザから `http://127.0.0.1:5000/` にアクセスすると "Hello, Wani" と表示されます。

## ルーティング
デコレータでルーティングを設定できます。
```Python
@app.route("/", ["GET"])
def hello(request):
    """ usersテーブルのレコードを全件取得し、一番目のレコードを表示 """
    u = WactiveRecord("users")
    all_users = u.all()
    return Response("Hello, {}".format(all_users[0]["name"]))


@app.route("/find_user/{id}", ["GET"])
def find_user(request, id):
    """ usersテーブルから引数idのレコードを見つける """
    u = WactiveRecord("users")
    record = u.find(id)
    return Response("{}".format(record.data))
   
   
@app.route("/data", method=["GET", "POST"])
def get_data(request):
    if request.method == "GET":
        return TemplateResponse("data-form.html")
    else:
        return Response("{}".format(request.forms["num"]))

```

## DB(SQLite)
Waniは標準のORM(WactiveRecord)で、SQLiteを扱うことができます。

### manage_db.py
`wani/wactive_record/manage_db.py` ではテーブルの作成、カラムの追加、インデックス付与などができます。  

* <B>テーブルの作成</B>  
authでユーザーが登録されているか検索する際はemailカラムをもとに検索を行うためemailカラムの追加が必須。  
idは自動付与される(PRIMARY KEY AUTOINCREMENT)。  
テーブルは `db/development.sqlite3` に保存。  
$ python manage_db.py create [table_name] [カラム名]:[型] ...  
`$ python manage_db.py create users "name:text" "year:int" "email":text`  

* <B>既存テーブルへのカラム追加</B>  
$ python manage_db.py add [table_name] [カラム名]:[型]  
`$ python manage_db.py add users "place:text"`    

* <B>既存カラムへインデックス付与</B>  
インデックス名はデフォルトで "カラム名index" になる。    
$ python manage_db.py index [table_name] [カラム名]  
`$ python manage_db.py index users name`  


### WactiveRecord(ORM)

```Python
from wani import WactiveRecord

u = WactiveRecord("users")
u.find(2)
```
`WactiveRecord(テーブル名)`でテーブル名に基づくWactiveRecordオブジェクトを生成できます。  

### WactiveRecord メソッド
* <b>all()</b>  
オブジェクトが持つレコードを全件取得  
`u.all()`
* <b>first()</b>  
オブジェクトが持つ最小idを取得  
`u.first()`
* <b>last()</b>  
オブジェクトが持つ最大レコードを全件取得  
`u.last()`
* <b>find(id: int)</b>  
オブジェクトの中で指定されたidレコードを1件取得  
`u.find(3)`
* <b>find_by(column_name=value)</b>  
オブジェクトの中で指定された条件のレコードを最初の1件取得  
`u.first(name=tom)`
* <b>where(rule: str)</b>  
オブジェクトの中で指定されたruleに基づくレコードを全件取得  
ruleは"place = tokyo"など、演算子の前後にスペース1つ入れて指定  
`u.where("place = tokyo")`

## Auth
