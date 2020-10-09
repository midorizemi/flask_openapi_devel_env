# OpenAPI

APIの仕様を作成するためのツールです．
デファクトスタンダード的なツールになっているようです．

サードパーティライブラリとして，
- suwagger-ui
- openapi-generator
- openapi-hub

などが存在する．
ローカル開発環境では，UIとgeneratorで十分．

## suwagger-ui
Docker-composeでサーバーを起動したいとき．
Specificationファイル（yaml) は必ず `/usr/share/nginx/html/` に配置すること．
また，UIサーバーにSpecificationファイルを明示的に渡す必要ああり，環境変数で設定しておくこと．

```docker-compose.yml
swagger-ui:
  image: swaggerapi/swagger-ui
  container_name: "swagger-ui"
  ports:
    - "8002:8080"
  volumes:
    - ./src/openapi/sample1_api.yaml:/usr/share/nginx/html/sample1_api.yaml
  environment:
    API_URL: sample1_api.yaml
```


## openapi-generator
### openapi-generator インストール

Dockerが用意されているので，イメージをダウンロードして docker runで実行するのが一番安定している．

`docker pull openapitools/openapi-generator-cli`

docker-compose経由ではなぜか，マウントしたデータが読み込まれないので，dockerで実行すること．

```sh
❯ docker run --rm \
-v `pwd`/src:/local -v `pwd`/src/openapi:/local/openapi -v `pwd`/src/api:/local/api \
openapitools/openapi-generator-cli generate \
-i /local/openapi/openapi.yml \
-g python-flask \
-o /local/api

```


### 自動生成したソースコード 解読メモ
openapi-generatorを使って自動生成したflaskアプリ.
次は，自動生成した flast プロジェクト
```
❯ tree . -N --dirsfirst
.
├── openapi_server
│   ├── controllers
│   │   ├── __init__.py
│   │   ├── pets_controller.py
│   │   └── security_controller_.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── base_model_.py
│   │   ├── error.py
│   │   └── pet.py
│   ├── openapi
│   │   └── openapi.yaml
│   ├── test
│   │   ├── __init__.py
│   │   └── test_pets_controller.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── encoder.py
│   ├── typing_utils.py
│   └── util.py
├── Dockerfile
├── README.md
├── git_push.sh
├── requirements.txt
├── setup.py
├── test-requirements.txt
└── tox.ini

5 directories, 22 files
```

APIアプリの本体は，openapi_server
生成時点で，reqiurments.txtの中身は次の通り．

```
connexion[swagger-ui] >= 2.6.0; python_version>="3.6"
# 2.3 is the last version that supports python 3.4-3.5
connexion[swagger-ui] <= 2.3.0; python_version=="3.5" or python_version=="3.4"
# connexion requires werkzeug but connexion < 2.4.0 does not install werkzeug
# we must peg werkzeug versions below to fix connexion
# https://github.com/zalando/connexion/pull/1044
werkzeug == 0.16.1; python_version=="3.5" or python_version=="3.4"
swagger-ui-bundle >= 0.0.2
python_dateutil >= 2.6.0
setuptools >= 21.0.0
```

バージョンの通り，Python3.4以上であることが前提となる．


エントリポイントは， `__main__.py` となっていてここでアプリケーションのインスタンスを生成している．

各パスへのリクエストのエンドポイントは，
APIの仕様に従って，x-openapi-router-controller のコントローラが定義されている．
