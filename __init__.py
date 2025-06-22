
from aqt import (QAction, QDialog, QHBoxLayout, QIcon, QKeySequence, QLabel, QMenu, QPixmap,
                QPushButton, QSize,QSystemTrayIcon, QTimer, QVBoxLayout, mw ,gui_hooks)
import os
import sys
from os.path import join, dirname
import platform
import subprocess
import pathlib
import time
import stat
import traceback
from.flipbook import Flipbook
import zipfile
from aqt.utils import tooltip
from anki.hooks import wrap
from aqt import addons

from .path_manager import shige_p
from .shige_tools.ajt_utils_find_executable import find_executable

from .shige_pop.popup_config import set_gui_hook_change_log
set_gui_hook_change_log()



ADD_ON_TITLE = "Anki Restart by Shige"
Anki_Restart_menu = None

restart_actions = {}
# ﾒﾆｭｰﾊﾞｰに追加する関数
def add_menu_bar(name,func,pngname):
    addon_path = dirname(__file__)
    icon_path = join(addon_path, pngname)
    icon = QIcon(icon_path)
    menu = QAction(icon, name, mw)
    menu.triggered.connect(func)
    mw.form.menubar.addAction(menu)
    restart_actions[name] = menu


# ｼｽﾃﾑﾄﾚｲに追加する関数
def ankiRestart_tray(name,func,pngname):
    addon_path = dirname(__file__)
    icon_path = join(addon_path, pngname)
    icon = QIcon(icon_path)
    # 名前をｲﾝｽﾀﾝｽごとに変更する
    setattr(mw, name, QSystemTrayIcon(icon))
    getattr(mw, name).show()

    def on_tray_icon_clicked(reason):
        # 右ｸﾘｯｸを無視
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            new_icon_path = join(addon_path, "Restart_Shift.png")
            new_icon = QIcon(new_icon_path)
            getattr(mw, name).setIcon(new_icon)
            func(False)
            getattr(mw, name).activated.disconnect(on_tray_icon_clicked)

    # ｼｽﾃﾑﾄﾚｲｱｲｺﾝをｸﾘｯｸしたら実行
    getattr(mw, name).activated.connect(on_tray_icon_clicked)
    # ﾂｰﾙﾁｯﾌﾟに名前を追加
    getattr(mw, name).setToolTip(name)

AnkiRestart = pathlib.Path(__file__).parent.absolute()

WINDOWS = "Windows"
MAC = "Darwin"
LINUX= "Linux"

# ﾌﾟﾗｯﾄﾌｫｰﾑごとに実行ﾌｧｲﾙを変更----------------
if platform.system() == WINDOWS:
    PLATFROM_SYSTEM = WINDOWS
    # Win
    fname = os.path.join(AnkiRestart, 'ankiRestart_win.exe')
    fname_console = os.path.join(AnkiRestart, 'ankiRestart_win_console.exe')
elif platform.system() == MAC:
    PLATFROM_SYSTEM = MAC
    # Mac
    # fname = os.path.join(AnkiRestart, 'ankiRestart_mac.app')
    # fname_console = os.path.join(AnkiRestart, 'ankiRestart_mac.app')
    fname = os.path.join(AnkiRestart, 'ankiRestart_mac')
    fname_console = os.path.join(AnkiRestart, 'ankiRestart_mac')
else:
    PLATFROM_SYSTEM = LINUX
    # linux
    fname = os.path.join(AnkiRestart, 'ankiRestart_linux')
    fname_console = os.path.join(AnkiRestart, 'ankiRestart_linux')
# -----------------------------------------------

def mac_zip_extract(): # たぶんいらない
    if not PLATFROM_SYSTEM == MAC:
        return
    if not os.path.exists(fname):
        try:
            # zipﾌｧｲﾙのﾊﾟｽ
            zip_path = os.path.join(AnkiRestart, 'ankiRestart_mac.zip')
            # 解凍先のﾃﾞｨﾚｸﾄﾘ
            extract_path = os.path.join(AnkiRestart)
            # zipﾌｧｲﾙを開く
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # 解凍先のﾃﾞｨﾚｸﾄﾘにﾌｧｲﾙを展開する
                zip_ref.extractall(extract_path)

        except Exception as e:
            # 実行ﾌｧｲﾙが見つからない場合
            config = mw.addonManager.getConfig(__name__)
            if config["errorAnimationEnable"]:
                music_sound_play("message")
                file_path = r"Error"
                scale = 1
                loop = False
                filename = ""
                frame_rate = 20
                flip = Flipbook(file_path,scale,loop,filename,frame_rate)
                flip.show()
            else:
                from.flipbook import Flipbook
                traceback.print_exc()
                raise e
