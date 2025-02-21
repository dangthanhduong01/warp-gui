# Warp UI for linux

Các bước cài đặt:
<code> 
python3 -m venv venv  # Tạo venv mới
source venv/bin/activate  # Kích hoạt venv
python3 install.py
</code>

Chạy code: sh ./run.sh

build:  pyinstaller --onefile --icon=warp.png --hidden-import=_tkinter --hidden-import=tkinter app.py