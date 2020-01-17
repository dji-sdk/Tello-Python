# -*- coding: utf-8 -*-
import cv2


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

        return success, close


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
