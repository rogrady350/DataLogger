import time
import math

#test simulation to for ads_reader
class TestADSReader:
    """
    SIMULATION for testing.
    
    Class responsible for hardware and channels.
    Initializes the ADS1115 and sets up the channels for reading voltage inputs.
    """
    def __init__(self):
        self.start_time = time.time()

    def read_voltage(self, channel_name):
        t = time.time() - self.start_time

        values = {
            "channel_0": 1.5 + 0.5 * math.sin(t * 0.5),
            "channel_1": 2.0 + 0.3 * math.sin(t * 0.4 + 1.0),
            "channel_2": 1.0 + 0.2 * math.sin(t * 0.7 + 2.0),
            "channel_3": 2.5 + 0.4 * math.sin(t * 0.3 + 0.5),
        }

        if channel_name not in values:
            raise ValueError(f"Invalid channel: {channel_name}")

        return values[channel_name]