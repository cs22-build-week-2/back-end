import json

# Opens map data
# Finds shortest path to each room

# {'room_id': {'n': 'room_id', 's': 'room_id', 'e': 'room_id', 'w': 'room_id'}}
# Do a BFS
def find_short_paths(firstRoom, goalRoom):
    traversing_map = {}
    # Loads current dfs_visited from txt file
    with open('map_ids.txt','r') as t:
        traversing_map = json.loads(t.readline())

    # Clean dfs_visited data
    for room in traversing_map.keys():
        if "previous_direction" in traversing_map[room]:
            del traversing_map[room]["previous_direction"]
        traversing_map[room]['room_id'] = room 

    print(traversing_map)

    unique_rooms = traversing_map
    parent = ""
    first_room_id = f'{firstRoom["room_id"]}'
    q = []
    q.append(unique_rooms[first_room_id])
    parent_rooms_for_path = {}

    already_checked = {}

    # Populates parent dict which will be used to create the shortest path
    while len(q) > 0:
        v = q.pop()
        # v = {'w': 83, 'room_id': '130'}

        # Assign room id
        room_id = v["room_id"]

        already_checked[room_id] = True

        # Remove "room_id" for going through directions
        del v["room_id"]
        # Assign parent from ID
        parent = room_id

        # Breaker variable
        skip = False

        # Add rooms to queue
        for direction in v:
            if f'{v[direction]}' in already_checked:
                continue
            else:
                if direction in parent_rooms_for_path:
                    parent_rooms_for_path[v[direction]].append(parent)
                else:
                    parent_rooms_for_path[v[direction]] = [parent]

                q.insert(0, unique_rooms[f'{v[direction]}'])

            if v[direction] == goalRoom:
                skip = True
                break

        # Add back "room_id" so it won't break
        v["room_id"] = room_id
        
        if skip:
            break

    # Go through parent_rooms_for_path to get path
    num_path = [f'{goalRoom}']
    room = parent_rooms_for_path[goalRoom][0]
    num_path.append(room)
    while room != first_room_id:
        num_path.append(parent_rooms_for_path[int(room)][0])
        room = parent_rooms_for_path[int(room)][0]

    # Order for rooms
    num_path.reverse()

    direction_path = []
    copy_allRooms = traversing_map
    for i in range(len(num_path)):
        room = num_path[i]
        del copy_allRooms[room]["room_id"]

        try:
            for direction in copy_allRooms[room]:
                if copy_allRooms[room][direction] == int(num_path[i+1]):
                    direction_path.append([direction, num_path[i+1]])
                    break
        except:
            break

    return direction_path
