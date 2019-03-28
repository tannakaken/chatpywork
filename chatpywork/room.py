#!/usr/bin/env python
"""
    file name: room.py
    python wrapper for ChatWork API v2 
"""

__author__ = "tannakaken"
__email__ = "tannakaken@gmail.com"
__credits__ = []
__licence__ = "MIT"
__mainteiner__ = "tannakaken"
__status__ = "production"
__version__ = "1.2.0"
__date__ = "2020-03-27"

import requests
import os
import os.path
import calendar
import csv
import io

# Chatwork API v2のURL
# http://developer.chatwork.com/ja/index.html
BASE_URL = 'https://api.chatwork.com/v2'

# アップロードファイルの上限
# http://developer.chatwork.com/ja/endpoint_rooms.html#POST-rooms-room_id-files
# 上記ドキュメントには5MBと書いてあるが、APIのレスポンスによれば、requestのcontentの上限が10MBであるようだ。
# 実際、10MB以下のファイルをアップロードすることの動作確認もできる。
# しかし、メッセージなども含めると、ファイル自体は10MB以下でも全体で10MBを超えることもありうるので、
# APIからのresponseのstatus codeが413になっていないかの確認は必要である。
FILE_LIMIT = 10485760

class Room:
    """
    chatworkのチャットルームに投稿するためのクラス
    """
    def __init__(self, roomid, apikey):
        """初期化する。
        
        1ルームごとに１つのオブジェクト。

        Parameters
        ----------
        roomid :str
            チャットルームのID（urlの最後の部分）
        apikey :str
            アカウントに付与されたAPI KEY（自分で取得する）。
        """
        self.roomid = roomid
        self.apikey = apikey

    def _to(self, message, to):
        """メッセージに宛先を付加する
        
        Parameters
        ----------
        message :str
            メッセージ本文
        to :dictionary
            投稿の宛先。Account Idとアカウントの名前の辞書
        
        Returns
        ----------
        str
            宛先が付加されたメッセージ
        >>> room = Room("","")
        >>> room._to("message", {})
        'message'
        >>> room._to("spam", {"42":"グレアム・チャップマン"})
        '[To:42] グレアム・チャップマンさん\\nspam'
        >>> room._to("egg and spam", {"42":"グレアム・チャップマン","48":"テリー・ジョーンズ"})
        '[To:42] グレアム・チャップマンさん\\n[To:48] テリー・ジョーンズさん\\negg and spam'
        """
        result = ''
        for chatworkid, name in to.items():
            result += "[To:{}] {}さん\n".format(chatworkid,name)
        return result + message

    def send_message(self, message, to={}):
        """メッセージを送信する。

        Parameters
        ----------
        message :str
            送信するメッセージ
        to :dictionary
            投稿の宛先。Account Idとアカウントの名前の辞書

        Returns
        ----------
        requests.Response
            requests.postの戻り値
        """
        post_url='{}/rooms/{}/messages'.format(BASE_URL, self.roomid)

        headers = {'X-ChatWorkToken': self.apikey}
        params = {'body': self._to(message, to)}
        return requests.post(post_url, headers=headers, data=params)

    def send_data(self, data, filename, mimetype, message="", to={}):
        """データを添付ファイルとして送信する
        
        Parameters
        ----------
        filepath :bites
            送信するデータ。10MBが上限。
        filename :str
            添付ファイル名
        mimetype :str
            ファイルのmedia type
        message :str
            添付ファイルに付加するメッセージ
        to :dict
            投稿の宛先。Account Idとアカウントの名前の辞書
        
        Returns
        ----------
        requests.Response
            requests.postの戻り値
        """
        if len(data) > FILE_LIMIT:
            return self.send_message("容量オーバー:アップロードするデータが大きすぎます", to=to)
        headers = {'X-ChatWorkToken': self.apikey}
        post_url = '{}/rooms/{}/files'.format(BASE_URL, self.roomid)
        message = self._to(message, to)
        if str:
            files = {'file': (filename, data, mimetype), 'message':message}
        else:
            files = {'file': (filename, data, mimetype)}
        response = requests.post(post_url, headers=headers, files=files)
        if response.status_code == 413:
            return self.send_message("容量オーバー:アップロードするデータが大きすぎました", to=to)
        return response


    def send_binaryfile(self, filepath, mimetype, message="", to={}):
        """バイナリファイルを送信する
        
        Parameters
        ----------
        filepath :str
            送信するファイルのパス。メッセージと合わせて10MBが上限。
        mimetype :str
            ファイルのマイムタイプ
        message :str
            添付ファイルに付加するメッセージ
        to :dictionary
            投稿の宛先。Account Idとアカウントの名前の辞書
        
        Returns
        ----------
        requests.Response
            requests.postの戻り値
        """
        filename = os.path.basename(filepath)
        with open(filepath, 'rb') as f:
            data = f.read()
        return self.send_data(data, filename, mimetype, message=message, to=to)


    def send_textfile(self, filepath, mimetype, fromencoding='utf-8', toencoding='utf-8', fromlinesep=None, tolinesep=None, message="", to={}):
        """文字列ファイルを送信する
        
        Parameters
        ----------
        filepath :str
            送信するファイルのパス。メッセージと合わせて10MBが上限。
        mimetype :str
            ファイルのmedia type
        fromencoding :str
            ローカルファイルのエンコード名。デフォルトはUTF-8
        toencoding :str
            添付ファイルのエンコード名。デフォルトはUTF-8
        fromlinesep :str
            ローカルファイルの改行コード。デフォルトはローカルOSの改行コード
        tolinesem :str
            添付ファイルの改行コード。デフォルトはローカルOSの改行コード
        message :str
            添付ファイルに付加するメッセージ
        to :dictionary
            投稿の宛先。Account Idとアカウントの名前の辞書
        Returns
        ----------
        requests.Response
            requests.postの戻り値
        """
        if fromlinesep is None:
            fromlinesep = os.linesep
        if tolinesep is None:
            tolinesep = os.linesep
        filename = os.path.basename(filepath)
        with open(filepath, 'r', newline=fromlinesep, encoding=fromencoding) as f:
            data = f.read()
            if tolinesep != fromlinesep:
                data= data.replace(fromlinesep, tolinesep)
            data = data.encode(toencoding)
        return self.send_data(data, filename, mimetype, message=message, to=to)

    def send_csv(self, csvarray, filename, delimiter=',', quotechar='"', linesep='\n', quoting=csv.QUOTE_MINIMAL, encode='utf-8', message="", to={}):
        """配列をcsvにして送信する
        
        Parameters
        ----------
        csvarrat :array
            csvにする二重配列。csvにした時にメッセージと合わせて10MBが上限。
        delimiter :str
            csvの区切り。デフォルトはコンマ
        quotechar :str
            csvの引用符。デフォルトは二重引用符
        linesep :str
            csvの改行コード。デフォルトはLF
        quoting :int
            csvのクオート方法を、csvのQUOTE_*定数で指定する。デフォルトはcsv.QUOTE_MINIMAL（必要な時だけクオートする）
        encode :str
            csvの文字コード。デフォルトはUTF-8
        message :str
            添付csvに付加するメッセージ
        to :dictionary
            投稿の宛先。Account Idとアカウントの名前の辞書
        
        Returns
        ----------
        requests.Response
            requests.postの戻り値
        """
        f = io.StringIO("")
        writer = csv.writer(f, delimiter=delimiter, quotechar=quotechar, lineterminator=linesep, quoting=quoting)
        writer.writerows(csvarray)
        f.seek(0)
        data = f.read().encode(encode)
        return self.send_data(data, filename, 'text/csv', message=message, to=to)

    def send_data_from_url(self, url, params={}, headers={}, message='', to={}):
        """URLからデータを取得してを送信する
        
        Parameters
        ----------
        url :str
            データのURL。メッセージと合わせて10MBが上限。
        params: dictionary
            httpリクエストのクエリ・パラメータ
        headers: dictionary
            httpリクエストのヘッダー
        message :str
            添付ファイルに付加するメッセージ
        to :dictionary
            投稿の宛先。Account Idとアカウントの名前の辞書
        Returns
        ----------
        requests.Response
            requests.postの戻り値
        """
        try:
            response = requests.get(url, params=params, headers=headers)
        except ConnectionError:
            message = "接続エラー: " + url + " からデータの取得中に接続エラーが発生しました。"
            return self.send_message(message, to=to)
        except HTTPError:
            message = "HTTPエラー: " + url + " からデータの取得中に不正なHTTPレスポンスがありました。"
            return self.send_message(message, to=to)
        except Timeout:
            message = "タイムアウト: " + url + " からデータの取得中にタイムアウトが発生しました。"
            return self.send_message(message, to=to)
        except TooManyRedirects:
            message = "リダイレクト超過: " + url + " からデータの取得中にリダイレクトが最大数を超過しました。"
            return self.send_message(message, to=to)
        if response.status_code != requests.codes.ok:
            if response.status_code == 400:
                message = "400 Bad Request: " + url + " へ不正なリクエストが行われました。"
            elif response.status_code == 401:
                message = "401 Unauthorized: " + url + "へのリクエストは必要な認証が行われませんでした。"
            elif response.status_code == 403:
                message = "403 Forbidden: " + url + " へのリクエストは禁止されています。"
            elif response.status_code == 404:
                message = "404 Not Found: " + url + " が見つかりませんでした。"
            else:
                message = response.status_code + ":" + url + " へのリクエストがOKではないステータスを返しました。"
            return self.send_message(message, to=to)
        data = response.content
        filename = os.path.basename(url)
        mimetype = response.headers['Content-Type']
        return self.send_data(data, filename, mimetype, message=message, to=to)

    def send_task(self, task, to_ids, limit=None):
        """新しいタスクを作成する

        Parameters
        ----------
        task :str
            作成するタスク
        to_ids :array
            担当者のID
        limit : datetime
            期限。オプショナル

        Returns
        ----------
        requests.Response
            requests.postの戻り値
        """
        post_url = '{}/rooms/{}/tasks'.format(BASE_URL, self.roomid)

        headers = {'X-ChatWorkToken': self.apikey}
        if limit:
            params = {'body': task, "to_ids": ",".join(to_ids), "limit":calendar.timegm(limit.utctimetuple())}
        else:
            params = {'body': task, "to_ids": ",".join(to_ids)}
            
        return requests.post(post_url, headers=headers, data=params)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
