import serial # pyserial
import time

def sendToArduino(sendStr):
    ser.write(sendStr.encode('utf-8')) # change for Python3


def recvFromArduino():
    global startMarker, endMarker
    
    ck = ""
    x = "z" # any value that is not an end- or startMarker
    byteCount = -1 # to allow for the fact that the last increment will be one too many
    
    # wait for the start character
    while  ord(x) != startMarker: 
        x = ser.read()
    
    # save data until the end marker is found
    while ord(x) != endMarker:
        if ord(x) != startMarker:
            ck = ck + x.decode("utf-8") # change for Python3
            byteCount += 1
        x = ser.read()
    
    return(ck)


def waitForArduino():

    # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded
    
    global startMarker, endMarker
    
    msg = ""
    while msg.find("Arduino is ready") == -1:

        while ser.inWaiting() == 0:
            pass
        
        msg = recvFromArduino()

        print(msg)
        print()
        

def runTest(testData, testSleepTime = 1):
    numLoops = len(testData)
    waitingForReply = False

    n = 0
    while n < numLoops:
        teststr = testData[n]

        if waitingForReply == False:
            sendToArduino(teststr)
            print ("Sent from PC -- LOOP NUM " + str(n) + " TEST STR " + teststr)
            waitingForReply = True

        if waitingForReply == True:

            while ser.inWaiting() == 0:
                pass
            
            dataRecvd = recvFromArduino()
            print ("Reply Received  " + dataRecvd)
            n += 1
            waitingForReply = False

            print ("===========")

        time.sleep(testSleepTime)

startMarker = 60
endMarker = 62

ports = ["COM3","COM4"]
baudRate = 9600
for serPort in ports:
    try:
        ser = serial.Serial(serPort, baudRate)
    except:
        pass
print("Serial port " + serPort + " opened  Baudrate " + str(baudRate))