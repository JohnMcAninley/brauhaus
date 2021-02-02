{
    "path": "",
    "verb": "",
    "data": ""
}

{
	"sensors": {
		["get", "new"],
        ""
	},
	"pid": {
		"get": "",
        "new": "",
        "setpoint": {
            "get": lambda r: pid.setpoint(r['name']),
            "set": lambda r: pid.setpoint(r['name'], r['setpoint'])
        },
        "mode": {
            "get": lambda r: pid.auto_mode(r['name']),
            "set": lambda r: pid.auto_mode(r['name'], r['auto'])
        },
        "tuning": {
            "get": lambda r: pid.tunings(r['name']),
            "set": lambda r: pid.tunings(r['name'], r['tunings'])
        },
        "autotune": {},
    },
    "pwm": {
        "get": "",
        "new": "",
        "period": {
            "get": lambda r: pwm.period(r['name']),
            "set": lambda r: pwm.period(r['name'], r['period'])
        },
        "duty_cycle": {
            "get": lambda r: pwm.duty_cycle(r['name']),
            "set": lambda r: pwm.duty_cycle(r['name'], r['duty_cycle'])
        }
    }
}
