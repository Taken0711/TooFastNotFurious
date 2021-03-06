from modeler import *
from shared import Orientation


def main():
    s = new_simulation()

    entry1 = entry_node().with_rate(0.2)
    s.add_node(entry1)
    entry2 = entry_node().with_rate(0.3)
    s.add_node(entry2)
    exit1 = exit_node()
    s.add_node(exit1)
    junction = stop().with_stop_on_road(Orientation.SOUTH)
    s.add_node(junction)

    s.add_road(entry1.connect(Orientation.WEST).to(junction).with_length(5))
    s.add_road(entry2.connect(Orientation.NORTH).to(junction).with_length(7))
    s.add_road(junction.connect(Orientation.NORTH).to(exit1).with_length(3))

    s.add_path(entry1.to(exit1).with_proportion(100))
    s.add_path(entry2.to(exit1).with_proportion(100))

    s.run_graphical_for(400)


if __name__ == '__main__':
    main()
