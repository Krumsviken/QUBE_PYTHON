from PID import PID
from Observer import Observer


class Packet:
    def __init__(self):
        self.Observer = Observer()
        self.pid = PID()
        self.plot_data = [[] * 6]
        self.resetEncoders = False

    def unpack(self):
        return [
            self.pid,
            self.resetEncoders,
        ]
