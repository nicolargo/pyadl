PyADL
=====

A simple Python Wrapper for the AMD/ATI ADL lib.

It will be used in Glances to monitor GPU performance.

For testing:
python test.py
Options:
  -h, --help           show this help message and exit
  -l, --list-adapters  Lists all detected and supported display adapters.
  -s, --status         Shows current clock speeds, core voltage, utilization
                       and performance level.
					   
					   
Example outputs:
	python test.py -s
	
	0. AMD Radeon (TM) R9 380 Series
			engine clock 978.63MHz, memory clock 1400MHz, core voltage -3.22637e+08VDC, performance level 0, utilization 100%
			fan speed 65% (2950 RPM) (default)
			temperature 77 C
			powertune 0%
			