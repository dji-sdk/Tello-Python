# -*- coding: utf-8 -*-

"""
ドローンが人を認識していない時に，人を探すクラスを入れたモジュール
"""

class Default:
    """
    人を探索，検知するクラス

    Attributes:
        drone obj:
            操作するドローン
    """
    def __init__(self, drone):
        """
        Defaultクラスの初期化
        """
        self.drone = drone


    def detect(self, frame):
        """
        被災者をyoloを用いて発見，bboxを作成するメソッド

        Parameters:
            frame int:
                カメラ画像

        Return:
            bbox int:
                検知した人の領域
        """
        bound = None







        # 人を検知後，self.drone.detect_flag を立てる
        return bound