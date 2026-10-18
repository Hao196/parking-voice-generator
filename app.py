"""停车场欢迎语 · 高品质语音生成器（Gradio 界面）。

本地运行：python app.py
也可免费部署到 HuggingFace Spaces，得到一个可在线体验的链接。
"""

import gradio as gr

from generate import PARKING_PHRASES, VOICES, get_duration, synthesize

# 下拉选项：[(显示名, voice_id), ...]
VOICE_CHOICES = [(label, vid) for vid, label in VOICES.items()]


def generate(text: str, voice: str, rate: int, pitch: int, volume: int):
    """生成语音，返回 (音频文件路径, 下载文件路径, 时长说明)。"""
    try:
        path = synthesize(text, voice, int(rate), int(pitch), int(volume))
        dur = get_duration(path)
        return path, path, f"本句时长约 {dur} 秒"
    except Exception as exc:  # noqa: BLE001
        raise gr.Error(f"生成失败：{exc}") from exc


with gr.Blocks(title="停车场欢迎语 · 高品质语音生成器") as demo:
    gr.Markdown("# 🅿️ 停车场欢迎语 · 高品质语音生成器")
    gr.Markdown(
        "输入话术，选一个音色，一键生成自然悦耳的车场语音，"
        "替换掉机械的「欢迎光临」。基于微软 Edge TTS，免费、无需 key。"
    )

    with gr.Row():
        textbox = gr.Textbox(
            label="话术内容（自由定制）",
            value=PARKING_PHRASES["欢迎光临"],
            lines=2,
            placeholder="输入要播报的话术，例如：欢迎光临，祝您停车愉快",
        )
        with gr.Column():
            voice_dd = gr.Dropdown(
                label="音色",
                choices=VOICE_CHOICES,
                value="zh-CN-XiaoxiaoNeural",
            )
            rate_sl = gr.Slider(-50, 50, value=0, step=5, label="语速（%，越大越快越短）")
            pitch_sl = gr.Slider(-20, 20, value=0, step=1, label="语调（Hz）")
            volume_sl = gr.Slider(-20, 20, value=0, step=1, label="音量（dB，正放大负缩小）")

    gr.Markdown("**快捷话术**：")
    with gr.Row():
        for label, phrase in PARKING_PHRASES.items():
            btn = gr.Button(label)
            btn.click(lambda p=phrase: p, outputs=textbox)

    gen_btn = gr.Button("🎙️ 生成语音", variant="primary")

    with gr.Row():
        audio_out = gr.Audio(label="试听")
        file_out = gr.File(label="下载 mp3")
    duration_out = gr.Textbox(label="时长", interactive=False)

    gen_btn.click(
        generate,
        inputs=[textbox, voice_dd, rate_sl, pitch_sl, volume_sl],
        outputs=[audio_out, file_out, duration_out],
    )


if __name__ == "__main__":
    demo.launch()
