import pygame as pg


class AudioManager:
    def __init__(self) -> None:
        pg.mixer.set_reserved(1)

        self.title_music_path: str = "DOOM/resources/audio/music/title.mp3"
        self.level_complete_music_path: str = "DOOM/resources/audio/music/level_complete.mp3"

        self.item_pickup: pg.mixer.Sound = self.load_sound("item_pickup.wav")
        self.weapon_pickup: pg.mixer.Sound = self.load_sound("weapon_pickup.wav")

        self.pistol: pg.mixer.Sound = self.load_sound("pistol.wav")
        self.shotgun: pg.mixer.Sound = self.load_sound("shotgun.wav")

        self.player_hurt: pg.mixer.Sound = self.load_sound("player_hurt.wav")
        self.player_death: pg.mixer.Sound = self.load_sound("player_death.wav")

        self.enemy_idle: pg.mixer.Sound = self.load_sound("enemy_idle.wav")
        self.enemy_death: pg.mixer.Sound = self.load_sound("enemy_death.wav")
        self.enemy_attack: pg.mixer.Sound = self.load_sound("enemy_attack.wav")
        self.enemy_hurt: pg.mixer.Sound = self.load_sound("enemy_hurt.wav")
    
    def load_sound(self, file: str) -> pg.mixer.Sound:
        return pg.mixer.Sound(f"DOOM/resources/audio/{file}")
    
    def play(self, sound: pg.mixer.Sound, volume: float = 1):
        channel = pg.mixer.find_channel(True)
        sound.stop()
        sound.set_volume(volume)
        channel.play(sound)
    
    def play_music(self, music_path: str) -> None:
        pg.mixer.music.load(music_path)
        pg.mixer.music.play(-1)
    
    def stop_music(self) -> None:
        pg.mixer.music.stop()
