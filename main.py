# AIDeskControl PixelArt GUI 终极版（第四个Block改为颜色选择器）
import os, json, threading, time, platform, webbrowser
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox, filedialog, ttk, colorchooser
from PIL import ImageGrab, Image, ImageTk
from openai import OpenAI

PROGRAM_WHITELIST = {"notepad.exe", "calc.exe", "chrome.exe"}
WEBSITE_WHITELIST = {"https://github.com", "https://www.google.com"}

def parse_command(client, command: str):
    try:
        prompt_system = (
            "你是桌面助手，将用户指令解析为JSON列表，每个元素包含intent和target，"
            "intent可为open_program, close_program, open_folder, close_folder, open_website, input_text, input_image，"
            "只允许打开/关闭程序、网页和文件夹，不允许删除。"
        )
        messages = [
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": command}
        ]
        response = client.chat.completions.create(model="deepseek-chat", messages=messages)
        content = response.choices[0].message.content.strip()
        actions = json.loads(content)
        if not isinstance(actions, list):
            actions = [actions]
        return actions
    except:
        return []

def execute_action_thread(action, gui, idx, total):
    intent = action.get("intent")
    target = action.get("target")
    gui.append_message("系统", f"正在执行: {intent} -> {target}")

    folder_path = None
    if intent == "open_folder":
        q = threading.Queue()
        def choose_folder():
            path = filedialog.askdirectory(title="请选择文件夹")
            q.put(path)
        gui.root.after(0, choose_folder)
        folder_path = q.get()

    progress_list = ["[░░░░░░░░░░]", "[██░░░░░░░░]", "[████░░░░░░]",
                     "[██████░░░░]", "[████████░░]", "[██████████]", "[完成!]"]
    for p in progress_list:
        gui.progress_label.config(text=p)
        gui.progress_label.update_idletasks()
        time.sleep(0.1)

    try:
        windir = os.environ.get('WINDIR', r'C:\Windows')
        if intent == "open_program" and target in PROGRAM_WHITELIST:
            path = os.path.join(windir, "system32", target) if target.lower() in ["notepad.exe","calc.exe"] else target
            os.system(f'start "" "{path}"')
            gui.append_message("系统", f"✅ 已打开程序：{target}")
        elif intent == "close_program" and target in PROGRAM_WHITELIST:
            os.system(f'taskkill /IM {target} /F')
            gui.append_message("系统", f"✅ 已关闭程序：{target}")
        elif intent == "open_folder":
            if folder_path:
                os.startfile(folder_path)
                gui.append_message("系统", f"✅ 已打开文件夹：{folder_path}")
            else:
                gui.append_message("系统", "⚠ 用户取消了选择")
        elif intent == "close_folder":
            gui.append_message("系统", f"⚠ Windows无法精确关闭文件夹窗口")
        elif intent == "open_website" and target in WEBSITE_WHITELIST:
            os.system(f'start "" "{target}"')
            gui.append_message("系统", f"✅ 已打开网页：{target}")
        elif intent == "input_text":
            gui.append_message("AI输出", target)
        elif intent == "input_image":
            gui.display_image(target)
        else:
            gui.append_message("系统", f"⚠ 不允许的操作或未知动作: {intent}")
    except Exception as e:
        gui.append_message("系统", f"❌ 执行失败: {e}")

    percent = int(((idx + 1) / total) * 100)
    gui.total_progress['value'] = percent
    gui.total_progress.update_idletasks()

