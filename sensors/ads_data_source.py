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

    #==Sensor Voltage Helpers==
    """
    Sensors:
    N20 Pressure: AEM 2000 PSIG Pressure Sensor Kit - AEM PN: 30-2130-2000, Ballenger PN: SNSR-03086
       -0 psi at 0.5 volts, 2000 psi at 4.5 volts, linear between
    Fuel Pressure: Honeywell 100 PSIG Stainless Pressure Sensor - PxL - Ballenger PN: SNSR-03112
       -0 psi at 0.5 volts, 100 psi at 4.5 volts, linear between
    Trans temperature (both): GM Delphi / Packard Fluid Temperature Sensor #12160855 Kit (with connector) - Ballenger PN: SNSR-02062CK
       -non-linear - use lookup table

    Pressure volt conversion constant:
    Temp volt conversion constant
    """
    #ads conversion constants
    PRESS_ADS_VOLT_CONV = 
    TEMP_ADS_VOLT_CONV =

    #pressure sensor voltage conversions
    def n20_volt_to_psi(self, volt):
        return (volt - 0.5) * 500
    def fuel_volt_to_psi(self, volt):
        return (volt - 0.5) * 25
    
    #temp sensor resistance scale
    TEMP_RESISTANCE_TABLE = [
        (-40, 402392), 
        (-35, 288981),
        (-30, 209817),
        (-25, 153922),
        (-20, 114026),
        (-15, 85256),
        (-10, 64306),
        (-5, 48910),
        (0, 37499),
        (5, 28977),
        (10, 22572),
        (15, 17717),
        (20, 14007),
        (25, 11150),
        (30, 8935),
        (35, 7204),
        (40, 5844),
        (45, 4768),
        (50, 3911),
        (55, 3226),
        (60, 2676),
        (65, 2232),
        (70, 1870),
        (75, 1574),
        (80, 1331),
        (85, 1131),
        (90, 964.7),
        (95, 826.2),
        (100, 710.2),
        (105, 612.9),
        (110, 530.9),
        (115, 461.5),
        (120, 402.6),
        (125, 352.3),
        (130, 309.3),
        (135, 272.4),
        (140, 240.6),
        (145, 213.2),
        (150, 189.3),
    ]

    #Celsius to Fahrenheit conversion
    def C_to_F_conv(temp_c):
        return(temp_c * 9/5 + 32)

    #trans temp voltage conversion
    def trans_volt_to_psi(self, volt):
        return ()

    #gauge value display
    def get_readings(self):
        n20_voltage = self.ads_reader.read_voltage('channel_0') * self.PRESS_ADS_VOLT_CONV
        n20_psi = self.n20_volt_to_psi(n20_voltage)

        fuel_voltage = self.ads_reader.read_voltage('channel_1') * self.PRESS_ADS_VOLT_CONV
        fuel_psi = self.fuel_volt_to_psi(fuel_voltage)

        trans_out_voltage = self.ads_reader.read_voltage('channel_2') * self.TEMP_ADS_VOLT_CONV
        trans_out_C = self.trans_volt_to_psi(trans_out_voltage)
        trans_out_F = self.C_to_F_conv(trans_out_C)

        trans_in_voltage = self.ads_reader.read_voltage('channel_3') * self.TEMP_ADS_VOLT_CONV
        trans_in_C = self.trans_volt_to_psi(trans_in_voltage)
        trans_in_F = self.C_to_F_conv(trans_in_C)


        return {
            "n20_psi": (n20_psi, "PSI", "N20 PSI"),
            "fuel_psi": (fuel_psi, "V", "Fuel PSI"),
            "trans_out": (trans_out_F, "V", "Trans (Converter) Out"),
            "trans_in": (trans_in_fahrenheit, "V", "Trans (Cooler Return) In")            
        }