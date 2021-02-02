import gpiozero

from . import output


# TODO read from settings
DEFAULT_PERIOD = 2.0
DUTY_CYCLE_MIN = 0.0
DUTY_CYCLE_MAX = 1.0


def setup(config):
	outputs = {}
	for o in config['outputs']:
		if o['type'] == "pwm":
			outputs[o['name']] = PWM(**o)
		else:
			raise Exception("Unsupported output type ({}) for output: {}}".format(output['type'], output['name']))
	return outputs

class PWM(output.Output):

	def __init__(self, *args, **kwargs):
		self.name = kwargs['name']
		self._device = gpiozero.PWMOutputDevice(pin=kwargs['pin'])
		self._period = kwargs.get('period', DEFAULT_PERIOD)
		self._device.frequency = 1.0 / self._period

	def serialize(self):
		return {'name': self.name, 'pin': self._device.pin, 'period': self._period}

	def period(self, period):
		#if period < self.PERIOD_MIN or period > self.PERIOD_MAX:
		#	raise Exception()
		self._period = period
		self._device.frequency = 1.0 / self._period

	def set(self, duty_cycle):
		if duty_cycle < DUTY_CYCLE_MIN or duty_cycle > DUTY_CYCLE_MAX:
			raise Exception()
		self._device.value = duty_cycle

	def enable(self):
		self._device.pulse(fade_in_time=0, fade_out_time=0, n=None, background=True)

	def disable(self):
		self._device.off()

	@property
	def enabled(self):
		return self._device.is_active

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
