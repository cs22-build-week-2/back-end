# Opens map data
# Finds shortest path to each room

# {'room_id': {'n': 'room_id', 's': 'room_id', 'e': 'room_id', 'w': 'room_id'}}
# Do a BFS
def find_short_paths(firstRoom, all_rooms):
    parent = ""
    q = []
    q.append(all_rooms[firstRoom["room_id"]])
    