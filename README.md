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

## installation

```
pip install chatpywork
```

## Usage

送信に必要なroom\_idは
  https://www.chatwork.com/#!rid123456789
のridの後の数字を使う（ridは含まない）。

api\_keyは、
ChatWorkのページの右上のアカウントの名前をクリックして出てくるアコーディオンの中にある
[API設定](https://www.chatwork.com/service/packages/chatwork/subpackages/api/token.php)
をクリックして飛んだページで取得できる。

```
import chatpywork
import datetime


room_id = '123456789'
api_key = 'abcdefghi123456789'

account_id1 = 'Account Id1'
account_id2 = 'Account Id2''

room = chatpywork.Room(room_id, api_key)

room.send_message("hello", to={account_id1:"宛先ユーザー"})

room.send_data(binarydata, "image.jpg", "image/jpeg", message="画像です", to={account_id1:"宛先ユーザー"})

room.send_binaryfile("image.png","image/png", message-"画像です", to={account_id1:"宛先ユーザー")

room.send_textfile("data.csv","text/csv", fromencode="utf-8", toencode="cp932", fromlinsep="\n", tolinesep="\r\n", message="収集したデータです", to={account_id1:"宛先ユーザー"})

room.send_csv([["ID","名前","年齢"],[1,"山田太郎","24"],[2,"鈴木二郎","30"]], "sample.csv", encode="cp932", linsep="\r\n", message="収集したデータです", to={account_id1:"宛先ユーザー"})

room.send_data_from_url("http://example.com/image.png", headers={"X-token":"some secret tpken"}, params={"q":"query"}, message="webで手に入れた画像です。", to={account_id1:"宛先ユーザー"})

room.send_tesk("牛乳買って", [account_id1, account_id2], limit=datetime.datetime(2020, 4, 1)) 
```

公式ドキュメントにはファイルのサイズの上限は5MBとありますが、
どうやらHTTPリクエストのボディ全体のサイズの上限が10MBのようで、それを超えなければ、アップロードできます。

データのダウンロード時のエラー、およびファイルの容量オーバーなどは、できる限りChatworkに送信しますが、
それも動かなければ、全てのメソッドがrequests.postのレスポンスのオブジェクトを返すので、それを使ってデバッグしてください。

ChatworkのAPIの使用制限は今の所５分間あたり300回です。
当たり前ですが、これを超えるとChatworkにはエラーの通知できませんので、
メソッドの戻り値に含まれるHTTPレスポンスのヘッダーに記載されたAPI使用の残り回数や、
429 Too Many Requestsなどを検知して、他のエラー通知の方法を試みてください。

# Author
淡中☆圏 \<tannakaken@gmail.com\>
Twitter: @tannakaken
