class ProbabilityMass(object):

    def __init__(self, hypotheses_list):
        self.dict_probability = {}
        for value in hypotheses_list:
            self.dict_probability[value] = 1

    def set(self, key, value=1):
        self.dict_probability[key] = value

    def mult(self, hypothesis, factor):
        self.dict_probability[hypothesis] *= float(factor)

    def normalize(self):
        total = sum(self.dict_probability.values())

        for key, value in self.dict_probability.iteritems():
            value = float(value) / total
            self.dict_probability[key] = value

    def get_probability_dict(self):
        return self.dict_probability


class Suite(ProbabilityMass):

    def __init__(self, hypotheses_list):
        ProbabilityMass.__init__(self, hypotheses_list)
        self.normalize()

    def update(self, data):
        for hypothesis, value in self.get_probability_dict().iteritems():
            like = self.likelihood(hypothesis, data)
            self.mult(hypothesis, like)
        self.normalize()

    def print_probability(self):
        for key, value in self.get_probability_dict().iteritems():
            print '%s, %s' % (key, value)

