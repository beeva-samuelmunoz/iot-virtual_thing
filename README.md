# Thing simulator

The purpose of this library is to simulate a device in order to generate a fleet of virtual devices and connect to an IoT system to generate synthetic data.

Features:
* À la Arduino device logic programming.
* Random events: reboot, device death.
* Battery simulation: consumption, capacity, cost per operation.

Limitations:
* The virtual device can't receive data asynchronously.

```python
from virtual_thing import VirtualThing

# Create a virtual thing
thing = VirtualThing(device_identifier)
```


## User-defined functions
The way to define the logic of the virtual device is through custom functions.

Every function receives as first parameter the device object. It contains the following attributes and functions:
* device.id (string): device identifier
* device.time_start (float): epoch in seconds. Time since the last bootup.
* device.battery (float): battery voltage. If there is no battery, -1 will be returned and there won't be power constraints.
* device.send (function): function to use for communications.


### Setup
This function is called every time the device boots up (first wered and after a reboot).
```python
def setup_function(device):
	# Here goes the setup device bootup logic.
	pass

thing.set_setup(setup_function)
```

### Loop
This function should handle the main functionality and is called every `sleep_seconds`.
```python
def loop (device):
	# Here goes the device logic
	pass

thing.set_loop(functions.loop, sleep_seconds)
```

### Send
This function is a wrapper to the communications function and lets the framework handle battery constraints.
The first parameter is the device and can accept an arbitrary number of parameters. It should be called from the setup or the loop functions like `device.send(<user params>)`.

The `loss_p` parameter defines the probability of loosing the message.
```python
def send_function(device, user_param_1, ... , user_param_n):
	# Here goes the communications logic
	pass

thing.set_send(send_function, loss_p)
```

## Events
### Communication

### Reboot
It is possible to set the reboot probability of the device after every loop. If this event is triggered, the device reboots, the setup function will be executed, and then it will get into the loop.
```python
thing.set_reboot_p(0.001)
```

### Death
It is possible to set the ddath probability of the device after every loop. It this event is triggered, the device will stop.
```python
thing.set_die_p(0.00001)
```


## Battery
It is possible to plug a virtual battery to the device in order to have consumption issues.

* v_max: nominal voltage for the battery.
* v_min: minimumn operative voltage for the device.
	capacity: float
				Battery capacity. For example mAh
* costs: dictionary with the associated working costs.
	* send: capacity lost on a single device send operation.
	* compute_sg: capacity lost per second running.
	* alive_sg: capacity lost per second alive. Independent from compute_sg.
	* behaviour: mapping function from cumulative cost to remaining voltage. Currently only `linear` behaviour is implemented.

```python
thing.set_battery(
		v_max=3.3,
		v_min=3.0,
		capacity=500,
		costs={
			"send": 2.0,
			"compute_sg": 1.0,
			"alive_sg": 0.1
		},
	  behaviour='lineal'
)
```


## Examples
In `example.py` there is full working program.

User defined function examples can be found in `things/`:
* `test.py`: devices print on the screen a program counter, battery level and the device id.
* `mqtt_temp.py`: devices publish information on a MQTT topic with a single connector.
