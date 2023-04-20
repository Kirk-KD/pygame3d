import pygame as pg


class AudioManager:
    def __init__(self) -> None:
        self.music_path: str = None

        self.pistol: pg.mixer.Sound = self.load_sound("pistol.wav")
        self.shotgun: pg.mixer.Sound = self.load_sound("shotgun.wav")
    
    def load(self, music_path: str) -> None:
        self.music_path = f"DOOM/resources/audio/music/{music_path}"
    
    def load_sound(self, file: str) -> pg.mixer.Sound:
        return pg.mixer.Sound(f"DOOM/resources/audio/{file}")
    
    def play(self, sound: pg.mixer.Sound):
        pg.mixer.Sound.play(sound)
    
    def play_music(self) -> None:
        pg.mixer.music.load(self.music_path)
        pg.mixer.music.play(-1)
    
    def stop_music(self) -> None:
        pg.mixer.music.stop()
