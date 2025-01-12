import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import configparser
from pathlib import Path
from typing import List, Tuple, Union

class RenameManagerGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("文件重命名管理工具")
        self.root.geometry("800x600")
        
        # 设置主窗口在屏幕中央
        self.center_window(self.root, 800, 600)
        
        # 获取程序所在目录
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe
            self.app_path = os.path.dirname(sys.executable)
        else:
            # 如果是python脚本
            self.app_path = os.path.dirname(os.path.abspath(__file__))
        
        # 历史记录文件和配置文件路径（放在程序目录下）
        self.HISTORY_FILE = os.path.join(self.app_path, '.rename_history')
        self.SETTINGS_FILE = os.path.join(self.app_path, 'settings.ini')
        Path(self.HISTORY_FILE).touch(exist_ok=True)
        
        # 是否仅处理当前目录
        self.current_dir_only = tk.BooleanVar(value=False)
        # 是否修改文件夹名
        self.rename_folders = tk.BooleanVar(value=False)
        
        # 加载上次的目录
        self.current_dir = self.load_last_directory()
        if not os.path.exists(self.current_dir):
            self.current_dir = os.getcwd()
        os.chdir(self.current_dir)
        
        self.create_widgets()
        self.refresh_file_list()
    
    def center_window(self, window: Union[tk.Tk, tk.Toplevel], width: int, height: int) -> None:
        """将窗口居中显示"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def load_last_directory(self) -> str:
        """从配置文件加载上次打开的目录"""
        config = configparser.ConfigParser()
        if os.path.exists(self.SETTINGS_FILE):
            config.read(self.SETTINGS_FILE, encoding='utf-8')
            return config.get('Settings', 'last_directory', fallback=os.getcwd())
        return os.getcwd()
    
    def save_last_directory(self, directory: str) -> None:
        """保存当前目录到配置文件"""
        config = configparser.ConfigParser()
        if os.path.exists(self.SETTINGS_FILE):
            config.read(self.SETTINGS_FILE, encoding='utf-8')
        
        if not config.has_section('Settings'):
            config.add_section('Settings')
        
        config.set('Settings', 'last_directory', directory)
        
        try:
            with open(self.SETTINGS_FILE, 'w', encoding='utf-8') as f:
                config.write(f)
        except PermissionError:
            messagebox.showerror("错误", "无法保存配置文件，请确保程序有写入权限！")
    
    def select_directory(self) -> None:
        """选择工作目录"""
        dir_path = filedialog.askdirectory(initialdir=self.current_dir)
        if dir_path:
            self.current_dir = dir_path
            os.chdir(dir_path)
            self.dir_label.config(text=f"当前目录: {dir_path}")
            self.save_last_directory(dir_path)  # 保存新选择的目录
            self.refresh_file_list()