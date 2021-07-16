from Hedgehog import *

text = ( 
"""
1 + 2 + 3 / 4 + 5; 
5 + 6 + 8 * 9 // 10;
1 + 2 * 3;
""")

hedgehog = ContextManager(text, None)
#result, error = hedgehog.exec()
#if result:
#	print(result)

while (user := input('>>>> ')) != 'break':

	result, error = hedgehog.exec(filetext=user)
	if result:
		print(result)