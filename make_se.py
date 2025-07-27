import numpy as np
import wave

def click_sound(rate=44100, length=0.04, freq=1800):
    t = np.linspace(0, length, int(rate * length), endpoint=False)
    # 短い矩形波でカチッとした音
    data = 0.7 * np.sign(np.sin(2 * np.pi * freq * t))
    # フェードアウト
    data *= np.linspace(1, 0, t.size)
    return data

def pin_sound(rate=44100, length=0.18, freq=2200):
    t = np.linspace(0, length, int(rate * length), endpoint=False)
    # 高音の減衰サイン波
    data = 0.6 * np.sin(2 * np.pi * freq * t)
    data *= np.exp(-6 * t)
    return data

def make_roulette_se(filename="seRoulette.wav", rate=44100):
    n_clicks = 13
    base_interval = 0.09  # 最初の間隔
    interval_growth = 1.22  # クリック間隔の増加率
    click = click_sound(rate)
    pin = pin_sound(rate)
    # クリック音を間隔を広げながら並べる
    sound = np.zeros(int(rate * 2.0))
    pos = 0
    interval = base_interval
    for i in range(n_clicks):
        idx = int(pos * rate)
        if idx + len(click) < len(sound):
            sound[idx:idx+len(click)] += click
        pos += interval
        interval *= interval_growth
    # 最後にピン音
    idx = int(pos * rate)
    if idx + len(pin) < len(sound):
        sound[idx:idx+len(pin)] += pin
    # 正規化
    sound = sound / np.max(np.abs(sound)) * 0.95
    sound = (sound * 32767).astype(np.int16)
    with wave.open(filename, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(sound.tobytes())

def make_result_se(filename="seResult.wav", duration=0.5, rate=44100):
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    # ファンファーレ風（和音：C, E, G）
    freqs = [523.25, 659.25, 783.99]
    data = sum(np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)
    # エンベロープ
    envelope = np.concatenate([
        np.linspace(0, 1, int(rate * 0.05)),
        np.ones(int(rate * 0.35)),
        np.linspace(1, 0, int(rate * 0.1))
    ])
    envelope = np.pad(envelope, (0, len(t) - len(envelope)), 'constant')
    data *= envelope * 0.5
    data = (data * 32767).astype(np.int16)
    with wave.open(filename, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(data.tobytes())
        
if __name__ == "__main__":
    make_roulette_se()
    make_result_se()
    print("seRoulette.wav と seResult.wav を生成しました。")