# Suppose there are two bowls of cookies. Bowl 1 contains 30 vanilla cookies and 10 chocolate cookies. Bowl 2 contains
# 20 of each. Now suppose you choose one of the bowls at random and, without looking, select a cookie at random.
# The cookie is vanilla. What is the probability that it came from Bowl 1?

from suite import Suite

class Cookie(Suite):

    def __init__(self, hypotheses_list, mix_data):
        Suite.__init__(self, hypotheses_list)
        # dictionary that holds the individual values for different cases
        self.mixes = mix_data

    def likelihood(self, hypothesis, data):
        mix = self.mixes[hypothesis]
        like = mix[data]
        return float(like)


hypotheses_list = ['Bowl1', 'Bowl2']

# hardcoded for now. Can be calculated easily based on input
mix_data = {'Bowl1': {'vanilla': 0.75, 'chocolate': 0.25}, 'Bowl2': {'vanilla': 0.5, 'chocolate': 0.5}}

cookie = Cookie(hypotheses_list, mix_data)
cookie.update('vanilla')
cookie.print_probability()