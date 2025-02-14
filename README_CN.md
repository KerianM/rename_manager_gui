# 文件重命名管理工具

[English](README.md) | [简体中文](README_CN.md)

一个用于批量重命名文件和文件夹的图形界面工具，支持递归操作。

## 功能特点

- 为文件/文件夹添加前缀
- 为文件/文件夹添加后缀（在扩展名之前）
- 删除文件名中的特定字符串
- 替换文件名中的字符串
- 撤销上一步操作
- 支持子目录递归操作
- 实时文件列表预览
- 操作历史记录跟踪

## 使用方法

1. 运行应用程序：
```bash
python rename_manager_gui.py
```

2. 主窗口将显示当前目录及其子目录中的所有文件和文件夹。

3. 选择操作：
   - **添加前缀**：在文件名开头添加文本
   - **添加后缀**：在文件扩展名之前添加文本
   - **删除字符串**：从文件名中删除特定文本
   - **替换字符串**：替换文件名中的文本
   - **撤销操作**：恢复上一次重命名操作
   - **刷新列表**：更新文件列表

4. 在弹出的对话框中输入所需文本并确认。

## 系统要求

- Python 3.12.0
- tkinter（通常随Python一起安装）

## 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件