class DeskControlPixelGUI:
    def __init__(self, root, client):
        self.client = client
        self.root = root
        self.root.title("AIDeskControl PixelArt GUI")
        self.root.geometry("1000x600")
        self.root.configure(bg="#EEE3D3")

        # 顶部工具栏
        self.toolbar_frame = tk.Frame(root, bg="#F0E6D2", height=40)
        self.toolbar_frame.pack(side="top", fill="x")
        self.add_toolbar_buttons()

        # 主分栏
        self.paned = tk.PanedWindow(root, orient="horizontal")
        self.paned.pack(fill="both", expand=True)

        # 左栏历史 + 滑块
        self.left_frame = tk.Frame(self.paned, bg="#F9F8F2", width=200)
        self.history_list = tk.Listbox(self.left_frame, bg="#FFF8E7", font=("Courier",10))
        self.history_list.pack(fill="both", expand=True, padx=2, pady=2)
        self.slider_frame = tk.Frame(self.left_frame, bg="#F0E6D2")
        self.slider_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(self.slider_frame, text="AI模式 (聊天 ↔ 操作)", bg="#F0E6D2").pack()
        self.slider_mode = tk.Scale(self.slider_frame, from_=0, to=100, orient="horizontal", bg="#F9F8F2")
        self.slider_mode.set(50)
        self.slider_mode.pack(fill="x")
        self.history_list.bind("<Double-1>", self.on_history_double_click)
        self.paned.add(self.left_frame)

        # 右栏聊天框 + 进度条 + 输入框
        self.right_frame = tk.Frame(self.paned, bg="#EEE3D3")
        self.paned.add(self.right_frame)
        for i in range(4):
            self.right_frame.rowconfigure(i, weight=(1 if i==0 else 0))
        self.right_frame.columnconfigure(0, weight=1)
        self.chat_display = scrolledtext.ScrolledText(self.right_frame, state='disabled',
                                                      wrap='word', font=("Press Start 2P",10),
                                                      bg="#F9F6F0")
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.total_progress = ttk.Progressbar(self.right_frame, orient="horizontal", length=400, mode="determinate")
        self.total_progress.grid(row=1, column=0, sticky="ew", padx=5, pady=2)
        self.progress_label = tk.Label(self.right_frame, text="", anchor="w",
                                       font=("Courier",10), bg="#DADADA")
        self.progress_label.grid(row=2, column=0, sticky="ew", padx=5, pady=2)
        self.input_frame = tk.Frame(self.right_frame, bg="#EFEFEF")
        self.input_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.input_frame.columnconfigure(0, weight=1)
        self.entry = tk.Entry(self.input_frame, font=("Press Start 2P",10))
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self.on_send)
        self.send_btn = tk.Button(self.input_frame, text="发送", font=("Press Start 2P",8),
                                  bg="#FFD700", command=self.on_send)
        self.send_btn.grid(row=0, column=1, padx=2)

    # ------------------------- 五个Block按钮
    def add_toolbar_buttons(self):
        tk.Button(self.toolbar_frame, text="🖼️", font=("Courier",12), command=self.capture_screenshot).pack(side="left", padx=2, pady=2)
        tk.Button(self.toolbar_frame, text="💧", font=("Courier",12), command=self.capture_area_interactive).pack(side="left", padx=2, pady=2)
        tk.Button(self.toolbar_frame, text="📦", font=("Courier",12), command=self.show_author_info).pack(side="left", padx=2, pady=2)
        tk.Button(self.toolbar_frame, text="🎨", font=("Courier",12), command=self.choose_chat_color).pack(side="left", padx=2, pady=2)
        tk.Button(self.toolbar_frame, text="⚙", font=("Courier",12), command=lambda:webbrowser.open("https://github.com/Yunle-Lee")).pack(side="left", padx=2, pady=2)

    # ------------------------- 颜色选择器功能
    def choose_chat_color(self):
        color = colorchooser.askcolor(title="选择聊天框背景颜色")
        if color[1]:
            self.chat_display.configure(bg=color[1])

    # ------------------------- 其他保留功能
    def capture_screenshot(self):
        img = ImageGrab.grab()
        path = os.path.join(os.getcwd(), "screenshot_full.png")
        img.save(path)
        self.append_message("系统","📷 已生成全屏截图")
        self.display_image(path)

    def capture_area_interactive(self):
        self.append_message("系统","📷 请在屏幕上拖动选择区域")
        top = tk.Toplevel(self.root)
        top.attributes("-fullscreen", True)
        top.attributes("-alpha", 0.3)
        canvas = tk.Canvas(top, bg='grey')
        canvas.pack(fill='both', expand=True)
        start_x = start_y = cur_rect = None
        def on_press(event):
            nonlocal start_x, start_y, cur_rect
            start_x = event.x_root
            start_y = event.y_root
            cur_rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=2)
        def on_drag(event):
            canvas.coords(cur_rect, start_x, start_y, event.x_root, event.y_root)
        def on_release(event):
            x1 = min(start_x, event.x_root)
            y1 = min(start_y, event.y_root)
            x2 = max(start_x, event.x_root)
            y2 = max(start_y, event.y_root)
            top.destroy()
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            path = os.path.join(os.getcwd(), "screenshot_area.png")
            img.save(path)
            self.append_message("系统","📷 已生成区域截图")
            self.display_image(path)
        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

    def show_author_info(self):
        messagebox.showinfo("作者信息","作者：李允乐\nGitHub：https://github.com/Yunle-Lee\n项目：AIDeskControl")

    def display_image(self,path):
        img = Image.open(path)
        img.thumbnail((200,200))
        photo = ImageTk.PhotoImage(img)
        self.chat_display.configure(state='normal')
        self.chat_display.image_create("end",image=photo)
        self.chat_display.insert("end","\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see("end")
        if not hasattr(self,"_images"): self._images=[]
        self._images.append(photo)

    def append_message(self,sender,message):
        self.history_list.insert("end",message)
        self.chat_display.configure(state='normal')
        color="blue" if sender=="用户" else "green"
        self.chat_display.insert("end",f"{sender}: {message}\n",sender)
        self.chat_display.tag_config(sender,foreground=color)
        self.chat_display.configure(state='disabled')
        self.chat_display.see("end")

    def on_history_double_click(self,event):
        selection = self.history_list.curselection()
        if selection:
            index = selection[0]
            command = self.history_list.get(index)
            self.entry.delete(0,"end")
            self.entry.insert(0,command)

    def on_send(self,event=None):
        user_input = self.entry.get().strip()
        if not user_input: return
        if user_input.lower() in ["退出","exit","quit"]:
            self.root.quit()
            return
        self.append_message("用户",user_input)
        self.entry.delete(0,"end")
        mode = self.slider_mode.get()
        if mode<50:
            try:
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role":"system","content":"你是友好的桌面 AI 助手，只聊天，不执行操作"},
                        {"role":"user","content":user_input}
                    ]
                )
                ai_text = response.choices[0].message.content.strip()
            except:
                ai_text="❌ AI 响应失败"
            self.append_message("AI",ai_text)
        else:
            actions = parse_command(self.client,user_input)
            if not actions:
                self.append_message("系统","❌ 解析失败或没有可执行动作")
                return
            total=len(actions)
            for idx,act in enumerate(actions):
                threading.Thread(target=execute_action_thread,args=(act,self,idx,total),daemon=True).start()

# ------------------------- 启动
def main():
    root = tk.Tk()
    root.withdraw()
    api_key = simpledialog.askstring("DeepSeek API Key","请输入你的 DeepSeek API Key:",show="*")
    if not api_key:
        messagebox.showerror("错误","未输入 API Key，程序退出")
        root.destroy()
        return
    client = OpenAI(api_key=api_key,base_url="https://api.deepseek.com")
    root.deiconify()
    app = DeskControlPixelGUI(root,client)
    root.mainloop()

if __name__=="__main__":
    main()