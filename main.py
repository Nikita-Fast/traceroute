import socket
import sys


def traceroute(dst):
    try:
        dst_name, _, dst_ip = socket.gethostbyaddr(dst)
    except socket.error:
        print("Host not found")
        exit(1)

    print("Traceroute to %s %s" % (dst_name, str(dst_ip)))
    for i in range(25):
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_udp.setsockopt(socket.SOL_IP, socket.IP_TTL, i + 1)

        socket_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        socket_icmp.settimeout(5)

        socket_udp.sendto(bytes("message", "utf-8"), (dst, 33534))
        name = ""

        try:
            address = socket_icmp.recvfrom(512)[1][0]

            try:
                name = socket.gethostbyaddr(address)[0]
            except socket.error:
                name = address

        except socket.error:
            address = None

        if address:
            print("%i %s %s" % (i + 1, name, address))
            if dst_ip[0] == address or name == dst_name:
                break
        else:
            print("%i *" % (i + 1))

        socket_udp.close()
        socket_icmp.close()


if __name__ == '__main__':
    traceroute(sys.argv[1])
    
