from pydub import AudioSegment
from pydub.silence import detect_leading_silence
import os

# 你的音频文件夹
AUDIO_FOLDER = r"C:\Users\未来可期\Desktop\py\py-my_audio\pinyin_clips"

# 裁剪配置（根据你录音的静音程度微调）
SILENCE_THRESHOLD = -40  # 静音阈值 dBFS
BUFFER = 20              # 保留一点点头尾，避免太生硬

def trim_silence(audio):
    # 裁剪前面的静音
    start_trim = detect_leading_silence(audio, silence_threshold=SILENCE_THRESHOLD)
    # 裁剪后面的静音
    end_trim = detect_leading_silence(audio.reverse(), silence_threshold=SILENCE_THRESHOLD)
    end_trim = len(audio) - end_trim
    # 保留一点缓冲
    start = max(0, start_trim - BUFFER)
    end = min(len(audio), end_trim + BUFFER)
    return audio[start:end]

def batch_trim_all_audios():
    files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith('.wav')]
    print(f"找到 {len(files)} 个音频，开始裁剪空白...")

    for fname in files:
        path = os.path.join(AUDIO_FOLDER, fname)
        sound = AudioSegment.from_file(path)
        trimmed = trim_silence(sound)
        trimmed.export(path, format='wav')
        print(f"已裁剪: {fname}")

    print("✅ 所有音频空白裁剪完成！")

if __name__ == "__main__":
    batch_trim_all_audios()