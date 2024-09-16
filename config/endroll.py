
from aqt import QTimer
from aqt import QWidget,QScrollArea
from os.path import join, dirname


background = "Space.png"

class EndrollWidget(QWidget):
    def __init__(self, parent, scroll_area:QScrollArea):
        super().__init__(parent)
        self.scroll_area = scroll_area
        backColor = "rgb(54, 54, 54)"

        addon_path = dirname(__file__)
        background_image = join(addon_path, background).replace('\\', '/')

        self.scroll_area.setObjectName("myScrollArea")
        self.scroll_area.setStyleSheet("""
            QAbstractScrollArea#myScrollArea {
                background-image: url(%s);
                background-attachment: fixed;
                background-color: %s;

            }
        """ % (background_image, backColor))

        # QTimerを作成
        self.timer = QTimer()
        # ﾀｲﾏｰのﾀｲﾑｱｳﾄｲﾍﾞﾝﾄにｽｸﾛｰﾙ位置を更新する関数を接続
        self.timer.timeout.connect(self.scroll_to_bottom)

    def scroll_to_bottom(self):
        try:
            current_value = self.scroll_area.verticalScrollBar().value()
            max_value = self.scroll_area.verticalScrollBar().maximum()

            if current_value < max_value:
                self.scroll_area.verticalScrollBar().setValue(current_value + 1)
            else:
                self.timer.stop()
        except Exception as e:
            self.timer.stop()

    def showEvent(self, event):
        # ﾀﾌﾞが表示されたときにﾀｲﾏｰを開始（1000ﾐﾘ秒＝1秒ごとに更新）
        self.timer.start(50)

    def hideEvent(self, event):
        # ﾀﾌﾞが非表示になったときにﾀｲﾏｰを停止
        self.timer.stop()
        self.scroll_area.verticalScrollBar().setValue(0)