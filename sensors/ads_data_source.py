from sensors.ads_reader import ADSReader

class ADSDataSource:
    """
    Data source class that interfaces with the ADSReader to fetch voltage data.
    Provides a method to get voltage readings from specified channels.
    """
    def __init__(self):
        self.ads_reader = ADSReader()

    def get_readings(self):
        nitrous_voltage = self.ads_reader.read_voltages('channel_0')

        return {
            "nitrous_psi": (nitrous_voltage, "V", "Nitrous PSI")
        }