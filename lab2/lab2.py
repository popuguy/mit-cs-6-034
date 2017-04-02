# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
	checked = [start]
	to_check = [[start]]
	path = []
	while len(to_check) > 0:
		path = to_check.pop()
		cur = path[-1]
		if cur == goal:
			return path
		children = sorted(graph.get_connected_nodes(cur), reverse=True)
		children = [child for child in children if child not in checked]
		checked += children
		to_check = [path + [child] for child in children] + to_check
	return None



## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
	checked = []
	path = []
	cur = start
	while len(path) > 0 or len(checked) == 0:
		if cur == goal:
			return path + [cur]
		children = [node for node in graph.get_connected_nodes(cur) \
			if node not in checked]
		checked.append(cur)
		if len(children) > 0:
			path.append(cur)
			cur = min(children)
		else:
			# backtrack
			cur = path.pop()
	return None


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
	agenda = [[start]]
	while len(agenda) > 0:
		path = agenda.pop()
		cur = path[-1]
		if cur == goal:
			return path
		children = graph.get_connected_nodes(cur)
		children.sort(key=lambda child: graph.get_heuristic(child, goal))
		agenda += [path + [c] for c in children if c not in path][::-1]
	return []


## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
	agenda = [[start]]
	#go through full agenda
	while len(agenda) > 0:
		new_agenda = []
		#work through all agenda items
		for item in range(len(agenda)):
			path = agenda[item]
			cur = path[-1]
			#end if goal achieved
			if cur == goal:
				return path
			#get candidate nodes
			children = graph.get_connected_nodes(cur)
			#add candidate paths
			new_agenda += [path + [c] for c in children if c not in path]
		#change to new candidate paths
		agenda = new_agenda[:]
		#sort by heuristic and prune to width
		agenda = sorted(agenda, \
			key=lambda a: graph.get_heuristic(a[-1], goal))[:beam_width]

	return []


## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
	total = 0
	for n in range(len(node_names) - 1):
		edge_length = graph.get_edge(node_names[n], node_names[n + 1]).length
		total += edge_length
	return total
def branch_and_bound(graph, start, goal):
	agenda = [[start]]
	while len(agenda) > 0:
		agenda.sort(key=lambda a:path_length(graph, a), reverse=True)
		path = agenda.pop()
		cur = path[-1]
		#since it's sorted, this must be optimal
		if cur == goal:
			return path
		children = graph.get_connected_nodes(cur)
		agenda += [path + [c] for c in children if c not in path]
	return []


def a_star(graph, start, goal):
	extended = []
	agenda = [[start]]
	while len(agenda) > 0:
		agenda.sort(key=lambda a:path_length(graph, a) + \
			graph.get_heuristic(a[-1], goal), reverse=True)
		path = agenda.pop()
		cur = path[-1]
		if cur == goal:
			return path
		children = graph.get_connected_nodes(cur)
		to_add = [c for c in children if c not in path and c not in extended]
		extended += to_add
		agenda += [path + [t] for t in to_add]
	return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
	checked = [goal]
	agenda = [goal]
	while len(agenda) > 0:
		cur = agenda.pop()
		children = graph.get_connected_nodes(cur)
		new_nodes = [n for n in children if n not in checked]
		agenda += new_nodes
		checked += new_nodes
		if graph.get_heuristic(cur, goal) > path_length(graph, branch_and_bound(graph, cur, goal)):
			return False
	return True

def is_consistent(graph, goal):
	checked = []
	agenda = [goal]
	while len(agenda) > 0:
		cur = agenda.pop()
		children = graph.get_connected_nodes(cur)
		new_nodes = [n for n in children if n not in checked]
		agenda += new_nodes
		base_heuristic = graph.get_heuristic(cur, goal)
		for node in new_nodes:
			neighbor_heuristic = graph.get_heuristic(node, goal)
			heuristic_distance = abs(neighbor_heuristic - base_heuristic)
			edge_length = graph.get_edge(cur, node).length
			if edge_length < heuristic_distance:
				return False
		checked.append(cur)
	return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '7'
WHAT_I_FOUND_INTERESTING = 'working out a*'
WHAT_I_FOUND_BORING = 'figuring out specifics of beam search'
