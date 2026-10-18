"""停车场欢迎语 · 语音生成核心模块。

基于微软 Edge TTS（edge-tts）：免费、免 API key、音色自然。
音量调整依赖 imageio-ffmpeg（自带 ffmpeg 二进制，随 pip 安装，无需单独装系统 ffmpeg）。
时长读取依赖 mutagen。
"""

import argparse
import asyncio
import os
import re
import subprocess
from datetime import datetime

import edge_tts
import imageio_ffmpeg
from mutagen.mp3 import MP3

# 音色库：voice_id -> 中文显示名（精选适合酒店/商业场景的自然音色）
VOICES = {
    "zh-CN-XiaoxiaoNeural": "晓晓（女·温柔知性）",
    "zh-CN-XiaoyiNeural": "晓伊（女·甜美亲切）",
    "zh-CN-XiaohanNeural": "晓涵（女·温婉柔和）",
    "zh-CN-YunxiNeural": "云希（男·年轻阳光）",
    "zh-CN-YunjianNeural": "云健（男·成熟稳重）",
    "zh-CN-YunyangNeural": "云扬（男·专业播音）",
    "zh-CN-liaoning-XiaobeiNeural": "晓北（东北·亲切接地气）",
    "zh-CN-shaanxi-XiaoniNeural": "晓妮（陕西·温柔亲和）",
}

# 停车场常用话术
PARKING_PHRASES = {
    "欢迎光临": "欢迎光临",
    "一路平安": "一路平安，请慢走",
    "临时车登记": "临时车辆，请登记后入场",
    "车位已满": "车位已满，请稍候",
    "车牌未识别": "车牌未识别，请重新入场",
}

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def _voice_short(voice_id: str) -> str:
    """从显示名提取音色简称，如 '晓晓（女·温柔知性）' -> '晓晓'。"""
    return VOICES[voice_id].split("（")[0]


def _safe_filename(text: str, max_len: int = 10) -> str:
    """清理文字，作为文件名片段。"""
    cleaned = re.sub(r'[\\/:*?"<>|\s]+', "", text)
    return cleaned[:max_len] or "语音"


def _apply_volume(src: str, dst: str, db: int) -> None:
    """用 ffmpeg 调整 mp3 音量。db 为正放大、为负缩小（单位 dB）。"""
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    gain = f"volume={db:+d}dB"
    cmd = [
        ffmpeg, "-y", "-i", src,
        "-af", gain,
        "-c:a", "libmp3lame", "-b:a", "192k",
        dst,
    ]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if proc.returncode != 0:
        raise RuntimeError(f"音量处理失败：{proc.stderr[-300:]}")


def synthesize(
    text: str,
    voice: str,
    rate: int = 0,
    pitch: int = 0,
    volume: int = 0,
    output_dir: str | None = None,
    output_path: str | None = None,
) -> str:
    """合成语音，返回输出 mp3 路径。

    text:   要朗读的文字
    voice:  音色 id（见 VOICES）
    rate:   语速，-50 ~ +50（百分比）
    pitch:  语调，-20 ~ +20（Hz）
    volume: 音量，-20 ~ +20（dB），0 为原始音量
    """
    text = (text or "").strip()
    if not text:
        raise ValueError("文字不能为空")
    if voice not in VOICES:
        raise ValueError(f"未知音色: {voice}（可选：{', '.join(VOICES)}）")

    output_dir = output_dir or OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    if output_path is None:
        fname = (
            f"{_safe_filename(text)}_{_voice_short(voice)}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        )
        output_path = os.path.join(output_dir, fname)

    rate_str = f"{rate:+d}%"
    pitch_str = f"{pitch:+d}Hz"

    async def _run():
        communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
        await communicate.save(output_path)

    asyncio.run(_run())

    # 音量后处理（edge-tts 不支持音量参数，用 ffmpeg 增益）
    if volume != 0:
        tmp = output_path + ".vol.mp3"
        _apply_volume(output_path, tmp, volume)
        os.replace(tmp, output_path)

    return output_path


def get_duration(path: str) -> float:
    """读取 mp3 时长（秒），保留 1 位小数。"""
    return round(MP3(path).info.length, 1)


def main():
    parser = argparse.ArgumentParser(description="停车场欢迎语语音生成器（edge-tts）")
    parser.add_argument("text", help="要朗读的文字，例如：欢迎光临")
    parser.add_argument(
        "-v", "--voice", default="zh-CN-XiaoxiaoNeural", help="音色 id，默认晓晓"
    )
    parser.add_argument("-r", "--rate", type=int, default=0, help="语速 -50~50（%%）")
    parser.add_argument("-p", "--pitch", type=int, default=0, help="语调 -20~20（Hz）")
    parser.add_argument("-vol", "--volume", type=int, default=0, help="音量 -20~20（dB）")
    parser.add_argument("-o", "--output", help="输出文件路径（默认自动生成）")
    args = parser.parse_args()

    path = synthesize(
        args.text, args.voice, args.rate, args.pitch, args.volume, output_path=args.output
    )
    dur = get_duration(path)
    print(f"已生成：{path}（时长 {dur} 秒）")


if __name__ == "__main__":
    main()
