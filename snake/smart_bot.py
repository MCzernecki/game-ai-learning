from settings import ACTION_UP, ACTION_DOWN, ACTION_RIGHT, ACTION_LEFT

class SmartBot:
    def choose_action(self, state):
        head_x = state["head_x"]
        head_y = state["head_y"]
        food_x = state["food_x"]
        food_y = state["food_y"]
        danger = state["danger"]

        preffered_actions = []

        if food_x > head_x:
            preffered_actions.append(ACTION_RIGHT)
        if food_x < head_x:
            preffered_actions.append(ACTION_LEFT)
        if food_y > head_y:
            preffered_actions.append(ACTION_DOWN)
        if  food_y < head_y:
            preffered_actions.append(ACTION_UP)

        for action in preffered_actions:
            if not danger[action]:
                return action

        for action in [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]:
            if not danger[action]:
                return action

        return ACTION_RIGHT