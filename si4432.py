import spidev
from time import sleep

from si4432c import *

class Si4432(spidev.SpiDev):
    def __init__(self,a,b):
        super().__init__(a,b)
        self.max_speed_hz = self.speed = 16000000
        # self.max_speed_hz = 4000000

    def enable_rx(self):
        self.reg_write(Si4432_OPERATING_MODE1, rxon)

    def enable_tx(self):
        self.reg_write(Si4432_OPERATING_MODE1, txon)

    def disable_tx(self):
        self.reg_write(Si4432_OPERATING_MODE1, 0x00)

    def rssi(self):
        return self.reg_read(Si4432_RSSI)

    def set_power(self, p):
        self.reg_write(Si4432_TX_POWER, p)

    def set_promisc(self, on):
        self.reg_write(Si4432_HEADER_ENABLE3, 0x00 if on else 0xff)

    def reg_read(self, reg):
        return self.xfer([reg, 0xFF])[1]

    def reg_write(self, reg, val):
        self.xfer([reg|0x80, val])

    def reset(self):
        self.reg_write(Si4432_OPERATING_MODE1, swres)
        sleep(0.01)

    def check(self):
        if self.reg_read(Si4432_DEVICE_TYPE) != device_type_code:
            return False
        if self.reg_read(Si4432_VERSION_CODE) != revision_B1:
            return False
        return True

    def configure_gpio(self):
        self.reg_write(Si4432_GPIO_CONFIGURATION0, output_tx_state)
        self.reg_write(Si4432_GPIO_CONFIGURATION1, output_rx_state)
        #self.reg_write(Si4432_GPIO_CONFIGURATION2, input_direct_digital)

    def set_frequency(self, Freq):
        hbsel = 0
        sbsel = 1

        if (Freq >= 480000000):
            hbsel = 1
            Freq /= 2

        N = int(Freq / 10000000)
        Carrier = int(( 4 * ( Freq - N * 10000000 )) / 625)
        Freq_Band = ( N - 24 ) | ( hbsel << 5 ) | ( sbsel << 6 )

        self.reg_write(Si4432_FREQUENCY_OFFSET1, 0)
        self.reg_write(Si4432_FREQUENCY_OFFSET2, 0)
        self.reg_write(Si4432_FREQUENCY_BAND, Freq_Band)
        self.reg_write(Si4432_NOMINAL_CARRIER_FREQUENCY1, (Carrier>>8) & 0xFF)
        self.reg_write(Si4432_NOMINAL_CARRIER_FREQUENCY0, Carrier & 0xFF)
        # sleep(0.002)
