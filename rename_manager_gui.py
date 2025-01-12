import tkinter as tk
from tkinter import ttk, messagebox
import os
from pathlib import Path

class RenameManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("文件重命名管理工具")
        self.root.geometry("800x600")
        
        # 设置主窗口在屏幕中央
        self.center_window(self.root, 800, 600)
        
        # 历史记录文件
        self.HISTORY_FILE = '.rename_history'
        if not os.path.exists(self.HISTORY_FILE):
            Path(self.HISTORY_FILE).touch()
        
        self.create_widgets()
        self.refresh_file_list()
    
    def center_window(self, window, width, height):
        """将窗口居中显示"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_dialog(self, title, width=400, height=180):
        """创建统一样式的对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.resizable(False, False)
        
        # 设置对话框在主窗口中央
        self.center_window(dialog, width, height)
        
        # 使对话框成为模态窗口
        dialog.grab_set()
        
        # 创建内容框架
        content_frame = ttk.Frame(dialog, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        return dialog, content_frame
        
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 文件列表
        list_frame = ttk.LabelFrame(main_frame, text="当前目录及子目录下的所有文件", padding="5")
        list_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.file_listbox = tk.Listbox(list_frame, width=80, height=20)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # 操作按钮
        btn_frame = ttk.Frame(main_frame, padding="5")
        btn_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Button(btn_frame, text="添加前缀", command=self.show_prefix_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加后缀", command=self.show_suffix_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除字符串", command=self.show_remove_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="替换字符串", command=self.show_replace_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="撤销操作", command=self.undo_operation).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="刷新列表", command=self.refresh_file_list).pack(side=tk.LEFT, padx=5)
    
    def get_all_files(self):
        """递归获取当前目录下的所有文件和文件夹"""
        all_files = []
        for root, dirs, files in os.walk('.'):
            # 排除以点开头的隐藏文件夹
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                # 排除程序自身和历史记录文件
                if file != 'rename_manager_gui.py' and file != '.rename_history' and not file.startswith('.'):
                    # 使用相对路径
                    rel_path = os.path.relpath(os.path.join(root, file), '.')
                    all_files.append(rel_path)
        return sorted(all_files)
    
    def refresh_file_list(self):
        """刷新文件列表"""
        self.file_listbox.delete(0, tk.END)
        for file in self.get_all_files():
            self.file_listbox.insert(tk.END, file)
    
    def log_operation(self, old_name, new_name):
        """记录重命名操作"""
        with open(self.HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{new_name}|{old_name}\n")
    
    def show_prefix_dialog(self):
        """显示添加前缀对话框"""
        dialog, content_frame = self.create_dialog("添加前缀")
        
        ttk.Label(content_frame, text="请输入要添加的前缀:").pack(pady=(0, 10))
        prefix_var = tk.StringVar()
        entry = ttk.Entry(content_frame, textvariable=prefix_var, width=40)
        entry.pack(pady=(0, 20))
        entry.focus()
        
        def apply_prefix():
            prefix = prefix_var.get()
            if not prefix:
                messagebox.showerror("错误", "前缀不能为空")
                return
            
            for file in self.get_all_files():
                dirname = os.path.dirname(file)
                basename = os.path.basename(file)
                if not basename.startswith(prefix):
                    new_basename = prefix + basename
                    new_name = os.path.join(dirname, new_basename) if dirname else new_basename
                    os.rename(file, new_name)
                    self.log_operation(file, new_name)
            
            self.refresh_file_list()
            dialog.destroy()
        
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(pady=(0, 10))
        ttk.Button(btn_frame, text="确定", command=apply_prefix, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
        
        # 绑定回车键
        dialog.bind('<Return>', lambda e: apply_prefix())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
    
    def show_suffix_dialog(self):
        """显示添加后缀对话框"""
        dialog, content_frame = self.create_dialog("添加后缀")
        
        ttk.Label(content_frame, text="请输入要添加的后缀:").pack(pady=(0, 10))
        suffix_var = tk.StringVar()
        entry = ttk.Entry(content_frame, textvariable=suffix_var, width=40)
        entry.pack(pady=(0, 20))
        entry.focus()
        
        def apply_suffix():
            suffix = suffix_var.get()
            if not suffix:
                messagebox.showerror("错误", "后缀不能为空")
                return
            
            for file in self.get_all_files():
                dirname = os.path.dirname(file)
                basename = os.path.basename(file)
                name, ext = os.path.splitext(basename)
                if not name.endswith(suffix):
                    new_basename = name + suffix + ext
                    new_name = os.path.join(dirname, new_basename) if dirname else new_basename
                    os.rename(file, new_name)
                    self.log_operation(file, new_name)
            
            self.refresh_file_list()
            dialog.destroy()
        
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(pady=(0, 10))
        ttk.Button(btn_frame, text="确定", command=apply_suffix, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
        
        # 绑定回车键
        dialog.bind('<Return>', lambda e: apply_suffix())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
    
    def show_remove_dialog(self):
        """显示删除字符串对话框"""
        dialog, content_frame = self.create_dialog("删除字符串")
        
        ttk.Label(content_frame, text="请输入要删除的字符串（多个用空格分隔）:").pack(pady=(0, 10))
        strings_var = tk.StringVar()
        entry = ttk.Entry(content_frame, textvariable=strings_var, width=40)
        entry.pack(pady=(0, 20))
        entry.focus()
        
        def apply_remove():
            strings = strings_var.get().strip().split()
            if not strings:
                messagebox.showerror("错误", "请至少输入一个要删除的字符串")
                return
            
            for file in self.get_all_files():
                dirname = os.path.dirname(file)
                basename = os.path.basename(file)
                new_basename = basename
                for s in strings:
                    new_basename = new_basename.replace(s, '')
                new_basename = ' '.join(new_basename.split())
                
                if new_basename != basename:
                    new_name = os.path.join(dirname, new_basename) if dirname else new_basename
                    os.rename(file, new_name)
                    self.log_operation(file, new_name)
            
            self.refresh_file_list()
            dialog.destroy()
        
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(pady=(0, 10))
        ttk.Button(btn_frame, text="确定", command=apply_remove, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
        
        # 绑定回车键
        dialog.bind('<Return>', lambda e: apply_remove())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
    
    def show_replace_dialog(self):
        """显示替换字符串对话框"""
        dialog, content_frame = self.create_dialog("替换字符串", height=220)
        
        ttk.Label(content_frame, text="请输入要替换的原字符串:").pack(pady=(0, 10))
        old_var = tk.StringVar()
        old_entry = ttk.Entry(content_frame, textvariable=old_var, width=40)
        old_entry.pack(pady=(0, 10))
        old_entry.focus()
        
        ttk.Label(content_frame, text="请输入替换后的新字符串:").pack(pady=(0, 10))
        new_var = tk.StringVar()
        new_entry = ttk.Entry(content_frame, textvariable=new_var, width=40)
        new_entry.pack(pady=(0, 20))
        
        def apply_replace():
            old_string = old_var.get()
            if not old_string:
                messagebox.showerror("错误", "原字符串不能为空")
                return
            
            new_string = new_var.get()
            for file in self.get_all_files():
                dirname = os.path.dirname(file)
                basename = os.path.basename(file)
                if old_string in basename:
                    new_basename = basename.replace(old_string, new_string)
                    new_name = os.path.join(dirname, new_basename) if dirname else new_basename
                    os.rename(file, new_name)
                    self.log_operation(file, new_name)
            
            self.refresh_file_list()
            dialog.destroy()
        
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(pady=(0, 10))
        ttk.Button(btn_frame, text="确定", command=apply_replace, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
        
        # 绑定回车键
        dialog.bind('<Return>', lambda e: apply_replace())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
    
    def undo_operation(self):
        """撤销上一步操作"""
        try:
            if not os.path.exists(self.HISTORY_FILE) or os.path.getsize(self.HISTORY_FILE) == 0:
                messagebox.showinfo("提示", "没有可撤销的操作")
                return
            
            with open(self.HISTORY_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if not lines:
                    messagebox.showinfo("提示", "没有可撤销的操作")
                    return
                
                last_operation = lines[-1].strip()
                new_name, old_name = last_operation.split('|')
                
                if os.path.exists(new_name):
                    # 确保目标文件夹存在
                    target_dir = os.path.dirname(old_name)
                    if target_dir and not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                        
                    os.rename(new_name, old_name)
                    
                    # 更新历史记录文件
                    with open(self.HISTORY_FILE, 'w', encoding='utf-8') as f:
                        f.writelines(lines[:-1])
                    
                    self.refresh_file_list()
                    messagebox.showinfo("成功", f"已撤销: {new_name} → {old_name}")
                else:
                    messagebox.showerror("错误", f"无法撤销：文件 {new_name} 不存在")
        except Exception as e:
            messagebox.showerror("错误", f"撤销操作失败: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = RenameManagerGUI(root)
    root.mainloop()