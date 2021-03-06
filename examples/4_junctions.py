from modeler import *
from shared import Orientation


def main():
    s = new_simulation()

    entry1 = entry_node().with_rate(0.8)
    s.add_node(entry1)
    entry2 = entry_node().with_rate(0.8)
    s.add_node(entry2)
    entry3 = entry_node().with_rate(0.8)
    s.add_node(entry3)
    entry4 = entry_node().with_rate(0.8)
    s.add_node(entry4)

    exit1 = exit_node()
    s.add_node(exit1)
    exit2 = exit_node()
    s.add_node(exit2)
    exit3 = exit_node()
    s.add_node(exit3)
    exit4 = exit_node()
    s.add_node(exit4)

    junction1 = stop().with_stop_on_road(Orientation.NORTH)
    s.add_node(junction1)
    junction2 = stop().with_stop_on_road(Orientation.EAST)
    s.add_node(junction2)
    junction3 = stop().with_stop_on_road(Orientation.NORTH)
    s.add_node(junction3)
    junction4 = stop().with_stop_on_road(Orientation.WEST)
    s.add_node(junction4)

    s.add_road(entry1.connect(Orientation.SOUTH).to(junction1).with_length(2).with_n_ways(1))
    s.add_road(junction1.connect(Orientation.WEST).to(exit1).with_length(2).with_n_ways(1))
    s.add_road(junction1.connect(Orientation.EAST).to(junction2).with_length(2).with_n_ways(1))

    s.add_road(entry2.connect(Orientation.WEST).to(junction2).with_length(2).with_n_ways(1))
    s.add_road(junction2.connect(Orientation.NORTH).to(exit2).with_length(2).with_n_ways(1))
    s.add_road(junction2.connect(Orientation.SOUTH).to(junction3).with_length(2).with_n_ways(1))

    s.add_road(entry3.connect(Orientation.NORTH).to(junction3).with_length(2).with_n_ways(1))
    s.add_road(junction3.connect(Orientation.EAST).to(exit3).with_length(2).with_n_ways(1))
    s.add_road(junction3.connect(Orientation.WEST).to(junction4).with_length(2).with_n_ways(1))

    s.add_road(entry4.connect(Orientation.EAST).to(junction4).with_length(2).with_n_ways(1))
    s.add_road(junction4.connect(Orientation.SOUTH).to(exit4).with_length(2).with_n_ways(1))
    s.add_road(junction4.connect(Orientation.NORTH).to(junction1).with_length(2).with_n_ways(1))

    s.add_path(entry1.to(exit1).with_proportion(25))
    s.add_path(entry1.to(exit2).with_proportion(25))
    s.add_path(entry1.to(exit3).with_proportion(25))
    s.add_path(entry1.to(exit4).with_proportion(25))

    s.add_path(entry2.to(exit2).with_proportion(25))
    s.add_path(entry2.to(exit3).with_proportion(25))
    s.add_path(entry2.to(exit4).with_proportion(25))
    s.add_path(entry2.to(exit1).with_proportion(25))

    s.add_path(entry3.to(exit3).with_proportion(25))
    s.add_path(entry3.to(exit4).with_proportion(25))
    s.add_path(entry3.to(exit1).with_proportion(25))
    s.add_path(entry3.to(exit2).with_proportion(25))

    s.add_path(entry4.to(exit4).with_proportion(25))
    s.add_path(entry4.to(exit1).with_proportion(25))
    s.add_path(entry4.to(exit2).with_proportion(25))
    s.add_path(entry4.to(exit3).with_proportion(25))

    s.run_graphical_for(1000)
    # s.with_report()


if __name__ == '__main__':
    main()
