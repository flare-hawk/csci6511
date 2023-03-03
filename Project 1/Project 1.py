'''
Project1.py 
Written by Eric Luo
'''

import heapq
import os.path 

#Define Heristic Function
def heuristic(state, action, target, target_volume, jugs, infinite_jug_id, debug=True):
    closest_distance=0
    curr_volume=state[infinite_jug_id]
    sort_jugs=sorted(list(jugs), reverse=True)
    if action=='start' or action=='empty' or action=='transfer':
        dist=abs(curr_volume-target_volume)
    elif action=='fill':
        dist=abs(curr_volume-target_volume+state[target])
        closest_distance+=1
    factor=1 if ((action!="fill" and curr_volume>target_volume) or (action=="fill" and curr_volume+state[target]>target_volume)) else 2
    if debug==True: print(f"dist:{dist}")
    for i, jug in enumerate(sort_jugs):
        if i != infinite_jug_id and dist>jug:
            closest_distance+=(dist//jug)*factor
            if debug==True: print(f"Remaining{dist}, fill {jug}, operate {(dist//jug)*2} times")
            dist=dist%jug
    if dist!=0:
        closest_distance+=dist/sort_jugs[-1]
    if debug==True: print(f"H:{closest_distance}\n")
    return closest_distance

#Functions for Next Steps
def possible_next_states(state, jugs, infinite_jug_id):
    next_states = []
    for i, jug in enumerate(jugs):
        # Fill a jug
        if state[i] < jug and infinite_jug_id!=i:
            next_state = state[:i] + (jug,) + state[i+1:]
            next_states.append(("fill",i,next_state))
        # Empty a jug
        if state[i] > 0 and infinite_jug_id!=i:
            next_state = state[:i] + (0,) + state[i+1:]
            next_states.append(("empty",i, next_state))
        for j, other_jug in enumerate(jugs):
            # Move water from one jug to another
            if i != j and state[i] > 0 and state[j] < other_jug:
                transfer = min(state[i], other_jug - state[j])
                if i<j:
                    next_state = state[:i] + (state[i] - transfer,) + state[i+1:j] + (state[j] + transfer,) + state[j+1:]
                else:
                    next_state = state[:j] + (state[j] + transfer,) + state[j+1:i] + (state[i] - transfer,) + state[i+1:]
                next_states.append(("transfer",(i,j), next_state))
    return next_states

#A* Search Driving Function 
def a_star(jugs, target_volume, infinite_jug_id=0, debug=False):
    start_state =  (0,) * len(jugs)
    heap = [(heuristic(start_state,'start', 0, target_volume, jugs, infinite_jug_id, debug), 0, 'start',0, start_state)]
    visited=[start_state]
    while heap:
        curr_est,curr_cost, curr_action, curr_target, curr_state = heapq.heappop(heap)
        if debug==True: print(f"Current Action:{curr_action}\nTarget:{curr_target}\nCurrent State:{curr_state}\nCurrent Est Cost:{curr_est}")
        if curr_state[0] == target_volume:
            return curr_cost
        for scenario in possible_next_states(curr_state, jugs, infinite_jug_id):
            action, target, next_state=scenario
            if next_state[0] == target_volume:
                if debug==True: print(f"Final Action:{action}\nTarget:{target}\nNext State:{next_state}")
                return curr_cost + 1
            next_cost=curr_cost + 1 
            if debug==True: print(f"Next Action:{action}\nTarget:{target}\nNext State:{next_state}")
            next_est_cost = curr_cost + 1 + heuristic(next_state, action, target, target_volume, jugs, infinite_jug_id, debug)
            if next_state not in [state for est_cost, cost, act, tar, state in heap] and next_state[0]-target_volume<max(jugs[1:]) and next_state not in visited:
                if debug==True: print(f"Queued Action:{action}\nTarget:{target}\nNext State:{next_state}\nNext Est Cost:{next_est_cost}")
                visited.append(next_state)
                heapq.heappush(heap, (next_est_cost,next_cost,action, target, next_state))
    return -1
    
if __name__=='__main__':
    #Program Starts
    print("A* Search for Water Jug Problem")
    print("Program Written by: Eric Luo")
    print("Program Starts...")
    #Debug Mode
    debug=' '
    while debug[0].lower() not in ['y','n']:
        debug=input("Debug Mode On [y/n]: ")
    debug = False if debug[0].lower()=='n' else True
    print(f"Debug: {debug}")
    #Exit Flag 
    flag=True
    while flag:        
        #Input File
        file=''
        while not os.path.isfile(file):
            file=input("Enter input file name:")
        with open(file,'r') as f:
            jugs_text=f.readline()
            target_volume=int(f.readline())
        jugs=tuple([float('inf')]+[int(jug) for jug in list(jugs_text.split(','))])
        #Show input 
        print(f"Jugs: {jugs[1:]}")
        print(f"Target Volume: {target_volume}")
        #Call A* Driver Function 
        print(f"Step Count: {a_star(jugs, target_volume, debug=debug)}")
        #Want to Continue
        flag=' '
        while flag[0].lower() not in ['y','n']:
            flag=input("Continue? [y/n]: ")
        flag = False if flag[0].lower()=='n' else True
    print("Program Exits.")
