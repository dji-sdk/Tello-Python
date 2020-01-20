# -*- coding: utf-8 -*-
import cv2
from detect_video import img, width, height
import time
import matplotlib.pyplot as plt
#import cv2 mainであるから必要なし?

"""
ドローンが認識した人に対して追跡するクラスを入れたモジュール
"""

class Approach:
    """
        追跡機能を持つクラス

        Attributes:
            drone obj:
                操作するドローン
            frame int:
                カメラ画像
            bbox int:
                認識した人のバウンディングボックスの情報
            track_type str:
                トラッカーのタイプ
                    ・Boosting
                    ・MIL
                    ・KCF
                    ・TLD
                    ・MedianFlow
                の4種類から選択(詳細はググれ)
    """

    def __init__(self, drone, frame, bbox, track_type):
        """
        Approachクラスの初期化
        """
        self.drone = drone # 操作するドローン
        self.tracker = self.select_tracker(track_type) # 指定されたタイプのトラッカーインスタンスの作成
        self.tracker.init(frame, bbox) # 作成したトラッカーの初期化．画像と認識した人の領域を与える

    def approach(self, frame):
        """
        認識した人をトラッカーを用いて追跡するメソッド

        Args:
            frame int:
                カメラ画像

        Return:
            success bool:
                追跡が成功しているかどうか
            close bool:
                追跡が終了したかどうか
        """

        # 追跡が失敗した場合にdrone.detect_flagを倒す
        # 追跡が成功し，接近できた場合にはdrone.close_flagを立てる

    def process(self):
        # self.search
        #探索したら
        # self.approach

        for i in range(5):
            time.sleep(1)
            img = self.drone.read()
            plt.imshow(img)





    def search(self):
        #cv2selectROIを使用する
        """
        被災者をyoloを用いて発見，bboxを作成するメソッド
        """

    def select_tracker(self, track_type):
        """
        コンストラクタで用いるトラッカー初期化用のメソッド

        Args:
            track_type str:
                指定されたタイプのトラッカー

        Returns:
            tracker obj:
                指定されたタイプのトラッカーインスタンス
        """
        tracker = cv2.TrackerBoosting_create() # テスト用に入れた

        return tracker

    def approach(self):

        #キャプチャで得たimageとboxを使用する
        drone.read_bbox()
        #追跡間隔 0.2s
        drone.tracking_interval = 0.2
        #人見つけたら接近　bboxの大きさを一定に保つよう動作


        """
        searchメソッドで得たbboxを元に，cv2のトラッキングを用いながら
        被災者に接近するメソッド
        """
        #bboxの中心を判定　4辺の位置を平均化
        #頂点の位置(22,134)(257,44)...から作られる長方形
        #bbox_length 縦横
        bcent = (0.5*(bbox(:,1)+bbox(:,1)),(0.5*(bbox(:,2)+bbox(:,2))))
        fcent = (120;160)#画像の中心点 ここは詳しく書き込み必須

        #追跡部分
        #距離判定は人のbox比/全体サイズで行う
        if ((detect_video.width)*(detect_video.height)/(240*320) < 0.1)#人との距離を保つ bbox小さくなりすぎた時
            drone.move_forward(0.2)
        elif ((detect_video.width)*(detect_video.height)/(240*320) > 0.6)
            drone.move_backward(0.2)
        else
            drone.move_stop#ホバリングのまま

        if (bcent(:,1)-fcent(:,1)=>40)#見つけた人が中央から外れたら中央に移動する操作
            drone.move_left(0.05)
            drone.rotate_ccw(5)
        elif (bcent(:,1)-fcent(:,1)=<-40)#優先度は上から順に?
            drone.move_right(0.05)
            drone.rotate_cw(5)
        elif (bcent(:,2)-fcent(:,2)=>20)
            drone.move_up(0.05)
        elif (bcent(:,2)-fcent(:,2)=<-20)
            self.move_down(0.05)
        else
            self.move_stop#ホバリングのまま　このプログラムは対話時も維持
