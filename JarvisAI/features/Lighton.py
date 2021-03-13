from pyfirmata import Arduino, util

port = Arduino("COM4")

port.digital[7].write(1)