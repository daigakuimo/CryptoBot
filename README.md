# 仮想通貨BOT
テクニカル分析を用いてBOTで利益を出すことを目標とする

## 環境
|  Name  |  Version  |
| ---- | ---- |
|  Mac OS  |         |
|  Python  |  3.7.5  |

## アクセスキーの設定
ex_config.envをコピーしてconfig.envを作る

config.env内に以下を記入
```
# アクセスキー
ACCESS_KEY = "ここに自分のCoinCheckのアクセスキーを書く"

# シークレットキー
SECRET_KEY = "ここに自分のCoinCheckのシークレットアクセスキーを書く"
```

config.envはgitignoreされてるのでアクセスキーが外に漏れる心配はない


## 参考資料
[Pythonでcoincheck APIを使ってみる。 自動取引プログラム作成に向けて](https://qiita.com/ti-ginkgo/items/7e15bdac6618c07534be#%E6%9D%BF%E6%83%85%E5%A0%B1-get)

[PythonからcoincheckのWebsocketAPIに接続する](https://qiita.com/flowphantom/items/f3e1f82cd6017028da26)