# Wani
WSGIの仕様に沿ったWebフレームワークです。  

## A Simple Example

## WactiveRecord(ORM)

```Python
from wani import WactiveRecord

u = WactiveRecord("users")
u.find(id)
```
`WactiveRecord(テーブル名)`でテーブル名に基づくWactiveRecordオブジェクトを生成できます。  

### WactiveRecord メソッド
* <b>all()</b>  
* <b>find(id: int)</b>  
* <b>find_by(column_name=value)</b>

## Auth
