from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
	 match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

def backchain_to_goal_tree(rules, hypothesis):
	ants = []
	rules1 = rules[:]
	for rule in rules1:
		# match takes the template as a string, must check all consequents
		for consequent in rule.consequent():
			var_dict = match(consequent, hypothesis)
			if var_dict != None:
				# have found matching rule
				antecedent = rule.antecedent()
				if isinstance(antecedent, basestring):												
					ants.append(backchain_to_goal_tree(rules, populate(antecedent, var_dict)))
				else:
					for i in range(len(antecedent)):
						antecedent[i] = backchain_to_goal_tree(rules, populate(antecedent[i], var_dict))
						ants.append(antecedent)
				continue
	return simplify(OR(hypothesis, OR(ants)))


# Here's an example of running the backward chainer - uncomment
# it to see it work:
# print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
