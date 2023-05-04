from socket import *
import argparse
import os
import pathlib
import sys
import platform

# get the arguments
arguments = sys.argv[1:]


#check that the number of args given is correct
if len(arguments) != 1:
    sys.exit("incorrect number of arguments, please give 1 argument.")


# store the given file name in a variable
fileName = arguments[0]

if len(fileName) <= 4:
    sys.exit("file name too short.")

extension = fileName[len(fileName) - 4:]

# verify that the file is a text file
if extension != ".txt":
    msg = fileName + " is not a text file, please provide a text file."
    sys.exit(msg)

# find out which os this file is running on
operatingSys = platform.system()

# the folder that contains the input file
file_root = "input_file/"

# find the path to the input file depending on which os the program is running on
if operatingSys == 'Windows':
    input_file = pathlib.WindowsPath(file_root+fileName)

else:
    input_file = pathlib.Path(file_root+fileName)

# check that the file exists
isExists = os.path.exists(input_file)
if (not isExists):
    msg = fileName + " does not exist in the input_file folder. Please provide a file that exists in the input_file folder."
    sys.exit(msg)


f = open(input_file, 'r')
data = f.read()
print(len(data))
size = os.stat(input_file)
print(size.st_size)
# Check that the size of the file is less than 80 bytes
# To check the number of characters in the file directly
# use len(data.decode()) > 80 where data is the encoded contents of the file
if size.st_size > 80:
    msg = fileName + " is too long. Please choose a file that has at most 80 characters."
    sys.exit(msg)


# open the input file
f = open(input_file, 'rb')
data = f.read()


hostname = gethostname()
host = gethostbyname(hostname)
serverPort = 9778
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, serverPort))
serverSocket.listen(4)
print("the server is ready to receive")

while True:
    try:
        connectionSocket, addr = serverSocket.accept()
    except:
        sys.exit("Something went wrong when trying to connect to a client")
    try:
        print("connected to ", addr)
        connectionSocket.sendall(data)
        connectionSocket.send(b"<end>")
        f.close()
        connectionSocket.close()
    except:
        f.close()
        connectionSocket.close()
        sys.exit("something went wrong when trying to send the data to a client")
