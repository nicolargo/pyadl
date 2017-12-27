PyADL
=====

A simple Python Wrapper for the AMD/ATI ADL lib.

It will be used in Glances to monitor GPU performance.

Usage:

First, import:
from pyadl import *

To get the supported devices list
Return: Array of ADLDevice
ADLManager.getInstance().getDevices()

For the following methods, device is an instance of ADLDevice

Get the current core voltage in mV
Return: Float
device.getCurrentCoreVoltage()

Get the current engine frequency in MHz
Return: Float
device.getCurrentEngineClock()

Get the current fan speed in a specified unit
Parameters: 
	speedType: ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE or ADL_DEVICE_FAN_SPEED_TYPE_RPM
Return: Integer
device.getCurrentFanSpeed(speedType):

Get the current memory frequency in MHz
Return: Float
device.getCurrentMemoryClock()

Get the current temperature in Celsius
Return: Float
device.getCurrentTemperature()

Get the current load in percentage
Return: Integer
device.getCurrentUsage():

Get the core voltage range
Parameters:
	reload: Force reload the cached data. Default: False
Return: (Min: Float, Max: Float)
device.getCoreVoltageRange(reload):

Get the engine clock frequency range 
Parameters:
	reload: Force reload the cached data. Default: False
Return: (Min: Float, Max: Float)
device.getEngineClockRange(reload):

Get the fan speed range in the specified unit
Parameters:
	speedType: ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE or ADL_DEVICE_FAN_SPEED_TYPE_RPM
	reload: Force reload the cached data. Default: False
Return: (Min: Integer, Max: Integer)
device.getFanSpeedRange(speedType, reload):

Get the memory clock frequency range (Min, Max)
Parameters:
	reload: Force reload the cached data. Default: False
Return: (Min: Float, Max: Float)
device.getMemoryClockRange(reload):


For testing:

python test.py
Options:
  -h, --help           show this help message and exit
  -l, --list-adapters  Lists all detected and supported display adapters.
  -s, --status         Shows current clock speeds, core voltage, utilization
                       and performance level.
					   
					   
Example outputs:
	On a single card machine:
	python test.py -s
	0. AMD Radeon (TM) R9 380 Series
        Engine core voltage: -2076327552 mV (0.0 mV - 0.0 mV)
        Engine clock: 975.54 MHz (150.0 MHz - 1200.0 MHz)
        Memory clock: 1400.0 MHz (75.0 MHz - 1750.0 MHz)
        Fan speed: 65 % (0 % - 100 %)
        Fan speed: 2958 RPM (0 RPM - 6000 RPM)
        Temperature: 77.0 Celsius
        Usage: 100 %
			
	On a miner rig with 5 RX 460:
	python test.py -s
	0. b'Radeon(TM) RX 460 Graphics'
			Engine core voltage: 1230037376 mV (0.0 mV - 0.0 mV)
			Engine clock: 1168.0 MHz (110.0 MHz - 1800.0 MHz)
			Memory clock: 1750.0 MHz (150.0 MHz - 2000.0 MHz)
			Fan speed: 35 % (0 % - 100 %)
			Fan speed: 1042 RPM (0 RPM - 4600 RPM)
			Temperature: 69.0 Celsius
			Usage: 100 %
	16. b'Radeon(TM) RX 460 Graphics'
			Engine core voltage: 757416320 mV (0.0 mV - 0.0 mV)
			Engine clock: 1142.11 MHz (110.0 MHz - 1800.0 MHz)
			Memory clock: 1750.0 MHz (150.0 MHz - 2000.0 MHz)
			Fan speed: 34 % (0 % - 100 %)
			Fan speed: 984 RPM (0 RPM - 4600 RPM)
			Temperature: 69.0 Celsius
			Usage: 100 %
	32. b'Radeon(TM) RX 460 Graphics'
			Engine core voltage: 1230037376 mV (0.0 mV - 0.0 mV)
			Engine clock: 1153.96 MHz (110.0 MHz - 1800.0 MHz)
			Memory clock: 1750.0 MHz (150.0 MHz - 2000.0 MHz)
			Fan speed: 33 % (0 % - 100 %)
			Fan speed: 989 RPM (0 RPM - 4600 RPM)
			Temperature: 70.0 Celsius
			Usage: 100 %
	48. b'Radeon(TM) RX 460 Graphics'
			Engine core voltage: 1230037376 mV (0.0 mV - 0.0 mV)
			Engine clock: 1098.78 MHz (110.0 MHz - 1800.0 MHz)
			Memory clock: 1750.0 MHz (150.0 MHz - 2000.0 MHz)
			Fan speed: 33 % (0 % - 100 %)
			Fan speed: 851 RPM (0 RPM - 4600 RPM)
			Temperature: 72.0 Celsius
			Usage: 100 %
	64. b'Radeon(TM) RX 460 Graphics'
			Engine core voltage: 1230037376 mV (0.0 mV - 0.0 mV)
			Engine clock: 1162.41 MHz (110.0 MHz - 1800.0 MHz)
			Memory clock: 1750.0 MHz (150.0 MHz - 2000.0 MHz)
			Fan speed: 33 % (0 % - 100 %)
			Fan speed: 858 RPM (0 RPM - 4600 RPM)
			Temperature: 67.0 Celsius
			Usage: 100 %