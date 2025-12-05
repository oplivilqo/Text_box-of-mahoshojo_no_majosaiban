**【注意: `main`分支当前处于不可用状态，请在下方[选择分支](#分支指引)】**

# 🎭魔法少女的魔女裁判 文本框生成器

一个基于Python的自动化表情包生成工具，能够快速生成带有自定义文本的魔法少女的魔女裁判文本框图片。[灵感来源与代码参考](https://github.com/MarkCup-Official/Anan-s-Sketchbook-Chat-Box)

## 预览
<img width="600" height="195" alt="5f10f4239bc8a82812e505fd0c4f5567" src="https://github.com/user-attachments/assets/6fb46a8d-4fc4-4d10-80a0-ed21fbb428bf" /><img width="600" height="195" alt="96038673678af657e937d20617322e81" src="https://github.com/user-attachments/assets/847c331e-9274-4b60-9b42-af0a80265391" />

## 分支指引
由于本项目正在蒸蒸日上（喜，有很多老师都为本项目提交了自己的贡献，但全都挤进main分支有点百家争鸣了（悲

因此本项目当前使用分支管理各位老师独具匠心的思路，下面提供各分支的预览与指北，可以根据自己的喜好选择合适的分支：

1. **主分支** 👈您在这里

2. **[古早版本](https://github.com/oplivilqo/manosaba_text_box/tree/legacy)**: `legacy`分支
   - 纯命令行界面，监听全局快捷键的古早版本，「但是没bug」。
3. **tkinter GUI** (现在还没合并但未来可期)
   - 简单易用的用户界面，同时带有预览。适合大多数用户。
   - 目前有三位老师正在爆肝：
      1. @YangQwQ _[PR #41](https://github.com/oplivilqo/manosaba_text_box/pull/41)_: [仓库地址](https://github.com/YangQwQ/Text_box-of-mahoushoujo_no_majosaiban-GUI) (已发布Release)
      2. @morpheus315 _[PR #32](https://github.com/oplivilqo/manosaba_text_box/pull/32)_: [仓库地址](https://github.com/morpheus315/Text_box-of-mahoushoujo_no_majosaiban-NEO) (已发布Release)
      3. @thgg678 _[PR #23](https://github.com/oplivilqo/manosaba_text_box/pull/23)_: [仓库地址](https://github.com/thgg678/Text_box-of-mahoushoujo_no_majosaiban)
4. **[textual TUI](https://github.com/oplivilqo/manosaba_text_box/tree/refresh)**: `refresh`分支(比较新) 或 _`main`分支(当前分支)_
   - 直接在运行终端展示的用户界面，适合少数喜欢终端UI的用户。但暂时无法实现图片预览。
   ![TUI界面截图](https://github.com/user-attachments/assets/5d1219c4-582f-4573-a605-065d6abc5337)
5. **[JavaScript WebUI](https://github.com/oplivilqo/manosaba_text_box/tree/lite)**: `lite`分支
   - 无需Python环境，使用浏览器实现的版本。适合偶尔生成图片的用户。
   ![JS版界面截图](https://github.com/user-attachments/assets/38d0e142-8707-4f43-b1a8-1bb0bcdbe848)

## 使用方法

### 核心功能

1. 切换角色 - 使用UI选择目标角色和表情
2. 输入文本 - 在聊天框或文本编辑器中输入想要添加的文本
3. 生成图片 - 按下 `Ctrl+E` 键自动生成并发送
4. 清理缓存 - 一键清理生成的临时图片

### 使用提醒

由于制作时采取了合成图片的思路，第一次切换角色后需要等待读条，无法立即使用



### 添加自定义角色
#### 第1步
请下载需要的角色图片，放置于`<根目录>/assets/chara/<角色名>`文件夹中，
并统一命名格式为`<角色名> (<差分编号>)`，如图：
<img width="230" height="308" alt="image" src="https://github.com/user-attachments/assets/892b6c8e-b857-482b-94be-07ad240f2a3b" />
> 注意角色名与编号之间的空格

#### 第2步
修改**2个**配置文件，位于`<根目录>/config`文件夹：
1. `chara_meta.yml`: 包含角色元数据，在末尾添加：
```yaml
warden:  # 填写角色名（与你的文件夹名相同）
  full_name: 典狱长  # 填写角色全名（仅用于可读性显示）
  emotion_count: 1   # 填写差分数量
  font: font3.ttf    # 填写使用的字体
```
2. `text_configs.yml`: 包含角色名称的显示方法，在末尾添加：
```yaml
warden:
  - text: 典 # 文字内容
    position: [ 759, 63 ]  # 绝对坐标
    font_color: [ 195, 209, 231 ]  # 颜色RGB值
    font_size: 196  # 文字大小
  - text: 狱 # 下面以此类推
    position: [ 948, 175 ]
    font_color: [ 255, 255, 255 ]
    font_size: 92
  - text: 长
    position: [ 1053, 117 ]
    font_color: [ 255, 255, 255 ]
    font_size: 147
  - text: ""
    position: [ 0, 0 ]
    font_color: [ 255, 255, 255 ]
    font_size: 1
```
由于制作时采取了合成图片的思路，第一次切换角色后需要等待合成，无法立即使用

另外，若要使用角色，请下载对应角色文件夹并放到main.py文件所在目录中

## 更新日志（学长说最好写个这东西，虽然没写过但是先养成习惯？）

### v1.1.5

- 增添了自主切换表情功能
- 将特殊字体改为红色


### 许可证

本项目基于MIT协议传播，仅供个人学习交流使用，不拥有相关素材的版权。进行分发时应注意不违反素材版权与官方二次创造协定。

## 结语

受B站上MarkCup做的夏目安安传话筒启发，以夏目安安传话筒为源代码编写了这样一个文本框脚本。
由于本人是初学者，第一次尝试写这种代码，有许多地方尚有改进的余地，望多多包含。

## QQ群

震撼来袭 魔裁吹水群
1037032551
目前只有个位数人😢

<div align="right">
  
### 以上. 柊回文————2025.11.15













