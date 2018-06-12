import pygame
from pygame.sprite import RenderClear

from simulator.junction import Junction
from simulator.right_priority_junction import RightPriorityJunction
from simulator.stop_junction import StopJunction
from simulator.traffic_light_junction import TrafficLightJunction
from visualizer.my_sprite import MySprite, StopSprite
from visualizer.point import Point


class GraphicJunction:

    def __init__(self, position, junction, cell_length=30, cell_height=30):
        super().__init__()
        self.position = position
        self.group = RenderClear()
        self.entity = junction
        self.cell_length = cell_length
        self.cell_height = cell_height
        self.angle = 0
        self.lights = []
        self.node_pos = []
        if isinstance(self.entity, Junction):
            surface = pygame.Surface((self.cell_length, self.cell_height))
            surface.fill((29, 17, 17))
            for i in range(len(self.entity.nodes)):
                for j in range(len(self.entity.nodes[i])):
                    point = self.position + Point(j * self.cell_length, -i * self.cell_height)
                    self.node_pos.append((self.entity.nodes[i][j], point))
        else:
            for i in self.entity.nodes:
                for n in i:
                    self.node_pos.append((n, self.position))

    def create_sprites(self):
        if type(self.entity) is RightPriorityJunction:
            for cell, pos in self.node_pos:
                surface = pygame.Surface((self.cell_length, self.cell_height))
                surface.fill((29, 17, 17))
                self.group.add(MySprite(pos, self.cell_length, self.cell_height, image=surface))
        elif type(self.entity) is StopJunction:
            self.entity: StopJunction
            nodes_orientations = [i for n in self.entity.get_end_of_predecessor(self.entity.stop_orientation) for i in
                                  n.successors]
            for cell, pos in self.node_pos:
                if cell not in nodes_orientations:
                    surface = pygame.Surface((self.cell_length, self.cell_height))
                    surface.fill((29, 17, 17))
                    self.group.add(MySprite(pos, self.cell_length, self.cell_height, image=surface))
                else:
                    self.group.add(StopSprite(pos, self.cell_length, self.cell_height, -self.entity.stop_orientation))
        elif type(self.entity) is TrafficLightJunction:
            self.entity: TrafficLightJunction
            nodes_orientations = [(k, o) for o in self.entity.state1_orientations + self.entity.state2_orientations
                                  for n in self.entity.get_end_of_predecessor(o) for k in n.successors]
            nodes = [k[0] for k in nodes_orientations]
            for cell, pos in self.node_pos:
                surface = pygame.Surface((self.cell_length, self.cell_height))
                surface.fill((29, 17, 17))
                self.group.add(MySprite(pos, self.cell_length, self.cell_height, image=surface))
                if cell in nodes:
                    orientations = [k[1] for k in nodes_orientations if k[0] == cell]
                    for o in orientations:
                        point = pos.rotate_point(o, pos + (self.cell_length, -self.cell_height))
                        surface = pygame.Surface((self.cell_length, self.cell_height), pygame.SRCALPHA)
                        pygame.draw.circle(surface, (255, 0, 0),
                                           (round(self.cell_length / 2), round(self.cell_height / 2)),
                                           round(self.cell_length / 2))
                        sprite = MySprite(point, round(self.cell_length / 2), round(self.cell_height / 2),
                                          image=surface)
                        self.group.add(
                            sprite)
                        self.lights.append(sprite)

    def draw(self, surface):
        self.group.draw(surface)
