
from aqt import (QApplication, QDialog, QFont, QFont, QFrame, QFrame, QHBoxLayout, QKeySequence,
    QLineEdit, QPainter, QPainterPath, QRectF, QScrollArea, QTabWidget, QWidget,Qt)
from aqt import QVBoxLayout, QLabel, QPushButton
from aqt import mw
from os.path import join, dirname
from aqt import QIcon
from aqt import QPixmap
from aqt.utils import openLink,tooltip
from aqt import QCheckBox
import platform
from .config import listOfSupportedPatrons as CreditData
from .config.endroll import EndrollWidget

TOGGLE_PRINT = False
THE_ADDON_NAME = "AnkiRestart by Shige"
BUTTON_WIDTH = 95

SET_LINE_EDID_WIDTH = 400
MAX_LABEL_WIDTH = 100

SET_SCALEDTOWIDTH = 400

def toggle_print(printtext):
    if TOGGLE_PRINT:
        print(">>>>>>>>>>>>>>>>>>",str(printtext))

# ---- ﾌｫﾝﾄの設定画面を作成するｸﾗｽ --------
class SetFontViewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(400)

        config = mw.addonManager.getConfig(__name__)
        self.Restart_Shift_enabled = config["Restart_Shift_enabled"]
        self.console_mode = config["console_mode"]
        self.AutoRestart_AfterSafeMode = config["AutoRestart_AfterSafeMode"]
        self.soundeffect = config["sound effect"]
        self.errorAnimationEnable = config["errorAnimationEnable"]
        self.autoRestartAfterUpdatingAddons = config["autoRestartAfterUpdatingAddons"]

        self.restart_shortcut =  config["restart_shortcut"]

        self.custom_excutable =  config["custom_excutable"]
        self.custom_path =  config["custom_path"]
        self.direct_mode = config["direct_mode"]

        self.custom_base_folder = config["custom_base_folder"]
        self.base_folder_path = config["base_folder_path"]

        self.menu_icon_enabled = config["menu_icon_enabled"]

        # Set window icon
        addon_path = dirname(__file__)
        self.icon_path = join(addon_path, r"Restart.png")
        self.logo_icon = QIcon(self.icon_path)
        self.setWindowIcon(self.logo_icon)

        # Set image on QLabel
        self.patreon_label = QLabel()
        patreon_banner_path = join(addon_path, r"banner_AnkiRestart.jpg")
        pixmap = QPixmap(patreon_banner_path)
        pixmap = pixmap.scaledToWidth(SET_SCALEDTOWIDTH, Qt.TransformationMode.SmoothTransformation)
        pixmap = self.pixmap_round(pixmap)

        self.patreon_label.setPixmap(pixmap)
        self.patreon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.patreon_label.setFixedSize(pixmap.width(), pixmap.height())
        # Connect mousePressEvent to slot
        self.patreon_label.mousePressEvent = self.open_patreon_Link
        # Set cursor
        self.patreon_label.setCursor(Qt.CursorShape.PointingHandCursor)
        # Connect enterEvent and leaveEvent to slots
        self.patreon_label.enterEvent = self.patreon_label_enterEvent
        self.patreon_label.leaveEvent = self.patreon_label_leaveEvent

        self.setWindowTitle(THE_ADDON_NAME)

        # QPushButtonを作成して、フォント名をprintする
        button = QPushButton('OK')
        button.clicked.connect(self.handle_button_clicked)
        button.clicked.connect(self.hide)
        button.setFixedWidth(BUTTON_WIDTH)

        # QPushButtonを作成して、フォント名をprintする
        button2 = QPushButton('Cancel')
        button2.clicked.connect(self.cancelSelect)
        button2.clicked.connect(self.hide)
        button2.setFixedWidth(BUTTON_WIDTH)

        button3 = QPushButton('RateThis')
        button3.clicked.connect(self.open_rate_this_Link)
        button3.setFixedWidth(BUTTON_WIDTH)

        button4 = QPushButton('Help')
        button4.clicked.connect(self.open_help_Link)
        button4.setFixedWidth(BUTTON_WIDTH)

        # ｳｨﾝﾄﾞｳにQFontComboBoxとQLabelとQPushButtonを追加
        layout = QVBoxLayout()

        #------------checkbox-----------------

        shift_Text = "Restart SafeMode Enabled"
        self.restartShiftOn = QCheckBox(shift_Text, self)
        self.restartShiftOn.setChecked(self.Restart_Shift_enabled)
        self.restartShiftOn.stateChanged.connect(self.handle_interval_percentage_on)
        self.restartShiftOn.setToolTip("Restart Anki in Safe Mode, and add a red restart button to menu.")

        AutoRestart_AfterSafeModeText = "Auto Restart After SafeMode"
        self.AutoRestart_AfterSafeModeOn = QCheckBox(AutoRestart_AfterSafeModeText, self)
        self.AutoRestart_AfterSafeModeOn.setChecked(self.AutoRestart_AfterSafeMode)
        self.AutoRestart_AfterSafeModeOn.setToolTip("If restarted in Safe Mode, when Anki is closed, automatically start Anki in Normal Mode")
        self.AutoRestart_AfterSafeModeOn.stateChanged.connect(self.handle_auto_restart_after_safemode_on)

        consoleModeText = "Show console(Windows)"
        self.consoleModeOn = QCheckBox(consoleModeText, self)
        self.consoleModeOn.setChecked(self.console_mode)
        if not platform.system() == 'Windows':
            self.consoleModeOn.setEnabled(False)  # win以外はﾁｪｯｸﾎﾞｯｸｽを無効化する
        self.consoleModeOn.stateChanged.connect(self.handle_value_of_card_status_on)
        self.consoleModeOn.setToolTip("Show console when restarting, probably only needed for Windows.")


        soundeffectText = "Sound Effect"
        self.soundeffectOn = QCheckBox(soundeffectText, self)
        self.soundeffectOn.setChecked(self.soundeffect)
        self.soundeffectOn.stateChanged.connect(self.handle_value_of_sound_effect_on)
        self.soundeffectOn.setToolTip("Sound effect when restarting Anki.")

        errorAnimation = "Error Animation"
        self.errorAnimationEnableOn = QCheckBox(errorAnimation, self)
        self.errorAnimationEnableOn.setChecked(self.errorAnimationEnable)
        self.errorAnimationEnableOn.stateChanged.connect(self.handle_error_animation_enable_on)
        self.errorAnimationEnableOn.setToolTip(
        "Play animation if reboot fails. (Probably when the restart execution app has been removed by antivirus software.)"
        )
        autoRestartAfterUpdatingAddonsText = "Restart After Updating Addons"
        self.autoRestartAfterUpdatingAddonsOn = QCheckBox(autoRestartAfterUpdatingAddonsText, self)
        self.autoRestartAfterUpdatingAddonsOn.setChecked(self.autoRestartAfterUpdatingAddons)
        self.autoRestartAfterUpdatingAddonsOn.stateChanged.connect(self.handle_auto_restart_after_updating_addons_on)
        self.autoRestartAfterUpdatingAddonsOn.setToolTip(
            "Show restart popup when updating add-ons.")

        self.restart_shortcut_label = self.create_line_edits_and_labels(
            "restart_shortcut", self.restart_shortcut, "Restart Shortcut")

        self.custom_excutable_label = self.create_checkbox(
        "Use Anki path manually","custom_excutable")
        tooltip_text = """
win : C:\Program Files\Anki\\anki.exe
Mac : /Applications/Anki.app
Linux : anki
"""
        self.custom_excutable_label.setToolTip(tooltip_text)

        self.custom_path_label = self.create_line_edits_and_labels(
        "custom_path", self.custom_path, "Anki path")

        self.direct_mode_label = self.create_checkbox(
            "No use executable file(Linux/Mac)","direct_mode")
        self.direct_mode_label.setToolTip(
        "Restart without waiting for Anki to close, may fail for some devices.")

        self.custom_base_folder_label = self.create_checkbox(
            "Use custom base folder(-b)","custom_base_folder"
        )
        tooltip_text2 = """
win : C:\path\\to\AnkiDataFolder
Mac/Linux : /path/to/AnkiDataFolder
"""
        self.custom_base_folder_label.setToolTip(tooltip_text2)



        self.base_folder_path_label = self.create_line_edits_and_labels(
            "base_folder_path",self.base_folder_path,"AnkiData"
        )

        self.menu_icon_enabled_label = self.create_checkbox(
            "Show icons on menubar","menu_icon_enabled"
        )

        layout.addWidget(self.patreon_label)

        # -----------------------------------------------------
        the_tab = QTabWidget(self)

        app_style = QApplication.instance().styleSheet()
        if not app_style:
            the_tab.setStyleSheet("background-color: transparent;")

        layout_one = QVBoxLayout()
        tab_one = QWidget()

        layout_one.addWidget(self.menu_icon_enabled_label)
        layout_one.addWidget(self.autoRestartAfterUpdatingAddonsOn)
        layout_one.addLayout(self.restart_shortcut_label)

        layout_one.addStretch(1)
        tab_one.setLayout(layout_one)

        # ------------------------------------------------------
        tab_two = QWidget()
        layout_two = QVBoxLayout()

        layout_two.addWidget(self.restartShiftOn)
        layout_two.addWidget(self.AutoRestart_AfterSafeModeOn)

        layout_two.addWidget(self.create_separator())#----------------
        layout_two.addWidget(self.consoleModeOn)

        layout_two.addWidget(self.create_separator())#----------------
        layout_two.addWidget(self.direct_mode_label)

        layout_two.addStretch(1)

        tab_two.setLayout(layout_two)

        # ------------------------------------------------------
        tab_three = QWidget()
        layout_three = QVBoxLayout()

        layout_three.addWidget(self.soundeffectOn)
        layout_three.addWidget(self.errorAnimationEnableOn)

        layout_three.addStretch(1)
        tab_three.setLayout(layout_three)

        # ------------------------------------------------------
        tab_four = QWidget()
        layout_four = QVBoxLayout()

        layout_four.addWidget(self.custom_excutable_label)
        layout_four.addLayout(self.custom_path_label)

        layout_four.addWidget(self.create_separator())#----------------

        layout_four.addWidget(self.custom_base_folder_label)
        layout_four.addLayout(self.base_folder_path_label)

        layout_four.addStretch(1)
        tab_four.setLayout(layout_four)

        # ------------------------------------------------------

        # tab ｸﾚｼﾞｯﾄ =================================================
        credit_layout = QVBoxLayout()
        credit_data_attributes = [
                                'credits',
                                'caractor',
                                'sound',
                                'addons',
                                'budle',
                                'patreon',
                                'thankYou',
                                ]

        font = QFont("Times New Roman", 15)
        # font.setItalic(True)
        for attribute in credit_data_attributes:
            label = QLabel(f'<style>body, a {{ color: white; }}</style><body>{getattr(CreditData, attribute)}</body>')
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(font)
            label.setOpenExternalLinks(True)
            credit_layout.addWidget(label)

        credit_layout.addStretch(1)

        # (Credit)ｽｸﾛｰﾙｴﾘｱを作成 ----------------------
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        tab_Credit = EndrollWidget(self,scroll_area)
        tab_Credit.setLayout(credit_layout)
        scroll_area.setWidget(tab_Credit)

        # ---- ﾀﾌﾞの設定 --------------------------------------
        the_tab.addTab(tab_one,"option")
        the_tab.addTab(tab_two,"develop")
        the_tab.addTab(tab_three,"sound")
        the_tab.addTab(tab_four,"custom")
        the_tab.addTab(scroll_area,"credit")
        layout.addWidget(the_tab)
        # --- ﾎﾞﾀﾝの設定 --------------------------------------

        button_layout = QHBoxLayout()
        button_layout.addWidget(button)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)
        button_layout.addWidget(button4)
        
        
        button_layout.addStretch(1)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        music_sound_play(r"open")

    # ------------ patreon label----------------------
    def patreon_label_enterEvent(self, event):
        addon_path = dirname(__file__)
        patreon_banner_hover_path = join(addon_path, r"Patreon_banner.jpg")
        self.pixmap = QPixmap(patreon_banner_hover_path)
        self.pixmap = self.pixmap.scaledToWidth(SET_SCALEDTOWIDTH, Qt.TransformationMode.SmoothTransformation)
        self.pixmap = self.pixmap_round(self.pixmap)
        self.patreon_label.setPixmap(self.pixmap)

    def patreon_label_leaveEvent(self, event):
        addon_path = dirname(__file__)
        patreon_banner_hover_path = join(addon_path, r"banner_AnkiRestart.jpg")
        self.pixmap = QPixmap(patreon_banner_hover_path)
        self.pixmap = self.pixmap.scaledToWidth(SET_SCALEDTOWIDTH, Qt.TransformationMode.SmoothTransformation)
        self.pixmap = self.pixmap_round(self.pixmap)
        self.patreon_label.setPixmap(self.pixmap)
    # ------------ patreon label----------------------

    def pixmap_round(self,pixmap):
        path = QPainterPath()
        path.addRoundedRect(QRectF(pixmap.rect()), 10, 10)  # 角の丸み
        rounded_pixmap = QPixmap(pixmap.size())
        rounded_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        pixmap = rounded_pixmap
        return pixmap

    # ｾﾊﾟﾚｰﾀを作成する関数=========================
    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("border: 1px solid gray")
        return separator
    # =================================================

    # ﾁｪｯｸﾎﾞｯｸｽを生成する関数=======================
    def create_checkbox(self, label, attribute_name):
        checkbox = QCheckBox(label, self)
        checkbox.setChecked(getattr(self, attribute_name))

        def handler(state):
            if state == 2:
                setattr(self, attribute_name, True)
            else:
                setattr(self, attribute_name, False)
            music_sound_play(r"select")

        checkbox.stateChanged.connect(handler)
        return checkbox
    #=================================================

    # ﾃｷｽﾄﾎﾞｯｸｽを作成する関数=========================
    def create_line_edits_and_labels(self, list_attr_name, list_items, b_name, b_index=None):

        main_layout = QVBoxLayout()
        items = list_items if isinstance(list_items, list) else [list_items]
        for i, item in enumerate(items):
            line_edit = QLineEdit(item)
            line_edit.textChanged.connect(lambda text,
                                        i=i,
                                        name=list_attr_name: self.update_list_item(name, i, text))
            line_edit.setMaximumWidth(SET_LINE_EDID_WIDTH)

            if i == 0:
                layout = QHBoxLayout()
                if b_index is not None:
                    b_name_attr = getattr(self, b_name)
                    label_edit = QLineEdit(b_name_attr[b_index])
                    label_edit.textChanged.connect(lambda text,
                                                i=i,
                                                b_name=b_name: self.update_label_item(b_name, b_index, text))
                    label_edit.setFixedWidth(MAX_LABEL_WIDTH)
                    layout.addWidget(label_edit)
                else:
                    label = QLabel(b_name)
                    label.setFixedWidth(MAX_LABEL_WIDTH)
                    layout.addWidget(label)
            else:
                label = QLabel()
                label.setFixedWidth(MAX_LABEL_WIDTH)
                layout = QHBoxLayout()
                layout.addWidget(label)

            line_edit = QLineEdit(item)
            line_edit.textChanged.connect(lambda text,
                                        i=i,
                                        name=list_attr_name: self.update_list_item(name, i, text))
            line_edit.setMaximumWidth(SET_LINE_EDID_WIDTH)
            layout.addWidget(line_edit)
            main_layout.addLayout(layout)
        return main_layout

    def update_label_item(self, b_name, index, text):
        update_label = getattr(self,b_name)
        update_label[index] = text
    def update_list_item(self, list_attr_name, index, text):
        # list_to_update = getattr(self, list_attr_name)
        # list_to_update[index] = text
        list_to_update = getattr(self, list_attr_name)
        if isinstance(list_to_update, list):
            list_to_update[index] = text
        else:
            setattr(self, list_attr_name, text)
    # ===================================================

    #-- open patreon link-----
    def open_patreon_Link(self,url):
        music_sound_play(r"openlink")
        openLink("http://patreon.com/Shigeyuki")

    #-- open rate this link-----
    def open_rate_this_Link(self,url):
        music_sound_play(r"Ratethis")
        openLink("https://ankiweb.net/shared/review/237169833")

    #-- open help link-----
    def open_help_Link(self,url):
        music_sound_play(r"Ratethis")
        openLink("https://forums.ankiweb.net/t/ankirestart-support-thread/34465")


    # --- cancel -------------
    def cancelSelect(self):
        music_sound_play(r"cancel")
        emoticons = [":-/", ":-O", ":-|"]
        selected_emoticon = random.choice(emoticons)
        tooltip("Canceled " + selected_emoticon)
        self.close()

    #------------checkbox-----------------
    def handle_interval_percentage_on(self, state):
        if state == 2:
            toggle_print('set interval True')
            self.Restart_Shift_enabled = True
        else:
            toggle_print('set interval False')
            self.Restart_Shift_enabled = False
        music_sound_play(r"select")

    def handle_value_of_card_status_on(self, state):
        if state == 2:
            toggle_print('set card status True')
            self.console_mode = True
        else:
            toggle_print('set card status False')
            self.console_mode = False
        music_sound_play(r"select")

    def handle_auto_restart_after_safemode_on(self, state):
        if state == 2:
            toggle_print('set card status True')
            self.AutoRestart_AfterSafeMode = True
        else:
            toggle_print('set card status False')
            self.AutoRestart_AfterSafeMode = False
        music_sound_play(r"select")

    def handle_value_of_sound_effect_on(self, state):
        if state == 2:
            toggle_print('set card status True')
            self.soundeffect = True
        else:
            toggle_print('set card status False')
            self.soundeffect = False
        music_sound_play(r"select")

    def handle_error_animation_enable_on(self, state):
        if state == 2:
            toggle_print('set card status True')
            self.errorAnimationEnable = True
        else:
            toggle_print('set card status False')
            self.errorAnimationEnable = False
        music_sound_play(r"select")

    def handle_auto_restart_after_updating_addons_on(self, state):
        if state == 2:
            toggle_print('set card status True')
            self.autoRestartAfterUpdatingAddons = True
        else:
            toggle_print('set card status False')
            self.autoRestartAfterUpdatingAddons = False
        music_sound_play(r"select")


    #------------checkbox-----------------

    def update_shortcut(self):
        from . import restart_Action,Anki_Restart_menu
        if restart_Action is not None:
            config = mw.addonManager.getConfig(__name__)
            restart_shortcut = config["restart_shortcut"]
            restart_Action.setShortcut(QKeySequence(restart_shortcut))

    def handle_button_clicked(self):
        music_sound_play(r"OK")
        self.save_config_fontfamiles()
        self.update_shortcut()

        emoticons = [":-)", ":-D", ";-)"]
        selected_emoticon = random.choice(emoticons)
        tooltip("Changed setting " + selected_emoticon)

    def save_config_fontfamiles(self):
        config = mw.addonManager.getConfig(__name__)
        config["Restart_Shift_enabled"] = self.Restart_Shift_enabled
        config["console_mode"] = self.console_mode
        config["AutoRestart_AfterSafeMode"] = self.AutoRestart_AfterSafeMode
        config["sound effect"] = self.soundeffect
        config["errorAnimationEnable"] = self.errorAnimationEnable
        config["autoRestartAfterUpdatingAddons"] = self.autoRestartAfterUpdatingAddons
        config["restart_shortcut"] =  self.restart_shortcut
        config["custom_excutable"] =  self.custom_excutable
        config["custom_path"] = self.custom_path
        config["direct_mode"] = self.direct_mode

        config["custom_base_folder"] = self.custom_base_folder
        config["base_folder_path"] = self.base_folder_path

        config["menu_icon_enabled"] = self.menu_icon_enabled

        mw.addonManager.writeConfig(__name__, config)
        toggle_print(config)

# -----------効果音の追加--------------
import random
from aqt.sound import play ,clearAudioQueue
import os
# ﾌｫﾙﾀﾞｰのﾊﾟｽ
def folder_file_path(folder):
    addon_path = dirname(__file__)
    audio_folder = join(addon_path, r'media/',folder)
    # ﾌｫﾙﾀﾞとﾃｷｽﾄを除外する
    audioName_list = [f for f in os.listdir(audio_folder)
                    if os.path.isfile(os.path.join(audio_folder, f))
                    and not f.endswith('.txt')]
    if not audioName_list:
        return None
    audio_name = '/{}'.format(random.choice(audioName_list))
    audio_path = audio_folder + audio_name
    return audio_path

def music_sound_play(folder):
    config = mw.addonManager.getConfig(__name__)
    if config["sound effect"]:
        path = folder_file_path(folder)
        if path:
            clearAudioQueue()
            play(path)
# -----------効果音の追加--------------

def SetAnkiRestartConfig():
    font_viewer = SetFontViewer()
    try:
        font_viewer.exec()
    except:
        font_viewer.exec_()
