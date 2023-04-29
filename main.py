#!/usr/bin/env python3.10

import itertools
import ursina as u
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar

crate_spread = 64
enabled = False

game = u.Ursina(width=800, height=600, title="Reckoning",
                icon="./assets/icons/logo.png")

ground = u.Entity(model=u.Terrain(heightmap="./assets/textures/heightmap.jpg"), collider="box", scale=u.Vec3(crate_spread * 4, 15, crate_spread * 4),
                  texture="grass", texture_scale=u.Vec3(4, 1, 4))

player = FirstPersonController(
    model="cube", z=-10, color=u.color.orange, origin_y=-1.5, position=u.Vec3(0, 10, 0))
player.collider = u.BoxCollider(player, size=(0, 1, 0))

vision_light = u.SpotLight(
    parent=u.camera, size=(25, 25, 25), origin=(0, 0, 0))
vision_light.look_at(u.Vec3(0, 0, 1))

player_health = HealthBar(
    roundness=0.5, scale=(0.5, 0.05), position=(0.5, -0.5), color=u.color.white, text_color=u.color.black)

for _ in range(128):
    u.Entity(model="cube", origin_y=-0.5, scale=2, texture="brick", texture_scale=(1, 2), x=u.random.uniform(-crate_spread, crate_spread) + crate_spread,
             z=u.random.uniform(-crate_spread, crate_spread), collider="box", scale_y=u.random.uniform(2, 3), color=u.color.hsv(0, 0, u.random.uniform(0.9, 1)))

for i, j in itertools.product(range(crate_spread), range(0, crate_spread, 2)):
    u.Entity(model="cube", origin_y=-0.5, scale=2, texture="brick", texture_scale=(1, 2), x=j,
             y=i, z=i, collider="box", scale_y=2, color=u.color.hsv(0, 0, u.random.uniform(0.9, 1)))


def update():
    player.speed = 12 if u.held_keys['shift'] else 8
    player_health.bar_color = u.color.rgb(
        255 * (100 - player_health.value), (255 * player_health.value) / 100, 0)
    player_health.text = f"{player_health.value} HP"

    # TODO: Give the sun a day-night cycle
    # i.e. change the direction every minute


def input(key):
    if key in ["-", "- hold"]:
        player_health.value -= 5
    elif key in ["=", "= hold"]:
        player_health.value += 5


def pause_input(key):
    global enabled

    if key == "tab":
        enabled = not enabled

        player.visible_self = not enabled
        player.cursor.enabled = not enabled
        u.mouse.locked = not enabled

        u.application.paused = enabled  # type: ignore


pause_handler = u.Entity(ignore_paused=True, input=pause_input)

if __name__ == "__main__":
    sun = u.DirectionalLight()
    u.Sky()

    game.run()
