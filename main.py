#!/usr/bin/env python3.10
# Create a 3D FPS Game

import itertools
import ursina as u
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

import time
import random
import math
import sys
import os

u.Entity.default_shader = lit_with_shadows_shader
crate_spread = 64
enabled = False

game = u.Ursina(width=800, height=600, title="Reckoning",
                fullscreen=False, icon="./assets/icons/logo.png")

ground = u.Entity(model="plane", collider="box", scale=crate_spread * 4,
                  texture="grass", texture_scale=(4, 4))

player = FirstPersonController(
    model="cube", z=-10, color=u.color.orange, origin_y=-0.5, speed=10)
player.collider = u.BoxCollider(player, size=(0, 1, 0))

vision_light = u.SpotLight(
    parent=u.camera, size=(25, 25, 25), origin=(0, 0, 0))
vision_light.look_at(u.Vec3(0, 0, 1))

for _ in range(128):
    u.Entity(model="cube", origin_y=-.5, scale=2, texture="brick", texture_scale=(1, 2), x=u.random.uniform(-crate_spread, crate_spread) + crate_spread,
             z=u.random.uniform(-crate_spread, crate_spread), collider="box", scale_y=u.random.uniform(2, 3), color=u.color.hsv(0, 0, u.random.uniform(.9, 1)))

for i, j in itertools.product(range(crate_spread), range(0, crate_spread, 2)):
    u.Entity(model="cube", origin_y=-.5, scale=2, texture="brick", texture_scale=(1, 2), x=j,
             y=i, z=i, collider="box", scale_y=2, color=u.color.hsv(0, 0, u.random.uniform(.9, 1)))


def pause_input(key):
    global enabled

    if key == "tab":
        enabled = not enabled

        player.visible_self = not enabled
        player.cursor.enabled = not enabled
        u.mouse.locked = not enabled

        u.application.paused = enabled


pause_handler = u.Entity(ignore_paused=True, input=pause_input)

if __name__ == "__main__":
    sun = u.DirectionalLight()
    sun.look_at(u.Vec3(1, -1, -1))
    u.Sky()

    game.run()
