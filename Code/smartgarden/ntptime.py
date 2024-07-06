import socket
import struct
import utime

NTP_DELTA = 3155673600
host = "pool.ntp.org"


def get_ntp_time():
    try:
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1b
        addr = socket.getaddrinfo(host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
        s.close()
        val = struct.unpack("!I", msg[40:44])[0]
        print("NTP time fetched successfully:", val - NTP_DELTA)
        return val - NTP_DELTA
    except Exception as e:
        print("Failed to get NTP time:", e)
        return None

def settime():
    t = get_ntp_time() + 7200  # Add 2 hours (7200 seconds)
    tm = utime.localtime(t)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)
    print("Current time set to:", utime.localtime())


