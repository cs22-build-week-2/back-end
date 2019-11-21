import time
import requests
import json

moveUrl = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'

# DFT
def create_map(headers, firstRoom, lengthOfRoom, traversed_map={}):
    # Starts timer
    # start_time = time.time()

    cooldown = firstRoom['cooldown']
    mapData = { 'room_id': firstRoom['room_id'], 'title': firstRoom['title'], 'terrain': firstRoom['terrain'], 'exits': firstRoom['exits']}
    # {room_id, title, items, terrain, exits}

    # Opens map.txt
    f = open('map.txt', 'a+')
    fp = open('map_ids.txt', 'a+')

    s = []
    s.append(mapData)
    dfs_visited = traversed_map
    previous_direction = "initialized"
    while len(s) > 0:
        if lengthOfRoom == len(dfs_visited.keys()):
            break

        # Get room from stack
        v = s.pop()
        v_room_id = f'{v["room_id"]}'
        exits = v["exits"]
        # Adds room to txt file
        f.write(json.dumps({'room_id': v["room_id"], 'title': v['title'], 'terrain': v['terrain'], 'exits': v['exits']}) + "\n")
        print(f'Current room: {v}')

        # Creates directions for rooms filled with "?"
        if v_room_id not in dfs_visited:
            dfs_visited[v_room_id] = {}
            for direction in exits:
                dfs_visited[v_room_id][direction] = "?"

        # Creates a previous direction added onto dfs, so this will be the last one traversed
        if "previous_direction" not in dfs_visited[v_room_id]:
                dfs_visited[v_room_id]["previous_direction"] = previous_direction

        # If all rooms are found, continue
        skip = False

        # Don't want to call this when initialized
        if previous_direction != "initialized": 
            if dfs_visited[v_room_id]["previous_direction"] != "initialized":
                # Make previous_direction the first item in array (so it gets popped last)
                index_of_previous_direction = exits.index(dfs_visited[v_room_id]["previous_direction"])
                # Switch previous_direction to first element
                exits[0], exits[index_of_previous_direction] = exits[index_of_previous_direction], exits[0]

        # Finds a direction with "?"
        try_direction = exits.pop()
        while dfs_visited[v_room_id][try_direction] != "?":
            if len(exits) > 0:
                try_direction = exits.pop()
            else:
                skip = True

        if skip:
            # end_time = time.time()
            # time_passed = end_time - start_time # sample number: 2.00056365215209996
            # remaining_time = cooldown - time_passed
            # # Pauses program for time
            # if remaining_time > 0:
            #     time.sleep(remaining_time + 1)
            time.sleep(cooldown)
            break
        else:
            # Sets previous direction
            if try_direction == "n":
                previous_direction = "s"
            elif try_direction == "s":
                previous_direction = "n"
            elif try_direction == "w":
                previous_direction = "e"
            elif try_direction == "e":
                previous_direction = "w"

            # End time
            # end_time = time.time()
            # time_passed = end_time - start_time # sample number: 2.00056365215209996
            # remaining_time = cooldown - time_passed
            # print('t', remaining_time)
            # # Pauses program for time
            # if remaining_time > 0:
            #     time.sleep(remaining_time + 1)
            time.sleep(cooldown)

            # Moves to try_direction
            post_data = { 'direction': try_direction }
            next_room = requests.post(moveUrl, json=post_data, headers=headers)
            next_room_data = next_room.json()
            s.append(next_room_data)

            # Add room to previous room
            dfs_visited[v_room_id][try_direction] = next_room_data["room_id"]
            cooldown = next_room_data["cooldown"]
            fp.write(json.dumps(dfs_visited) + '\n')

    print('done')
    f.close()
    fp.close()
    return dfs_visited