#--------------------------------------


# -----------効果音の追加--------------
import random
from aqt.sound import play ,clearAudioQueue

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


# ---------Anki Restart---------------------
def restart_mw_close():
    print("restart_mw_close")
    mw.close()

def restart_anki(toggle_Shift=False):

    # Macの場合はZIPを解凍する
    # mac_zip_extract()

    config = mw.addonManager.getConfig(__name__)

    sys_executable =  find_executable("anki") # ﾌﾟﾛｸﾞﾗﾑの実行ﾌｧｲﾙを探す
    if not sys_executable:
        sys_executable = sys.executable

    config['executable'] = sys_executable
    config["shiftRestart"] = toggle_Shift
    mw.addonManager.writeConfig(__name__, config)

    # ｺﾝｿｰﾙの有無(for windows)
    console_mode = config["console_mode"]
    direct_mode = config["direct_mode"]

    try:
        global fname
        # if direct_mode and PLATFROM_SYSTEM == MAC:
        #     subprocess.Popen([sys_executable], start_new_session=True)
        # elif direct_mode and PLATFROM_SYSTEM == LINUX:
        #     subprocess.Popen([sys_executable], start_new_session=True)

        # elif console_mode and PLATFROM_SYSTEM == WINDOWS:
        #     # ｺﾝｿｰﾙ有り(Windowsのみ)
        #     subprocess.Popen([fname_console])
        # else: # ｺﾝｿｰﾙ無し
        #     mode = os.stat(fname).st_mode
        #     # 実行可能な場合に実行権限を与える
        #     if not mode & stat.S_IXUSR:
        #         os.chmod(fname, mode | stat.S_IXUSR)
        #     subprocess.Popen([fname])

        if direct_mode and PLATFROM_SYSTEM == MAC:
            proc = subprocess.Popen([sys_executable], start_new_session=True)
            print(f"subprocess started: pid={proc.pid}")
        elif direct_mode and PLATFROM_SYSTEM == LINUX:
            proc = subprocess.Popen([sys_executable], start_new_session=True)
            print(f"subprocess started: pid={proc.pid}")

        elif console_mode and PLATFROM_SYSTEM == WINDOWS:
            proc = subprocess.Popen([fname_console])
            print(f"subprocess started: pid={proc.pid}")
        else: # ｺﾝｿｰﾙ無し
            mode = os.stat(fname).st_mode
            if not mode & stat.S_IXUSR:
                os.chmod(fname, mode | stat.S_IXUSR)
            proc = subprocess.Popen([fname])
            print(f"subprocess started: pid={proc.pid}")


        # 同期の設定を保存して無効化
        if config.get("disable_auto_sync_when_restarting", True):
            print("autoSync : ",mw.pm.profile["autoSync"])
            config["user_auto_Sync"]= mw.pm.profile["autoSync"]
            mw.pm.profile["autoSync"] = False
            mw.addonManager.writeConfig(__name__, config)
            print("user_auto_Sync : ",config["user_auto_Sync"])

            autosync =  mw.pm.auto_syncing_enabled()
            print(f"restart sync {autosync}")

        music_sound_play("RestartSound") # 効果音

        time.sleep(0.5)
        mw.close()

    except Exception as e:
        # 実行ﾌｧｲﾙが見つからない場合
        if config["errorAnimationEnable"]:
            music_sound_play("message") # 効果音
            file_path = r"Error"
            scale = 1
            loop = False
            filename = ""
            frame_rate = 20
            flip = Flipbook(file_path,scale,loop,filename,frame_rate)
            flip.show()
        else:
            print(e)
            traceback.print_exc()
        raise e

        # 実行ﾌｧｲﾙを使用せずに起動 !ﾊﾞｸﾞが多い
        # Mac>ﾀｽｸﾊﾞｰのｱｲｺﾝが重複
        # Linux>たまに失敗､ﾌﾘｰｽﾞ?
        # Win>たまに失敗
        # mw.close()
        # if toggle_Shift: # safe modeで起動
        #     subprocess.Popen([sys.executable,"--safemode"])
        # else: # 通常ﾓｰﾄﾞで起動
        #     subprocess.Popen([sys.executable])
