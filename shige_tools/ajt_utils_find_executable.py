
# Copyright (C) Ren Tatsumoto 2021-2025 <tatsu at autistici.org> and contributors <https://github.com/tatsumoto-ren>
# Copyright (C) Shigeyuki 2025 <http://patreon.com/Shigeyuki>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# NOTE:(by Shigeඞ)
# This code is based on the "Ajatt-Tools" code included in the "AJT Media Converter" by Ren Tatsumoto.
# Ajatt-Tools, ajt_common: <https://github.com/Ajatt-Tools/ajt_common>
#              utils.py:   <https://github.com/Ajatt-Tools/ajt_common/blob/main/utils.py>
# AJT Media Converter:
#                   Github: <https://github.com/Ajatt-Tools/PasteImagesAsWebP>
#                   AddonPage: <https://ankiweb.net/shared/info/1151815987>

### Why this file is needed? ###
# The path to run ffmpeg in subprocess can be obtained by shutil.which("ffmpeg").
# But according to the code in the add-on “Watch Foreign Language Movies with Anki”
# there seems to be a problem when running subprocess from a Gui app on Mac.
#   (Addon: "Watch Foreign Language Movies with Anki" https://ankiweb.net/shared/info/939347702)
#   https://docs.brew.sh/FAQ#my-mac-apps-dont-find-usrlocalbin-utilities
# So we need to add Path to the environment variable.
# e.g: movies2anki.py <https://github.com/kelciour/movies2anki/blob/main/movies2anki.py>
# if is_mac and '/usr/local/bin' not in os.environ['PATH'].split(':'):
#     os.environ['PATH'] = "/usr/local/bin:" + os.environ['PATH']
# The Ajatt-Tools code uses FALLBACK_PATHS to search for Path so it looks more unbreakable(maybe).


import os
import shutil

def find_executable(name: str):
    path = shutil.which(name)
    if path:
        return path

    FALLBACK_PATHS = [
        "/usr/local/bin",
        "/opt/homebrew/bin",
        "/usr/bin",
        "/bin",
        os.path.expanduser("~/.local/bin"),
    ]

    for path_to_dir in FALLBACK_PATHS:
        if os.path.isfile(path_to_exe := os.path.join(path_to_dir, name)):
            return path_to_exe
    return None


# e.g.
# from .ajt_utils_find_executable import find_executable
# def get_ffmpeg_exe_path():
#    ffmpeg_exe_path := find_executable("ffmpeg")