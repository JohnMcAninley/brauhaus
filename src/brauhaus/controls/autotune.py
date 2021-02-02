import autotune

from . import pid


OUTPUT_LIMITS = (0.0, 1.0)
DEFAULT_TUNINGS = {'Kp': 2.0, 'Ki': 1.0, 'Kd': 5.0}
DEFAULT_P_ON_M = False
DEFAULT_SETPOINT = 0.0
DEFAULT_SAMPLE_TIME = 0.1


class Autotune(pid.PID):

	def __init__(self, *args, **kwargs):
		self.name = kwargs['name']
		# TODO are input and output required?
		self.input = kwargs.get('input')
		self.output = kwargs.get('output')
		self._paused = False

		self._autotune = autotune.PIDAutotune(
			kwargs.get('setpoint', DEFAULT_SETPOINT), 10,
			sample_time=kwargs.get('sample_time', DEFAULT_SAMPLE_TIME),
			out_min=kwargs.get('output_limits', OUTPUT_LIMITS)[0],
			out_max=kwargs.get('output_limits', OUTPUT_LIMITS)[1]
		)

	def compute(self, input):
		self._autotune.run(input)
		return self._autotune.output

	@property
	def auto(self):
		return (self._autotune.state == PIDAutotune.STATE_RELAY_STEP_UP or
			self._autotune.state == PIDAutotune.STATE_RELAY_STEP_DOWN)

	def auto_mode(self, auto, last_output=None):
		self._pid.set_auto_mode(auto, last_output=last_output)

	def setpoint(self, sp):
		#if sp < self.SETPOINT_MIN or sp > self.SETPOINT_MAX:
		#	raise Exception()
		self._autotune.setpoint = sp

	def pause(self):
		if not self._pid.auto_mode:
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
		attr.pop('_paused')
		attr.pop('_autotune')
		kp, ki, kd = self._pid.tunings
		return attr
