#!/usr/bin/env python3
"""
UDP video streaming client
Receives packets, reassembles frames, decodes JPEG and displays with OpenCV.
Header format (same as server):
  4 bytes: frame_id (unsigned int)
  2 bytes: packet_id (unsigned short)
  1 byte : marker (0/1)
"""
import socket
import struct
import numpy as np
import cv2
import argparse
import time

HEADER_FMT = "!IHB"
HEADER_SIZE = struct.calcsize(HEADER_FMT)
RECV_BUF = 65536  # buffer size for recvfrom

def run_client(listen_ip, listen_port, timeout=3.0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_ip, listen_port))
    sock.settimeout(1.0)
    print(f"Listening on {(listen_ip, listen_port)}")

    frames = {}  # frame_id -> { 'parts': dict(p_id->bytes), 'last_received': time, 'expected_last_packet': None }
    last_displayed = -1
    try:
        while True:
            try:
                packet, addr = sock.recvfrom(RECV_BUF)
            except socket.timeout:
                # cleanup old frames that timed out
                now = time.time()
                stale = [fid for fid, info in frames.items() if now - info['last_received'] > timeout]
                for fid in stale:
                    del frames[fid]
                continue

            if len(packet) < HEADER_SIZE:
                continue
            header = packet[:HEADER_SIZE]
            payload = packet[HEADER_SIZE:]
            frame_id, packet_id, marker = struct.unpack(HEADER_FMT, header)

            info = frames.get(frame_id)
            if info is None:
                info = {'parts': {}, 'last_received': time.time(), 'expected_last_packet': None}
                frames[frame_id] = info

            info['parts'][packet_id] = payload
            info['last_received'] = time.time()
            if marker == 1:
                info['expected_last_packet'] = packet_id

            # if we know last packet id, and we have all packets from 0..last -> assemble
            exp = info.get('expected_last_packet')
            if exp is not None:
                # check if we have all parts 0..exp
                have_all = all((i in info['parts']) for i in range(exp+1))
                if have_all:
                    # assemble
                    data_bytes = b''.join(info['parts'][i] for i in range(exp+1))
                    arr = np.frombuffer(data_bytes, dtype=np.uint8)
                    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                    if frame is not None:
                        cv2.imshow("UDP Video (press q to quit)", frame)
                        last_displayed = frame_id
                        key = cv2.waitKey(1) & 0xFF
                        if key == ord('q'):
                            break
                    else:
                        # decode error
                        print(f"Decode failed for frame {frame_id} (size {len(data_bytes)})")
                    # remove from dict to free memory
                    del frames[frame_id]

    except KeyboardInterrupt:
        print("Client stopped by user.")
    finally:
        sock.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Video Streaming Client")
    parser.add_argument("--ip", default="0.0.0.0", help="IP to bind to (default 0.0.0.0)")
    parser.add_argument("--port", "-p", type=int, default=9999, help="Listening UDP port (default 9999)")
    parser.add_argument("--timeout", type=float, default=3.0, help="Frame assembly timeout (seconds)")
    args = parser.parse_args()
    run_client(args.ip, args.port, args.timeout)
