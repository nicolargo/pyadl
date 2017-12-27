# Copyright (C) 2017 by Gergo Szabo <szager88@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

class ADLError(Exception):
    pass

try:
    from .adl_api import *
except OSError:
    raise ADLError("Driver not found!")
# RuntimeError raises from adl_api if OS not supported

ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE = ADL_DL_FANCTRL_SPEED_TYPE_PERCENT
ADL_DEVICE_FAN_SPEED_TYPE_RPM = ADL_DL_FANCTRL_SPEED_TYPE_RPM

class ADLManager(object):

    __instance = None

    @staticmethod
    def getInstance():
        if ADLManager.__instance == None:
            ADLManager()

        return ADLManager.__instance

    def getDevices(self):
        return self.devices

    def __init__(self):
        if ADLManager.__instance != None:
            raise Exception("ADLManager is a singleton")

        self.context = ADL_CONTEXT_HANDLE()
        if ADL2_Main_Control_Create(ADL_Main_Memory_Alloc, 1, byref(self.context)) != ADL_OK:
            raise ADLError("ADL2_Main_Control_Create failed.")


        num_adapters = c_int(-1)
        if ADL2_Adapter_NumberOfAdapters_Get(self.context, byref(num_adapters)) != ADL_OK:
            raise ADLError("ADL2_Adapter_NumberOfAdapters_Get failed.")

        # allocate an array of AdapterInfo, see ctypes docs for more info
        AdapterInfoArray = (AdapterInfo * num_adapters.value)()

        # AdapterInfo_Get grabs info for ALL adapters in the system
        if ADL2_Adapter_AdapterInfo_Get(self.context, cast(AdapterInfoArray, LPAdapterInfo), sizeof(AdapterInfoArray)) != ADL_OK:
            raise ADLError("ADL2_Adapter_AdapterInfo_Get failed.")

        self.devices = []

        for adapter in AdapterInfoArray:
            index = adapter.iAdapterIndex
            busNum = adapter.iBusNumber
            udid = adapter.strUDID

            adapterID = c_int(-1)

            if ADL2_Adapter_ID_Get(self.context, index, byref(adapterID)) != ADL_OK:
                #raise ADLError("ADL2_Adapter_Active_Get failed.")
                continue # Skip the adapter which does not have an id (Probably not AMD/ATI card)

            found = False
            for device in self.devices:
                if (device.adapterID == adapterID.value):
                    found = True
                    break

            # save it in our list if it's the first controller of the adapter
            if (found == False):
                self.devices.append(ADLDevice(index, adapterID, busNum, udid, adapter.strAdapterName))

        if len(self.devices) == 0:
            raise ADLError("Not found any ATI/AMD card")

        ADLManager.__instance = self

    def __del__(self):
        ADL2_Main_Control_Destroy(self.context)

    def __isDeviceValid(self, device):
        return device != None and device in self.devices



    # Return the Device's current core voltage in mV
    def getCurrentCoreVoltage(self, device):
        if self.__isDeviceValid == False:
            raise ADLError("Invalid device")

        activity = ADLPMActivity()
        activity.iSize = sizeof(activity)

        if ADL2_Overdrive5_CurrentActivity_Get(self.context, device.adapterIndex, byref(activity)) != ADL_OK:
            raise ADLError("Failed to get CurrentUsage")

        return activity.iVddc

    # Return the Device's current engine frequency in MHz
    def getCurrentEngineClock(self, device):
        if self.__isDeviceValid == False:
            raise ADLError("Invalid device")

        activity = ADLPMActivity()
        activity.iSize = sizeof(activity)

        if ADL2_Overdrive5_CurrentActivity_Get(self.context, device.adapterIndex, byref(activity)) != ADL_OK:
            raise ADLError("Failed to get CurrentEngineClock")

        return activity.iEngineClock/100.0

    # Return the Device's current fan speed in a specified unit (ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE or ADL_DEVICE_FAN_SPEED_TYPE_RPMS)
    def getCurrentFanSpeed(self, device, speedType):
        if self.__isDeviceValid == False:
            raise ADLError("Invalid device")
        if speedType != ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE and speedType != ADL_DEVICE_FAN_SPEED_TYPE_RPM:
            raise ADLError("Invalid fan speed type")

        fan_speed = {}
        fan_speed_value = ADLFanSpeedValue()
        fan_speed_value.iSize = sizeof(fan_speed_value)
        fan_speed_value.iSpeedType = speedType

        if ADL2_Overdrive5_FanSpeed_Get(self.context, device.adapterIndex, 0, byref(fan_speed_value)) != ADL_OK:
            raise ADLError("Failed to get CurrentFanSpeed")

        return fan_speed_value.iFanSpeed

    # Return the Device's current memory frequency in MHz
    def getCurrentMemoryClock(self, device):
        if self.__isDeviceValid == False:
            raise ADLError("Invalid device")

        activity = ADLPMActivity()
        activity.iSize = sizeof(activity)

        if ADL2_Overdrive5_CurrentActivity_Get(self.context, device.adapterIndex, byref(activity)) != ADL_OK:
            raise ADLError("Failed to get CurrentMemoryClock")

        return activity.iMemoryClock/100.0

    # Return the Device's current temperature in Celsius
    def getCurrentTemperature(self, device):
        if self.__isDeviceValid == False:
            raise ADLError("Invalid device")

        temperature = ADLTemperature()
        temperature.iSize = sizeof(temperature)

        if ADL2_Overdrive5_Temperature_Get(self.context, device.adapterIndex, 0, byref(temperature)) != ADL_OK:
            raise ADLError("Failed to get CurrentTemperature")

        return temperature.iTemperature/1000.0

    # Return the Device's current load (%)
    def getCurrentUsage(self, device):
        if self.__isDeviceValid == False:
            raise ADLError("Invalid device")

        activity = ADLPMActivity()
        activity.iSize = sizeof(activity)

        if ADL2_Overdrive5_CurrentActivity_Get(self.context, device.adapterIndex, byref(activity)) != ADL_OK:
            raise ADLError("Failed to get CurrentUsage")

        return activity.iActivityPercent


    # Return the Device's core voltage range (Min, Max)
    def getCoreVoltageRange(self, device, reload = False):
        if self.__isDeviceValid == False:
            raise ADLError("Invalid device")

        if reload or device.coreVoltageRange == None:
            od_parameters = ADLODParameters()
            od_parameters.iSize = sizeof(od_parameters)
            if ADL2_Overdrive5_ODParameters_Get(self.context, device.adapterIndex, byref(od_parameters)) != ADL_OK:
                raise ADLError("Failed to get EngineClockRange")

            device.coreVoltageRange = (od_parameters.sVddc.iMin/100.0, od_parameters.sVddc.iMax/100.0)

        return device.coreVoltageRange

    # Return the Device's engine clock frequency range (Min, Max)
    def getEngineClockRange(self, device, reload = False):
        if self.__isDeviceValid == False:
            raise ADLError("Invalid device")

        if reload or device.engineClockRange == None:
            od_parameters = ADLODParameters()
            od_parameters.iSize = sizeof(od_parameters)
            if ADL2_Overdrive5_ODParameters_Get(self.context, device.adapterIndex, byref(od_parameters)) != ADL_OK:
                raise ADLError("Failed to get EngineClockRange")

            device.engineClockRange = (od_parameters.sEngineClock.iMin/100.0, od_parameters.sEngineClock.iMax/100.0)

        return device.engineClockRange

    def getFanSpeedRange(self, device, speedType, reload = False):
        if self.__isDeviceValid == False:
            raise ADLError("Invalid device")
        if speedType != ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE and speedType != ADL_DEVICE_FAN_SPEED_TYPE_RPM:
            raise ADLError("Invalid fan speed type")

        if reload or (device.fanSpeedPercentageRange == None and speedType == ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE) or (device.fanSpeedRPMRange == None and speedType == ADL_DEVICE_FAN_SPEED_TYPE_RPM):

            fan_speed_info = ADLFanSpeedInfo()
            fan_speed_info.iSize = sizeof(fan_speed_info)

            if ADL2_Overdrive5_FanSpeedInfo_Get(self.context, device.adapterIndex, 0, byref(fan_speed_info)) != ADL_OK:
                raise ADLError("Failed to get FanSpeedRange")

            device.fanSpeedPercentageRange = (fan_speed_info.iMinPercent, fan_speed_info.iMaxPercent)
            device.fanSpeedRPMRange = (fan_speed_info.iMinRPM, fan_speed_info.iMaxRPM)

        if speedType == ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE:
            return device.fanSpeedPercentageRange

        elif speedType == ADL_DEVICE_FAN_SPEED_TYPE_RPM:
            return device.fanSpeedRPMRange

        return None

    # Return the Device's memory clock frequency range (Min, Max)
    def getMemoryClockRange(self, device, reload = False):
        if self.__isDeviceValid == False:
            raise ADLError("Invalid device")

        if reload or device.memoryClockRange == None:
            od_parameters = ADLODParameters()
            od_parameters.iSize = sizeof(od_parameters)
            if ADL2_Overdrive5_ODParameters_Get(self.context, device.adapterIndex, byref(od_parameters)) != ADL_OK:
                raise ADLError("Failed to get EngineClockRange")

            device.memoryClockRange = (od_parameters.sMemoryClock.iMin/100.0, od_parameters.sMemoryClock.iMax/100.0)

        return device.memoryClockRange

