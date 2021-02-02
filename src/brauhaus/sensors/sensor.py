class Sensor():

	def __init__(self):
		pass

	def read(self):
		pass

	@property
	def last(self):
		NotImplemented()

	def serialize(self):
		return self.__dict__.copy()
