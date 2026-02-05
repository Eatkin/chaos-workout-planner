import os
import random
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

import pygame

from hero_workout.logging_config import get_logger
from hero_workout.config import MUSIC_SRC


class MusicHandler:
    def __init__(self, fade_ms: int = 1000, music_dir: str = MUSIC_SRC):
        """
        music_dir: directory where mp3/wav files are stored
        fade_ms: fade-in/out duration in milliseconds
        """
        self.logger = get_logger(self.__class__.__name__)
        self.music_dir = Path(music_dir)
        self.fade_ms = fade_ms

        pygame.mixer.init()
        self.playlist = self._load_music()
        self.track_positions: Dict[str, float] = {}  # remember position in seconds for each track
        self.current_track: Optional[str] = None

    def _load_music(self) -> List[str]:
        if not self.music_dir.exists():
            return []
        return [str(f) for f in self.music_dir.iterdir() if f.suffix.lower() in ('.mp3', '.wav', '.ogg')]

    def play(self) -> None:
        """Play a random track from last known position."""
        if not self.playlist:
            return
        track = random.choice(self.playlist)
        self.current_track = track
        pos = self.track_positions.get(track, 0.0)
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(loops=-1, start=pos)
        volume = 1.0
        # Dumb override for LOUD AS HELL Team Mekano
        self.logger.debug(f"Playing track {self.current_track}")
        if "Mekano" in self.current_track:
            self.logger.debug("Team Mekano detected, quietening!")
            volume = 0.3
        pygame.mixer.music.set_volume(volume)

    def stop(self, fadeout: bool = True) -> None:
        """Stop current track with optional fade out and save position."""
        if not self.current_track:
            return
        if fadeout:
            pygame.mixer.music.fadeout(self.fade_ms)
        else:
            pygame.mixer.music.stop()
        # Save position
        if pygame.mixer.music.get_busy():
            self.track_positions[self.current_track] = pygame.mixer.music.get_pos() / 1000.0

    def next_track(self) -> None:
        """Stop current track and play a new random track."""
        self.stop(fadeout=True)
        self.play()

    def quieten(self) -> None:
        """Sets volume to half"""
        vol = pygame.mixer.music.get_volume()
        target_vol = vol * 0.5
        self.logger.debug(f"Quietening to {target_vol}")
        pygame.mixer.music.set_volume(target_vol)

    def louden(self) -> None:
        """Sets volume to double"""
        vol = pygame.mixer.music.get_volume()
        target_vol = vol * 2
        self.logger.debug(f"Increasing volume to {target_vol}")
        pygame.mixer.music.set_volume(target_vol)


    def pause(self) -> None:
        pygame.mixer.music.pause()

    def unpause(self) -> None:
        pygame.mixer.music.unpause()

    def is_playing(self) -> bool:
        return pygame.mixer.music.get_busy()
