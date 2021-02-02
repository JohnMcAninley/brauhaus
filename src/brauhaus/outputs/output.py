class Output():

	def __init__(self):
		self._paused = False

	def enable(self):
		pass

	def disable(self):
		pass

	@property
	def enabled(self):
		pass

	def set(self):
		pass

	def pause(self):
		if not self.enabled:
			return
		self._paused = True
		self.disable()

	def unpause(self):
		if not self._paused:
			return
		self._paused = False
		self.enable()

	def serialize(self):
		attr = self.__dict__.copy()
		attr.pop('_paused')
		return attr
