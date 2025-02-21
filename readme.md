Tạo venv:
<code> 
python3 -m venv venv  # Tạo venv mới
source venv/bin/activate  # Kích hoạt venv
pip install -r requirements.txt  # Cài đặt lại các package
</code>

Chạy code: sh ./run.sh

build:  pyinstaller --onefile --icon=warp.png --hidden-import=_tkinter --hidden-import=tkinter app.py