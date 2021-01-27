import simple_pid


MODULE = "pid"

SAMPLE_TIME = 1.0
OUTPUT_LIMITS = (0.0, 1.0)
DEFAULT_CONTROL = 'PID'
DEFAULT_TUNINGS = (2.0, 1.0, 5.0)


def setup():
	controls = []
	config = settings.read(MODULE)
	for control in config['controls']:
		c = PID()
		c.load(control)
		c.start()
		controls.append(c)


def auto_mode(pid, auto):
	if auto:
		_auto_setup(pid)
	else:
		_manual_setup(pid)
	# TODO is mode persistent?


def _auto_setup(pid):
	pid.set_auto_mode(True, last_output=pid.output.duty_cycle)


def _manual_setup(pid):
	pid.auto_mode = False


def setpoint(pid, sp):
	if sp < pid.SETPOINT_MIN or sp > pid.SETPOINT_MAX:
		raise Exception()
	pid.setpoint = sp
	# TODO is setpoint persistent?


def tunings(pid, (kp, ki, kd)):
	pid.tunings = (kp, ki, kd)
	# TODO write to settings


class PID():

	def __init__(self):
		pass

	def load(self, config):
		self.name = config['name']
		self.control = config['control'] if 'control' in config else DEFAULT_CONTROL
		self.tunings = config['tunings'] if 'tunings' in config else DEFAULT_TUNINGS
		self.p_on_ = config['tunings'] if 'tunings' in config else DEFAULT_TUNINGS
		self.pid = None

	def serialize(self):
		pass

	def start(self):
		self.pid = simple_pid.PID()
