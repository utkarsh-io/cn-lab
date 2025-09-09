import socket

name = "XYZ"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('10.xx.x.xxx', 9999))
server_socket.listen()

print("Server is listening on port 9999")

while True:
    conn, addr = server_socket.accept()
    print(f"\nConnected by {addr}")

    connfile = conn.makefile('r', encoding='utf-8')
    cname = connfile.readline().strip()
    line = connfile.readline().strip()
    try:
        cval = int(line)
    except:
        cval = -1

    if not (1 <= cval <= 100):
        print("Invalid number received. Closing server.")
        connfile.close()
        conn.close()
        server_socket.close()
        break

    val = 0
    while True:
        num = int(input("Enter Number between 1 and 100: "))
        val = num
        if 1 <= num <= 100:
            break

    print(f"Client Name: {cname}")
    print(f"Server Name: {name}")
    print(f"Client Number: {cval}")
    print(f"Server Number: {val}")
    print(f"Sum: {cval + val}")

    conn.sendall((name + "\n").encode())
    conn.sendall((str(val) + "\n").encode())

    connfile.close()
    conn.close()
