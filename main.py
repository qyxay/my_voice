from pypinyin import pinyin, Style
import os
from pydub import AudioSegment
import subprocess

AUDIO_FOLDER = r"C:\Users\未来可期\Desktop\py\py-my_audio\pinyin_clips"

def split_pinyin(py):
    # 整体认读音节
    whole_readings = {
        'zhi','chi','shi','ri','zi','ci','si',
        'yi','wu','yu','ye','yue','yuan','yin','yun','ying'
    }

    # 声调映射
    tone_map = {
        'ā':'a','á':'a','ǎ':'a','à':'a',
        'ō':'o','ó':'o','ǒ':'o','ò':'o',
        'ē':'e','é':'e','ě':'e','è':'e',
        'ī':'i','í':'i','ǐ':'i','ì':'i',
        'ū':'u','ú':'u','ǔ':'u','ù':'u',
        'ǖ':'ü','ǘ':'ü','ǚ':'ü','ǜ':'ü',
    }

    # 去掉声调
    py_no_tone = ''
    for c in py:
        py_no_tone += tone_map.get(c, c)

    # 整体认读 → 不拆
    if py_no_tone in whole_readings:
        return py, ''

    # ======================
    # 🔥 强制修复 zhuang / chuang / shuang
    # 直接拆成 声母 + āng
    # ======================
    if py.startswith('zh'):
        return 'zh', py[-3:]  # 取最后3个音（āng/áng/ǎng/àng）
    if py.startswith('ch'):
        return 'ch', py[-3:]
    if py.startswith('sh'):
        return 'sh', py[-3:]

    # 正常拆分
    if py and py[0] in 'bpmfdtnlgkhjqxzcsryw':
        return py[0], py[1:]

    return '', py


def text_to_combined_audio(text):
    pinyin_list = [p[0] for p in pinyin(text, style=Style.TONE)]
    print("拼音：", " ".join(pinyin_list))

    combined = AudioSegment.empty()

    for py in pinyin_list:
        sm, ym = split_pinyin(py)
        
        # 先把当前字的 声母+韵母 拼成流畅的一段
        char_audio = AudioSegment.empty()
        for part in [sm, ym]:
            if not part:
                continue
            path = os.path.join(AUDIO_FOLDER, f"{part}.wav")
            if os.path.exists(path):
                audio = AudioSegment.from_file(path)
                
                if len(char_audio) == 0:
                    char_audio = audio
                else:
                    # 🔥 核心：2ms 极淡过渡，不卡壳、不杂音
                    char_audio = char_audio.append(audio, crossfade=100)
        
        # 把这个字的完整发音加到总音频里
        combined += char_audio

    # 导出成临时完整音频
    temp = "temp_play.wav"
    combined.export(temp, format="wav")
    return temp

def play_once(file):
    subprocess.run(
        ["powershell", "-c", f"(New-Object Media.SoundPlayer '{file}').PlaySync();"],
        creationflags=0x08000000,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

if __name__ == "__main__":
    text = input("请输入汉字：")
    audio_file = text_to_combined_audio(text)
    play_once(audio_file)
    os.remove(audio_file)