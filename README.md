![AIDeskControl Logo](https://github.com/Yunle-Lee/Pics_of_all_my-projects/blob/main/kk.png)

# AIDeskControl - PixelArt GUI 桌面 AI 助手

**AIDeskControl** 是一个基于 **Python + Tkinter + DeepSeek API** 的桌面 AI 助手，提供可视化 PixelArt 风格的操作界面。它可以解析自然语言指令，实现文件夹、程序、网页的打开/关闭，同时支持 AI 聊天和图片显示功能。

---
# 使用说明:
1.运行程序，填写deepseek api key<br>
![pic0](https://github.com/Yunle-Lee/Pics_of_all_my-projects/blob/main/11.png)<br>
2.填写上的api key你是无法看见的<br>
![pic1](https://github.com/Yunle-Lee/Pics_of_all_my-projects/blob/main/12.png)<br>
3.进入对话框(`执行框`)<br>
![pic2](https://github.com/Yunle-Lee/Pics_of_all_my-projects/blob/main/13.png)<br>
4.这个是按钮块，第一个是截全屏(`主屏`)，第二是拉框截图，第三是作者信息，第四是自定义背景色，最后一个跳转我的github<br>
![pic3](https://github.com/Yunle-Lee/Pics_of_all_my-projects/blob/main/14.png)<br>
5.左下角是对话与操作的调节<br>
![pic4](https://github.com/Yunle-Lee/Pics_of_all_my-projects/blob/main/15.png)<br>
6.自定义可以选择你喜欢的颜色<br>
![pic5](https://github.com/Yunle-Lee/Pics_of_all_my-projects/blob/main/16.png)<br>
7.这个是作者信息的弹窗<br>
![pic6](https://github.com/Yunle-Lee/Pics_of_all_my-projects/blob/main/17.png)<br>
8.这个就是一般对话过程中的样子<br>
![pic7](https://github.com/Yunle-Lee/Pics_of_all_my-projects/blob/main/18.png)<br>

## 功能特点

1. **五大 Block 功能**
   - 🖼️ **全屏截图**：截取整个屏幕并在聊天框显示  
   - 💧 **区域截图**：鼠标拖动选择截图区域  
   - 📦 **作者信息**：弹出窗口显示作者信息和 GitHub 链接  
   - 🎨 **主题颜色选择**：选择聊天框背景颜色  
   - ⚙ **GitHub**：直接打开项目 GitHub 页面  

2. **聊天/操作模式**
   - 左下滑块控制 AI 模式：
     - 聊天模式：AI 仅回答问题  
     - 操作模式：AI 执行指令（打开程序/文件夹/网页等）  

3. **多动作执行与进度条**
   - 支持一条指令触发多个操作  
   - 单行动态进度条 + 总进度条反馈操作状态  

4. **文件夹/程序/网页操作**
   - 可通过自然语言指令打开或关闭程序、文件夹和网页  
   - 支持多动作同时执行  

5. **图片和截图显示**
   - 聊天框可显示生成的截图和图片  

6. **PixelArt GUI 风格**
   - 左侧历史记录栏  
   - 右侧聊天窗口 + 动态进度条 + 输入框  
   - 滑块控制模式  

---

## 安装与依赖

### 1. 克隆仓库

```bash
git clone https://github.com/Yunle-Lee/Touchwithchat.git
cd AIDeskControl
