# Monty Hall was the original host of the game show Let’s Make a Deal. The
# Monty Hall problem is based on one of the regular games on the show. If
# you are on the show, here’s what happens:
# • Monty shows you three closed doors and tells you that there is a prize
#   behind each door: one prize is a car, the other two are less valuable
#   prizes like peanut butter and fake finger nails. The prizes are arranged
#   at random.
# • The object of the game is to guess which door has the car. If you guess
#   right, you get to keep the car.
# • You pick a door, which we will call Door A. We’ll call the other doors
#   B and C.
# • Before opening the door you chose, Monty increases the suspense by
#   opening either Door B or C, whichever does not have the car. (If the
#   car is actually behind Door A, Monty can safely open B or C, so he
#   chooses one at random.)
# • Then Monty offers you the option to stick with your original choice or
#   switch to the one remaining unopened door.
#
# The question is, should you “stick” or “switch” or does it make no difference?


# Here hypothesis represents the probability of car being behind a particular door.
# Hypothesis A=> car is behind door A, B=> car is behind door B, C=> car behind door C
from suite import Suite


class MontyHall(Suite):

    def __init__(self, hypotheses_list, user_selected_door):
        Suite.__init__(self, hypotheses_list)
        self.user_selected_door = user_selected_door

    def likelihood(self, hypothesis, host_selected_door):
        if host_selected_door == hypothesis:
            # the host can not select the door which has car behind it, so in this case prob is 0
            return 0.0
        elif hypothesis == self.user_selected_door:
            # if user selects the door where car is present, host can open any of the other two doors with a probability
            # of 0.5
            return 0.5
        else:
            # if the code reaches here, it means that user has not selected a door which has car behind it
            # so there is one door(hypothesis) which has car behind it and other one which doesn't.
            # host can not open the door which has car behind it, so he has to open the remaining door for sure.
            return 1.0

hypotheses_list = ['A', 'B', 'C']
user_selected_door = 'A'

monty_hall = MontyHall(hypotheses_list, user_selected_door)
monty_hall.update('B')
monty_hall.print_probability()