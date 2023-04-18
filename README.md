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

### inky pHat / ACeP 7-Color

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

### Advanced Color ePaper （ACeP） 7-Color

4 inch のカラー電子ペーパーで、Raspberry Pi に取り付け、OS を起動したら以下の手順に従ってセットアップする

https://www.waveshare.com/wiki/4.01inch_e-Paper_HAT_(F)_Manual#Working_With_Raspberry_Pi

example

https://github.com/waveshare/e-Paper.git の [ここ](https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/examples/epd_4in01f_test.py)

## 定期実行する方法

スクリプトを/opt 直下へ引っ越し

```bash
sudo cp -r weather_forecast_viewer/ /opt/
```

systemd の設定

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

## メモ

### systemd

- [Raspberry Pi で systemd を使ってプログラムを自動実行する](https://qiita.com/molchiro/items/ee32a11b81fa1dc2fd8d)
- [systemd タイマーの書き方。OnCalendar の timer 設定の記述方法とチェック方法をおさらいする。cron の代替にするサンプル集](https://takuya-1st.hatenablog.jp/entry/2020/04/24/032822)
- [systemd .timer について調べた事を記事にしておく](https://www.souichi.club/raspberrypi/systemd-timer/)
- [systemd で timer の作り方（最小限のサンプル）](https://qiita.com/aosho235/items/7656d5568af8f48b2dc1)
- [crontab を捨て systemd に定期実行を任せよう](https://qiita.com/narikei/items/ca4823c7f6790f0cbe0b)
- [RasPi のプログラムを自動起動に！その 2 systemd 編](https://miho-diary.hatenablog.com/entry/2017/10/30/004153)
- [systemd サービスユニット覚書](https://qiita.com/ch7821/items/369090459769c603bb6b)

### Python

- [自身の IP アドレスを取得したい](https://edosha.hatenablog.jp/entry/2017/08/09/150636)

### Pillow

- [使用可能な色リスト](https://drafts.csswg.org/css-color-4/)
- [画像の色を高速に置換する](https://qiita.com/pashango2/items/d6dda5f07109ee5b6163)

###
