# Timos — 帽子と鞄のオンラインショップ

職人がひとつずつ仕立てた帽子（帽子）と鞄（鞄）を扱う ECアプリです。
商品検索・カテゴリ閲覧・商品詳細・カート・購入・会員登録／ログイン・会員情報管理・
管理者機能（商品の登録／編集／削除、注文のキャンセル）を備えています。

---

## 技術スタック

| 項目 | 内容 |
|------|------|
| 言語 | Python 3.10 以上 |
| フレームワーク | Django 5.1 |
| データベース | MySQL 8.x（`utf8mb4`） |
| DB ドライバ | mysqlclient |
| フロント | Django テンプレート + 静的 CSS（`shopapp/static/style.css`） |

---

## 必要なもの（前提）

- Python 3.10+
- MySQL 8.x（ローカルで起動できること）
- `git`

---

## セットアップ手順

### 1. リポジトリの複製

```bash
git clone https://github.com/Suuhoshi/Timos.git
cd Timos
```

### 2. 仮想環境を作成して有効化

```bash
python -m venv .venv
source .venv/bin/activate        # Windows は .venv\Scripts\activate
```

### 3. MySQL にデータベースを作成

`config/settings.py` は既定で次の接続情報を使います（環境変数で上書き可能）。
データベース名 `Timos`・文字コード `utf8mb4` で作成してください。

```sql
CREATE DATABASE Timos CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

| 設定 | 既定値 | 上書き用の環境変数 |
|------|--------|--------------------|
| エンジン | `django.db.backends.mysql` | `DB_ENGINE` |
| データベース名 | `Timos` | `DB_NAME` |
| ユーザー | `root` | `DB_USER` |
| パスワード | `P@ssw0rd` | `DB_PASSWORD` |
| ホスト | `127.0.0.1` | `DB_HOST` |
| ポート | `3306` | `DB_PORT` |

接続情報が既定と異なる場合は、`runserver` の前に環境変数を設定してください
（`.env.example` を参考に）。例：

```bash
export DB_USER=youruser
export DB_PASSWORD=yourpassword
```

### 4. マイグレーションを実行（テーブル作成）

```bash
python manage.py migrate
```

### 5. サンプルデータを投入（任意）

`sample_data.txt` は商品・カテゴリ・テスト会員・管理者などの生 SQL です。
**マイグレーションでテーブルが作られた後**に流し込みます。

```bash
mysql -u root -p Timos < sample_data.txt
```

### 6. 開発サーバーを起動

```bash
python manage.py runserver
```

ブラウザで http://127.0.0.1:8000/ を開きます。

---

## アクセス先と動作確認

| 画面 | URL |
|------|-----|
| トップ（ランディング） | http://127.0.0.1:8000/ |
| ショップ（商品検索） | http://127.0.0.1:8000/shopapp/ |
| 会員ログイン | http://127.0.0.1:8000/shopapp/login |
| カート | http://127.0.0.1:8000/shopapp/cart |
| 管理者ログイン | http://127.0.0.1:8000/shopapp/admin/login/ |
| Django 標準管理サイト | http://127.0.0.1:8000/admin/ |

### テスト用アカウント（`sample_data.txt` 投入時）

| 種別 | ID | パスワード |
|------|----|-----------|
| 会員 | `user01` / `user02` / `user03` | `01` / `02` / `03` |
| 管理者 | `admin01` / `admin02` / `admin03` | `01` / `02` / `03` |

> Django 標準管理サイト（`/admin/`）を使う場合は別途
> `python manage.py createsuperuser` でスーパーユーザーを作成してください。

---

## ブランチ構成

| ブランチ | 用途 |
|----------|------|
| `main` | 安定版 |
| `develop` | 開発の統合先 |

---

## デザインシステム

UI は `shopapp/static/style.css` に集約しています。
- フォント：Zen Old Mincho（見出し）/ Zen Kaku Gothic New（本文）— Google Fonts から読み込み
- 配色トークン：クリーム地・フォレストグリーン・真鍮ゴールド（CSS カスタムプロパティ）
- 全テンプレートは `shopapp/templates/base.html` を `{% extends %}` で継承し、共通ヘッダー／フッターを共有

---

## ディレクトリ構成（抜粋）

```
Timos/
├── manage.py
├── requirements.txt
├── sample_data.txt              # サンプル投入用の生 SQL
├── .env.example                 # 環境変数のサンプル
├── config/                      # プロジェクト設定（settings, urls, wsgi …）
└── shopapp/                     # アプリ本体
    ├── models.py                # User / Category / Item / Cart / Purchase / Admin
    ├── views.py                 # 画面ロジック
    ├── urls.py                  # ルーティング
    ├── forms.py
    ├── migrations/
    ├── static/style.css         # デザインシステム CSS
    └── templates/               # base.html を継承する各画面
```

---

## 補足・注意点

- **開発用設定です。** `config/settings.py` は `DEBUG = True`、`ALLOWED_HOSTS = ['*']`、
  ソースに直書きの `SECRET_KEY` を含みます。本番では必ず環境変数化し、`DEBUG = False` に
  してください。
- **CSRF ミドルウェアは無効化されています**（`config/settings.py` の
  `CsrfViewMiddleware` がコメントアウト）。学習用途のための措置です。本番運用や公開時は
  有効化し、各フォームの `{% csrf_token %}` と合わせて利用してください。
- パスワードは平文で保存される簡易実装です。実運用では Django の認証
  （`django.contrib.auth`）やハッシュ化の導入を推奨します。
