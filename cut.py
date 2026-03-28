from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

# ===================== 配置 =====================
INPUT_FILE = "C:/Users/未来可期/Desktop/py/py-my_audio/video.mp4"  # 你的视频路径

# 静音切割参数
SILENCE_THRESHOLD = -40
MIN_SILENCE_LEN = 300
KEEP_SILENCE = 20

# 拼音列表（和你录音顺序完全一致）
PINYIN_LIST = [
    # --------------- 声母 ----------------
    'b', 'p', 'm', 'f', 'd', 't', 'n', 'l',
    'g', 'k', 'h', 'j', 'q', 'x',
    'zh', 'ch', 'sh', 'r', 'z', 'c', 's',
    'y', 'w',

    # --------------- 单韵母（带调）----------------
    'ā', 'á', 'ǎ', 'à',
    'ō', 'ó', 'ǒ', 'ò',
    'ē', 'é', 'ě', 'è',
    'ī', 'í', 'ǐ', 'ì',
    'ū', 'ú', 'ǔ', 'ù',
    'ǖ', 'ǘ', 'ǚ', 'ǜ',

    # --------------- 复韵母（带调）----------------
    'āi', 'ái', 'ǎi', 'ài',
    'ēi', 'éi', 'ěi', 'èi',
    'uī', 'uí', 'uǐ', 'uì',
    'āo', 'áo', 'ǎo', 'ào',
    'ōu', 'óu', 'ǒu', 'òu',
    'iū', 'iú', 'iǔ', 'iù',
    'iē', 'ié', 'iě', 'iè',
    'üē', 'üé', 'üě', 'üè',
    'ēr', 'ér', 'ěr', 'èr',

    # --------------- 前鼻韵母（带调）----------------
    'ān', 'án', 'ǎn', 'àn',
    'ēn', 'én', 'ěn', 'èn',
    'īn', 'ín', 'ǐn', 'ìn',
    'ūn', 'ún', 'ǔn', 'ùn',
    'ǖn', 'ǘn', 'ǚn', 'ǜn',

    # --------------- 后鼻韵母（带调）----------------
    'āng', 'áng', 'ǎng', 'àng',
    'ēng', 'éng', 'ěng', 'èng',
    'īng', 'íng', 'ǐng', 'ìng',
    'ōng', 'óng', 'ǒng', 'òng',


    # --------------- 整体认读音节（带调）----------------
    'zhī', 'zhí', 'zhǐ', 'zhì',
    'chī', 'chí', 'chǐ', 'chì',
    'shī', 'shí', 'shǐ', 'shì',
    'rī', 'rí', 'rǐ', 'rì',
    'zī', 'zí', 'zǐ', 'zì',
    'cī', 'cí', 'cǐ', 'cì',
    'sī', 'sí', 'sǐ', 'sì',

    'yī', 'yí', 'yǐ', 'yì',
    'wū', 'wú', 'wǔ', 'wù',
    'yū', 'yú', 'yǔ', 'yù',

    'yē', 'yé', 'yě', 'yè',
    'yuē', 'yué', 'yuě', 'yuè',
    'yuān', 'yuán', 'yuǎn', 'yuàn',
    'yīn', 'yín', 'yǐn', 'yìn',
    'yūn', 'yún', 'yǔn', 'yùn',
    'yīng', 'yíng', 'yǐng', 'yìng'
]

# ===================== 核心函数 =====================
def split_and_save():
    print("加载视频/音频中...")
    
    # ✅ 修复点：自动识别格式，不再强制wav
    sound = AudioSegment.from_file(INPUT_FILE)

    print("正在按静音切割...")
    chunks = split_on_silence(
        sound,
        min_silence_len=MIN_SILENCE_LEN,
        silence_thresh=SILENCE_THRESHOLD,
        keep_silence=KEEP_SILENCE
    )

    print(f"切割完成，共 {len(chunks)} 段")

    if len(chunks) != len(PINYIN_LIST):
        print(f"⚠️  警告：切割出 {len(chunks)} 段，但音标有 {len(PINYIN_LIST)} 个")

    os.makedirs("pinyin_clips", exist_ok=True)

    for i, chunk in enumerate(chunks):
        if i >= len(PINYIN_LIST):
            break
        name = PINYIN_LIST[i]
        fname = f"pinyin_clips/{name}.wav"
        chunk.export(fname, format="wav")
        print(f"已保存: {fname}")

    print("✅ 全部保存完成！")

if __name__ == "__main__":
    split_and_save()