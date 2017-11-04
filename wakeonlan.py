#!/usr/bin/env python3

import socket
import struct

def send_udp_packet(*macs, ip_addr="255.255.255.255", port=9):
    """
    Wake up devices with given MAC addresses.
    Wake on lan must be enabled on the host device(s).
    
    Arguments:
    *macs    -- One or more macaddresses of machines to wake.
    
    Keyword arguments:
    ip_addr  -- the ip address of the host to send the magic packet
                to, defaults to the broadcast address: 255.255.255.255
    port     -- the port to send the magic packet to, defaults to 9 (old 
                discard port, 7 is a popular alternative but is used by the 
                old echo protocol resulting in potentially more noise)
    """
    packets = []
    for mac in macs:
        packets.append(magic_packet(mac_from_string(mac)))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect((ip_addr, port))
    for packet in packets:
        sock.send(packet)
        print(packet)
    sock.close()


def mac_from_string(mac_address, seperator=""):
    if seperator:
        mac_address = mac_address.split(seperator)
    else:
        possible_seperators = set([":", ".", " ", "-"])
        for seperator in possible_seperators:
            if seperator in mac_address:
                mac_address = [int(x, 16) for x in mac_address.split(seperator)]
                break
        else:
            raise ValueError("Incorrect MAC address format: could not locate seperator")
    
    if len(mac_address) == 6:
        for byte in mac_address:
            if byte > 0xff:
                raise ValueError("Incorrect MAC address format: value not between 0 and ff")
        else:
            return mac_address


def magic_packet(mac_address):
    """
    Make a magic packet.
    The magic packet is a broadcast frame containing anywhere within its 
    payload 6 bytes of all ones (255 in decimal or 0xff in hexadecimal), 
    followed by sixteen repetitions of the target computer's 48-bit MAC 
    address, for a total of 102 bytes.

    Arguments:
    mac_address -- list of six numbers
    """
    return struct.pack('B'*102,
            *[0xff]*6, 
            #*[int(byte, 16) for byte in mac_address]*16)
            *mac_address*16)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Wake on LAN')
    parser.add_argument(
        "macs",
        metavar="MAC address(es)",
        nargs="+",
        help="MAC address of one or more devices you are trying to wake.")
    parser.add_argument(
        "--ip",
        help="Use if you wish to send to another IP address than the broadcast address.")
    parser.add_argument(
        "-p", "--port",
        help='Port number to send WOL-packet to')
    args = parser.parse_args()
    send_udp_packet(*args.macs)
