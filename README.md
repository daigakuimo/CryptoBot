# 仮想通貨BOT
DEXへの上場やロック解除を監視して取引してくれるBOT

## 環境
|  Name  |  Version  |
| ---- | ---- |
|  Mac OS  |         |
|  Python  |  3.7.5  |

## configの設定
ex_config.envをもとにconfig.envを作成

wallet_A = "*** メタマスクのアドレス ***"
key_A = "*** メタマスクの秘密鍵 ***"

## 使い方
1.上記のconfigの設定を行う

2.Approve.pyで取引したいトークンをapproveする

3.上場戦ならBSCFairTradeまたはHarmonyFairTradeで狙っているトークンのアドレスを入力して実行

## 参考資料
[納豆男爵のDeFi Bot作り①~⑤](https://note.com/natto_baron/n/nc5fe180b2e2e)

[Pythonでcoincheck APIを使ってみる。 自動取引プログラム作成に向けて](https://qiita.com/ti-ginkgo/items/7e15bdac6618c07534be#%E6%9D%BF%E6%83%85%E5%A0%B1-get)

[PythonからcoincheckのWebsocketAPIに接続する](https://qiita.com/flowphantom/items/f3e1f82cd6017028da26)