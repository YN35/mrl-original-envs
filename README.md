# オリジナルのMineRLの環境たち

## How to use

それぞれの環境内のrun.pyを実行する

## 環境一覧

### nativesurvival-v0

バニラのサバイバルの状態に極限まで近づけた環境

コマンド入力にも対応しており以下のようなコードを貼ることですべてのエージェントでコマンドが実行される。

```
env.set_next_chat_message("command")
env.set_next_chat_message("/tp @a 100 200 100")
```