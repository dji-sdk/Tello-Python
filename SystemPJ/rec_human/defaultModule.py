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
            success bool:
                人が検知できたかどうか

            bbox int:
                検知した人の領域
        """
        return success, bbox