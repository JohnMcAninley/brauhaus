import time
import logging

import settings
from sensors import onewire
from outputs import pwm
from controls import pid

import client
import api


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Brauhaus():

	def __init__(self):
		self._main_power = False
		self._push_interval = 1.0
		self._last_push_time = time.time() - self._push_interval

	def setup(self):
		self._sensors = onewire.setup(settings.read("sensors"))
		self._controls = {c['name']: pid.PID(**c) for c in settings.read("pid")['pids']}
		self._outputs = pwm.setup(settings.read("pwm"))
		self._client = client.Client(**settings.read("client")['client'])
		self._client.connect()

	def run(self):
		while True:
			# Read current temperatures
			for sensor in self._sensors.values():
				# TODO cant't read temperature
				val = sensor.read()
				logger.debug("{}: {}".format(sensor.name, val))

			for control in self._controls.values():
				if control.auto:
					output_val = control.compute(
						self._sensors[control.input].last)
					self._outputs[control.output].set(output_val)

			if time.time() - self._last_push_time > self._push_interval:
				if self._client.push({name: s.last for name, s in self._sensors.items()}):
					self._last_push_time = time.time()

	def enable_main_power(self):
		self._main_power = True
		for o in self._outputs:
			if o.paused:		# redundant check
				o.unpause(o)
				self._unpause_controls(o)

	def disable_main_power(self):
		self._main_power = False
		for o in self._outputs:
			if o.enabled:		# redundant check
				o.pause(o)
				self._pause_controls(o)

	def enable_output(self, output):
		if not self._main_power:
			# TODO mark output as paused
			return
		self._unpause_controls(output)
		output.enable()

	def disable_output(self, output):
		self._pause_controls(output)
		output.disable()

	def _unpause_controls(self, output):
		for c in self._controls.values():
			if c.output == output.name and c.paused:
				c.unpause(last_input=0.0)

	def _pause_controls(self, output):
		for c in self.controls.values():
			if c.output == output.name and c.auto:
				c.pause()

	def set_output(self, output, duty):
		if any(c.output == output.name and c.pid.auto_mode for c in self.controls):
			# raise Exception()
			return
		output.duty_cycle(duty)

	def _handle(self):
		handlers = {
			"outputs": {
				"enable": (self.enable_output, ['id']),
				"disable": (self.disable_output, ['id']),
				"set": (self.set_output, ['id', 'value'])
			},
			"controls": {
				"auto": (self.set_mode, ['id', 'auto']),
				"setpoint": (self.set_setpoint, ['id', 'value']),
			},
			"sensors": {}
		}
		req = self._client.read()
		if not req:
			return
		status, res = api.validate(req, handlers)
		if status:
			resource = self.__dict__.get('_' + req['resource']).get('id')
			if resource:
				handler = handlers[resource][req['action']]
				res = handler[0](**{a: req[a] for a in handler[1]})
			else:
				res = {"error: invalid parameter: {}".format(req['resource'])}
		self._client.push(res)


if __name__ == "__main__":
	brauhaus = Brauhaus()
	brauhaus.setup()
	brauhaus.run()
