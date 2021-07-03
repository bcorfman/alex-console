def expand(layout, loc, char, return_fringe=False):
    nodes = []
    fringe = []
    src_row, src_col = loc
    for row, col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = src_row + row, src_col + col
        new_node = layout[new_row][new_col]
        if new_node == char:
            nodes.append((new_row, new_col))
        elif return_fringe and new_node != ' ':
            fringe.append((new_row, new_col))
    return nodes, fringe


def depth_first_search(layout, row, col, char, return_fringe=False):
    start_node = (row, col)
    frontier = [start_node]
    visited = set()
    visited.add(start_node)  # because if I just try to pass the tuple into the set __init__, it treats it as two ints
    total_fringe = set()
    while frontier:
        loc = frontier.pop()
        nodes, fringe = expand(layout, loc, char, return_fringe)
        for node in nodes:
            if node not in visited:
                visited.add(node)
                frontier.append(node)
        for node in fringe:
            if node not in total_fringe:
                total_fringe.add(node)
    return list(visited), total_fringe
