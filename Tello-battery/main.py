#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello    # tello.pyをインポート
import time # time.sleepを使いたいので

# メイン関数本体
def main():

    # Telloクラスを使って，droneというインスタンス(実体)を作る
    drone = tello.Tello('', 8889) 

    #Ctrl+cが押されるまでループ
    try:
        while True:
            print( drone.get_battery() )    # バッテリー残量を問い合わせてプリント
            time.sleep(0.3) # 0.3s待つ

    except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
        print( "SIGINTを検知" )

    # telloクラスを削除
    del drone


# "python main.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":      # importされると"__main__"は入らないので，実行かimportかを判断できる．
    main()    # メイン関数を実行

