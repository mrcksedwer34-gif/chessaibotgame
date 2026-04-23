import random

def player(prev_play, opponent_history=[], 
           my_history=[],
           detected=["none"],
           pairs=[{}]):

    beats = {"R": "P", "P": "S", "S": "R"}
    
    # Detect new match and reset state
    if prev_play == "" and len(opponent_history) > 0:
        opponent_history.clear()
        my_history.clear()
        pairs[0].clear()
        detected[0] = "none"
    
    # First move of match (prev_play is empty string)
    if prev_play == "":
        print(f"FIRST MOVE: my_hist={my_history}, opp_hist={opponent_history}")
        my_history.append("P")
        return "P"
    
    # Record opponent's move
    print(f"RECORD: prev={prev_play}, opp_hist before={opponent_history}")
    opponent_history.append(prev_play)
    print(f"RECORD: opp_hist after={opponent_history}")
    
    # ---- Quincy Detection ----
    quincy_pat = ["R", "R", "P", "P", "S"]
    if detected[0] in ("none", "quincy"):
        is_quincy = all(opponent_history[i] == quincy_pat[i % 5] 
                       for i in range(len(opponent_history)))
        # DEBUG
        if len(opponent_history) >= 3:
            print(f"Q DETECT: opp={opponent_history}, is_q={is_quincy}, det={detected[0]}")
        if is_quincy and len(opponent_history) >= 4:
            detected[0] = "quincy"
            print(f"Q DETECTED! Now using quincy strategy")
    
    if detected[0] == "quincy":
        my_history.append("x")  # placeholder
        return beats[quincy_pat[len(opponent_history) % 5]]
    
    # ---- Kris Detection ----
    # Kris plays what beats our last move
    if detected[0] in ("none", "kris") and len(my_history) >= 2:
        # Check last 3 moves for pattern
        check_len = min(3, len(opponent_history))
        kris_matches = 0
        for i in range(len(opponent_history) - check_len, len(opponent_history)):
            if i >= 0 and i < len(my_history):
                if opponent_history[i] == beats[my_history[i]]:
                    kris_matches += 1
        
        ratio = kris_matches / check_len if check_len > 0 else 0
        
        if ratio >= 0.5:
            detected[0] = "kris"
    
    if detected[0] == "kris":
        # Kris will play what beats our last move
        kris_move = beats[my_history[-1]]
        my_guess = beats[kris_move]
        my_history.append(my_guess)
        return my_guess
    
    # ---- Adaptive for Abbey/Mrugesh ----
    # Track what opponent plays after each move
    if len(opponent_history) >= 2:
        last = opponent_history[-1]
        predictions = {"R": 0, "P": 0, "S": 0}
        
        # Look through history for patterns after 'last'
        for i in range(len(opponent_history) - 1):
            if opponent_history[i] == last:
                next_move = opponent_history[i + 1]
                predictions[next_move] += 1
        
        if max(predictions.values()) > 0:
            predicted = max(predictions, key=predictions.get)
            guess = beats[predicted]
        else:
            # Cycle moves to counter Mrugesh frequency tracking
            guess = ["R", "P", "S"][len(my_history) % 3]
    else:
        guess = "R"
    
    my_history.append(guess)
    return guess
