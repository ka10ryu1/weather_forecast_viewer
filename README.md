# weather_forecast_viewer

天気予報を取得し、表示するためのレポジトリ

# とりあえず動かす

## ライブラリ

- pip3
  - matplotlib
  - numpy（upgrade）
  - beautifulsoup4
  - requests
- apt
  - libopenjp2-7
  - python3-numpy
  - python3-matplotlib
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

### OS インストール

Raspberry Pi Imager で OS をインストールする。  
以下は「Raspberry Pi OS Lite (32bit)」をインストールして進めている。

「Ctrl+Shift+X」で ssh などの設定も OS 書き込み時にやってくれるので、先に設定しておくのがおすすめ。  
[参考](https://dev.classmethod.jp/articles/raspberry-pi-imager-v1-6-update/)

無事に起動できたら、upgrade しておくこと。

### inky pHat

#### inky pHat の利用

Raspberry Pi に inky pHat を取り付け、OS を起動したら以下の手順に従ってセットアップする

https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat

example

https://github.com/pimoroni/inky

## 定期実行する方法

スクリプトを/opt直下へ引っ越し

```bash
sudo cp -r weather_forecast_viewer/ /opt/
```

systemdの設定

```bash
sudo cp show_* /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable show_ip.service
sudo systemctl enable show_weather.timer
sudo reboot
```

### 設定を変更したい場合

設定を変更した設定ファイルを再度`/etc/systemd/system/`に置く

```bash
sudo cp show_* /etc/systemd/system/
sudo systemctl daemon-reload
```

設定が変更されているかは`systemctl show <unit_name>`で確認できる

```bash
sudo systemctl show show_weather.timer
```


## エラーが出た

### `/usr/bin/env: ‘python3\r’: No such file or directory`

対応策

```bash
sudo apt install dos2unix
dos2unix /PATH/TO/YOUR/WINDOWS_FILE
```

[参考](https://askubuntu.com/questions/896860/usr-bin-env-python3-r-no-such-file-or-directory)

### `findfont: Font family 'IPAexGothic' not found.`

正しく fonts-ipaexfont-gothic をインストールしていても発生する場合があります。

```bash
$ ls ~/.cache/matplotlib/
fontlist-v330.json
$ rm ~/.cache/matplotlib/fontlist-v330.json
```

※`fontlist-v330.json`は違う名前の場合があります

[参考](https://self-development.info/ipaexgothic%E3%81%AB%E3%82%88%E3%82%8Bmatplotlib%E3%81%AE%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%8C%96%E3%80%90python%E3%80%91/)
