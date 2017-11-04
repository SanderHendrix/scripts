#!/usr/bin/env python3

def encrypt(msg, key):
    return "".join([chr(ord(x)^ord(y)) for x, y in zip(msg, key)])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="One-time pad")
    parser.add_argument("message", 
            help="Message to encrypt")
    parser.add_argument("key", 
            help="Key for encryption")
    args = parser.parse_args()

    if len(args.message) != len(args.key):
        raise ValueError("Key and message length do not match!")
    print(encrypt(args.message, args.key))
