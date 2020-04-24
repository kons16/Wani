# Wani
WSGIの仕様に沿ったWebフレームワークです。  

## A Simple Example

## WactiveRecord(ORM)

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
