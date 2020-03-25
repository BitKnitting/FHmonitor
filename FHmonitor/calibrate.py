from FHmonitor.atm90_e32_pi import ATM90e32
from FHmonitor.error_handling import handle_exception
import json
import logging
logger = logging.getLogger(__name__)


class Calibrate:

    def __init__(self):
        self.lineFreq, self.PGAGain, self.VoltageGain, self.CurrentGainCT1,
        self.CurrentGainCT2 = self._get_stored_calibration_values(self)

        self.lineFreq = 4485  # 4485 for 60 Hz (North America)
        self.PGAGain = 21     # 21 for 100A (2x), 42 for >100A (4x)
        self.VoltageGain = 36650
        self.CurrentGainCT1 = 25368
        self.CurrentGainCT2 = 25358

    # -----------------------------------------------------------
    def get_voltage_calibration_values(self):
        voltage_kill_a_watt = self._get_kill_a_watt_input()
        logger.info(f'Kill-A-watt voltage reading:    {voltage_kill_a_watt}V')
        energy_sensor = ATM90e32(self.lineFreq, self.PGAGain, self.VoltageGain,
                                 self.CurrentGainCT1, 0, self.CurrentGainCT2)
        voltage_reading = energy_sensor.line_voltageA
        logger.info(f'Energy monitor voltage reading: {voltage_reading}V')

    def _get_stored_calibration_values(self):
        try:
            with open("calibration.json") as json_file:
                json_data = json.load(json_file)
                lineFreq = json_data['lineFreq']
                print(f'line frequency: {lineFreq}')

        except OSError as e:
            handle_exception(e)

    def _get_kill_a_watt_input(self):

        # Input Kill-A-Watt reading for reference value.
        while True:
            try:
                voltage_kill_a_watt = float(
                    input("Enter Kill-A-Watt Voltage reading: "))
            except ValueError:
                print('Sorry, I didn\'t undestand that.  Please try again.')
                continue
            else:
                break

        return voltage_kill_a_watt
