import tkinter as tk  # 匯入 tkinter 模組，提供 GUI 功能
from tkinter import ttk, messagebox  # 匯入彈出式通知模組
from PIL import Image, ImageTk  # 圖像處理模組
from datetime import datetime, timedelta  # 日期與時間模組
import json  # JSON 模組

# 智慧家居的主應用程式窗口
class SmartHomeApp(tk.Tk):
    
    # 初始化設定
    def __init__(self):
        super().__init__()  # 呼叫 tk.Tk 類別的初始化方法
        self.title("智慧家居管理系统")  # 設置應用程式標題
        
        # 初始狀態都設為關閉或沒有數據
        self.light_state = False
        self.ac_state = False
        self.tv_state = False
        self.camera_state = False
        self.washing_machine_state = False
        self.ac_timer = None
        self.washing_machine_timer = None
        self.home_time = None

        # 創建 GUI 元件
        self.create_widgets()

        # 更新目前時間
        self.update_current_time()

        # 載入上次的狀態
        self.load_last_state()

    # 創建 GUI 元件
    def create_widgets(self):

        # 創建一個標籤分頁使其填滿系統視窗
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # 遠端遙控器分頁
        remote_control_frame = ttk.Frame(self.notebook)
        self.notebook.add(remote_control_frame, text="遠端遙控器")

        # 屋內設備使用狀況圖像顯示分頁
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="屋內設備使用狀況")

        # 設備開關設定在頂部，且垂直方向的間距為 10
        button_frame = tk.Frame(remote_control_frame)
        button_frame.pack(side=tk.TOP, pady=10)

        # 設定大燈按鈕，被點擊時切換狀態
        self.light_button = tk.Button(button_frame, text="大燈：關", command=self.toggle_light, font=('標楷體', 14, 'bold'))
        self.light_button.pack(side=tk.LEFT, padx=10)
        # 設定冷氣按鈕，被點擊時切換狀態
        self.ac_button = tk.Button(button_frame, text="冷氣：關", command=self.toggle_ac, font=('標楷體', 14, 'bold'))
        self.ac_button.pack(side=tk.LEFT, padx=10)
        # 設定電視按鈕，被點擊時切換狀態
        self.tv_button = tk.Button(button_frame, text="電視：關", command=self.toggle_tv, font=('標楷體', 14, 'bold'))
        self.tv_button.pack(side=tk.LEFT, padx=10)
        # 設定洗衣機按鈕，被點擊時切換狀態
        self.washing_machine_button = tk.Button(button_frame, text="洗衣機：關", command=self.toggle_washing_machine, font=('標楷體', 14, 'bold'))
        self.washing_machine_button.pack(side=tk.LEFT, padx=10)
        # 設定監視器按鈕，被點擊時切換狀態
        self.camera_button = tk.Button(button_frame, text="監視器：關", command=self.toggle_camera, font=('標楷體', 14, 'bold'))
        self.camera_button.pack(side=tk.LEFT, padx=10)
        
        # 設定定時器框架
        timer_frame = tk.Frame(remote_control_frame)
        timer_frame.pack(side=tk.TOP, pady=10)

        # 詢問是否啟用定時
        self.timer_label = tk.Label(timer_frame, text="是否啟用定時功能：", font=('標楷體', 12))
        self.timer_label.pack(side=tk.LEFT, padx=10)
        # 追蹤選擇框的狀態
        self.timer_var = tk.BooleanVar()
        # 創建一個選擇框
        # 當用戶點擊選擇框時，self.timer_var 的值就會相應地改變
        # 使用 variable 參數確保控件與變數同步更新

        self.timer_checkbox = tk.Checkbutton(timer_frame, text="啟用", variable=self.timer_var, font=('標楷體', 12), command=self.toggle_timer)
        self.timer_checkbox.pack(side=tk.LEFT, padx=10)

        # 抵達房間時間框架
        home_time_frame = tk.Frame(remote_control_frame)
        home_time_frame.pack(side=tk.TOP, pady=10)

        # 抵達房間時間標籤
        self.home_time_label = tk.Label(home_time_frame, text="設定抵達房間時間（格式：小時:分鐘）：", font=('標楷體', 12))
        self.home_time_label.pack(side=tk.LEFT, padx=10)
        # 使用 Entry 元件來讓用戶輸入時間
        self.home_time_entry = tk.Entry(home_time_frame, font=('標楷體', 12))
        self.home_time_entry.pack(side=tk.LEFT, padx=10)
        # 時間確認按鈕
        self.confirm_button = tk.Button(home_time_frame, text="確認", command=self.confirm_time, font=('標楷體', 12))
        self.confirm_button.pack(side=tk.LEFT, padx=10)

        # 圖像框架
        image_frame = ttk.Frame(settings_frame)
        image_frame.pack(side=tk.TOP, pady=10)

        # 圖像標籤
        self.image_label1 = tk.Label(image_frame, image=None)
        self.image_label1.pack(side=tk.LEFT, padx=10)
        self.image_label2 = tk.Label(image_frame, image=None)
        self.image_label2.pack(side=tk.LEFT, padx=10)
        self.image_label3 = tk.Label(image_frame, image=None)
        self.image_label3.pack(side=tk.LEFT, padx=10)
        self.image_label4 = tk.Label(image_frame, image=None)
        self.image_label4.pack(side=tk.LEFT, padx=10)
        self.image_label5 = tk.Label(image_frame, image=None)
        self.image_label5.pack(side=tk.LEFT, padx=10)
        
        # 顯示並設定屋內使用狀況圖片
        self.set_images()
        
        # 顯示設定/預設時間按鈕
        self.show_setting_button = tk.Button(self, text="顯示設定/預設時間", command=self.show_home_time, font=('標楷體', 12))
        self.show_setting_button.pack(pady=(30,10))

        # 提示按鈕和目前時間框架
        # 創建底部框架
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        # 提示按鈕
        self.tips_button = tk.Button(bottom_frame, text="提示(i)", command=self.show_notification, font=('標楷體', 12))
        self.tips_button.pack(side=tk.RIGHT, padx=10, pady=10)  # 提示按鈕位於右下角，並留有一定距離

        # 目前時間標籤
        self.current_time_label = tk.Label(bottom_frame, text="", font=('標楷體', 12))
        self.current_time_label.pack(side=tk.LEFT, pady=10, anchor="center")  # anchor="center" 將標籤置中

    # 顯示時間資訊的彈出式視窗
    def show_home_time(self):
        home_time_str = self.home_time_entry.get()  # 獲取使用者回家時間
        try:
            hours, minutes = map(int, home_time_str.split(':'))  # 將字串用:拆成小時和分鐘
            self.home_time = datetime.now().replace(hour=hours, minute=minutes, second=0, microsecond=0)  # 設定抵家時間
            ac_start_time = self.home_time - timedelta(minutes=10)  # 冷氣預定時間
            washing_machine_start_time = self.home_time + timedelta(minutes=50)  # 洗衣機預定時間

            # 設定一個新視窗顯示時間設定
            home_time_window = tk.Toplevel(self)
            home_time_window.title("回家時間/功能預定開啟時間")

            # 從self.home_time獲取並顯示現在時間
            home_time_label = tk.Label(home_time_window, text="抵家時間: {}".format(self.home_time.strftime("%H:%M")), font=('標楷體', 12))
            home_time_label.pack(padx=20, pady=10)

            # 檢測預定時間是否被啟用
            ac_start_time_label_text = "冷氣開啟時間: {}".format(ac_start_time.strftime("%H:%M")) if self.timer_var.get() else "冷氣開啟時間: (未設置)"
            # 從ac_start_time獲取並顯示現在時間
            ac_start_time_label = tk.Label(home_time_window, text=ac_start_time_label_text, font=('標楷體', 12))
            ac_start_time_label.pack(padx=20, pady=10)

            # 檢測預定時間是否被啟用
            washing_machine_start_time_label_text = "洗衣機開啟時間: {}".format(washing_machine_start_time.strftime("%H:%M")) if self.timer_var.get() else "洗衣機開啟時間: (未設置)"
            # 從washing_machine_start_time獲取並顯示現在時間
            washing_machine_start_time_label = tk.Label(home_time_window, text=washing_machine_start_time_label_text, font=('標楷體', 12))
            washing_machine_start_time_label.pack(padx=20, pady=10)
        except ValueError:
            print("輸入的時間格式不正確，請使用正確格式：小時:分鐘。")

    # 設定屋內設備圖像
    def set_images(self):
        # 取用不同情況的圖像
        self.light_off_image = Image.open("light_off.jpeg").resize((100, 100))
        self.light_on_image = Image.open("light_on.jpg").resize((100, 100))
        self.ac_off_image = Image.open("ac_off.jpeg").resize((100, 100))
        self.ac_on_image = Image.open("ac_on.jpeg").resize((100, 100))
        self.tv_off_image = Image.open("tv_off.jpeg").resize((100, 100))
        self.tv_on_image = Image.open("tv_on.jpg").resize((100, 100))
        self.washing_machine_off_image = Image.open("washing_machine_off.png").resize((100, 100))
        self.washing_machine_on_image = Image.open("washing_machine_on.png").resize((100, 100))
        self.camera_off_image = Image.open("camera_off.jpg").resize((100, 100))
        self.camera_on_image = Image.open("camera_on.jpg").resize((100, 100))

        # 轉換為 PhotoImage 物件，以便在 Tkinter 標籤中顯示
        self.light_off_photo = ImageTk.PhotoImage(self.light_off_image)
        self.light_on_photo = ImageTk.PhotoImage(self.light_on_image)
        self.ac_off_photo = ImageTk.PhotoImage(self.ac_off_image)
        self.ac_on_photo = ImageTk.PhotoImage(self.ac_on_image)
        self.tv_off_photo = ImageTk.PhotoImage(self.tv_off_image)
        self.tv_on_photo = ImageTk.PhotoImage(self.tv_on_image)
        self.washing_machine_off_photo = ImageTk.PhotoImage(self.washing_machine_off_image)
        self.washing_machine_on_photo = ImageTk.PhotoImage(self.washing_machine_on_image)
        self.camera_off_photo = ImageTk.PhotoImage(self.camera_off_image)
        self.camera_on_photo = ImageTk.PhotoImage(self.camera_on_image)

        # 確保初始化皆為關閉
        self.update_images()

    # 將所有圖像初始化設為關閉
    def update_images(self):
        self.image_label1.config(image=self.light_off_photo) #config用來設置更新
        self.image_label2.config(image=self.ac_off_photo)
        self.image_label3.config(image=self.tv_off_photo)
        self.image_label4.config(image=self.washing_machine_off_photo)
        self.image_label5.config(image=self.camera_off_photo)

    # 切換大燈狀態
    def toggle_light(self):
        self.light_state = not self.light_state # 切換的狀態相反
        self.update_light_button() # 更新按鈕外觀

    # 切換冷氣狀態
    def toggle_ac(self):
        self.ac_state = not self.ac_state
        self.update_ac_button()

    # 切換電視狀態
    def toggle_tv(self):
        self.tv_state = not self.tv_state # 切換的狀態相反
        self.update_tv_button() # 更新按鈕外觀

    # 切換洗衣機狀態
    def toggle_washing_machine(self):
        self.washing_machine_state = not self.washing_machine_state # 切換的狀態相反
        self.update_washing_machine_button()  # 更新按鈕外觀
        
    # 切換監視器狀態
    def toggle_camera(self):
        # 當關閉
        if self.camera_state:
            self.camera_state = False
            self.update_camera_button() # 更新按鈕外觀
            self.close_camera_details() # 關閉監視器畫面
        # 當開啟
        else:
            self.camera_state = True
            self.update_camera_button() # 更新按鈕外觀
            self.show_camera_details() # 開啟監視器畫面

    # 關閉監視器直播畫面
    def close_camera_details(self):
        for widget in self.winfo_children(): # 找出所有彈出式視窗
            if isinstance(widget, tk.Toplevel): # 如果是tk.Toplevel類型的視窗則關閉
                widget.destroy()

    # 顯示監視器畫面
    def show_camera_details(self):
        camera_window = tk.Toplevel(self) # 創建新視窗 
        camera_window.title("監視器影像畫面")
        camera_label = tk.Label(camera_window, text="監視器已開啟，正在直播畫面...")
        camera_label.pack(padx=20, pady=20)

    # 更新按鍵以及設備圖片
    def update_light_button(self):
        # 當開啟
        if self.light_state:
            self.light_button.config(text="大燈：開", bg='orange') # 按鍵顏色改為橘色
            self.image_label1.config(image=self.light_on_photo) # 設備圖片改為開啟
        # 當關閉
        else:
            self.light_button.config(text="大燈：關", bg='SystemButtonFace')# 按鍵顏色改為預設顏色
            self.image_label1.config(image=self.light_off_photo) # 設備圖片改為關閉

    def update_ac_button(self):
        if self.ac_state:
            self.ac_button.config(text="冷氣：開", bg='orange')
            self.image_label2.config(image=self.ac_on_photo)
        else:
            self.ac_button.config(text="冷氣：關", bg='SystemButtonFace')
            self.image_label2.config(image=self.ac_off_photo)

    def update_tv_button(self):
        if self.tv_state:
            self.tv_button.config(text="電視：開", bg='orange')
            self.image_label3.config(image=self.tv_on_photo)
        else:
            self.tv_button.config(text="電視：關", bg='SystemButtonFace')
            self.image_label3.config(image=self.tv_off_photo)

    def update_washing_machine_button(self):
        if self.washing_machine_state:
            self.washing_machine_button.config(text="洗衣機：開", bg='orange')
            self.image_label4.config(image=self.washing_machine_on_photo)
        else:
            self.washing_machine_button.config(text="洗衣機：關", bg='SystemButtonFace')
            self.image_label4.config(image=self.washing_machine_off_photo)

    def update_camera_button(self):
        if self.camera_state:
            self.camera_button.config(text="監視器：開", bg='orange')
            self.image_label5.config(image=self.camera_on_photo)
        else:
            self.camera_button.config(text="監視器：關", bg='SystemButtonFace')
            self.image_label5.config(image=self.camera_off_photo)

    # 創建消息框以給予用戶通知
    def notification(self, message):
        messagebox.showinfo("通知", message)

    def toggle_timer(self):
        if self.timer_var.get():
            self.home_time_entry.config(state=tk.NORMAL)
            self.confirm_button.config(state=tk.NORMAL)
            self.set_ac_timer()  # 設置冷氣定時器
            self.set_washing_machine_timer()  # 設置洗衣機定時器
        else:
            self.cancel_washing_machine_timer()  # 取消洗衣機定時器
            self.cancel_ac_timer()  # 取消冷氣定時器
            self.home_time_entry.config(state=tk.DISABLED)
            self.confirm_button.config(state=tk.DISABLED)

    def cancel_washing_machine_timer(self):
        if self.washing_machine_timer is not None:
            self.after_cancel(self.washing_machine_timer)  # 取消洗衣機定時器
            self.washing_machine_timer = None  # 定時器設定為沒有預定

    def cancel_ac_timer(self):
        if self.ac_timer is not None:
            self.after_cancel(self.ac_timer)  # 取消冷氣定時器
            self.ac_timer = None  # 定時器設定為沒有預定

    def set_ac_timer(self):
        if self.ac_state == False:
            if self.home_time is None:
                return
            
            ac_start_time = self.home_time - timedelta(minutes=10)
            current_time = datetime.now()
            time_diff = (ac_start_time - current_time).total_seconds()
            if self.home_time > current_time:
                if 0 <= -time_diff < 600:
                    self.toggle_ac()
                    self.notification("冷氣已自動開啟")
                if time_diff > 0:
                    self.notification("冷氣預計在回家前10分鐘自動開啟")
                    if self.timer_var.get():  # 檢查定時器的啟用狀態
                        self.ac_timer = self.after(int(time_diff * 1000), self.check_ac_timer)

    def check_ac_timer(self):
        if self.timer_var.get():  # 再次檢查定時器的啟用狀態
            self.toggle_ac()
            self.notification("冷氣已自動開啟")

    def set_washing_machine_timer(self):
        if self.washing_machine_state == False :
            if self.home_time is None:
                return
            if self.washing_machine_timer is not None:
                self.after_cancel(self.washing_machine_timer)  # 取消之前的洗衣機定時器
            washing_machine_start_time = self.home_time + timedelta(minutes=50)
            current_time = datetime.now()
            time_diff = (washing_machine_start_time - current_time).total_seconds()
            if time_diff > 0:
                self.washing_machine_timer = self.after(int(time_diff * 1000), self.toggle_washing_machine)
                self.after(int(time_diff * 1000), lambda: self.notification("洗衣機已自動開啟")) 
                self.notification("洗衣機預計在回家50分鐘後自動開啟")


    # 更新目前時間
    def update_current_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.current_time_label.config(text=f"目前時間：{current_time}") # f允許在字串中使用變數，並將它們的值插入到字串中
        self.current_time_label.after(1000, self.update_current_time) # 每1000毫秒更新一次

    # 讀取上次的使用紀錄
    def load_last_state(self):
        try:
            with open("last_state.json", "r") as file: # 打開 "last_state.json" 文件來讀取保存的狀態信息
                last_state = json.load(file) # 將文件中的內容解析為 JSON 格式
                
                # 將初始化設定改為上次紀錄，如果沒有紀錄則保持原狀
                self.light_state = last_state.get("light_state", False)
                self.ac_state = last_state.get("ac_state", False)
                self.tv_state = last_state.get("tv_state", False)
                self.camera_state = last_state.get("camera_state", False)
                self.washing_machine_state = last_state.get("washing_machine_state", False)
                self.timer_var.set(last_state.get("timer_enabled", False))  # 定時器的狀態
                
                self.home_time_entry.delete(0, tk.END) # 輸入框中的任何已有的資料
                self.home_time_entry.insert(0, last_state.get("home_time", ""))  # 上次時間，不存在則為空
                
                self.update_buttons()#更新按鍵狀況

                # 根據定時器的狀態設置抵達房間時間輸入框的狀態
                if not self.timer_var.get():
                    self.home_time_entry.config(state=tk.DISABLED)
                    self.confirm_button.config(state=tk.DISABLED)

                # 監視器如果上次紀錄是被開啟，這次打開也會一並打開直播畫面
                if self.camera_state:
                    self.show_camera_details()
        except FileNotFoundError:
            print("未找到上一次的狀態文件，將使用默認值。")

    # 一次性處理更新按鍵
    def update_buttons(self):
        self.update_light_button()
        self.update_ac_button()
        self.update_tv_button()
        self.update_washing_machine_button()
        self.update_camera_button()

    # 將當前文件保存
    def save_last_state(self):
        last_state = {
            "light_state": self.light_state,
            "ac_state": self.ac_state,
            "tv_state": self.tv_state,
            "camera_state": self.camera_state,
            "washing_machine_state": self.washing_machine_state,
            "timer_enabled": self.timer_var.get(),  # Save timer status
            "home_time": self.home_time_entry.get()  # Save home arrival time setting
        }
        # 寫入JSON文件
        with open("last_state.json", "w") as file:
            json.dump(last_state, file)

    # 在關閉前將程式儲存
    def on_closing(self):
        self.save_last_state()  
        self.destroy() #當主視窗被關閉，確保其他視窗也被關閉

    # 設定確認按鈕，只有在按下確認的時候時間才能被編輯
    def confirm_time(self):
        time_str = self.home_time_entry.get()
        try:
            hour, minute = map(int, time_str.split(":")) # map可以把一個函數應用到一個序列（比如列表）的每一個元素上
            self.home_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            self.notification(f"已設定抵達時間：{self.home_time.strftime('%H:%M')}")
            self.set_ac_timer()
            self.set_washing_machine_timer()
        except ValueError:
            self.notification("請輸入正確的時間格式（小時:分鐘）")

    # 顯示通知
    def show_notification(self):
        show_tips = tk.Toplevel(self)
        show_tips.title("提示information")
        show_tips_one = tk.Label(show_tips, text="1. 時間請按照（小時:分鐘）來輸入，請用24小時制", font=('標楷體', 14))
        show_tips_two = tk.Label(show_tips, text="2. 編輯時間必須點擊確認才會存取", font=('標楷體', 14))
        show_tips_three = tk.Label(show_tips, text="3. 在距離回家十分鐘內，開啟啟用定時，將立即開啟冷氣", font=('標楷體', 14))
        show_tips_four = tk.Label(show_tips, text="4. 如果設定當下的時間已超過，即將設定的時間，定時功能將不會運行", font=('標楷體', 14))
        show_tips_five = tk.Label(show_tips, text="5. 如果設定當下冷氣已開啟，到達預定時間點時，就算冷氣關閉也不會自動開啟，請確保在冷氣關閉時設定回家時間", font=('標楷體', 14))
        show_tips_one.pack(padx=20, pady=10)
        show_tips_two.pack(padx=20, pady=10)
        show_tips_three.pack(padx=20, pady=10)
        show_tips_four.pack(padx=20, pady=10)
        show_tips_five.pack(padx=20, pady=10)
# 確保程式被直接執行
if __name__ == "__main__":
    app = SmartHomeApp() # 智能家居管理系統應用程式
    app.protocol("WM_DELETE_WINDOW", app.on_closing)  # 當用戶要關閉程式將執行app.on_closing
    app.mainloop()  # 開始程式 