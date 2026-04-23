def player(prev_play, opponent_history=[], my_history=[]):
    import random

    # Reset
    if prev_play == "":
        opponent_history.clear()
        my_history.clear()

    opponent_history.append(prev_play)

    beats = {"R": "P", "P": "S", "S": "R"}

    # First move
    if len(opponent_history) == 1:
        move = "P"
        my_history.append(move)
        return move

    # ---- Detect Kris ----
    if len(my_history) >= 2:
        is_kris = True
        for i in range(1, len(opponent_history)):
            if opponent_history[i] != beats[my_history[i-1]]:
                is_kris = False
                break

        if is_kris:
            predicted = beats[my_history[-1]]
            move = beats[predicted]
            my_history.append(move)
            return move

    # ---- Pattern detection (Abbey/Mrugesh killer) ----
    if len(opponent_history) >= 3:
        last_two = "".join(opponent_history[-2:])
        counts = {"R": 0, "P": 0, "S": 0}

        for i in range(len(opponent_history) - 2):
            if opponent_history[i] + opponent_history[i+1] == last_two:
                next_move = opponent_history[i+2]
                counts[next_move] += 1

        if max(counts.values()) > 0:
            prediction = max(counts, key=counts.get)
        else:
            prediction = random.choice(["R", "P", "S"])
    else:
        prediction = random.choice(["R", "P", "S"])

    move = beats[prediction]

    # ---- Anti-loop randomness (break Abbey cycles) ----
    if random.random() < 0.1:
        move = random.choice(["R", "P", "S"])

    my_history.append(move)
    return move
    
    # ---- Detect Quincy (fixed pattern) ----
    quincy_pattern = ["R", "R", "P", "P", "S"]
    if len(opponent_history) >= 5:
        is_quincy = True
        for i in range(len(opponent_history)):
            if opponent_history[i] != quincy_pattern[i % 5]:
                is_quincy = False
                break

        if is_quincy:
            predicted = quincy_pattern[len(opponent_history) % 5]
            move = beats[predicted]
            my_history.append(move)
            return move

    # ---- Frequency-based strategy (beats Mrugesh & Abbey) ----
    count = {"R": 0, "P": 0, "S": 0}
    for move in opponent_history:
        if move in count:
            count[move] += 1

    most_common = max(count, key=count.get)
    move = beats[most_common]

    # Add slight randomness to avoid being predictable
    if random.random() < 0.1:
        move = random.choice(["R", "P", "S"])

    my_history.append(move)
    return move