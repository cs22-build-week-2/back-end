from threading import Timer
import requests
import json

moveUrl = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'

def create_map(headers, firstRoom, lengthOfRoom):
    # sample usage
    # t = Timer(30.0, "hello")
    # t.start() # after 30 seconds, "hello" will be printed
    # t = Timer(cooldown, )

    cooldown = firstRoom['cooldown']
    mapData = { 'room_id': firstRoom['room_id'], 'title': firstRoom['title'], 'items': firstRoom['items'], 'terrain': firstRoom['terrain'], 'exits': firstRoom['exits'], 'color': 'grey'}
    print(mapData)
    # {room_id, title, items, terrain, exits}

    # Opens map.txt
    f = open('map.txt', 'a')

    s = []
    s.append(mapData)
    dfs_visited = {}
    while len(s) > 0:
        if lengthOfRoom == len(dfs_visited.keys()):
            break

        # Get room from stack
        v = s.pop()
        v_room_id = v["room_id"]
        exits = v["exits"]
        # Adds room to txt file
        f.write(json.dumps(v) + "\n")

        # Creates directions for rooms filled with "?"
        if v not in dfs_visited:
            dfs_visited[v_room_id] = {}
            for direction in exits:
                dfs_visited[v_room_id][direction] = "?"

        # Finds a direction with "?"
        skip = False
        try_direction = exits.pop()
        while dfs_visited[v_room_id][try_direction] != "?":
            if len(exits) > 0:
                try_direction = exits.pop()
            else:
                skip = True
        if skip:
            continue

        # Moves to try_direction
        post_data = { 'direction': try_direction }
        next_room = requests.post(moveUrl, json=post_data, headers=headers)
        next_room_data = next_room.json()

        # Add room to previous room
        dfs_visited[v_room_id][try_direction] = next_room_data["room_id"]
