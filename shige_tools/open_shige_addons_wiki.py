
from aqt import QLabel, Qt, mw
from aqt.utils import openLink

class WikiQLabel(QLabel):
    def __init__(self, text, url, parent=None):
        super().__init__(parent)
        self.url = url

        if isinstance(text, QLabel):
            text = text.text()

        self.setText(f'{text} <a href="{url}" style="text-decoration:none;">❔️</a>')
        self.setOpenExternalLinks(True)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.linkActivated.connect(self.open_link)
        # self.setCursor(Qt.CursorShape.PointingHandCursor)

    def open_link(self, link):
        openLink(link)