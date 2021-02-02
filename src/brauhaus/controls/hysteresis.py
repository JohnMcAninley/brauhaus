from . import control

class Hysteresis(control.Control):

    def __init__(self, setpoint, hysteresis, forward=True, on=1.0, off=0.0):
        super()
        self._setpoint = setpoint
        self._hysteresis = hysteresis
        self._forward = forward
        self._on = on
        self._off = off

    def setpoint(self, sp):
        self._sp = sp

    def set_band(self, hysteresis):
        self._hysteresis = hysteresis

    def compute(self, val):
        return self._on if (-1)**self._forward * (val - self._sp) > self._hysteresis else self._off
