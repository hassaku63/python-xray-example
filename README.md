# README

X-Ray SDK (for Python) を動かしてみるサンプルアプリケーションです

## アプリケーションの概要

外部システムで発生した issue のオープン/クローズイベントを何らかの方法で受け付けて、社内の issue tracking に連携する仕組み、を想定しています（例えば Datadog 等の監視によるアラート, GitHub Actions の実行結果を webhook 連携したようなもの）

今回例示するソースでは、連携先の issue tracking には Backlog を利用しています

### 構成

Step Functions のステートマシンを2つ構築します。
それぞれ外部システムで発生した issue の「発生」と「復旧(解消)」の webhook イベントよしなに変換したものを入力に受け付けて動作するような想定をしています

（以下蛇足）

外部システムから Webhook 経由でイベントを飛ばす想定ですが、そこから Step Functions に連携するまでの部分は今回作っていません。
ミニマムに作るのであれば API Gateway を噛ませて後ろの Lambda でよしなに実装する案か、あるいは（外部システム側が対応しているなら） Webhook を直接 EventBridge に連携し、Rule でイベント種別 (open or close) をふるい分けして Rule の後段に構成した SQS + Lambda あたりにステートマシンを叩かせるような構成が考えられます。

また、今回の実装では API Token などの機密情報が Lambda の環境変数に暗号化しない状態で直接入ってしまいます。
手抜き実装ゆえそうなっていますが、本来的には秘匿対象の情報は Secret Manager あたりに持たせる仕様とするのが推奨です。

## Deploy

デプロイの実行環境として以下が必要です。
Node.js は Serverless Framework が動作するバージョンなら何でもよいです。

- Python 3.8
- Node.js 18.x + Serverless Framework 3.x
- AWS CLI と、有効なプロファイルの設定（CloudFormation Deploy が実行できるだけの権限を持ったポリシーが必要）

### .env

1. Node.js + Serverless Framework 関係の依存をインストール (npm install)
2. Python の依存関係をインストール (pip install, 手元で動かさずにデプロイするだけなら実行不要)
3. `sample.env` を複製して `.env` を作成し、適宜値を埋める
4. デプロイ (npx sls deploy -s _stage-name_ --region _region-name_)