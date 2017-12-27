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

from __future__ import print_function
import os, sys
from optparse import OptionParser
from pyadl import *

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

            devices = ADLManager.getInstance().getDevices()
            for device in devices:
                print("{0}. {1}".format(device.adapterIndex, device.adapterName))

        elif options.action == "status":

            devices = ADLManager.getInstance().getDevices()
            for device in devices:
                print("{0}. {1}".format(device.adapterIndex, device.adapterName))

                coreVoltageMin, coreVoltageMax = device.getCoreVoltageRange()
                print ("\tEngine core voltage: {0} mV ({1} mV - {2} mV)".format(device.getCurrentCoreVoltage(), coreVoltageMin, coreVoltageMax))

                coreFrequencyMin, coreFrequencyMax = device.getEngineClockRange()
                print ("\tEngine clock: {0} MHz ({1} MHz - {2} MHz)".format(device.getCurrentEngineClock(), coreFrequencyMin, coreFrequencyMax))

                memoryFrequencyMin, memoryFrequencyMax = device.getMemoryClockRange()
                print ("\tMemory clock: {0} MHz ({1} MHz - {2} MHz)".format(device.getCurrentMemoryClock(), memoryFrequencyMin, memoryFrequencyMax))

                fanSpeedPercentageMin, fanSpeedPercentageMax = device.getFanSpeedRange(ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE)
                print ("\tFan speed: {0} % ({1} % - {2} %)".format(device.getCurrentFanSpeed(ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE), fanSpeedPercentageMin, fanSpeedPercentageMax))

                fanSpeedRPMMin, fanSpeedRPMMax = device.fanSpeedRPMRange     #can use this, because device.getFanSpeedRange grab % and RPM in the same time
                                                                            #or also can use device.getFanSpeedRange(ADL_DEVICE_FAN_SPEED_TYPE_RPM)
                print ("\tFan speed: {0} RPM ({1} RPM - {2} RPM)".format(device.getCurrentFanSpeed(ADL_DEVICE_FAN_SPEED_TYPE_RPM), fanSpeedRPMMin, fanSpeedRPMMax))

                print ("\tTemperature: {0} Celsius".format(device.getCurrentTemperature()))
                print ("\tUsage: {0} %".format(device.getCurrentUsage()))
        else:
            parser.print_help()

    except ADLError as err:
        result = 1
        print(err)

    sys.exit(result)
