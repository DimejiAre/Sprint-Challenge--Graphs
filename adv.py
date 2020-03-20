from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Queue, Stack

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

graph = {}

# create dictionary for each room when visited
def create_room():
    room = {}
    for exit in player.current_room.get_exits():
        room[exit] = "?"
        graph[player.current_room.id] = room

# Algorithm to find random exit that hasn't been explored yet
def current_room_unexplored_exit():
    unexplored = []
    for exit in player.current_room.get_exits():
        if graph[player.current_room.id][exit] == "?":
            unexplored.append(exit)

    return random.choice(unexplored)

def path_to_unexplored_room(starting_room):
    q = Queue()
    q.enqueue([starting_room])
    visited = set()

    while q.size() > 0:
        path = q.dequeue()
        room = path[-1]

        if list(graph[room].values()).count('?') != 0:
            return path
        if room not in visited:
            visited.add(room)

            for next_room in graph[room].values():
                new_path = path.copy()
                new_path.append(next_room)
                q.enqueue(new_path)



print("graph: ", graph)
print("traversal path", traversal_path)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

# print("currentroom id", player.current_room.id)
# print("current room: ", player.current_room.get_exits())
# print("visited rooms: ", visited_rooms)
# print(len(room_graph), len(graph))

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
