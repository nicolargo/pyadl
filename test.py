import os, sys
from optparse import OptionParser
from pyadl import *
import collections

class ADLError(Exception):
	pass

adapters = []

def list_adapters():
   
	context = ADL_CONTEXT_HANDLE()
	if ADL2_Main_Control_Create(ADL_Main_Memory_Alloc, 1, byref(context)) != ADL_OK:
		raise ADLError("ADL2_Main_Control_Create failed.")
	
	num_adapters = c_int(-1)
	if ADL2_Adapter_NumberOfAdapters_Get(context, byref(num_adapters)) != ADL_OK:
		raise ADLError("ADL2_Adapter_NumberOfAdapters_Get failed.")
	
	# allocate an array of AdapterInfo, see ctypes docs for more info
	AdapterInfoArray = (AdapterInfo * num_adapters.value)() 
	
	# AdapterInfo_Get grabs info for ALL adapters in the system
	if ADL2_Adapter_AdapterInfo_Get(context, cast(AdapterInfoArray, LPAdapterInfo), sizeof(AdapterInfoArray)) != ADL_OK:
		raise ADLError("ADL2_Adapter_AdapterInfo_Get failed.")

	deviceAdapter = collections.namedtuple('DeviceAdapter', ['AdapterIndex', 'AdapterID', 'BusNumber', 'UDID'])
	devices = []
	
	for adapter in AdapterInfoArray:
		index = adapter.iAdapterIndex
		busNum = adapter.iBusNumber
		udid = adapter.strUDID
				
		adapterID = c_int(-1)
		
		if ADL2_Adapter_ID_Get(context, 0, byref(adapterID)) != ADL_OK:
			raise ADLError("ADL2_Adapter_Active_Get failed.")

		found = False
		for device in devices:
			if (device.AdapterID.value == adapterID.value):
				found = True
				break
		
		# save it in our list if it's the first controller of the adapter
		if (found == False):
			devices.append(deviceAdapter(index,adapterID,busNum,udid))
	
		adapter_info = []
	for device in devices:
		adapter_info.append(AdapterInfoArray[device.AdapterIndex])
	
	ADL2_Main_Control_Destroy(context)
	
	return adapter_info
	
def show_status():
	adapters = list_adapters()
	
	context = ADL_CONTEXT_HANDLE()
	if ADL2_Main_Control_Create(ADL_Main_Memory_Alloc, 1, byref(context)) != ADL_OK:
		raise ADLError("ADL2_Main_Control_Create failed.")
		
	for index, info in enumerate(adapters):
		print "%d. %s" % (index, info.strAdapterName)

		activity = ADLPMActivity()
		activity.iSize = sizeof(activity)
		
		if ADL2_Overdrive5_CurrentActivity_Get(context, info.iAdapterIndex, byref(activity)) != ADL_OK:
			raise ADLError("ADL2_Overdrive5_CurrentActivity_Get failed.")
		
		print ("	engine clock %gMHz, memory clock %gMHz, core voltage %gVDC, performance level %d, utilization %d%%" % 
					(activity.iEngineClock/100.0, activity.iMemoryClock/100.0, activity.iVddc,
					 activity.iCurrentPerformanceLevel, activity.iActivityPercent))
			
		fan_speed = {}
		for speed_type in (ADL_DL_FANCTRL_SPEED_TYPE_PERCENT, ADL_DL_FANCTRL_SPEED_TYPE_RPM):	
			fan_speed_value = ADLFanSpeedValue()
			fan_speed_value.iSize = sizeof(fan_speed_value)
			fan_speed_value.iSpeedType = speed_type

			if ADL2_Overdrive5_FanSpeed_Get(context, info.iAdapterIndex, 0, byref(fan_speed_value)) != ADL_OK:
				fan_speed[speed_type] = None
				continue
		
			fan_speed[speed_type] = fan_speed_value.iFanSpeed
			user_defined = fan_speed_value.iFlags & ADL_DL_FANCTRL_FLAG_USER_DEFINED_SPEED

		if bool(fan_speed[ADL_DL_FANCTRL_SPEED_TYPE_PERCENT]) and bool(fan_speed[ADL_DL_FANCTRL_SPEED_TYPE_RPM]):
			print "	fan speed %d%% (%d RPM) (%s)" % (fan_speed[ADL_DL_FANCTRL_SPEED_TYPE_PERCENT],
														fan_speed[ADL_DL_FANCTRL_SPEED_TYPE_RPM],
														"user-defined" if user_defined else "default")
		elif bool(fan_speed[ADL_DL_FANCTRL_SPEED_TYPE_PERCENT]):
			print "	fan speed %d%% (%s)" % (fan_speed[ADL_DL_FANCTRL_SPEED_TYPE_PERCENT],
											   "user-defined" if user_defined else "default")				
		elif bool(fan_speed[ADL_DL_FANCTRL_SPEED_TYPE_RPM]) is True:
			print "	fan speed %d RPM (%s)" % (fan_speed[ADL_DL_FANCTRL_SPEED_TYPE_RPM],
												 "user-defined" if user_defined else "default")
		else:
			print "	unable to get fan speed"
			
		temperature = ADLTemperature()
		temperature.iSize = sizeof(temperature)
			
		if ADL2_Overdrive5_Temperature_Get(context, info.iAdapterIndex, 0, byref(temperature)) != ADL_OK:
			raise ADLError("ADL2_Overdrive5_Temperature_Get failed.")
		
		print "	temperature %g C" % (temperature.iTemperature/1000.0)
		
		# Powertune level
		powertune_level_value = c_int()
		dummy = c_int()
		
		if ADL2_Overdrive5_PowerControl_Get(context, info.iAdapterIndex, byref(powertune_level_value), byref(dummy)) != ADL_OK:
			raise ADLError("ADL_Overdrive5_PowerControl_Get failed.")

		print "	powertune %d%%" % (powertune_level_value.value)
		
	ADL2_Main_Control_Destroy(context)
	
if __name__ == "__main__":
	usage = "usage: %prog [options]"
	
	parser = OptionParser(usage=usage)
	
	parser.add_option("-l", "--list-adapters", dest="action", action="store_const", const="list_adapters",
					  help="Lists all detected and supported display adapters.")
	parser.add_option("-s", "--status", dest="action", action="store_const", const="status",
					  help="Shows current clock speeds, core voltage, utilization and performance level.")
	
	(options, args) = parser.parse_args()
	
	result = 0

	try:

		if options.action == "list_adapters":
			adapters = list_adapters()
			for index, info in enumerate(adapters):
				print "%d. %s" % (index, info.strAdapterName)
		elif options.action == "status":
			show_status()
		else:
			parser.print_help()
	
	except ADLError, err:
		result = 1
		print err
		
	sys.exit(result)