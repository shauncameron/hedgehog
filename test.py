a = type.__dict__.copy()
a.update(str.__dict__.copy())

for attr, func in a.items():
	print(f'"{attr}"', '-->', func)