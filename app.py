import tkinter as tk
from tkinter import Canvas
import subprocess
import requests

# URL to check warp status
WARP_URL = "https://www.cloudflare.com/cdn-cgi/trace/"


class WarpApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Warp UI")
        self.root.geometry("300x400")
        self.root.configure(bg="#000000")  # Màu nền đen

        # Tiêu đề "WARP"
        self.title_label = tk.Label(root, text="WARP PRO+", font=("Arial", 24, "bold"), fg="red", bg="#000000")
        self.title_label.pack(pady=10)


        self.refresh_button = tk.Button(root, text="1.1.1.1", command=self.check_warp_status, font=("Arial", 12))
        self.refresh_button.pack(pady=10)

        # State toggle (False = OFF, True = ON)
        self.toggle_state = tk.BooleanVar(value=False)

        # State label
        self.status_label = tk.Label(root, text="Disconnected", font=("Arial", 14), fg="white", bg="#000000")
        self.status_label.pack(pady=5)

        # Canvas Toggle Switch
        self.canvas = Canvas(root, width=120, height=60, bg="#000000", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Background toggle
        # self.canvas.create_oval(2, 2, 60, 28, fill="white", outline="white")

        # Hình nền toggle
        self.toggle_bg = self.canvas.create_rounded_rectangle(5, 5, 115, 55, radius=30, fill="orange", outline="orange")

        # Round button toggle
        self.toggle_btn = self.canvas.create_oval(10, 10, 50, 50, fill="white")

        self.canvas.bind("<Button-1>", self.on_toggle_click)

        # Description "Your network is now private"
        # Create canvas for description
        self.desc_label = Canvas(root, width=250, height=30, bg="#000000", highlightthickness=0)
        self.desc_label.pack(pady=5)
        # Display "Your Internet is" white
        self.text_desc = self.desc_label.create_text(70, 15, text="Your Internet is now", font=("Arial", 10), fill="white")
        # Display "private" red
        self.text_privacy_status = self.desc_label.create_text(155, 15, text="private", font=("Arial", 10, "bold"), fill="red")


        # self.desc_label = tk.Label(root, text="Your Internet is private.", font=("Arial", 10), fg="red", bg="#000000")
        # self.desc_label.pack(pady=5)

        # Check state when app running
        self.check_warp_status()
    
    # Function  
    def check_warp_status(self):
        try:
            self.status_label.config(text="Checking...", fg="yellow")
            self.root.update_idletasks()

            statersp = requests.get(WARP_URL, timeout=5)
            warp_state = dict(line.split('=') for line in statersp.text.strip().split("\n"))
            warp_status = warp_state.get("warp", "off")
            if warp_status == "on":
                self.toggle_state.set(True)
                self.update_toggle_ui(True)
            else:
                self.toggle_state.set(False)
                self.update_toggle_ui(False)
        except Exception as e:
            self.status_label.config(text="Error Checking", fg="orange")


    def run_warp_cli(self):
        command = "warp-cli connect" if self.toggle_state.get() else "warp-cli disconnect"
        subprocess.run(command, shell=True)
        # try:
        #     result = subprocess.run(command, shell=True, capture_output=True, text=True)
        #     self.output_text.delete(1.0, tk.END)  # Xóa kết quả cũ
        #     self.output_text.insert(tk.END, result.stdout if result.stdout else result.stderr)
        # except Exception as e:
        #     self.output_text.insert(tk.END, f"Error: {str(e)}")

    # Change state toggle
    def update_toggle_ui(self, state):
        if state:
            self.canvas.itemconfig(self.toggle_bg, fill="green", outline="green")  # Màu xanh khi bật
            self.canvas.coords(self.toggle_btn, 70, 10, 110, 50)  # Di chuyển nút tròn sang phải
            self.status_label.config(text="Connected", fg="white")
        else:
            self.canvas.itemconfig(self.toggle_bg, fill="orange", outline="orange")  # Màu cam khi tắt
            self.canvas.coords(self.toggle_btn, 10, 10, 50, 50)  # Di chuyển nút tròn sang trái
            self.status_label.config(text="Disconnected", fg="gray")

        self.update_desc_text(state)

    def update_desc_text(self, is_connected):
        if is_connected:
            self.desc_label.itemconfig(self.text_privacy_status, text="private", fill="red")  # Connected
        else:
            self.desc_label.itemconfig(self.text_privacy_status, text="public", fill="green")  # Disconnected
    # Change state toggle
    # def toggle_switch(self):
    #     state = self.toggle_state.get()
    #     self.canvas.itemconfig(self.toggle_btn, fill="green" if state else "red")  # Đổi màu
    #     self.canvas.coords(self.toggle_btn, 30 if state else 5, 5, 55 if state else 30, 25)  # Di chuyển nút
    #     self.status_label.config(text="Connected" if state else "Disconnected")
        
    # Event click on toggle
    def on_toggle_click(self, event):
        """Handler when click to switch"""
        new_state = not self.toggle_state.get()
        self.toggle_state.set(new_state)  # Đảo trạng thái
        self.update_toggle_ui(new_state)
        self.run_warp_cli()  # Gọi hàm thực thi lệnh khi toggle thay đổi
        

# Tạo hình chữ nhật bo góc
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1, x2, y1 + radius,
        x2, y2 - radius,
        x2, y2, x2 - radius, y2,
        x1 + radius, y2,
        x1, y2, x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# Thêm hàm tạo hình chữ nhật bo góc vào Canvas
Canvas.create_rounded_rectangle = create_rounded_rectangle

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = WarpApp(root)
    root.mainloop()

