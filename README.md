
# Websocketハンズオン
## 概要
- **Websocketの概要**:
  Websocketは、双方向通信を可能にする技術。このハンズオンでは、ローカルネットワーク上で複数人が疑似チャットできる環境を構築する。
- **目標**:
  1. PythonでFastapiのWebsocketサーバーを立ち上げる。
  2. vscodeでDevcontainer開発環境を用いてnodeクライアントとしてWebsocket通信を行う。

※技術自体の詳細な説明は省略。GitやDocker、docker-composeの基本的なセットアップが済んでいることを前提とする。

## セットアップ
### サーバーのセットアップ
1. [リポジトリ](https://github.com/marcosanyo/websocket_server.git)をクローンする。
   ```sh
   git clone https://github.com/marcosanyo/websocket_server.git
   ```
2. ディレクトリに移動する。
   ```sh
   cd websocket_server
   ```
3. 特定のポートを指定したい場合は、`docker-compose.yaml`のポートを変更する。
   ```yaml
   services:
     websocket:
       ports:
         - "9001:9001"
   ```
4. Docker Composeでビルド＆立ち上げを行う。
   ```sh
   docker-compose up --build
   ```

### クライアントのセットアップ
1. [リポジトリ](https://github.com/marcosanyo/websocket_client.git)をクローンする。
   ```sh
   git clone https://github.com/marcosanyo/websocket_client.git
   ```
2. vscodeのホームディレクトリとして開く。
   ```sh
   code websocket_client
   ```
3. Visual Studio Codeで`ctrl+shift+P`キーから`Rebuild Container`を実行する。
   - Devcontainer拡張がインストールされている前提。

## 通信の確認
1. サーバーのローカルIPアドレスを調べる。
   - LinuxやWSL2の場合:
     ```sh
     ip route | awk '/default via/ {print $3}'
     ```
   - Macの場合:
     ```sh
     ipconfig getifaddr en0
     ```
2. クライアントのターミナルから以下のコマンドを実行する。
   ```sh
   wscat -c ws://<サーバーのIPアドレス>:9001/ws
   ```
   ※`<サーバーのIPアドレス>`には調べたIPアドレスを入力する。

3. 以下のように表示されれば接続完了。
   ```sh
   < Welcome, User1!
   < Server: User1 joined the chat
   ```

4. メッセージを入力しエンターを押すと、参加者全員にチャットが返る。
   ```sh
   > こんにちは
   < User1: こんにちは
   ```

## 備考
- 動作はMacで確認したが、LinuxやWindowsでも同様に動作するはず。
- WSL2ではWindows側にポートフォワーディングが必要な場合がある。`netsh`コマンドで対応可能らしい。(未確認)
  ```sh
  netsh interface portproxy add v4tov4 listenport=9001 listenaddress=0.0.0.0 connectport=9001 connectaddress=<WSL2のIPアドレス>
  ```
