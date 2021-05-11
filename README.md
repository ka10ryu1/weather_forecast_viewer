# weather_forecast_viewer
天気予報を取得し、表示するためのレポジトリ

# とりあえず動かす

## ライブラリ

- pip3
  - matplotlib
  - numpy（upgrade）
- apt
  - libopenjp2-7
  - python-numpy
  - libatlas-base-dev
  - fonts-ipaexfont-gothic
  - fontconfig

## 端末上に表示

```bash
python3 ./main_emoji.py
```

## 画像として表示

```bash
python3 ./main_img.py
```

# お天気表示デバイス導入手順

## ハードウェア

### Raspberry pi Zero WH

### inky pHat

## ソフトウェア

### OSインストール

Raspberry Pi ImagerでOSをインストールする。  
以下は「Raspberry Pi OS Lite (32bit)」をインストールして進めている。

「Ctrl+Shift+X」でsshなどの設定もOS書き込み時にやってくれるので、先に設定しておくのがおすすめ。  
[参考](https://dev.classmethod.jp/articles/raspberry-pi-imager-v1-6-update/)

無事に起動できたら、upgradeしておくこと。

### inky pHat

#### inky pHatの利用

Raspberry Pi にinky pHatを取り付け、OSを起動したら以下の手順に従ってセットアップする

https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat  

example

https://github.com/pimoroni/inky



## 定期実行

cron
