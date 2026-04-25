import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class ADSReader:
    """
    Class responsible for hardware and channels.
    Initializes the ADS1115 and sets up the channels for reading voltage inputs.
    """
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(i2c)

        self.channels = {
            'channel_0': AnalogIn(self.ads, ADS.P0),
            'channel_1': AnalogIn(self.ads, ADS.P1),
            'channel_2': AnalogIn(self.ads, ADS.P2),
            'channel_3': AnalogIn(self.ads, ADS.P3),
        }

    def read_voltage(self, channel_name):
        if channel_name not in self.channels:
            raise ValueError(f"Invalid channel name: {channel_name}")
        
        return self.channels[channel_name].voltage
        