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
    N2O Pressure: AEM 2000 PSIG Pressure Sensor Kit - AEM PN: 30-2130-2000, Ballenger PN: SNSR-03086
       -0 psi at 0.5 volts, 2000 psi at 4.5 volts, linear between
    Fuel Pressure: Honeywell 100 PSIG Stainless Pressure Sensor - PxL - Ballenger PN: SNSR-03112
       -0 psi at 0.5 volts, 100 psi at 4.5 volts, linear between
    Trans temperature (both): GM Delphi / Packard Fluid Temperature Sensor #12160855 Kit (with connector) - Ballenger PN: SNSR-02062CK
       -non-linear - use lookup table

    Pressure volt conversion constant: (5.1Kohms + 10Kohms)/10Kohms = 1.51
    Temp uses ads 3.3V and a 10Kohm pullup resistor
    """
    #ads conversion constants
    PRESS_ADS_VOLT_CONV = 1.51
    TEMP_VREF = 3.3
    TEMP_RESISTOR = 10000

    #pressure sensor voltage conversions
    def n2o_volt_to_psi(self, volt):
        return (volt - 0.5) * 500
    def press100_volt_to_psi(self, volt):
        return (volt - 0.5) * 25
    
    #Celsius to Fahrenheit conversion
    def C_to_F_conv(self, temp_c):
        return(temp_c * 9/5 + 32)
    
    #temp sensor resistance scale
    TEMP_RESISTANCE_TABLE = [
        (-40, 402392), (-35, 288981), (-30, 209817), (-25, 153922), (-20, 114026),
        (-15, 85256), (-10, 64306), (-5, 48910), (0, 37499), (5, 28977),
        (10, 22572), (15, 17717), (20, 14007), (25, 11150), (30, 8935),
        (35, 7204), (40, 5844), (45, 4768), (50, 3911), (55, 3226),
        (60, 2676), (65, 2232), (70, 1870), (75, 1574), (80, 1331),
        (85, 1131), (90, 964.7), (95, 826.2), (100, 710.2), (105, 612.9),
        (110, 530.9), (115, 461.5), (120, 402.6), (125, 352.3), (130, 309.3),
        (135, 272.4), (140, 240.6), (145, 213.2), (150, 189.3)
    ]

    def resistance_to_temp_c(self, resistance):
        table = self.TEMP_RESISTANCE_TABLE

        #table resistance goes high -> low as temp increases
        if resistance >= table[0][1]:
            return table[0][0]

        if resistance <= table[-1][1]:
            return table[-1][0]

        for i in range(len(table) - 1):
            temp_low, resistance_high = table[i]
            temp_high, resistance_low = table[i + 1]

            if resistance_high >= resistance >= resistance_low:
                ratio = (resistance_high - resistance) / (resistance_high - resistance_low)
                return temp_low + ratio * (temp_high - temp_low)

        return table[-1][0]

    def thermistor_resistance_from_voltage(self, volt):
        #guard against divide by zero if voltage is at/above VREF
        if volt >= self.TEMP_VREF:
            return 0

        return self.TEMP_RESISTOR * (volt / (self.TEMP_VREF - volt))

    #trans temp voltage conversion
    def trans_volt_to_degrees_F(self, volt):
        resistance = self.thermistor_resistance_from_voltage(volt)
        temp_c = self.resistance_to_temp_c(resistance)
        return self.C_to_F_conv(temp_c)
      

    #gauge value display
    def get_readings(self):
        chan0_voltage = self.ads_reader.read_voltage('channel_0') * self.PRESS_ADS_VOLT_CONV
        n2o_psi = self.n2o_volt_to_psi(chan0_voltage)
        ebp_psi = self.press100_volt_to_psi(chan0_voltage)

        fuel_voltage = self.ads_reader.read_voltage('channel_1') * self.PRESS_ADS_VOLT_CONV
        fuel_psi = self.press100_volt_to_psi(fuel_voltage)

        trans_out_voltage = self.ads_reader.read_voltage('channel_2')
        trans_out_F = self.trans_volt_to_degrees_F(trans_out_voltage)

        trans_in_voltage = self.ads_reader.read_voltage('channel_3')
        trans_in_F = self.trans_volt_to_degrees_F(trans_in_voltage)

        return {
            "n2o_psi": (n2o_psi, "PSI", "N2O PSI"),
            "ebp_psi": (ebp_psi, "PSI", "EBP PSI"),
            "fuel_psi": (fuel_psi, "PSI", "Fuel PSI"),
            "trans_out": (trans_out_F, "F", "Trans (Converter) Out"),
            "trans_in": (trans_in_F, "F", "Trans (Cooler Rtn) In")            
        }