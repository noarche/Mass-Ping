import subprocess
import platform
import threading
from queue import Queue

# Check if the IP is responsive to ping
def is_host_responsive(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    
    response = subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return response == 0

# The worker function to be executed by threads
def worker():
    while True:
        ip = queue.get()
        
        if is_host_responsive(ip):
            with lock:
                with open("output.txt", "a") as out_file:
                    out_file.write(ip + "\n")
                    print(f"{ip} is responsive, saved to output.txt")

        queue.task_done()

# Load IP addresses from input.txt
with open("input.txt", "r") as file:
    ip_addresses = [line.strip() for line in file.readlines()]

queue = Queue()
lock = threading.Lock()

# Spawn 5 worker threads
for _ in range(5):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

# Feed IP addresses to the queue
for ip in ip_addresses:
    queue.put(ip)

queue.join()
