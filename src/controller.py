from pyardmods import *

print()
print()

rightMotorPin = 10
leftMotorPin = 11
HIGH = 255
LOW = 0

waitForArduino()

testSleepTime = 1
test = False
if test:
    testData = []
    testData.append(f"<{rightMotorPin},{HIGH},1>")
    testData.append(f"<{rightMotorPin},{LOW},1>")
    testData.append(f"<{leftMotorPin},{HIGH},1>")
    testData.append(f"<{leftMotorPin},{LOW},1>")
    runTest(testData)

if not test:
    print("Send data with formated with: ")
    print("<pin>,<0-255 (power)>")
    print("'exit' to quit program")
    while True:
        message = input("> ")
        if message == "exit": break
        else: 
            try:    
                sendToArduino("<" + message + ",0>")
            except:
                print("Error!")
                pass


ser.close

