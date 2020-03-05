#!/home/pi/projects/FitHome_monitor/venv/bin/python3

#####################################################
# Read active and reactive power from the atm90e32 then
# store within mongodb.
#
# copyright Margaret Johnson, 2020.
# Please credit when evolving your code with this code.
########################################################


from FHmonitor.error_handling import handle_exception
from FHmonitor.atm90_e32_pi import ATM90e32
from FHmonitor.store import MongoDB
import logging
logger = logging.getLogger(__name__)


class Monitor:

    def __init__(self):
        self.db = None
        self.energy_sensor = None
    ####################################################
    # Initialize the energy sensor.  The properties are
    # are written to atm90e32 registers during initialization.
    # They are specific to the Power and Current Transformers
    # being used.  An exception occurs if the write cannot
    # be verified.
    ####################################################

    def init_sensor(self, lineFreq=4485, PGAGain=21, VoltageGain=36650,
                    CurrentGainCT1=25368, CurrentGainCT2=25358):
        """
        Initialize the atm90e32 by setting registry properties.  The lineFreq
        and PGAGain are unique to a house's location (in the case of)

        :return: True if meter is initialized.
            False if meter could not be initialized.
        """
        lineFreq = 4485  # 4485 for 60 Hz (North America)
        PGAGain = 21     # 21 for 100A (2x), 42 for >100A (4x)
        VoltageGain = 36650  # Based on reading app notes on calibration
        CurrentGainCT1 = 25368  # My calculation
        CurrentGainCT2 = 25368  # My calculation
        try:
            self.energy_sensor = ATM90e32(lineFreq, PGAGain, VoltageGain,
                                          CurrentGainCT1, 0, CurrentGainCT2)
            logger.info('Energy meter has been initialized.')
            # We have an instance of the atm90e32.  Let's check if we get
            # sensible readings.
            sys0 = self.energy_sensor.sys_status0
            if (sys0 == 0xFFFF or sys0 == 0):
                e = 'EXCEPTION: Cannot connect to the energy meter.'
                handle_exception(e)
            logger.info('Energy meter is working.')
            return True
        except Exception as e:
            handle_exception(e)
            return False

    def open_db(self):
        try:
            self.db = MongoDB("mongodb://localhost:27017/",
                              "FitHome", "aggregate")
        except Exception as e:
            self.db = None
            handle_exception(e)
            return False
        return True

    def close_db(self):
        if self.db is not None:
            self.db.close()

    ####################################################
    # Get the current active and reactive power readings.
    ####################################################

    def take_reading(self):
        """read the active and reactive power readings from
        the atm90e32 registers.

        :return: (Pa, Pr) Where Pa is the float value for the
            active power reading and Pr is the float value for
            the reactive power reading.
        """
        Pa = self.energy_sensor.total_active_power
        Pr = self.energy_sensor.total_reactive_power
        logger.info(
            f'Active Power reading: {Pa}  Reactive Power Reading: {Pr}')
        return Pa, Pr

    ####################################################
    # Store the reading into mongo db.
    ####################################################

    def store_reading(self, Pa, Pr):
        if self.db is None:
            logger.error(
                'Not connected to a mongo database.  Cannot store reading.')
            return False
        reading = {"Pa": Pa, "Pr": Pr, }
        self.db.save(reading)
        return True
