from abc import ABC

from simulator.stop_junction import StopJunction
from simulator.road import Road
from simulator.abstract_entity import AbstractEntity


class Roundabout(AbstractEntity, ABC):

    INTERVAL = 2

    def __init__(self, simulator, io_roads, n_of_ways):
        self.io_roads = io_roads
        self.n_of_ways = n_of_ways
        self.entities = []
        self.yields = {}
        self.roads = {}
        for o in io_roads.keys():
            ios = {}
            ios[o] = io_roads[o]
            ios[o.invert()] = (sum(io_roads[o]) - n_of_ways, n_of_ways)
            ios[o.left()] = (0, n_of_ways)
            ios[o.right()] = (n_of_ways, 0)
            stop = StopJunction(simulator, ios, o)
            self.yields[o] = stop
            self.entities.append(stop)
        for o in self.yields.keys():
            road = Road(simulator, self.INTERVAL, o.invert(), n_of_ways)
            road.add_predecessor(o.invert(), self.yields[o])
            self.yields[o.left()].add_predecessor(o.invert(), road)
            self.roads[o] = road
            self.entities.append(road)
        super().__init__(simulator, self.get_nodes())

    def do_add_predecessor(self, orientation, predecessor):
        self.yields[orientation.invert()].add_predecessor(orientation, predecessor)

    def _add_successor(self, orientation, successor):
        super()._add_successor(orientation, successor)
        self.yields[orientation]._add_successor(orientation, successor)

    def get_end_of_predecessor(self, orientation):
        return self.predecessors[orientation].get_end(orientation)

    def compute_next(self):
        # Everything is handle by simulator since entities are also reference there
        pass

    def apply_next(self):
        # Everything is handle by simulator since entities are also reference there
        pass

    def get_start(self, orientation):
        return self.yields[orientation].get_start(orientation)

    def get_end(self, orientation):
        return self.yields[orientation].get_end(orientation)

    def is_dependency_satisfied(self, source):
        return True

    def get_nodes(self):
        # Everything is handle by simulator since entities are also reference there
        return []

