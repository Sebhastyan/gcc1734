# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import*

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    visited = set()                             # Conjunto para acompanhar nós visitados
    stack=util.Stack()                          # Pilha para manter os nós a serem explorados
    startNode=(problem.getStartState(),[])
    stack.push(startNode)
    while not stack.isEmpty():
        vertex = stack.pop()                    # Desempilha o nó do topo da pilha
        location=vertex[0]
        path=vertex[1]
        if location not in visited:
            visited.add(location)               # Marca o nó como visitado
            if problem.isGoalState(location):
                return path
            # Empilhe os vizinhos não visitados do nó atual
            successors=problem.expand(location)
            for suc in list(successors):
                if suc[0] not in visited:
                    stack.push((suc[0],path+[suc[1]]))            
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    queue=util.Queue()                          # Conjunto para acompanhar nós visitados
    visited=[]                                  # Fila para manter os nós a serem explorados
    startNode=(problem.getStartState(),[])                           
    queue.push(startNode)                       # Enfileire o nó inicial
    while not queue.isEmpty():
        vertex=queue.pop()                      # Retire o nó da frente da fila
        location=vertex[0]
        path=vertex[1]
        if location not in visited:
            visited.append(location)
            if problem.isGoalState(location):
                return path
            # Enfileire os vizinhos não visitados do nó atual
            successors=problem.expand(location)
            for suc in list(successors):
                if suc[0] not in visited:
                    queue.push((suc[0],path + [suc[1]]))
    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# def aStarSearch(problem, heuristic=nullHeuristic):
#     """Search the node that has the lowest combined cost and heuristic first."""
#     "*** YOUR CODE HERE ***"
#     util.raiseNotDefined()

def aStarSearch(problem, heuristic=nullHeuristic):
    from util import PriorityQueue

    # Fila de prioridade para armazenar os estados a serem explorados
    open_list = PriorityQueue()

    # Conjunto para armazenar os estados já explorados
    closed_set = set()

    # Dicionário para manter o custo mínimo conhecido de cada estado explorado
    g_scores = {}

    # Contador para quebrar empates entre estados com custos iguais
    counter = 0

    # Estado inicial
    start_state = problem.getStartState()

    # Custo inicial é zero
    initial_g_score = 0

    # Inicialização da fila de prioridade com o estado inicial
    open_list.push((start_state, [], initial_g_score, counter), initial_g_score)

    # Inicialização do dicionário de custos
    g_scores[start_state] = initial_g_score

    while not open_list.isEmpty():
        current_state, path, current_g_score, _ = open_list.pop()

        # Verifica se o estado atual é o estado objetivo
        if problem.isGoalState(current_state):
            return path

        # Verifica se o estado já foi explorado
        if current_state in closed_set:
            continue  # Ignorar estados repetidos

        # Marca o estado como explorado
        closed_set.add(current_state)

        # Expande os sucessores do estado atual
        for successor_state, action, step_cost in problem.expand(current_state):
            new_path = path + [action]
            new_g_score = current_g_score + step_cost

            # Verifica se o estado não foi explorado e se o novo caminho é melhor
            if (successor_state not in closed_set and
                (successor_state not in g_scores or new_g_score < g_scores[successor_state])):
                counter += 1
                open_list.push((successor_state, new_path, new_g_score, counter), new_g_score + heuristic(successor_state, problem))
                g_scores[successor_state] = new_g_score

    return []  # Se chegarmos aqui, não encontramos um caminho válido

def iterativeDeepeningSearch(problem):
    """
    Perform Depth-First Iterative Deepening Search (IDS).
    Returns a solution if found.
    """
    for depth in range(1, sys.maxsize):  # Usar sys.maxsize como profundidade máxima
        result = depthLimitedSearch(problem, depth)
        if result is not None:
            return result

def depthLimitedSearch(problem, limit):
    """
    Perform Depth-Limited Search up to a given depth limit.
    Returns a solution if found or None if the limit is reached.
    """
    visited = set()                       # Conjunto para acompanhar nós visitados
    stack = util.Stack()                  # Pilha para manter os nós a serem explorados
    startNode = (problem.getStartState(), [])
    stack.push(startNode)

    while not stack.isEmpty():
        vertex = stack.pop()               # Desempilha o nó do topo da pilha
        location = vertex[0]
        path = vertex[1]

        if location not in visited:
            visited.add(location)          # Marca o nó como visitado

            if problem.isGoalState(location):
                return path

            # Empilhe os vizinhos não visitados do nó atual
            successors = problem.expand(location)
            for suc in list(successors):
                if suc[0] not in visited and len(path) < limit:  # Verifica a profundidade limite
                    stack.push((suc[0], path + [suc[1]]))

    return None



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ids=iterativeDeepeningSearch
