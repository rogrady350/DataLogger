#simulated test data. changes over time.

import time, math

#returns a dict of sensor_id: value, unit, label
class TestDataSource:

    #attach current time as new when new TestDataSource is created
    def __init__(self):
        self.start_time = time.time()

    #return a dict of sensor_id: (value, unit, label)
    def get_readings(self):
        t = time.time() - self.start_time

        oil_temp  = 200 + 10 * math.sin(t * 0.2)
        trans_pan = 180 + 15 * math.sin(t * 0.15 + 1.0)
        trans_out = 210 + 20 * math.sin(t * 0.12 + 2.0)
        fuel_psi  = 55 + 5 * math.sin(t * 0.25 + 0.5)

        return {
            "oil_temp":  (oil_temp, "°F", "Oil Temp"),
            "trans_post": (trans_pan, "°F", "Trans Post"),
            "trans_out": (trans_out, "°F", "Trans Out"),
            "fuel_psi":  (fuel_psi, "PSI", "Fuel PSI")
        }
    