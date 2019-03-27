# chatpywork
python wrapper for ChatWork API v2 

プログラマ的にはSlackなどの方がフレンドリーですが、
事務作業の現場などではchatworkが使われていることが多いです。
そして、そういう現場こそ、pythonが活躍する本来の場なのでは、と考えています。

chatworkのAPIくらいなら、requestsから叩くこともできますが、
chatworkの投稿の自動化をする際によくあるタスクとして、ファイルのアップロードなどがあります。
特にcsvなどが多いんですね。

csv自体にはなんの文句もないんですが、その際、
文字コードや改行コードなどの前時代的な問題が発生してイライラさせられます。

今時、UTF-8を「不正なバイナリ」などとして受け入れないプログラムの方がどうかしていますが、
pythonで事務作業を自動化したいと考える日本企業のcsvのターゲットはe飛伝だったりする場合が多く、
これは実態はcp932であるShift\_JISしか受け付けないし、CRLF以外の改行コードも改行とはみなしてくれない。
近い将来に対応してくれるともあまり期待できない。

というわけで、その苦労の成果だけでも切り出しておこうとしたのが、このパッケージです。

chatworkのAPIは他にもたくさんありますが、事務で自動化したいと思う案件が多いのは主に作成系であると思われるので、
現状はそこに限ってます。

# Usage

```
import chatpywork
import datetime


roomid = '123456789'
api_key = 'abcdefghi123456789'

account_id1 = 'Account Id1'
account_id2 = 'Account Id2''

room = chatpywork.Room(roomid, api_key)

room.send_message("hello", to={account_id1:"宛先ユーザー"})

room.send_data(binarydata, "image.jpg", "image/jpeg", message="画像です", to={account_id1:"宛先ユーザー"})

room.send_binaryfile("image.png","image/png", message-"画像です", to={account_id1:"宛先ユーザー")

room.send_textfile("data.csv","text/csv", fromencode="utf-8", toencode="cp932", fromlinsep="\n", tolinesep="\r\n", message="収集したデータです", to={account_id1:"宛先ユーザー"})

room.send_tesk("牛乳買って", [account_id1, account_id2], limit=datetime.datetime(2020, 4, 1)) 
```
