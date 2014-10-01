#Code adopted from https://github.com/codebox/bayesian-classifier
import sys
from learn import Learn
from classify import Classify
from reset import Reset
from status import Status

modes = {}

def register_mode(mode_class):
	modes[mode_class.__name__.lower()] = mode_class

def main(args):
	try:
		register_mode(Learn)
		register_mode(Classify)
		register_mode(Reset)
		register_mode(Status)

		usage = 'Usage: %s %s <mode specific args>' % (args[0], '|'.join(modes.keys()))

		if (len(args) < 2):
			raise ValueError(usage)

		mode_name = args[1]
		if mode_name not in modes:
			raise ValueError(usage + '\nUnrecognised mode: ' + mode_name)

		mode = modes[mode_name]()
		mode.validate(args)
		return mode.output(mode.execute())
		
	except Exception as ex:
		print ex
