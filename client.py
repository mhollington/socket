from socket import *
import os
import pathlib
import sys
import argparse
import platform

arguments = sys.argv[1:]

#check that the number of args given is correct
if len(arguments) != 2:
    sys.exit("incorrect number of arguments give, please give 2 arguments")


# store the given file name in a variable
serverName = arguments[0]
fileName = arguments[1]



if len(fileName) <= 4:
    sys.exit("file name too short")

extension = fileName[len(fileName) - 4:]

if extension != ".txt":
    msg = fileName + " is not a text file, please provide a text file"
    sys.exit(msg)

# find out which os this file is running on
operatingSys = platform.system()

# the folder that contains the input file
file_root = "output_file/"

# find the path to the input file depending on which os the program is running on
if operatingSys == 'Windows':
    output_file = pathlib.WindowsPath(file_root+fileName)

else:
    output_file = pathlib.Path(file_root+fileName)

isExists = os.path.exists(output_file)
if (not isExists):
    msg = fileName + " does not exist in the output_file folder"
    sys.exit(msg)


hostname = gethostname()
if serverName != hostname:
    msg = "wrong server name given, the correct server name is " + hostname
    sys.exit(msg)

# find the ip address of the host
ip = gethostbyname(hostname)

try:
    serverPort = 9778
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((ip, serverPort))
except ConnectionRefusedError:
    msg = "no server to connect with at port " + str(serverPort)
    sys.exit(msg)


file_content = b""
done = False
# open the output_file
try:
    fb = open(output_file, 'wb')
except:
    clientSocket.close()
    sys.exit("The output file could not be opened")

# receive the file that should be copied to the output_file and store it in file_content
try:
    while not done:
        data = clientSocket.recv(200)
        if file_content[-5:] == b"<end>":
            done = True
        else:
            file_content += data
except:
    fb.close()
    clientSocket.close()
    sys.exit("something went wrong when the client was recieving the data")

file_content = file_content[:len(file_content) - 5]
print("the file has been received")

# write the contents of the received file to the out_put file
try:
    fb.write(file_content)
except:
    fb.close()
    clientSocket.close()
    sys.exit("The copied file contents could not be written to the output file")

fb.close()
clientSocket.close()