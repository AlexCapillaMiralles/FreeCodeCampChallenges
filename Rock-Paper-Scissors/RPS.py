# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import numpy as np
import random
from math import exp
from math import log
def player(prev_play, opponent_history=[], guess_history=[], Q = [], p_o = [], predictions = []):

  #starting counters, useful later for calculating rewards
    if not hasattr(player, "t_counter"):
      player.t_counter = 0
    if not hasattr(player, "q_counter"):
      player.q_counter = 0
    if not hasattr(player, "m_counter"):
      player.m_counter = 0
    if not hasattr(player, "a_counter"):
      player.a_counter = 0
    if not hasattr(player, "counter"):
      player.counter = 0
    if not hasattr(player, "last_strategy_change"):
      player.counter = 0
    
    if player.t_counter == 1000:
      player.t_counter = 0
      player.m_counter = 0
      player.q_counter = 0
      player.counter = 0
      player.a_counter = 0
      opponent_history.clear()
      guess_history.clear()
      Q.clear()
      p_o.clear()
      predictions.clear()
    opponent_history.append(prev_play)
    L_rate = 0.84
    GAMMA = 0.1
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    epsilon = 1 - len(opponent_history)/1000
  
    player.t_counter += 1

  
  #creating Q
    if len(opponent_history) == 1:
      p_o.append({"RR": 0,"RP": 0,"RS": 0,"PR": 0,"PP": 0,"PS": 0,"SR": 0,"SP": 0,"SS": 0,})
      for _ in range(9):
        Q.append([0,0,0])
    if len(opponent_history) < 3:
      guess = "R"


  #defining the current states and rewards
    if len(opponent_history) > 2:
      guess1 = guess_history[-2]
      guess2 = guess_history[-1]
      prev_play1 = opponent_history[-2]
      
      #if draw 
      if guess1 == prev_play1:
        reward = -0.1
        if guess1 == "P":
          state = 3
        if guess1 == "R":
          state = 0
        if guess1 == "S":
          state = 6

      #if won
      if guess1 == "P" and prev_play1 == "R":
        reward = 1
        state = 5

      if guess1 == "R" and prev_play1 == "S":
        reward = 1
        state = 1

      if guess1 == "S" and prev_play1 == "P":
        reward = 1
        state = 7
      
      #if lost
      if guess1 == "P" and prev_play1 == "S":
        reward = -1
        state = 4
      
      if guess1 == "R" and prev_play1 == "P":
        reward = -1
        state = 2
      
      if guess1 == "S" and prev_play1 == "R":
        reward = -1
        state = 8

      #for the quincy
      if len(opponent_history) > 6 and opponent_history[-7] == prev_play1 \
      and opponent_history[-6] == prev_play and opponent_history[-8] == \
      opponent_history[-3] and player.q_counter >= player.m_counter: 
        player.q_counter += 1
        if player.q_counter > 400:
          epsilon = 0.6
        if state in [1, 5, 7]:
          reward = 1.5
        if state in [2, 4, 8]:
          reward = -1.5
        if state in [3, 6, 0]:
          reward = -0.15

      #for mrugesh
      if len(opponent_history) > 13 and player.q_counter < 500 \
      and player.a_counter < 200:
        last_ten = guess_history[-12:-2]
        last_eleven = guess_history[-13:-3]
        last_twelve = guess_history[-14:-4]
        most_frequent = max(set(last_ten), key=last_ten.count)
        previous_frequent = max(set(last_eleven), key=last_eleven.count)
        prev2_frequent = max(set(last_twelve), key=last_twelve.count)
        player.m_counter += 1
        if player.m_counter > 400:
          epsilon = 0.6
        if opponent_history[-2]  ==  ideal_response[most_frequent] \
        and opponent_history[-3]  == ideal_response[previous_frequent] \
        and opponent_history[-4] == ideal_response[prev2_frequent]:
          if state in [1, 5, 7]:
            reward = 1.5
          if state in [2, 4, 8]:
            reward = -1.5
          if state in [3, 6, 0]:
            reward = -0.15

      #for kris
      if len(opponent_history) > 5 and opponent_history[-4] \
      == ideal_response[guess_history[-5]] and opponent_history[-3] \
      == ideal_response[guess_history[-4]] and opponent_history[-2] \
      == ideal_response[guess_history[-3]]:
        player.counter += 1
        if player.counter > 5 and player.t_counter < 30 or player.counter > 30:
              if state in [1, 5, 7]:
                reward = 1.5
              if state in [2, 4, 8]:
                reward = -1.5
              if state in [3, 6, 0]:
                reward = -0.15
    
      #for abbey
      if len(opponent_history) ==3:
        p_o[0]["RR"] +=1
      last_two = "".join(guess_history[-3:-1])
      if len(last_two) == 2:
          p_o[0][last_two] += 1
      potential_plays = [
        guess_history[-2] + "R",
        guess_history[-2] + "P",
        guess_history[-2] + "S"]
      sub_order = {
        k : p_o[0][k]
        for k in potential_plays if k in p_o[0]
      }
      prediction = max(sub_order, key=sub_order.get)[-1:]
      predictions.append(prediction)

        #desperately trying to defeat abbey, when the pattern of abbey
        #changes and implementing it in the reward calculation.
      def detect_strategy_change(opponent_history, threshold=0.75):
        recent_moves = opponent_history[-3:]
        move_counts = {move: recent_moves.count(move) \
                       for move in set(recent_moves)}
        entropy = -sum((count /len(recent_moves))* log(count/ len(recent_moves), 2) for count in move_counts.values())
        return entropy > threshold

      if detect_strategy_change(opponent_history):
        player.last_strategy_change = player.t_counter

      if len(predictions) > 3 and ideal_response[predictions[-2]] == \
      prev_play1 and ideal_response[predictions[-3]] \
      == opponent_history[-3] and player.m_counter < 200 and \
      ideal_response[predictions[-4]] == opponent_history[-4]:
        player.a_counter += 1
        if player.a_counter > 400:
          epsilon = 0.8 if player.t_counter - \
          player.last_strategy_change > 3 else 0.6
        if player.a_counter > 50:
          GAMMA = 0.2
          if player.t_counter - player.last_strategy_change > 3:
            if state in [1, 5, 7]:
                reward = 1.25
            elif state in [2, 4, 8]:
                reward = -1.75
            elif state in [3, 6, 0]:
                reward = -0.2
          else:
            if state in [1, 5, 7]:
                reward = 1.5
            elif state in [2, 4, 8]:
                reward = -1.5
            elif state in [3, 6, 0]:
                reward = -0.15
      
    #defining what has been the current action
      if guess2 == "R":
        c_action = 0
      if guess2 == "P":
        c_action = 1
      if guess2 == "S":
        c_action = 2

    #defining what is the next state
      if guess2 == prev_play:
        if guess2 == "P":
          next_state = 3
        if guess2 == "R":
          next_state = 0
        if guess2 == "S":
          next_state = 6

      if guess2 == "P" and prev_play == "S":
        next_state = 4
      if guess2 == "P" and prev_play == "R":
        next_state = 5
      if guess2 == "R" and prev_play == "S":
        next_state = 1
      if guess2 == "R" and prev_play == "P":
        next_state = 2
      if guess2 == "S" and prev_play == "P":
        next_state = 7
      if guess2 == "S" and prev_play == "R":
        next_state = 8
        
      #updating Q
      Q[state][c_action] = Q[state][c_action] + L_rate*(reward+ \
      GAMMA*np.max(Q[next_state]) - Q[state][c_action])
      #taking an action
      if random.uniform(0,1) > epsilon:
        action = random.randint(0,2)
      else:
        action = np.argmax(Q[next_state][:])
        
      #traducing the action into the guess
      if action == 0:
        guess = "R"
      if action == 1:
        guess = "P"
      if action == 2:
        guess = "S"
    #creating a matrix of guesses
    guess_history.append(guess)
    return guess
