import logging
import os
import socket
import sys
import traceback

import time


class IOSocket:
    """
     * Socket for communication
    """

    def __init__(self, port):
        self.BUFF_SIZE = 8192
        self.END = '\n'
        self.TOKEN_SEP = '#'
        self.port = port
        self.hostname = "127.0.0.1"
        self.logfilename = "./logs/clientLog.txt"
        self.connected = False
        self.socket = None
        self.logfile = open(self.logfilename, "a")

    def initBuffers(self):
        while not self.connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print ("Selected host is: " + str(self.hostname))
                print ("Selected port is: " + str(self.port))
                self.socket.connect((self.hostname, self.port))
                self.connected = True
                print ("Client connected to server [OK]")
            except Exception as e:
                logging.exception(e)
                print("Client connected to server [FAILED]")
                traceback.print_exc()
                sys.exit()

    def writeToFile(self, line):
        sys.stdout.write(line + os.linesep)
        self.logfile.write(line + os.linesep)
        sys.stdout.flush()
        self.logfile.flush()

    def writeToServer(self, messageId, line, log):
        msg = str(messageId) + self.TOKEN_SEP + line + "\n"
        try:
            self.socket.send(bytes(msg))
            if log:
                self.writeToFile(msg.strip('\n'))
        except Exception as e:
            logging.exception(e)
            print ("Write " + self.logfilename + " to server [FAILED]")
            traceback.print_exc()
            sys.exit()

    def readLine(self):
        try:
            # return self.socket.recv(1024000)
            totest = self.recv_end()
            return totest
        except Exception as e:
            logging.exception(e)
            print ("Read from server [FAILED]")
            traceback.print_exc()
            sys.exit()

    def recv_end(self):
        total_data = []
        data = ''
        while True:
            data = self.socket.recv(8192)
            if self.END in data:
                total_data.append(data[:data.find(self.END)])
                break
            total_data.append(data)
            if len(total_data) > 1:
                last_pair = total_data[-2] + total_data[-1]
                if self.END in last_pair:
                    total_data[-2] = last_pair[:last_pair.find(self.END)]
                    total_data.pop()
                    break
        return ''.join(total_data)