# ---------Anki Restart---------------------

# Ankiをｾｰﾌﾓｰﾄﾞで再起動
def restart_anki_shift(toggle_Shift=True):
    config = mw.addonManager.getConfig(__name__)
    config['shiftRestart'] = True
    mw.addonManager.writeConfig(__name__, config)
    print(config)
    restart_anki(True)




def set_autoSync(*args,**kwargs):
    config = mw.addonManager.getConfig(__name__)
    if config.get("disable_auto_sync_when_restarting", True):
        try:# 同期の設定を復元する
            if not config["user_auto_Sync"] == None :
                # 保存した設定を読み込む
                mw.pm.profile["autoSync"] = config["user_auto_Sync"]
            # 設定を削除
            config["user_auto_Sync"] = None
            mw.addonManager.writeConfig(__name__, config)
        except Exception as e:
            # なんかのｴﾗｰ
            print("user_auto_Sync error",e)
            raise e



def setup_Restart_icon():
    config = mw.addonManager.getConfig(__name__)
    # try:# 同期の設定を復元する
    #     if not config["user_auto_Sync"] == None :
    #         # 保存した設定を読み込む
    #         mw.pm.profile["autoSync"] = config["user_auto_Sync"]
    #     # 設定を削除
    #     config["user_auto_Sync"] = None
    #     mw.addonManager.writeConfig(__name__, config)
    # except Exception as e:
    #     # なんかのｴﾗｰ
    #     print("user_auto_Sync error",e)
    #     raise e

    try:# ｱｲｺﾝを作成する
        if PLATFROM_SYSTEM == MAC:
            # Mac
            if config["Restart_Shift_enabled"] and config["menu_icon_enabled"]:
                ankiRestart_tray("sRestart",restart_anki_shift,"Restart_Shift.png")
            if config["menu_icon_enabled"]:
                ankiRestart_tray("Restart",restart_anki,"Restart.png")
        else:
            # win
            # inux
            if config["menu_icon_enabled"]:
                add_menu_bar("Restart",restart_anki,"Restart.png")
                # 設定でOFFにする
                if config["Restart_Shift_enabled"]:
                    add_menu_bar("sRestart",restart_anki_shift,"Restart_Shift.png")
    except Exception as e:
        print(e)
        raise e

def remove_menu_bar(name):
    action = restart_actions.get(name)
    if action:
        mw.form.menubar.removeAction(action)
        del restart_actions[name]

def set_icon_at_last_position(*args,**kwargs):
    try:
        config = mw.addonManager.getConfig(__name__)
        if config["menu_icon_enabled"]:
            remove_menu_bar("Restart")
            add_menu_bar("Restart", restart_anki, "Restart.png")
            if config["Restart_Shift_enabled"]:
                remove_menu_bar("sRestart")
                add_menu_bar("sRestart", restart_anki_shift, "Restart_Shift.png")
    except Exception as e:
        raise e
try:setup_Restart_icon()
except Exception as e:
    raise e
# # ﾒｲﾝｳｨﾝﾄﾞｳが開いたら実行
gui_hooks.main_window_did_init.append(set_icon_at_last_position)
gui_hooks.main_window_did_init.append(set_autoSync)

restart_Action = None

