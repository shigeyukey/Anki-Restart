
import subprocess
import json
import os
import sys
import psutil

"""
### PyInstaller ###
各ﾌﾟﾗｯﾄﾌｫｰﾑごとにﾋﾞﾙﾄﾞが必要

[win - noconsole]
python -m PyInstaller ankiRestart.py -n ankiRestart_win --onefile --noconsole --clean

[win - console]
python -m PyInstaller ankiRestart.py -n ankiRestart_win_console --onefile --console --clean

[mac]
python -m PyInstaller ankiRestart.py -n ankiRestart_mac --onefile --noconsole --clean

chmod +x ankiRestart_mac.app

[linux] linuxhCentOS-6.0が互換性が高いっぽい
python3 -m PyInstaller ankiRestart.py -n ankiRestart_linux --onefile --noconsole --clean

chmod +x ankiRestart_linux
ls -l ankiRestart_linux

"""
# pyinstallerの誤検出について
# https://github.com/pyinstaller/pyinstaller/blob/develop/.github/ISSUE_TEMPLATE/antivirus.md

# ------------------------------------

if getattr(sys, 'frozen', False):
    # PyInstallerでﾊﾟｯｹｰｼﾞﾝｸﾞされた場合
    AnkiRestart = os.path.dirname(sys.executable)
else:
    # ｽｸﾘﾌﾟﾄから直接実行された場合
    AnkiRestart = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------

fname=os.path.join(AnkiRestart,'meta.json')
with open(fname, 'r', encoding='utf-8') as f:
    data = json.load(f)

# ------------ 設定ﾌｧｲﾙを読み込む ---------
executable_path = data['config']['executable']

try:
    custom_base_folder = data['config']['custom_base_folder']
    base_folder_path =  data['config']['base_folder_path']
except:
    custom_base_folder = False

try:
    shiftRestart = data['config']['shiftRestart']
    AutoRestart_AfterSafeMode = data['config']['AutoRestart_AfterSafeMode']
except:
    shiftRestart = False
    AutoRestart_AfterSafeMode = False

try:
    custom_excutable = data['config']['custom_excutable']
    custom_path = data['config']['custom_path']
except:custom_excutable = False
# --------------------------------------

check_executable_path = executable_path
if custom_excutable:
    executable_path = custom_path

# --- Ankiが実行中か確認 -----------------
for proc in psutil.process_iter(['pid', 'name']):
    if proc.name() == os.path.basename(check_executable_path):
        print("Restarting Anki, please wait...")
        proc.wait()
        break
# --------------------------------------

# ---- ｾｰﾌﾓｰﾄﾞ-------------------------
if shiftRestart:
    try:
        if custom_base_folder:
            subprocess.Popen([executable_path, "--safemode","-b", base_folder_path])
        else:
            subprocess.Popen([executable_path, "--safemode"])

        if AutoRestart_AfterSafeMode:
            # ｾｰﾌﾓｰﾄﾞで起動した後に閉じたら通常ﾓｰﾄﾞで起動
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.name() == os.path.basename(check_executable_path):
                    proc.wait()
            if custom_base_folder:
                subprocess.Popen([executable_path,"-b", base_folder_path])
            else:
                subprocess.Popen([executable_path])
    except:
        pass

    # ---- 通常ﾓｰﾄﾞで起動 --------
else:
    try:
        if custom_base_folder:
            subprocess.Popen([executable_path, "-b", base_folder_path])
        else:
            subprocess.Popen([executable_path])
    except:
        pass
print(" --- run Restart --- ")