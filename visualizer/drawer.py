import time
from math import pi

import pygame
from pygame.locals import *

from simulator import EntryNode, RoadNode
from visualizer.road import GraphicRoad, rotate_point

HEIGHT = 7
WIDTH = 12

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Drawing:

    def __init__(self, simulator):
        pygame.init()
        self.simulator = simulator
        self.continue_drawing = 1
        self.fenetre = pygame.display.set_mode((1600, 900))
        self.nodes = simulator.nodes
        pygame.display.flip()

    def generateRoadAndDraw(self):
        entry_nodes = [n for n in self.nodes if type(n) is EntryNode]
        visited, roads = Drawing.depth_first_search(entry_nodes)
        self.drawRoad(roads)
        return roads

    def drawRoad(self, roads):
        point = (500, 500)
        cell_length = 30
        height = 30
        nodes = {}
        graphic_roads = []
        for road in roads:
            orientation = road["road"][0].orientation
            angle = orientation * pi / 180
            if road["entry"] in nodes:
                point = nodes[road["entry"]]
            if road["exit"] in nodes:
                point = nodes[road["exit"]]
                angle = angle + pi
            road_length = len(road["road"])
            xa, ya = rotate_point(angle, (point[0] + road_length * cell_length, point[1]), point)

            nodes[road["exit"]] = (int(xa), int(ya))
            graphic_road = GraphicRoad(point[0], point[1], xa, ya, road["road"], cell_length, height)
            graphic_roads.append(graphic_road)
            # graphic_road.update(road["road"])
            # graphic_road.draw(self.fenetre)
            # graphic_road.
        return graphic_roads

    @staticmethod
    def depth_first_search(start):
        visited, stack = set(), start
        roads = []
        road = {"entry": None, "road": [], "exit": None}
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                if type(vertex) is RoadNode:
                    visited.add(vertex)
                    road["road"].append(vertex)
                else:
                    road["exit"] = vertex
                    roads.append(road)
                    road = {"entry": vertex, "road": [], "exit": None}
                stack.extend(set(vertex.successors) - visited)

        return visited, [r for r in roads if len(r["road"]) != 0]

    def draw(self):
        roads = self.generateRoadAndDraw()
        graphic_roads = self.drawRoad(roads)
        while self.continue_drawing:
            self.simulator.tick()
            for graphic_road in graphic_roads:
                graphic_road.update()
                graphic_road.draw(self.fenetre)
            time.sleep(1)
            pygame.display.flip()
            self.fenetre.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.continue_drawing = 0
