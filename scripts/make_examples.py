"""重新生成 examples/ 目录下的示例音频，保证示例可复现。

用法：python scripts/make_examples.py
"""

import os
import sys

# 确保能 import 项目根的 generate 模块（无论从哪个目录运行）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate import synthesize

# (话术, 音色 id, 输出文件名)
EXAMPLES = [
    ("欢迎光临", "zh-CN-XiaoxiaoNeural", "欢迎光临_晓晓.mp3"),
    ("欢迎光临", "zh-CN-YunjianNeural", "欢迎光临_云健.mp3"),
    ("欢迎光临", "zh-CN-XiaoyiNeural", "欢迎光临_晓伊.mp3"),
    ("一路平安，请慢走", "zh-CN-XiaoxiaoNeural", "一路平安_晓晓.mp3"),
    ("一路平安，请慢走", "zh-CN-YunjianNeural", "一路平安_云健.mp3"),
]


def main():
    out_dir = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "examples")
    )
    os.makedirs(out_dir, exist_ok=True)
    for text, voice, fname in EXAMPLES:
        path = synthesize(text, voice, output_path=os.path.join(out_dir, fname))
        print(f"已生成：{path}")


if __name__ == "__main__":
    main()
