import simple_pid

from . import control


OUTPUT_LIMITS = (0.0, 1.0)
DEFAULT_TUNINGS = {'Kp': 2.0, 'Ki': 1.0, 'Kd': 5.0}
DEFAULT_P_ON_M = False
DEFAULT_SETPOINT = 0.0
DEFAULT_SAMPLE_TIME = 0.1


class PID(control.Control):

	def __init__(self, *args, **kwargs):
		super()
		self.name = kwargs['name']
		# TODO are input and output required?
		self.input = kwargs.get('input')
		self.output = kwargs.get('output')
		self._pid = simple_pid.PID(**kwargs.get('tunings', DEFAULT_TUNINGS),
			setpoint=kwargs.get('setpoint', DEFAULT_SETPOINT),
			sample_time=kwargs.get('sample_time', DEFAULT_SAMPLE_TIME),
			output_limits=tuple(kwargs.get('output_limits', OUTPUT_LIMITS)),
			auto_mode=False,
			proportional_on_measurement=kwargs.get('p_on_m', DEFAULT_P_ON_M)
		)

	def compute(self, input):
		return self._pid(input)

	def serialize(self):
		attr = self.__dict__.copy()
		attr.pop('_pid')
		kp, ki, kd = self._pid.tunings
		attr['tunings'] = {'Kp': kp, 'Ki': ki, 'Kd': kd}
		attr['setpoint'] = self._pid.setpoint
		attr['sample_time'] = self._pid.sample_time
		attr['output_limits'] = self._pid.output_limits
		attr['p_on_m'] = self._pid.proportional_on_measurement
		return attr

	def tunings(self, tunings):
		self._pid.tunings = tunings

	@property
	def auto(self):
		return self._pid.auto_mode

	def auto_mode(self, auto, last_output=None):
		self._pid.set_auto_mode(auto, last_output=last_output)

	def setpoint(self, sp):
		#if sp < self.SETPOINT_MIN or sp > self.SETPOINT_MAX:
		#	raise Exception()
		self._pid.setpoint = sp
