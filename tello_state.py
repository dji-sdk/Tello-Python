import socket
from time import sleep
import curses

INTERVAL = 0.2



def report(str):
    stdscr.addstr(0, 0, str)
    stdscr.refresh()

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    local_ip = ''
    local_port = 8890
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
    socket.bind((local_ip, local_port))

    tello_ip = '192.168.10.1'
    tello_port = 8889
    tello_adderss = (tello_ip, tello_port)

    socket.sendto('command'.encode('utf-8'), tello_adderss)

    try:
        index = 0
        while True:
            index += 1
            response, ip = socket.recvfrom(1024)
            if response == 'ok':
                continue
            out = response.replace(';', ';\n')
            out = 'Tello State:\n' + out
            report(out)
            sleep(INTERVAL)
    except KeyboardInterrupt:
        curses.echo()
        curses.nocbreak()
        curses.endwin()


