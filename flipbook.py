

from aqt.qt import QWidget,QLabel,QPixmap
from aqt import QTimer, Qt, mw
import os
from os.path import join, dirname
import random
from typing import List



class Flipbook(QWidget) :

    """
    【 透過pngの連番画像をｱﾆﾒ化するｸﾗｽ 】
    pngﾌｧｲﾙのみに対応しています
    image : ﾌｫﾙﾀﾞの名前
    scale : 拡大率
    loop : 繰り返しの有無
    filename : ﾌｧｲﾙの名前
    frame_rate : 1秒間のｺﾏ数(24fps)
    """

    count_image = 0
    total_count_image: List[QPixmap] = []
    loop = False

    def __init__(self,image:str,scale:float=1,
                loop:bool= False,filename=""
                ,frame_rate:int=24):
        super().__init__(mw)

        # ｸﾗｽ内変数をｲﾝｽﾀﾝｽ作成時に初期化
        self.count_image = 0
        self.total_count_image = []
        self.loop = loop

        # ﾌﾚｰﾑﾚｰﾄを1000分のﾐﾘ秒に変換(24fps→41min)
        self.frame_rate = int(1000 / frame_rate)

        # 背景を透過し､最前面に表示
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        # 背景を透明にします
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # ｳｨｼﾞｴｯﾄの下にあるものをｸﾘｯｸ可能にします
        # NOTE: 上と下の関数を一行にするとERRORが発生します
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.add_image(image,scale,loop,filename,frame_rate)

    def add_image(self,image,scale,loop,filename,frame_rate):
        # 最初のｲﾒｰｼﾞを取得する
        self.total_count_image = self.load_image(image,filename)
        if self.total_count_image == None:
            return
        # 画像の読み込みと表示
        self.pixmap = QPixmap(self.total_count_image[self.count_image])
        # 拡大縮小
        self.pixmap = self.pixmap.scaled(self.pixmap.width()* scale,self.pixmap.height() * scale)

        # アニメを表示するラベルの作成
        self.flip_label = QLabel(self)

        # 画像の表示
        self.flip_label.setPixmap(self.update_flip())

        # ラベルのサイズを画像に合わせる
        self.flip_label.setFixedSize(self.pixmap.size())

        # ウィジェットのサイズを画像に合わせる
        self.setFixedSize(self.pixmap.size())

        # 親ウィンドウの中央に移動する
        # 親ウィンドウ
        mw_w = mw.frameGeometry().width()
        mw_h = mw.frameGeometry().height()

        # 子ウィンドウ
        image_h = self.pixmap.height()
        image_w = self.pixmap.width()
        image_y = int(( mw_h /2) - image_h/2 )
        image_x = int(( mw_w /2) - image_w/2 )

        # NOTE: 子のXとYの原点は親の左上隅になる
        self.move(image_x,image_y)

        # Qtimer
        self.Flip_timer = QTimer(self)
        self.Flip_timer.timeout.connect(lambda:self.count_flip(loop))
        self.Flip_timer.setInterval(self.frame_rate)
        self.Flip_timer.start()  # ﾃﾞﾌｫﾙﾄ40(24fps)1000ミリ秒 = 1秒,

    # 連番画像を数字で変更
    def update_flip(self):
        return self.total_count_image[self.count_image]

    # 画像のｱｯﾌﾟﾃﾞｰﾄ
    def count_flip(self,loop):
        # ｶｳﾝﾄｱｯﾌﾟ
        self.count_image += 1
        # 画像の更新
        self.flip_label.setPixmap(self.update_flip())

        # 画像がすべて表示後
        if self.count_image >= len(self.total_count_image)-1:
            if loop :
                # ループ再生する場合は最初のフレームへ
                self.count_image = 0
            else :
            # ﾀｲﾏｰをｽﾄｯﾌﾟ
                del self.pixmap # ﾒﾓﾘをｸﾘｱ
                self.total_count_image.clear() # ﾒﾓﾘをｸﾘｱ
                self.Flip_timer.stop()
                # ｳｲﾝﾄﾞｳを閉じる
                self.close()
                # NOTE: ﾒﾓﾘをｸﾘｱしないとQpixmapでﾒﾓﾘｰﾘｰｸが発生

    def load_image(self,image,filename):
        # 連番画像の読み込み
        addon_path = dirname(__file__)
        # 連番画像ﾌｫﾙﾀﾞからﾌｧｲﾙを読み込み
        self.user_files_folder = join(addon_path, r"media/", image)
        try :
            # ﾌｫﾙﾀﾞ名のﾘｽﾄを取得
            folders = [f for f in os.listdir(self.user_files_folder)
                    if os.path.isdir(join(self.user_files_folder, f))]
        except :
            return None
        # ﾌｫﾙﾀﾞ内に何もなければ
        if not folders:
            return None
        # ﾌｫﾙﾀﾞをﾗﾝﾀﾞﾑにひとつ選択
        random_folder = random.choice(folders)
        folder_path = join(self.user_files_folder,random_folder)

        # フォルダ内のファイル数をカウント
        num_frames = len([f for f in os.listdir(folder_path) if f.endswith('.png')])
        # 画像ﾘｽﾄを取得
        self.total_count_image.clear()  # ﾒﾓﾘをｸﾘｱ
        self.total_count_image = [QPixmap(f'{folder_path}/{random_folder} ({i+1}).png') for i in range(num_frames)]
        self.count_image = 0  # ﾒﾓﾘをｸﾘｱ
        return self.total_count_image


# ﾎﾟｯﾌﾟｱｯﾌﾟする関数
def show_popup(image:str,scale,loop,filename):
    if image == None:
        pass
    # ポップアップ表示する
    flip = Flipbook(image,scale,loop)
    flip.show()


