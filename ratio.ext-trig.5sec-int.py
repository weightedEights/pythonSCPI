# For now, this script will load a pre-generated state file (*.sta) which is stored locally on the counter
# In the future, this script will include UI elements to allow changes to measurement states

import visa
import time
import os
from datetime import datetime
from subprocess import call


def main():
    printHeader()

    logFilePath = os.getcwd()
    instrumentIP = "TCPIP0::172.20.0.125::inst0::INSTR"
    stateFile = "INT:\\RAT.EXTRIG.5sec.sta"

    inst = instConnect(instrumentIP)
    instID = inst.query('*IDN?')
    print(instID)

    instLoadState(inst, stateFile)  # read local-to-inst state file and prepare instrument to take measurement

    instDataStart(inst)    # start measurement and store data in instrument buffer

    logFile = logFileSetup(logFilePath)

    try:
        dataLogging(logFile, inst)   # automatically start logging data and writing to file, abort on user input
    except KeyboardInterrupt:
        pass

    instDisconnect(inst)    # abort measurement routine and disconnect from the instrument


def printHeader():
    print("---------------------------------")
    print("   Keysight 53220A Data Logger")
    print("   " + str(datetime.now()))
    print("---------------------------------")


def instConnect(instIP):
    rm = visa.ResourceManager()
    inst = rm.open_resource(instIP)

    return inst


def instLoadState(inst, sta):
    inst.write('*CLS')
    time.sleep(1)
    inst.write('*RST')
    time.sleep(1)
    inst.write(':MMEMory:LOAD:STATe "%s"' % sta)


def instDataStart(inst):
    inst.write(':INITiate:IMMediate')


def logFileSetup(path):

    logFilePath = os.path.join(path, "logs")
    if not os.path.exists(logFilePath):
        os.mkdir(logFilePath)

    timeStamp = time.strftime("%Y%m%d")
    ind = 1
    logFile = os.path.join(logFilePath, "counterLog.{}.{:03d}.csv".format(timeStamp, ind))

    while os.path.exists(logFile):
        ind += 1
        logFile = os.path.join(logFilePath, "counterLog.{}.{:03d}.csv".format(timeStamp, ind))

    with open(logFile, "w") as log:
        log.write("Time, CounterData\n")

    return logFile


def dataLogging(logFile, inst):
    print("Log file path: " + os.path.abspath(logFile))
    print("Logging initiated..")

    inst.write(':FORMat:DATA %s' % ('ASC'))

    while True:
        time.sleep(1)
        measurementBlock = inst.query_binary_values(':R? %d' % (1), 's', False)
        meas = str(measurementBlock)[3:-2]

        if meas != "":
            print(meas)
            with open(logFile, 'a') as log:
                log.write(str(datetime.now()) + "," + meas + "\n")


def instDisconnect(inst):
    inst.close()
    visa.ResourceManager().close()


if __name__ == '__main__':
    main()
