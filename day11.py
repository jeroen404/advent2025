#!/usr/bin/env python3

from functools import cache

class Device:
    def __init__(self, name: str, connections: list[str]):
        self.name = name
        self.connections = connections
    def __repr__(self) -> str:
        return f"Device(name={self.name}, connections={self.connections})"
    def iterate_connections(self):
        for conn in self.connections:
            yield conn
    @staticmethod
    def from_string(s: str):
        parts = s.strip().split(':')
        name = parts[0].strip()
        connections_part = parts[1].strip()
        connections = [conn.strip() for conn in connections_part.split(' ') if conn.strip()]
        return Device(name, connections)
        

devices: dict[str, Device] = {}

try:
    while True:
        line = input()
        device = Device.from_string(line)
        devices[device.name] = device
except EOFError:
    pass

@cache
def nb_paths_to(start_device_name: str, stop_device_name: str) -> int:
    global devices
    if start_device_name == stop_device_name:
        return 1
    total_paths = 0
    for conn in devices[start_device_name].connections:
        total_paths += nb_paths_to(conn, stop_device_name)
    return total_paths

start_device_name = "you"
stop_device_name = "out"
print(f"Total distinct paths from {start_device_name} to {stop_device_name}: {nb_paths_to(start_device_name, stop_device_name)}")

# Total distinct paths from dac to fft: 0

out_device = Device("out", [])
devices["out"] = out_device

svr_to_fft = nb_paths_to("svr", "fft")
fft_to_dac = nb_paths_to("fft", "dac")
dac_to_out = nb_paths_to("dac", "out")

total_svr_to_out_via_fft_dac = svr_to_fft * fft_to_dac * dac_to_out
print(f"Total distinct paths from svr to out via fft and dac: {total_svr_to_out_via_fft_dac}")

