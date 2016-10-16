Four Steps to Computational Creativity
======================================

Here is going to be a short explanation for computation creativity based on
Dan Ventura's article in ICCC 2016 :cite:`ventura2016`. ::

	# Generation using stochastic process
	def create():
		a = []
		while not DONE:
			a = a + random_atom()
		return a

	# Generation by plagiarizing an inspiring set
	def create(inspiring_set):
		a = random_select(inspiring_set)
		return a

	# Generation by memorizing an inspiring set
	def create(inspiring_set):
		model = memorize(inspiring_set)
		a = random_from_memory(model)
		return a

	# Generation by generalizing an inspiring set
	def create(inspiring_set):
		model = build_model(inspiring_set)
		a = generalize_from_model(model)
		return a

	# Generation by modeling an inspiring set and filtering artifacts via
	# fitness function
	def create(inspiring set):
		model = build_model(inspiring_set)
		while score < theta:
			a = generate(model)
			score = fitness(a)
		return a
