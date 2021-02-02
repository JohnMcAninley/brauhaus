class Control():

	def __init__(self):
		self._auto = False
		self._paused = False

	@property
	def auto(self):
		return self._auto

	def auto_mode(self, mode):
		self._auto = mode

	def setpoint(self, sp):
		raise NotImplemented()

	def compute(self, input):
		raise NotImplemented()

	def pause(self):
		if not self.auto:
			return
		self._paused = True
		self.auto_mode(False)

	def unpause(self, last_output=0.0):
		if not self._paused:
			return
		self._paused = False
		self.auto_mode(True, last_output)

	def serialize(self):
		attr = self.__dict__.copy()
		attr.pop('_auto')
		attr.pop('_paused')
		return attr
