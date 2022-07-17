import socket


class UdpClient:
    hostip: str
    group: str
    port: int
    # hop restriction
    ttl = 2

    on_backend_send_connection_data = None

    backend_ip: str = None

    def __init__(self, hostip, group, port, ttl=2):
        self.hostip = hostip
        self.group = group
        self.port = port
        self.ttl = ttl

    def find_backend(self):
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
        allips = [ip[-1][0] for ip in interfaces]

        msg = str(self.port+1).encode()
        print(f'sending on {self.hostip}')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((self.hostip, 0))
        sock.sendto(msg, ("255.255.255.255", self.port))
        sock.close()

    def wait_for_backend_answer(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("0.0.0.0", self.port + 1))
        while True:
            print("waiting to receive message")
            data, address = sock.recvfrom(1024)
            print(f'received {len(data)} bytes from {address}')
            print(data)
            backend_ip = data.decode()
            self.on_backend_send_connection_data(backend_ip)
            break

    def wait_for_backend_requests(self, backend_ip: str = None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("0.0.0.0", self.port))

        while True:
            print("waiting to receive message")
            data, address = sock.recvfrom(1024)

            print(f'received {len(data)} bytes from {address}')
            print(data)

            send_to_port = int(data.decode())

            print('sending acknowledgement to', address)
            print('sending acknowledgement to', address[0])
            if backend_ip is None:
                sock.sendto(self.hostip.encode(), (address[0],send_to_port))
            else:
                sock.sendto(backend_ip.encode(), (address[0],send_to_port))

