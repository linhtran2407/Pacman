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

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    explored = set()  # mark visited nodes
    stack = util.Stack()  # frontier using the initial state of the problem
    initialNode = Node(problem.getStartState(), None, None, 0, 0)
    stack.push(initialNode)

    while not stack.isEmpty():
        currentNode = stack.pop()

        # if node contains goal state
        if problem.isGoalState(currentNode.getCurrentState()):
            return solution(currentNode)

        # mark the current node as explored
        explored.add(currentNode.getCurrentState())

        # expand the current node and explore all its children
        for successor in problem.getSuccessors(currentNode.getCurrentState()):
            successorState, successorAction = successor[0], successor[1]
            # if the child state was not explored, push the child node to frontier
            if successorState not in explored:
                successorNode = Node(
                    successorState, currentNode, successorAction, 0, 0)
                stack.push(successorNode)

    return []


# def breadthFirstSearch(problem):
#     """Search the shallowest nodes in the search tree first."""
#     explored = set()  # mark visited nodes
#     queue = util.Queue()  # frontier using the initial state of the problem
#     initialNode = Node(problem.getStartState(), None, None, 0, 0)
#     queue.push(initialNode)

#     while not queue.isEmpty():
#         currentNode = queue.pop()

#         # if node contains goal state
#         if problem.isGoalState(currentNode.getCurrentState()):
#             return solution(currentNode)

#         # mark the current node as explored
#         explored.add(currentNode.getCurrentState())

#         # expand the current node and explore all its children
#         for successor in problem.getSuccessors(currentNode.getCurrentState()):
#             successorState, successorAction = successor[0], successor[1]
#             # if the child state was not explored, push the child node to frontier
#             if successorState not in explored:
#                 successorNode = Node(
#                     successorState, currentNode, successorAction, 0, 0)
#                 queue.push(successorNode)

#     return []

def breadthFirstSearch(problem, initialNode):
    """Search the shallowest nodes in the search tree first."""
    explored = set()  # mark visited nodes
    queue = util.Queue()  # frontier using the initial state of the problem
    initialNode = Node(problem.getStartState(), None, None, 0, 0)
    queue.push(initialNode)

    while not queue.isEmpty():
        currentNode = queue.pop()

        # if node is one of the corners
        if problem.isGoalState(currentNode.getCurrentState()):
            # if the goal node is not in the visited corner list yet
            if (currentNode.getCurrentState() not in problem.visitedCorners):
                problem.visitedCorners.append(currentNode.getCurrentState())
            if not problem.visitAllGoals():
                return breadthFirstSearch(problem, currentNode)
            else:
                return solution(currentNode)

        # mark the current node as explored
        explored.add(currentNode.getCurrentState())

        # expand the current node and explore all its children
        for successor in problem.getSuccessors(currentNode.getCurrentState()):
            successorState, successorAction = successor[0], successor[1]
            # if the child state was not explored, push the child node to frontier
            if successorState not in explored:
                successorNode = Node(
                    successorState, currentNode, successorAction, 0, 0)
                queue.push(successorNode)

    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    explored = set()  # mark visited nodes
    pq = util.PriorityQueue()  # frontier using the initial state of the problem
    initialNode = Node(problem.getStartState(), None, None, 0, 0)
    pq.push(initialNode, initialNode.getTotalPathCost())

    while not pq.isEmpty():
        currentNode = pq.pop()

        # if node contains goal state
        if problem.isGoalState(currentNode.getCurrentState()):
            return solution(currentNode)

        # expand the current node if it's not explored and explore all its children
        if currentNode.getCurrentState() not in explored:
            # mark the current node as explored
            explored.add(currentNode.getCurrentState())
            # loop through list of successors
            for successor in problem.getSuccessors(currentNode.getCurrentState()):
                successorState, successorAction = successor[0], successor[1]
                # create successor node and push to frontier along with priority value
                successorNode = Node(
                    successorState, currentNode, successorAction, 1, currentNode.getTotalPathCost()+1)
                pq.push(successorNode, successorNode.getTotalPathCost())

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    explored = set()  # mark visited nodes
    pq = util.PriorityQueue()  # frontier using the initial state of the problem
    initialNode = Node(problem.getStartState(), None, None,
                       0, 0)
    pq.push(initialNode, initialNode.getTotalPathCost() +
            heuristic(problem.getStartState(), problem))

    while not pq.isEmpty():
        currentNode = pq.pop()

        # if node contains goal state
        if problem.isGoalState(currentNode.getCurrentState()):
            return solution(currentNode)

        # expand the current node if it's not explored and explore all its children
        if currentNode.getCurrentState() not in explored:
            # mark the current node as explored
            explored.add(currentNode.getCurrentState())
            # loop through list of successors
            for successor in problem.getSuccessors(currentNode.getCurrentState()):
                successorState, successorAction = successor[0], successor[1]
                # create successor node and push to frontier along with priority value
                successorNode = Node(
                    successorState, currentNode, successorAction, 1, currentNode.getTotalPathCost()+1)
                pq.push(successorNode, successorNode.getTotalPathCost() +
                        heuristic(successorState, problem))

    return []


def solution(currentNode):
    solutionActions = []

    while currentNode.getParent() != None:
        solutionActions.append(currentNode.getActions())
        currentNode = currentNode.getParent()

    print("Solution length: ", len(solutionActions))
    return solutionActions[::-1]


class Node:
    def __init__(self, state, parent, actions, stepCost, totalPathCost):
        self.state = state  # current state
        self.parent = parent  # parent node
        self.actions = actions  # action taken to get to the state
        self.stepCost = stepCost  # step cost
        self.totalPathCost = totalPathCost  # total path cost

    def getCurrentState(self):
        return self.state

    def getParent(self):
        return self.parent

    def getActions(self):
        return self.actions

    def getStepCost(self):
        return self.stepCost

    def getTotalPathCost(self):
        return self.totalPathCost


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
