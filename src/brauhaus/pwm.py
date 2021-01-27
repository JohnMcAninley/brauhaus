import gpiozero

import settings


MODULE = "sensors"

# TODO read from settings
DEFAULT_PERIOD = 2.0


def setup():
	outputs = []
	config = settings.read(MODULE)
	for output in config['outputs']:
		if output['type'] == "pwm":
			o = PWM()
			o.load(output)
			output.append(o)
		else:
			raise Exception("Unsupported output type ({}) for output: {}}".format(output['type'], output['name']))


class PWM():

	def __init__(self):
		pass

	def load(self, config):
		self.name = config['name']
		self.pin = config['pin']
		self.period = config['period'] if 'period' in config else DEFAULT_PERIOD
		self.device = gpiozero.PWMOutputDevice(pin=self.pin)
		self.device.frequency = 1.0 / self.period

	def serialize(self):
		return {'name': self.name, 'pin': self.pin, 'period': self.period}

	def period(self, period):
		if period < self.PERIOD_MIN or period > self.PERIOD_MAX:
			raise Exception()
		self.period = period
		self.device.frequency = 1.0 / self.period
		# TODO does the pulse change automatically?
		settings.update(MODULE, self.serialize())

	def duty_cycle(self, duty_cycle):
		if duty_cycle < self.DUTY_CYCLE_MIN or duty_cycle > self.DUTY_CYCLE_MAX:
			raise Exception()
		self.device.value = duty_cycle
		# TODO is duty cycle persistent?

	def enable(self):
		# TODO interlock conditions
		self.device.pulse(fade_in_time=0, fade_out_time=0, n=None, background=True)

	def disable(self):
		self.device.off()
