import os
import sys
from pathlib import Path

cur_path = sys.path[0]

print(cur_path)
print(Path.home())

os.system("pip install -r requirements.txt")
os.system("mkdir -p ~/.local/share/icons")
os.system("cp {}/icons/warp.png ~/.local/share/icons/warp.png".format(cur_path))

desktop_file = '{}/.local/share/applications/warp.desktop'.format(Path.home())

file = open(desktop_file, 'w+')
file.write('''[Desktop Entry]
Name=Warp Cli GUI
Version=1.0
Comment=A gui app base on warp-cli for linux
Exec=python3 {}/app.py
Icon=warp
Terminal=false
Type=Application
'''.format(cur_path))
print('Desktop file created at "{}"'.format(desktop_file))