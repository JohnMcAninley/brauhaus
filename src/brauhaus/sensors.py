from w1thermsensor import W1ThermSensor

import settings


MODULE = "sensors"

BOIL_REF = 210.64		# TODO read from settings
FREEZE_REF = 32.0		# TODO units


def startup():
	# TODO 1 Wire must be up already to run without sudo privileges
	devices = []
	config = settings.read(MODULE)
	for sensor in config['sensors']:
		s = Sensor()
		s.load(sensor)
		s.connect()
		devices.append(s)
	return devices


def discover():
	# Find all sensors on bus
	return w1thermsensor.get_available_sensors()


def unconfigured():
	sensors = discover()
	# TODO don't read from settings file
	configured = settings.read(MODULE, "sensors")
	configured_ids = [s.id for s in configured]
	return [s for s in sensors if s.id not in [configured_ids]]


def new(address, name, required=False):
	# TODO can same address be configured > 1x
	# if address in configured_sensors:
	#	return
	s = Sensor(address, name, required)
	s.connect()
	settings.append(MODULE, s)


class Sensor():

	def __init__(self, *args, **kwargs):
		self.address = kwargs['address'] if 'address' in kwargs else None
		self.name = kwargs['name'] if 'name' in kwargs else None
		self.required = kwargs['required'] if 'required' in kwargs else None
		self.sensor = None
		self.last_raw = None
		self.last = None

	def load(self, config):
		self.name = config['name']
		self.address = config['address']
		self.required = config['required'] if 'required' in config else False

	def serialize(self):
		return {'name': self.name, 'address': self.address, 'required': self.required}

	def connect(self):
		try:
			self.sensor = W1ThermSensor(sensor_id=self.address)
		except w1thermsensor.NoSensorFoundError as e:
			if self.required:
				logger.warn("Required sensor {} could not be connected. PID restricted to manual mode.".format(self.name))
				# TODO prevent PID from running in auto
			else:
				logger.info("Sensor {} could not be connected".format(self.name))

	def read(self):
		self.last_raw = self.sensor.get_temperature()
		self.last = self.correct(reading) if self.correct else self.last_raw
		return self.last

	def correct(self, reading):
	 	return (BOIL_REF - FREEZE_REF) * (reading - self.freeze_exp) / (self.boil_exp - self.freeze_exp) + FREEZE_REF

	def calibrate(self):
		# TODO
		pass
