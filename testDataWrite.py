# This script has the sole purpose to read messages form the instrument and write, ONLY after connection has already
#been established. Will not disconnect.

from datetime import datetime
import time
import visa
import os

timeStamp = time.strftime("%Y%m%d")
ind = 1
logFile = "counterLog.{}.{:03d}.csv".format(timeStamp,ind)

while os.path.exists(logFile):
    ind += 1
    logFile = "counterLog.{}.{:03d}.csv".format(timeStamp, ind)

with open(logFile, "w") as log:
    log.write("Time, CounterData\n")


instIP = "TCPIP0::172.20.0.125::inst0::INSTR"
inst = visa.ResourceManager().open_resource(instIP)
inst.write(':FORMat:DATA %s' % ('ASC'))

print("Log file path: " + os.path.abspath(logFile))
print("Counter measurements are currently being logged.")

while True:
    try:
        time.sleep(1)
        measurementBlock = inst.query_binary_values(':R? %d' % (1), 's', False)
        meas = str(measurementBlock)[2:-2]

        if meas != "":
            print(meas)
            with open(logFile, 'a') as log:
                log.write(str(datetime.now()) + "," + meas + "\n")

    except KeyboardInterrupt:
        break

