'''
CSCI 6511 - Project 2
Coloring Graphs
Python 3.10
'''

from typing import List, Dict
from collections import defaultdict, deque
import heapq
import copy
import re
from os import path

class GraphColoringCSP:
    def __init__(self, vertices: List[int], edges: List[List[int]], num_colors: int):
        self.vertices = vertices
        self.edges = edges
        self.num_colors = num_colors
        self.domains = defaultdict(lambda: set(range(1,num_colors+1)))
        for i,vertex in enumerate(vertices):
            self.domains[vertex] = set(range(1,num_colors+1))
        
        self.curr_domains=copy.deepcopy(self.domains)
        
        self.constraints = defaultdict(list)
        for u, v in edges:
            self.constraints[u].append(v)
            self.constraints[v].append(u)
    
    def ac3(self, queue, assignment={}):
        self.curr_domains=copy.deepcopy(self.domains)
        for v in assignment:
            self.curr_domains[v]=set([assignment[v]])
        while queue:
            (i, j) = queue.pop(0)
            if i in assignment and j in assignment:
                continue
            if self.revise(i, j):
                if len(self.curr_domains[i]) == 0:
                    return False
                for k in self.constraints[i]:
                    if k != j:
                        queue.append((k, i))
        return True
    
    def revise(self, i, j):
        revised = False
        discarded_values=[]
        for x in self.curr_domains[i]:
            if all(not self.consistent(x, y, i, j) for y in self.curr_domains[j]):
                discarded_values.append(x)
                revised = True
        for x in discarded_values:
            self.curr_domains[i].discard(x)
        return revised
    
    def consistent(self, x, y, i, j):
        return x != y
    
    def select_unassigned_variable(self, assignment):
        unassigned = [v for i, v in enumerate(self.vertices) if v not in assignment]
        #Minimum Remaining Value 
        min_value=self.num_colors
        min_value_vertices=[]
        for i, v in enumerate(unassigned):
            if len(self.curr_domains[v])<min_value:
                min_value=len(self.curr_domains[v])
                min_value_vertices=[v]
            elif len(self.curr_domains[v])==min_value:
                min_value_vertices.append(v)
        if len(min_value_vertices)==1:        
            return min_value_vertices[0]
        else:
            #Tie Breaking 
            #Maximum Constraint Number and Constraint Vertices Holder
            max_cons=0
            max_cons_vertices=[]
            #Tie Breaking Process 
            for i, v in enumerate(min_value_vertices):
                count=0
                for n,u in enumerate(self.constraints[v]):
                    if u not in assignment:
                        count+=1
                if max_cons==count:
                    max_cons_vertices.append(v)
                elif max_cons<count:
                    max_cons_vertices=[v]
            #Choose the first vertex with maximum remaining constraints within min value variables
            return max_cons_vertices[0] 
            
    def order_domain_values(self, variable, assignment):
        #Order domain values by least constraining values
        return sorted(list(self.curr_domains[variable]), key=lambda color: self.least_constraining_value(variable, color, assignment))
    
    def least_constraining_value(self, variable, color, assignment):
        count=0
        for u in self.constraints[variable]:
            if u not in assignment and color in self.curr_domains[u]:
                count+=1
        return count
    
    def backtrack_search(self, assignment):
        if len(assignment) == len(self.vertices):
            return assignment
        #Run AC3 Before Selection of Variables to Update the Current Domains 
        queue = [(v, u) for i,v in enumerate(self.vertices) for u in self.constraints[v]]
        if self.ac3(queue, assignment)==False:
            return None
        #Select Minimum Remaining Values with Tie Breaking
        variable = self.select_unassigned_variable(assignment)
        #Select the least constraining color
        for value in self.order_domain_values(variable, assignment):
            new_assignment = copy.deepcopy(assignment)
            new_assignment[variable] = value
            result = self.backtrack_search(new_assignment)
            if result is not None:
                return result
        return None
    
    def color_graph(self):
        assignment = self.backtrack_search({})
        if assignment is None:
            return None
        colors = {key: None for key in self.vertices}
        for vertex, color in assignment.items():
            colors[vertex] = color
        return colors
    
def read_input(file):
    with open(file, 'r', encoding='utf-8') as f:
        contents=f.readlines()
        num_colors=-1
        edges=deque([])
        vertices=deque([])
        for i, t in enumerate(contents):
            if t.strip()=="" or t.strip()[0]=="#":
                continue
            elif num_colors==-1:
                num_colors=int(re.sub("^Colors[ ]*=[ ]*","",t.strip(),flags=re.IGNORECASE))
            else: 
                edge=sorted([int(v.strip()) for n, v in enumerate(t.split(","))])
                if edge not in edges:
                    edges.append(edge)
                for n,v in enumerate(edge):
                    if v not in vertices:
                        vertices.append(v)
    return num_colors, list(vertices), list(edges)

if __name__=="__main__":
    #Intro
    print("CSCI 6511 AI")
    print("Project 2")
    print("Code Written by Eric Luo")
    print("Last Edited Feb 22, 2023")
    #Program Starts 
    print("Program starts...")
    #Get Input File Name
    while True:
        file=input('Please enter input file name:')
        if path.isfile(file)==True:
            break 
    #Read Input File
    num_colors, vertices, edges = read_input(file)
    #Initialize Graph
    print("Initialize Graph")
    gph=GraphColoringCSP(vertices=vertices, edges=edges, num_colors=num_colors)
    #Coloring The Graph 
    print("Start Coloring...")
    colors=gph.color_graph()
    #Print Outcome
    if colors is None:
        print("Coloring Failed.")
    else:
        print("Coloring Done...")
        print("Coloring Outcome:")
        for v in colors:
            print(f"\tVertex {v} is colored with color {colors[v]}")
    print("Print Finished...")
    print("Program Exists.")
