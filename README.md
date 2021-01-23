# nogiblogimg
乃木陽
画像取得陽

開発はdevelopでします。

# これはなに

自動で画像をいっぱいとるよ

# インストール方法

```
$ pip install git+https://github.com/OumeNogizakaUnit/nogiblogimg.git
```

# 使い方

```
$ nogiblogimg --help
Usage: nogiblogimg [OPTIONS] SAVEDIR

  SAVEDIR に画像を保存する

Options:
  -s, --start [%Y%m]  集計開始月  [default: 201111]
  -e, --end [%Y%m]    集計終了月  [default: 201112]
  --help              Show this message and exit.


```

## 開発準備

```
$ poetry install
```

## 開発者へ

以下のコマンドで`flake8が使えます`

```
$ poetry run poe lint
```

以下のコマンドで`autopep8`, `autoflake`, `isort`が使えます

```
$ poetry run poe format
```
