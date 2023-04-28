"""Module for the game's player character.

This module contains the Player class, which represents the player character in the game.
The player can move around the game world, aim and shoot weapons, and take damage.

Attributes:
    None

Classes:
    `Player`: Represents the player character in the game.
"""

import math
import pygame as pg

from config import *
from weapon import *
from inventory import Inventory


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

    def __init__(self, game) -> None:
        self.game = game
        self.angle: float = 0
        self.x, self.y = 1.5, 1.5
        self.diag_move_corr = 1 / math.sqrt(2)
        self.mouse_rel: float = 0

        self.inventory: Inventory = Inventory(self.game)

        self.weapon: Weapon = None  # avoid circular initialization by setting this later
        self.weapon_shot: bool = False

        self.health: int = 100
        self.armor: int = 0
    
    def single_weapon_fire(self, event: pg.event.Event) -> None:
        """
        Fire the player's weapon once if the left mouse button is pressed, and the weapon is ready to fire.
        Decreases the weapon's ammo count by one and plays the weapon's firing sound.
        
        Args:
            event (pygame.event.Event): A pygame event object containing the event type and button pressed.
        
        Returns:
            None
        """

        # Check if the mouse button is pressed down, and if it is the left button and the player is not currently shooting or reloading.
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.weapon_shot and not self.weapon.reloading and self.weapon.ammo > 0:
                # If these conditions are met, play the weapon sound, decrease the ammo count, and set the weapon_shot and reloading flags to True.
                self.weapon.play_sound()
                self.weapon.ammo -= 1
                self.weapon_shot = True
                self.weapon.reloading = True
    
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

        # if event.type == pg.KEYDOWN:
        #     key = event.key
        #     if key == pg.K_2 or key == pg.K_AT:
        #         weapon = 0
        #     elif key == pg.K_3 or key == pg.K_HASH:
        #         weapon = 1
        #     elif key == pg.K_4 or key == pg.K_DOLLAR:
        #         weapon = 2
        #     elif key == pg.K_5 or key == pg.K_PERCENT:
        #         weapon = 3
        #     elif key == pg.K_6 or key == pg.K_CARET:
        #         weapon = 4
        #     elif key == pg.K_7 or key == pg.K_AMPERSAND:
        #         weapon = 5
        #     else:
        #         weapon = -1
            
        

    def set_weapon(self, weapon: Weapon) -> None:
        """This function literally just sets the weapon."""

        # Set the weapon to be the weapon. The weapon is now the weapon. This comment is as useless as this function.
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
        self.health -= amount
        # if health below 0 (die)
        if self.health <= 0:
            # set to 0
            self.health = 0
            # kill the player :D
            self.death()
    
    def death(self) -> None:
        """Die."""

        ...  # TODO
    
    def movement(self) -> None:
        """Handles the movement."""

        # calculates the angles
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        # delta x and y
        dx, dy = 0, 0

        # multiply the speed by deltatime
        speed = PLAYER_MOVE_SPEED * self.game.deltatime

        # get all keys pressed
        keys = pg.key.get_pressed()
        num_key_pressed = -1

        # sprint
        if keys[pg.K_LSHIFT]:
            speed *= 1.65
        
        # calculate the player position in the next frame with trigonometry
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

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
    
    @property
    def position(self) -> tuple[float, float]:
        return self.x, self.y
    
    @property
    def grid_position(self) -> tuple[int, int]:
        return int(self.x), int(self.y)

    def update(self) -> None:
        self.movement()
        self.mouse_control()
        self.switch_weapon()
        self.weapon.update()
