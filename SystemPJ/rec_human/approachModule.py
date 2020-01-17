# -*- coding: utf-8 -*-

import time
import cv2


class Approach:


    def __init__(self, drone):
        self.drone = drone
        self.DetectFlag = False
        self.CloseFlag = False

    
    def process(self):

        
        while True:

            # droneから画像を取得，表示する
            frame = self.drone.read() # 取得した画像がからであれば処理を1つスキップ
            if frame is None or frame.size == 0: 
                continue

            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) # cv2用にrbgの並びを入れ替え
            small_image = cv2.resize(image, dsize=(480,360)) # 画像をリサイズ

            cv2.imshow("camera", small_image) # 名称が"camera"のウィンドウに画像を表示
            cv2.waitKey(5) # よくわからんがこれを入れないと画像が正しく表示されない



            # 前回の処理で人を検知してるかどうかで処理を割り振る
            if not self.DetectFlag: # 検知していない場合はsearchメソッドで人を探す
                self.search(small_image) # searchメソッドに画像を渡し，処理を行う
            elif:
                self.approach(small_image) # approachメソッドに画像を渡し，処理を行う



            # approachメソッドでCloseFlagが立っていたらメソッドを終了
            if self.CloseFlag:
                break

        except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
		    print( "SIGINTを検知" )

    

    def search(self, frame):
        """
        被災者をyoloを用いて発見，bboxを作成するメソッド
        """
        
    def approach(self, frame):
        """
        searchメソッドで得たbboxを元に，cv2のトラッキングを用いながら
        被災者に接近するメソッド
        """
