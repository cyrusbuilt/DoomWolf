from typing import Optional
import pygame as pg
import math
from engine import constants as con


class RayCaster:

    def __init__(self, game):
        self.game = game
        self.ray_casting_result: tuple[float, float, int, float | int] = ()
        self.objects_to_render: list[tuple[float, pg.Surface,
                                           tuple[int, int]]] = []
        self.textures: Optional[dict] = self.game.object_renderer.wall_textures

    def refresh_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values
            surface: pg.Surface = self.textures[texture]
            left_top = offset * (con.TEXTURE_SIZE - con.SCALE)
            if proj_height < con.HEIGHT and self.textures:
                wall_column = surface.subsurface(left_top, 0, con.SCALE,
                                                 con.TEXTURE_SIZE)
                wall_column = pg.transform.scale(wall_column,
                                                 (con.SCALE, proj_height))
                wall_pos = (ray * con.SCALE,
                            con.HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = con.TEXTURE_SIZE * con.HEIGHT / proj_height
                w_height = con.HALF_TEXTURE_SIZE - texture_height // 2
                wall_column = surface.subsurface(left_top, w_height, con.SCALE,
                                                 texture_height)
                wall_column = pg.transform.scale(wall_column,
                                                 (con.SCALE, con.HEIGHT))
                wall_pos = (ray * con.SCALE, 0)

            render = (depth, wall_column, wall_pos)
            self.objects_to_render.append(render)

    def ray_cast(self):
        self.ray_casting_result = []
        texture_vert = 1
        texture_hor = 1
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - con.HALF_FOV + 0.0001
        for ray in range(con.NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # Horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(con.MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break

                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # Verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(con.MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break

                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Depth, texture offset
            if depth_vert < depth_hor:
                depth = depth_vert
                texture = texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth = depth_hor
                texture = texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # Remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Projection
            proj_height = con.SCREEN_DIST / (depth + 0.0001)

            # Ray casting result
            result = (depth, proj_height, texture, offset)
            self.ray_casting_result.append(result)
            ray_angle += con.DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.refresh_objects_to_render()
