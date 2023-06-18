"""Module for the game's player character.

This module contains the Player class, which represents the player character in the game.
The player can move around the game world, aim and shoot weapons, and take damage.

Attributes:
    None

Classes:
    `Player`: Represents the player character in the game.
"""

# import future and typing
from __future__ import annotations

import math
from typing import TYPE_CHECKING, Tuple
import pygame as pg

from config import PLAYER_MOVE_SPEED, PLAYER_SIZE_SCALE, MOUSE_MAX_REL, MOUSE_SPEED, CLASSIC_MOUSE_SPEED, FPS
from weapon import Weapon
from inventory import Inventory
from menu.level_complete_menu import LevelCompleteMenu

if TYPE_CHECKING:
    from game import Game


class Player:
    """A class representing the player character in the game.

    Attributes:
        `game` (`Game`): The game instance this player belongs to.
        `angle` (`float`): The current angle the player is facing.
        `x` (`float`): The current x coordinate of the player in the game world.
        `y` (`float`): The current y coordinate of the player in the game world.
        `diag_move_corr` (`float`): Correction factor for diagonal movement.
        `mouse_rel` (`float`): The relative movement of the mouse.
        `inventory` (`Inventory`): The player's inventory instance.
        `weapon` (`Weapon`): The current weapon the player is holding.
        `weapon_shot` (`bool`): Flag indicating whether a shot has been fired.
        `health` (`int`): The current health points of the player.
        `armor` (`int`): The current armor points of the player.
    """

    def __init__(self, game: Game) -> None:
        self.game: Game = game
        self.angle: float = 0
        self.x, self.y = 1.5, 1.5
        self.diag_move_corr = 1 / math.sqrt(2)
        self.mouse_rel: float = 0

        self.inventory: Inventory = Inventory(self.game)

        self.weapon: Weapon = None  # avoid circular initialization by setting this later
        self.weapon_shot: bool = False

        self.health: int = 100
        self.health_cap: int = 100
        self.armor: int = 0
        self.armor_cap: int = 100
        self.damage_reduction: float = 0

    def single_weapon_fire(self, event: pg.event.Event) -> None:
        """
        Fire the player's weapon once if the left mouse button is pressed, and the 
        weapon is ready to fire. Decreases the weapon's ammo count by one and plays 
        the weapon's firing sound.
        
        Args:
            event (pygame.event.Event): A pygame event object containing the event 
                type and button pressed.
        
        Returns:
            None
        """

        if not self.game.classic_control:
            # Check if the mouse button is pressed down, and if it is the left button
            # and the player is not currently shooting or reloading.
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.shoot()

    def shoot(self) -> None:
        if self.is_dead:
            return

        if (not self.weapon_shot and
            not self.weapon.reloading and
            self.weapon.ammo > 0):
            # If these conditions are met, play the weapon sound, decrease the
            # ammo count, and set the weapon_shot and reloading flags to True.
            self.weapon.play_sound()
            self.weapon.ammo -= 1
            self.weapon_shot = True
            self.weapon.reloading = True

            self.game.shots_fired += 1

    def switch_weapon(self) -> None:
        """Check keyboard inputs to switch weapon."""

        keys = pg.key.get_pressed()
        if keys[pg.K_2]:
            weapon = 0
        elif keys[pg.K_3]:
            weapon = 1
        elif keys[pg.K_4]:
            weapon = 2
        elif keys[pg.K_5]:
            weapon = 3
        elif keys[pg.K_6]:
            weapon = 4
        elif keys[pg.K_7]:
            weapon = 5
        else:
            weapon = -1

        if weapon != -1 and self.inventory.has_weapon_at(weapon):
            self.set_weapon(self.inventory.weapons[weapon])

    def set_weapon(self, weapon: Weapon) -> None:
        """This function literally just sets the weapon."""

        if isinstance(weapon, type(self.weapon)):
            return

        self.weapon = weapon

    def give_weapon(self, weapon: Weapon) -> None:
        self.set_weapon(weapon)

        for w in self.inventory.weapons:
            if w.__class__ == weapon.__class__:
                return

        self.inventory.add_weapon(weapon)

    def take_damage(self, amount: int) -> None:
        """Make the player suffer and take damage."""

        # take damage
        reduced = int(amount * self.damage_reduction)
        self.health -= amount - reduced
        self.armor -= reduced

        # if armor is gone
        if self.armor < 0:
            self.armor = 0
            self.damage_reduction = 0

        # if health below 0 (die)
        if self.health <= 0:
            # set to 0
            self.health = 0
            # kill the player :D
            self.death()
        else:
            self.game.audio_manager.player_hurt.stop()
            self.game.audio_manager.play(self.game.audio_manager.player_hurt)

    def heal(self, amount: int) -> None:
        """Heal the player"""

        if self.is_dead:
            return

        self.health += amount
        if self.health > self.health_cap:
            self.health = self.health_cap

    def set_armor(self, amount: int) -> None:
        self.armor = amount

    def set_damage_reduction(self, percentage: float) -> None:
        self.damage_reduction = percentage

    def set_armor_cap(self, new_cap: int) -> None:
        self.armor_cap = new_cap

    def death(self) -> None:
        """Die."""

        self.mouse_rel = 0
        self.game.deaths += 1

        self.game.audio_manager.play(self.game.audio_manager.player_death)

    def movement(self) -> None:
        """Handles the movement."""

        # calculates the angles
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        # delta x and y
        dx, dy = 0, 0

        # multiply the speed by deltatime
        speed = PLAYER_MOVE_SPEED * self.game.deltatime
        classic_mouse_speed = CLASSIC_MOUSE_SPEED * self.game.deltatime
        rel = 700 * self.game.deltatime

        # get all keys pressed
        keys = pg.key.get_pressed()
        num_key_pressed = -1

        # sprint
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
            speed *= 1.65
            classic_mouse_speed *= 1.65
            rel *= 1.65

        # calculate the player position in the next frame with trigonometry
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        clear_mouse_rel = True

        if self.game.classic_control:
            if keys[pg.K_UP]:
                num_key_pressed += 1
                dx += speed_cos
                dy += speed_sin
            
            if keys[pg.K_DOWN]:
                num_key_pressed += 1
                dx += -speed_cos
                dy += -speed_sin
            
            if keys[pg.K_LEFT]:
                if keys[pg.K_LALT] or keys[pg.K_RALT]:  # strafe left
                    num_key_pressed += 1
                    dx += speed_sin
                    dy += -speed_cos
                else:  # turn left
                    clear_mouse_rel = False
                    self.angle -= classic_mouse_speed
                    self.mouse_rel = -rel
            
            if keys[pg.K_RIGHT]:
                if keys[pg.K_LALT] or keys[pg.K_RALT]:  # starfe right
                    num_key_pressed += 1
                    dx += -speed_sin
                    dy += speed_cos
                else:  # turn right
                    clear_mouse_rel = False
                    self.angle += classic_mouse_speed
                    self.mouse_rel = rel
            
            if keys[pg.K_COMMA]:  # strafe left
                num_key_pressed += 1
                dx += speed_sin
                dy += -speed_cos
            
            if keys[pg.K_PERIOD]:  # strafe right
                num_key_pressed += 1
                dx += -speed_sin
                dy += speed_cos
        else:
            # W
            if keys[pg.K_w]:
                num_key_pressed += 1
                dx += speed_cos
                dy += speed_sin
            # S
            if keys[pg.K_s]:
                num_key_pressed += 1
                dx += -speed_cos
                dy += -speed_sin
            # A
            if keys[pg.K_a]:
                num_key_pressed += 1
                dx += speed_sin
                dy += -speed_cos
            # D
            if keys[pg.K_d]:
                num_key_pressed += 1
                dx += -speed_sin
                dy += speed_cos

        # diagnal move speed correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        # check collision (its literally in the method name)
        self.check_collision(dx, dy)

        # set the angle back in range
        self.angle %= math.tau

        # clear rel
        if clear_mouse_rel:
            self.mouse_rel = 0

    def check_collision(self, dx: float, dy: float) -> None:
        """Check collision."""

        # restore player size from the deltatime
        scale = PLAYER_SIZE_SCALE / self.game.deltatime

        # if player's x is unoccupied, move
        if self.game.level.map.unoccupied(int(self.x + dx * scale), int(self.y)):
            self.x += dx

        # if the player's y is unoccupied, move
        if self.game.level.map.unoccupied(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def mouse_control(self) -> None:
        self.mouse_rel = pg.mouse.get_rel()[0]
        self.mouse_rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.mouse_rel))
        self.angle += self.mouse_rel * MOUSE_SPEED

    def use_lever(self) -> None:
        if self.game.level.png_map.can_use_lever(self):
            if self.game.kills_percentage >= 70:
                self.game.stop_timer()
                self.game.open_menu(LevelCompleteMenu(self.game))
            else:
                self.game.hud_renderer.console("kill at least 70% of all enemies to proceed.", FPS * 2.5)

    @property
    def position(self) -> Tuple[float, float]:
        return self.x, self.y

    @property
    def grid_position(self) -> Tuple[int, int]:
        return int(self.x), int(self.y)

    @property
    def is_dead(self) -> bool:
        return self.health <= 0

    def update(self) -> None:
        if self.is_dead:
            return
        
        self.movement()
        if not self.game.classic_control:
            self.mouse_control()
        self.switch_weapon()
        self.weapon.update()