# ----------------設定ｳｨﾝﾄﾞｳを追加--------------------
from .AnkiRestartConfig import SetAnkiRestartConfig
from aqt.utils import qconnect
# ----- add-onのconfigをｸﾘｯｸしたら設定ｳｨﾝﾄﾞｳを開く -----
def add_config_button():
    global restart_Action
    global Anki_Restart_menu
    config = mw.addonManager.getConfig(__name__)
    mw.addonManager.setConfigAction(__name__, SetAnkiRestartConfig)
    # ----- ﾒﾆｭｰﾊﾞｰに追加 -----
    Addon_path = dirname(__file__)

    Anki_Restart_menu = QMenu(shige_p.anki_restart, mw)
    mw.form.menuTools.addMenu(Anki_Restart_menu)

    gear_icon_path = join(Addon_path, shige_p.gear_icon_png)
    addon_Action = QAction(QIcon(gear_icon_path),shige_p.anki_restart_setting, mw)
    qconnect(addon_Action.triggered, SetAnkiRestartConfig)
    Anki_Restart_menu.addAction(addon_Action)

    Anki_Restart_menu.addSeparator()

    icon_path = join(Addon_path, shige_p.restart_icon_png)
    restart_Action = QAction(QIcon(icon_path),shige_p.restart_anki_now, mw)
    qconnect(restart_Action.triggered, restart_anki)
    Anki_Restart_menu.addAction(restart_Action)

    restart_shortcut = config["restart_shortcut"]
    restart_Action.setShortcut(QKeySequence(restart_shortcut))

    if config["Restart_Shift_enabled"]:
        shift_icon_path = join(Addon_path, shige_p.restart_shift_icon_png)
        shift_restart_Action = QAction(QIcon(shift_icon_path),
                                    shige_p.restart_anki_now_with_the_shift_key_presse, mw)
        qconnect(shift_restart_Action.triggered, restart_anki_shift)
        Anki_Restart_menu.addAction(shift_restart_Action)

add_config_button()
# ---------------------------------------------





# 開発中 ==========

"""
from aqt.qt import *
import aqt

def print_shortcuts(widget, key):
    # If the widget is a QAction or QShortcut, and its shortcut matches the specified key, print it
    if isinstance(widget, QShortcut):
        shortcut = widget.key()
        if not shortcut.isEmpty() and shortcut.toString() == key:
            parent_name = widget.parent().objectName() if widget.parent() else 'No parent'
            print(f"QShortcut:{shortcut.toString()}, Parent: {parent_name}")
            widget.activated.connect(lambda: print(f"QShortcut '{shortcut.toString()}' activated"))
            widget.activatedAmbiguously.connect(lambda: print(f"QShortcut '{shortcut.toString()}' activated ambiguously"))
    # If the widget has child widgets, recursively call this function for each of them
    elif widget.children():
        for child in widget.children():
            print_shortcuts(child, key)

# Specify the key to search for
key = 'Z'

print_shortcuts(aqt.mw, key)
"""




"""
from aqt import QApplication
from aqt import QAction

def print_shortcuts(widget):
    # ｳｨｼﾞｪｯﾄが QAction の場合､ｼｮｰﾄｶｯﾄを表示
    if isinstance(widget, QAction):
        shortcut = widget.shortcut()
        if not shortcut.isEmpty():
            print(f"{widget.text()}:{shortcut.toString()}")
    # ｳｨｼﾞｪｯﾄが子ｳｨｼﾞｪｯﾄを持つ場合､それぞれに対してこの関数を再帰的に呼び出す
    elif widget.children():
        for child in widget.children():
            print_shortcuts(child)

print_shortcuts(mw)

"""

"""
# https://www.reddit.com/r/Anki/comments/8v8rya/comment/e1lmjcr/?utm_source=reddit&utm_medium=web2x&context=3

from aqt.qt import *
import aqt

dialog = aqt.dialogs.open("AddCards", mw) # or "Browser", "EditCurrent"
sc = dialog.findChildren(QShortcut)

for i in sc:
    parent_name = i.parent().objectName() if i.parent() else "No parent"
    print(f"Shortcut key: {i.key().toString()}, Parent widget: {parent_name}")


from aqt.qt import *
import aqt

for dialog_name, dialog_info in aqt.dialogs._dialogs.items():
    dialog = aqt.dialogs.open(dialog_name, mw)
    sc = dialog.findChildren(QShortcut)

    for i in sc:
        parent_name = i.parent().objectName() if i.parent() else "No parent"
        print(f"Dialog: {dialog_name}, Shortcut key: {i.key().toString()}, Parent widget: {parent_name}")



"""
"""

"""

"""
AddonsDialog
EditCurrent
sync_log


"""
"""

from aqt.qt import *
import aqt

dialog_names_to_open = ["Browser", "EditCurrent", "AddCards"]

for dialog_name, dialog_info in aqt.dialogs._dialogs.items():
    try:
        dialog = aqt.dialogs.open(dialog_name, aqt.mw)
        sc = dialog.findChildren(QShortcut)

        for i in sc:
            parent_name = i.parent().objectName() if i.parent() else "No parent"
            print(f"{i.key().toString()},{dialog_name},{parent_name}")

        dialog.close()
    except Exception as e:
        try:
            dialog.close()
        except:
            pass
        print(f"Failed to open dialog: {dialog_name}. Error: {e}")

# """



