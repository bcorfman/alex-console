from levelscan import load_layout, find_elevators


def test_room_creation():
    layout = load_layout('level1.txt')
    rooms = find_elevators(layout)
    elevator1 = rooms[0]
    elevator1.identify_exits(layout)
    elevator2 = rooms[1]
    elevator2.identify_exits(layout)
    assert (len(elevator1.exits) == 2 and len(elevator2.exits) == 2)
