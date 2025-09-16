#!/usr/bin/env python3
"""
UDP video streaming server
Sends each JPEG-encoded frame split into chunks.
Header format (network byte order):
  4 bytes: frame_id (unsigned int)
  2 bytes: packet_id (unsigned short)
  1 byte : marker (0 = more packets, 1 = last packet of frame)
Total header size = 7 bytes
"""
import socket
import cv2
import numpy as np
import struct
import time
import argparse
import math
import sys

HEADER_FMT = "!IHB"   # frame_id: unsigned int, packet_id: unsigned short, marker: unsigned char
HEADER_SIZE = struct.calcsize(HEADER_FMT)
CHUNK_SIZE = 60000    # payload bytes per UDP packet (adjust for network MTU if required)

def send_video(video_path, dest_ip, dest_port, quality=80):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (dest_ip, dest_port)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video:", video_path)
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or math.isnan(fps):
        fps = 25.0
    frame_interval = 1.0 / fps

    frame_id = 0
    print(f"Streaming to {addr}, fps={fps:.2f}, chunk={CHUNK_SIZE} bytes")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("End of video or read error.")
                break

            # optional resize (uncomment if needed)
            # frame = cv2.resize(frame, (640, 360))

            # encode as JPEG
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            result, encimg = cv2.imencode('.jpg', frame, encode_param)
            if not result:
                print("Failed to encode frame", frame_id)
                continue

            data = encimg.tobytes()
            total_len = len(data)
            num_packets = math.ceil(total_len / CHUNK_SIZE)
            # send packets
            for p_id in range(num_packets):
                start = p_id * CHUNK_SIZE
                end = start + CHUNK_SIZE
                chunk = data[start:end]
                marker = 1 if p_id == (num_packets - 1) else 0
                header = struct.pack(HEADER_FMT, frame_id, p_id, marker)
                packet = header + chunk
                try:
                    sock.sendto(packet, addr)
                except Exception as e:
                    print("Send error:", e)
                # small sleep to avoid flooding (tweak if needed)
                # time.sleep(0.0005)

            frame_id = (frame_id + 1) & 0xFFFFFFFF
            time.sleep(frame_interval)
    except KeyboardInterrupt:
        print("Server stopped by user.")
    finally:
        cap.release()
        sock.close()
        print("Server exited.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Video Streaming Server")
    parser.add_argument("--video", "-v", required=True, help="Path to video file (or device index e.g. 0 for webcam)")
    parser.add_argument("--ip", default="127.0.0.1", help="Destination IP to send to (client IP). Default 127.0.0.1")
    parser.add_argument("--port", "-p", type=int, default=9999, help="Destination UDP port (default 9999)")
    parser.add_argument("--quality", type=int, default=80, help="JPEG quality (0-100). Default 80")
    args = parser.parse_args()

    # allow webcam index
    try:
        video_arg = int(args.video)
    except Exception:
        video_arg = args.video

    send_video(video_arg, args.ip, args.port, args.quality)
