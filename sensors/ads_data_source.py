#from sensors.ads_reader import ADSReader
from sensors.test_ads_reader import TestADSReader

class ADSDataSource:
    """
    Data source class that interfaces with the ADSReader to fetch voltage data.
    Provides a method to get voltage readings from specified channels.
    """
    def __init__(self):
        #self.ads_reader = ADSReader()
        self.ads_reader = TestADSReader()

    def get_readings(self):
        nitrous_voltage = self.ads_reader.read_voltage('channel_0')
        trans_in_voltage = self.ads_reader.read_voltage('channel_1')
        trans_out_voltage = self.ads_reader.read_voltage('channel_2')
        fuel_voltage = self.ads_reader.read_voltage('channel_3')

        return {
            "nitrous_psi": (nitrous_voltage, "V", "Nitrous PSI"),
            "trans_in": (trans_in_voltage, "V", "Trans In"),
            "trans_out": (trans_out_voltage, "V", "Trans Out"),
            "fuel_psi": (fuel_voltage, "V", "Fuel PSI")
        }