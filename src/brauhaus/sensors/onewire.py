import w1thermsensor
from w1thermsensor import W1ThermSensor

from . import sensor


BOIL_REF = 210.64		# TODO read from settings
FREEZE_REF = 32.0		# TODO units


def setup(config):
	devices = {}
	for c in config['sensors']:
		owt = OneWire(**c)
		owt.connect()
		devices[c['name']] = owt
	return devices


def discover():
	# Find all sensors on bus
	return W1ThermSensor.get_available_sensors()


def unconfigured(discovered, configured):
	configured_ids = [s.address for s in configured]
	return [s for s in discovered if s.id not in [configured_ids]]


def configure(address, name):
	# TODO can same address be configured > 1x
	s = OneWire(name=name, address=address)
	s.connect()
	return s


class OneWire(sensor.Sensor):

	def __init__(self, *args, **kwargs):
		self.name = kwargs['name']
		self._address = kwargs['address']
		self._preprocess = kwargs.get('preprocess', False)
		self._boil_exp = kwargs.get('boil_exp', BOIL_REF)
		self._freeze_exp = kwargs.get('freeze_exp', FREEZE_REF)
		self._sensor = None
		self._connected = False
		self._last_raw = None
		self._last = None

	def connect(self):
		try:
			self._sensor = W1ThermSensor(sensor_id=self._address)
			self._connected = True
		except w1thermsensor.NoSensorFoundError:
			self._sensor = None
			self._connected = False
		return self._connected

	def read(self):
		self._last_raw = self._sensor.get_temperature()
		self._last = self._correct(self._last_raw) if self._preprocess else self._last_raw
		return self.last

	def _correct(self, reading):
		return (BOIL_REF - FREEZE_REF) * (reading - self._freeze_exp) / (self.boil_exp - self._freeze_exp) + FREEZE_REF

	def calibrate(self):
		# TODO
		pass

	@property
	def last(self):
		return self._last

	def serialize(self):
		attr = super().serialize()
		attr.pop('_sensor')
		attr.pop('_connected')
		attr.pop('_last_raw')
		attr.pop('_last')
		return attr
