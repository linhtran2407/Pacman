from game import Agent
from game import Directions
import random


class DumbAgent(Agent):
    """An agent that goes West until it can't."""

    def getAction(self, state):
        print("Location: ", state.getPacmanPosition())
        print("Actions available: ", state.getLegalPacmanActions())
        print("Ghost state: ", state.getGhostStates())

        if Directions.WEST in state.getLegalPacmanActions():
            print("Going West.")
            return Directions.WEST
        else:
            print("Stopping.")
            return Directions.STOP


class RandomAgent(Agent):
    """An agent that goes randomly."""

    def getAction(self, state):
        dir = random.choice(state.getLegalActions())
        print("Direction: ", dir)
        return dir


class BetterRandomAgent(Agent):
    """An agent that goes randomly 4 directions without stopping."""

    def getAction(self, state):
        # get all possible directions and remove the choice to stop
        possibleDirections = state.getLegalActions()
        possibleDirections.remove(Directions.STOP)
        # randomly choose one from the possible options
        dir = random.choice(possibleDirections)
        print("Direction: ", dir)
        return dir


class ReflexAgent(Agent):
    """
    This agent should look at the possible legal actions, and if one of these actions would cause a food pellet 
    to be eaten, it should choose that action. If none of the immediate actions lead to food, it should choose 
    randomly from the possibilities (excluding 'Stop').
    """

    def getAction(self, state):
        for dir in state.getLegalActions():
            # get state and Pacnman's position when Pacman takes the next action
            nextState = state.generatePacmanSuccessor(dir)
            x, y = nextState.getPacmanPosition()
            # return the next action if it leads to food
            if (state.hasFood(x, y)):
                print("Direction: ", dir)
                return dir

        # if none actions lead to food, choose randomly excluding "Stop"
        possibleDirections = state.getLegalActions()
        possibleDirections.remove(Directions.STOP)
        dir = random.choice(possibleDirections)
        print("Direction: ", dir)
        return dir

        # Prof.'s solution
        # legalMoves = state.getLegalActions()
        # legalMoves.remove('Stop')

        # succ = [(m, state.generatePacmanSuccessor(0, m)) for m in legalMoves]
        # # 0 is index of Pacman. for each move in legalMoves, generate state of next move and put in succ array
        # # as a tuple of (move, state), or (m, s)

        # movesWithFood = [m for m, s in succ
        #                  if state.hasFood(*s.getPacmacPosition())]
        # # for each move in the tuple (m, s) in the succ array, if there is food at the
        # # next move, add m in the array movesWithFood
        # # "*" explode the tuple (x, y) that indicates Pacman position, and pass (x, y)
        # # as param into the func

        # if len(movesWithFood) > 0:
        #     action = random.choice(movesWithFood)
        #     # print
        # else:
        #     action = random.choice(legalMoves)
        #     # print
        # return action
