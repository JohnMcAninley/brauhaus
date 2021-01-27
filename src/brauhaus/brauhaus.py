import sensors
import pwm
import pid


class Brauhaus():

	def __init__(self):
		pass

	def setup(self):
		self.sensors = sensors.setup()
		self.outputs = pwm.setup()
		pid.setup()

	def run(self):
		while True:
			# Read current temperatures
			for sensor in self.sensors:
				# TODO cant't read temperature 
				sensor.read()
			# TODO temperature correction
			for pid in pids:
				output = pid(value)

if __name__ == "__main__":
	brauhaus = Brauhaus()
	brauhaus.setup()
	brauhaus.run()