class ADLDevice(object):

    def __init__(self, adapterIndex, adapterID, busNumber, uuid, name):
        self.adapterIndex = adapterIndex
        self.adapterID = adapterID.value
        self.adapterName = name
        self.busNumber = busNumber
        self.uuid = uuid
        self.coreVoltageRange = None
        self.engineClockRange = None
        self.memoryClockRange = None
        self.fanSpeedPercentageRange = None
        self.fanspeedRPMRange = None

    # Return the current core voltage in mV
    def getCurrentCoreVoltage(self):
        return ADLManager.getInstance().getCurrentCoreVoltage(self)

    # Return the current engine frequency in MHz
    def getCurrentEngineClock(self):
        return ADLManager.getInstance().getCurrentEngineClock(self)

    # Return the current fan speed in a specified unit (ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE or ADL_DEVICE_FAN_SPEED_TYPE_RPMS)
    def getCurrentFanSpeed(self, speedType):
        return ADLManager.getInstance().getCurrentFanSpeed(self, speedType)

    # Return the current memory frequency in MHz
    def getCurrentMemoryClock(self):
        return ADLManager.getInstance().getCurrentMemoryClock(self)

    # Return the current temperature in Celsius
    def getCurrentTemperature(self):
        return ADLManager.getInstance().getCurrentTemperature(self)

    # Return the current load (%)
    def getCurrentUsage(self):
        return ADLManager.getInstance().getCurrentUsage(self)

    # Return the core voltage range (Min, Max)
    def getCoreVoltageRange(self, reload = False):
        return ADLManager.getInstance().getCoreVoltageRange(self, reload)

    # Return the engine clock frequency range (Min, Max)
    def getEngineClockRange(self, reload = False):
        return ADLManager.getInstance().getEngineClockRange(self, reload)

    # Get the fan speed range in the specified unit (ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE or ADL_DEVICE_FAN_SPEED_TYPE_RPMS)
    def getFanSpeedRange(self, speedType, reload = False):
        return ADLManager.getInstance().getFanSpeedRange(self, speedType, reload)

    # Return the memory clock frequency range (Min, Max)
    def getMemoryClockRange(self, reload = False):
        return ADLManager.getInstance().getMemoryClockRange(self, reload)
