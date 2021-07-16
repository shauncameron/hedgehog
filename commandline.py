import argparse
from Hedgehog import *
import os 

argparser = argparse.ArgumentParser()

OPENINTERPRETER = 10200010

argparser.add_argument('file', help='Open and interpret file', type=str, nargs='*', default=OPENINTERPRETER)
argparser.add_argument('--r', help='Additionally write out the return result of the file', action='store_true')
argparser.add_argument('--se', help='Suppress returned error', action='store_true')

args = argparser.parse_args()

# Do args

if args.file == OPENINTERPRETER:

	hedgehog = ContextManager('')

	while (user := input('>>>> ')) != 'break':

		result, error = hedgehog.exec(filetext=user)
		if result:
			if isinstance(result, HedgehogType):
				print(result.__hh_repr__())
			else:
				print('Type: ', type(result))
				print(result)

elif os.path.isfile(args.file):

	hedgehog = ContextManager(text)
	#result, error = hedgehog.exec()
	#if result:
	#	print(result)

	while (user := input('>>>> ')) != 'break':

		result, error = hedgehog.exec(filetext=user)
		if result:
			print(result)

else:

	print('Hedgehog: Could not open file "%s", it does not exist' % args.file)