#--------- auto_restart_after_updating_addons ------------

# from aqt.addons import download_encountered_problem

# def my_show_log_to_user(parent, log):
#     config = mw.addonManager.getConfig(__name__)
#     if config["autoRestartAfterUpdatingAddons"]:
#         have_problem = addons.download_encountered_problem(log)
#         if have_problem:
#             pass # ｴﾗｰがあった場合は何もしない
#         else:
#             restart_anki(False)



def my_show_log_to_user(parent, log, *args, **kwargs):
    try:
        config = mw.addonManager.getConfig(__name__)
        if config["autoRestartAfterUpdatingAddons"]:
            have_problem = addons.download_encountered_problem(log)
            if have_problem:
                pass # ｴﾗｰがあった場合は何もしない
            else:
                dialog = ConfirmDialog(mw)
                returnValue = dialog.exec()
                if returnValue == QDialog.DialogCode.Accepted:
                    restart_anki(False)
    except Exception as e:
        d = True
        if d:tooltip("Anki Restart Error : " + str(e))
        pass


# mw.pm.meta["last_addon_update_check"] = 1722384000
# print("")
# print("")
# print("")
# print(mw.pm.meta["last_addon_update_check"])
# print("")
# print("")
# print("")


try:
    addons.show_log_to_user = wrap(addons.show_log_to_user, my_show_log_to_user)
except Exception as e:
    d = True
    if d:tooltip("Anki Restart Error : " + str(e))

try:
    from aqt import main
    main.show_log_to_user = wrap(main.show_log_to_user, my_show_log_to_user)
except Exception as e:
    d = True
    if d:tooltip("Anki Restart Error : " + str(e))



# def restart_after_addons_update(*args, **kwargs):
#     QTimer.singleShot(1000,try_restart_after_update)

# def try_restart_after_update():
#     try:
#         config = mw.addonManager.getConfig(__name__)
#         if config["autoRestartAfterUpdatingAddons"]:
#             dialog = ConfirmDialog()
#             returnValue = dialog.exec()
#             if returnValue == QDialog.DialogCode.Accepted:
#                 restart_anki(False)
#     except Exception as e:
#         pass
# # ﾌｯｸを登録する
# gui_hooks.addon_manager_did_install_addon.append(restart_after_addons_update)



class ConfirmDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfirmDialog, self).__init__(parent)

        self.setWindowTitle(ADD_ON_TITLE) # ﾀｲﾄﾙを設定

        Addon_path = dirname(__file__)
        Icon_path = join(Addon_path, r"Restart.png")
        shige_icon_path = join(Addon_path, r"shige_icon.png")
        self.setWindowIcon(QIcon(shige_icon_path))

        self.layout = QVBoxLayout(self)
        self.hbox = QHBoxLayout()
        self.label = QLabel(self)
        self.pixmap = QPixmap(Icon_path)
        self.pixmap = self.pixmap.scaledToHeight(35)
        self.label.setPixmap(self.pixmap)
        self.label.setFixedSize(self.pixmap.size())
        self.hbox.addWidget(self.label)

        self.text = QLabel("Restart Anki now?", self)
        self.hbox.addWidget(self.text)
        self.layout.addLayout(self.hbox)

        self.buttonBox = QHBoxLayout()
        self.yesButton = QPushButton("Yes", self)
        self.yesButton.clicked.connect(self.accept)
        self.yesButton.setFixedSize(QSize(80, self.yesButton.sizeHint().height()))
        self.buttonBox.addWidget(self.yesButton)

        self.noButton = QPushButton("No", self)
        self.noButton.clicked.connect(self.reject)
        self.noButton.setFixedSize(QSize(80, self.noButton.sizeHint().height()))
        self.buttonBox.addWidget(self.noButton)
        self.layout.addLayout(self.buttonBox)

#--------- auto_restart_after_updating_addons ------------



from .shigeAPI import shigeAPI
# for my add-on: BreakTimer https://ankiweb.net/shared/info/174058935
shigeAPI.restart_anki.add(restart_anki)