# 🅿️ 停车场欢迎语 · 高品质语音生成器

> 把停车场道闸里那句机械的「欢迎光临」，换成自然悦耳、与酒店调性匹配的声音。

## 为什么做这个

高档酒店的停车场，车一进去却是 8 毛钱电子表式的机械音「欢迎光临」，
和酒店花大价钱做的门脸、香氛、背景音乐完全不搭。

这个小工具：**输入话术 → 选音色 → 一键生成高品质 mp3**，用来替换道闸里的机械语音。
全程免费，无需 API key。

## 效果试听

同一句「欢迎光临」，不同音色对比（点击即可播放）：

| 音色 | 试听 |
|---|---|
| 晓晓（女·温柔知性） | [▶ 播放](examples/欢迎光临_晓晓.mp3) |
| 云健（男·成熟稳重） | [▶ 播放](examples/欢迎光临_云健.mp3) |
| 晓伊（女·甜美亲切） | [▶ 播放](examples/欢迎光临_晓伊.mp3) |
| 一路平安 · 晓晓 | [▶ 播放](examples/一路平安_晓晓.mp3) |
| 一路平安 · 云健 | [▶ 播放](examples/一路平安_云健.mp3) |

## 功能

- ✅ 输入任意话术，一键生成 mp3
- ✅ 8 款免费中文音色（温柔女声 / 甜美女声 / 成熟男声 / 年轻男声 / 播音腔 / 方言）
- ✅ 语速、语调、音量可调（音量 -20～+20 dB）
- ✅ 生成后显示时长，方便控制播报长短
- ✅ 预置停车场常用话术（欢迎光临 / 一路平安 / 临时车登记 / 车位已满 / 车牌未识别）
- ✅ 全程免费，无需注册、无需 API key

## 快速开始

### 在线体验（推荐）

部署到 HuggingFace Spaces 后，得到一个链接，打开即用，无需安装任何东西。
详见下方「部署到 HuggingFace Spaces」。

### 本地运行

```bash
# 1. 克隆
git clone <你的仓库地址>
cd parking-voice-generator

# 2. 安装依赖（国内建议加清华镜像）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 启动
python app.py
```

浏览器打开 http://127.0.0.1:7860 即可使用。

### 命令行用法

```bash
# 生成「欢迎光临」，默认音色晓晓
python generate.py "欢迎光临"

# 指定音色（成熟男声）+ 调语速语调音量
python generate.py "欢迎光临" -v zh-CN-YunjianNeural -r +10 -p -2 -vol +6

# 指定输出路径
python generate.py "一路平安，请慢走" -v zh-CN-XiaoxiaoNeural -o out.mp3
```

## 部署到 HuggingFace Spaces（免费在线链接）

1. 注册 [HuggingFace](https://huggingface.co) 账号；
2. 新建一个 Space，SDK 选 **Gradio**；
3. 把本仓库的 `app.py` 和 `requirements.txt` 推到 Space；
4. Space 自动构建，得到一个 `https://<用户名>-<空间名>.hf.space` 的在线链接。

## 技术栈

- Python
- [edge-tts](https://github.com/rany2/edge-tts)：微软 Edge 在线 TTS，免费、免 key、音色自然
- [Gradio](https://gradio.app)：Web 界面
- imageio-ffmpeg / mutagen：音量调整与时长读取（均为 pip 依赖，无需单独安装系统 ffmpeg）

## 项目结构

```
.
├── app.py                # Gradio Web 界面（本地运行 / 部署 HF Spaces）
├── generate.py           # 核心生成逻辑（合成 + 音量 + 时长），也可命令行使用
├── scripts/
│   └── make_examples.py  # 一键重新生成 examples/ 示例音频
├── examples/             # 预生成的示例音频
├── requirements.txt      # 依赖清单
├── LICENSE               # MIT 许可证
└── README.md
```

## 音色列表

| 音色 | 说明 |
|---|---|
| 晓晓 | 女 · 温柔知性 |
| 晓伊 | 女 · 甜美亲切 |
| 晓涵 | 女 · 温婉柔和 |
| 云希 | 男 · 年轻阳光 |
| 云健 | 男 · 成熟稳重 |
| 云扬 | 男 · 专业播音 |
| 晓北 | 东北 · 亲切接地气 |
| 晓妮 | 陕西 · 温柔亲和 |

## 后续迭代计划

- [ ] 声音克隆（录一段自己的声音，生成任意话术）
- [ ] 自录音色库
- [ ] 批量生成
- [ ] 更多停车场 / 门禁场景话术模板

## 免责声明

本项目生成的语音仅用于合法用途。使用他人声音（尤其是名人 / 公众人物）进行商业播报前，
请务必取得授权。

## License

[MIT](LICENSE)
