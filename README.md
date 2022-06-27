# AtCoder Problem Parser

[AtCoder](https://atcoder.jp/)の問題文をMarkdown形式に変換するツールです。

## Requirements

- Python 3.8.10

## Installation

### Download this repository

このリポジトリをローカルにクローンします。

```
git clone https://github.com/fjnkt98/atcoder_problem_parser.git
```

### Create python virtual environment

`venv`を使用してPythonの仮想環境を作成します。

```
cd atcoder_problem_parser
python3 -m venv env
source env/bin/activate
```

### Install package

本パッケージをインストールします。

```
pip install -e .
```

インストールにより、`app`コマンドが使えるようになります。

## Usage

`ABC`、`ARC`、`AGG`の問題を変換する際は、`contest`引数と`problem`引数を指定することができます。

例: AtCoder Beginner Contest 253 Cの場合
```
app ABC253 C
```

問題のURLを直接指定することも可能です。

```
app --url=https://atcoder.jp/contests/abc253/tasks/abc253_c
```

変換結果は標準出力に表示されます。Markdownファイルとして欲しい場合は、リダイレクトを使用してください。

```
app ABC253 C > result.md
```