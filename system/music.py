import pygame
import threading
import subprocess

def play_music(music_file):
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # ループ再生

def run_stretching_exercise(script_file):
    subprocess.run(["python3", script_file])

if __name__ == "__main__":
    music_file = "Radio.mp3"  # 音楽ファイルのパスを指定してください
    script_file = "time_exercise.py"  # 実行するスクリプトのファイル名

    # 音楽を再生するスレッドを作成
    music_thread = threading.Thread(target=play_music, args=(music_file,))
    music_thread.start()

    # ストレッチングエクササイズのスクリプトを実行
    run_stretching_exercise(script_file)

    # スクリプトが終了したら音楽を止める
    pygame.mixer.music.stop()