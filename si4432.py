import spidev
from time import sleep

from si4432c import *

class Si4432(spidev.SpiDev):
    def __init__(self,a,b):
        super().__init__(a,b)
        self.max_speed_hz = 4000000

    def reg_read(self, reg):
        return self.xfer([reg, 0xFF])

    def reg_write(self, reg, val):
        self.xfer([reg|0x80, val])

    def reset(self):
        self.reg_write(Si4432_OPERATING_MODE1, swres)
        sleep(0.001)
        value = self.reg_read(Si4432_INTERRUPT_STATUS1)
        value = self.reg_read(Si4432_INTERRUPT_STATUS2)
        return (value[1] | ipor) != 0

    def spi_read_register(self, reg):
        v = self.reg_read(reg)[1]
        print(f"[i] read_reg({reg}) = {v}")
        return v

    def spi_write_register(self, reg, val):
        print(f"[i] write_reg({reg}) = {val}")
        self.reg_write(reg, val)

    def check(self):
        type = self.spi_read_register(Si4432_DEVICE_TYPE)
        if type != device_type_code:
            print(f"[E] type: {type} <> {device_type_code} (will be)")
            return False
        version = self.spi_read_register(Si4432_VERSION_CODE);
        if version != revision_B1:
            print(f"[E] version: {version} <> {revision_B1} (will be)")
            return False
        return True

    def configure_gpio(self):
        self.spi_write_register(Si4432_GPIO_CONFIGURATION0, output_tx_state)
        self.spi_write_register(Si4432_GPIO_CONFIGURATION1, output_rx_state)
        #self.spi_write_register(Si4432_GPIO_CONFIGURATION2, input_direct_digital)

    def set_frequency(self, Freq):
        if (Freq >= 480000000):
            hbsel = 1
            Freq = Freq / 2
        else:
            hbsel = 0
        sbsel = 1
        N = int(Freq / 10000000)
        Carrier = ( 4 * ( Freq - N * 10000000 )) / 625
        Freq_Band = ( N - 24 ) | ( hbsel << 5 ) | ( sbsel << 6 )
        print(f"{N=}, {Carrier=}, {Freq_Band=}, {hbsel=}")
        self.spi_write_register(0x73, 0)
        self.spi_write_register(0x74, 0)
        self.spi_write_register(0x75, Freq_Band)
        self.spi_write_register(0x76, (int(Carrier)>>8) & 0xFF)
        self.spi_write_register(0x77, int(Carrier) & 0xFF)
        sleep(0.002)


    # Transmitter setup 
    def init_tx_direct(self):
        # * Transmit power: ?? dBm 
        self.spi_write_register( Si4432_TX_POWER, txpow_max | lna_sw )

        # * Transmit data rate: 4096 bps 
        self.spi_write_register( Si4432_TX_DATA_RATE1, 0x21) # 0x218E = 8590 
        self.spi_write_register( Si4432_TX_DATA_RATE0, 0x8E) # gives 4096.03 bps 

        # * Transmit mode: direct mode, clock and data on GPIO 
        self.spi_write_register( Si4432_MODULATION_CONTROL1, txdtrtscale ) # data rate < 30 kbps 
        self.spi_write_register( Si4432_MODULATION_CONTROL2, tx_data_clock_gpio | dtmod_direct_gpio | modtyp_gfsk)

        # * Frequency deviation: 5000 Hz, BW = 18192 Hz by Carson's rule 
        self.spi_write_register( Si4432_FREQUENCY_DEVIATION, 8) 


    def init_tx_packet(self):
        # * Transmit power: ?? dBm 
        self.spi_write_register( Si4432_TX_POWER, txpow_max | lna_sw )

        # * Transmit data rate: 2000 bps 
        self.spi_write_register( Si4432_TX_DATA_RATE1, 0x10) # 0x1062 = 4194 
        self.spi_write_register( Si4432_TX_DATA_RATE0, 0x62) # gives 1999.8 bps 

        # * Transmit mode: FIFO mode, GFSK modulation 
        self.spi_write_register( Si4432_MODULATION_CONTROL1,
                          txdtrtscale           | # data rate < 30 kbps 
                          manppol               | # sets preamble polarity 
                          enmaninv )             # preamble bits inverted 
        self.spi_write_register( Si4432_MODULATION_CONTROL2,
                          tx_data_clock_none    | # data clock not available 
                          dtmod_fifo            | # FIFO mode 
                          modtyp_gfsk )          # GFSK modulation 

        # * Frequency deviation: 5000 Hz, BW = 14 kHz by Carson's rule 
        self.spi_write_register( Si4432_FREQUENCY_DEVIATION, 8) 


    # Set up to receive 2 kbps, 5 kHz deviation packets 
    def init_rx_packet(self):
        # IF_FILTER_BANDWIDTH: 
        # dwn3_bypass = 0, ndec_exp = 2, filset = 0xB = 11 
        # decimate by 2^2 = 4, filset = 1 gives 18.9 kHz bandwidth 
        # decimate by 2^2 = 4, filset = 11 not in table, may give 120 kHz bandwidth! 
        self.spi_write_register(Si4432_IF_FILTER_BANDWIDTH,                   0x2B)
        self.spi_write_register(Si4432_CLOCK_RECOVERY_GEARSHIFT_OVERRIDE,     0x03)
        self.spi_write_register(Si4432_CLOCK_RECOVERY_OVERSAMPLING_RATIO,     0xF4)
        self.spi_write_register(Si4432_CLOCK_RECOVERY_OFFSET2,                0x20)
        self.spi_write_register(Si4432_CLOCK_RECOVERY_OFFSET1,                0x41)
        self.spi_write_register(Si4432_CLOCK_RECOVERY_OFFSET0,                0x89)
        self.spi_write_register(Si4432_CLOCK_RECOVERY_TIMING_LOOP_GAIN1,      0x01)
        self.spi_write_register(Si4432_CLOCK_RECOVERY_TIMING_LOOP_GAIN0,      0x1A)
        self.spi_write_register(Si4432_OOK_COUNTER_VALUE_1,                   0x40)
        self.spi_write_register(Si4432_OOK_COUNTER_VALUE_2,                   0x0A)
        self.spi_write_register(Si4432_SLICER_PEAK_HOLD,                      0x1D)
        self.spi_write_register(Si4432_CHARGE_PUMP_CURRENT_TRIMMING,          0x80)
        # AGC_OVERRIDE1: read out AGC control from bits [4:0] 
        self.spi_write_register(Si4432_AGC_OVERRIDE1,                         0x60)
        self.spi_write_register(Si4432_AFC_LOOP_GEARSHIFT_OVERRIDE,           0x40)
        self.spi_write_register(Si4432_AFC_TIMING_CONTROL,                    0x0A)
        self.spi_write_register(Si4432_AFC_LIMIT,                             0x1D)


    def packet_config(self):
        # tx_fifo_almost_full =  
        # self.spi_write_register(Si4432_TX_FIFO_CONTROL1, rxafthr_mask) 
        tx_fifo_almost_empty = 4 # threshold for txffaam interrupt 
        rx_fifo_almost_full = 55 # threshold for rxffafull interrupt 
        self.spi_write_register(Si4432_TX_FIFO_CONTROL2, tx_fifo_almost_empty)
        self.spi_write_register(Si4432_RX_FIFO_CONTROL, rx_fifo_almost_full)
        self.spi_write_register(Si4432_DATA_ACCESS_CONTROL,
                         enpacrx    | # automatic rx packet handling 
                         enpactx    | # automatic tx packet handling 
                         encrc      | # check CRC against data fields only 
                         crc_ibm_16 ) # use IBM 16 CRC polynomial 
        bcen = 0x80            # broadcast address check enable 
        hdch = 0x08            # received header bytes to be checked 
        self.spi_write_register(Si4432_HEADER_CONTROL1, bcen | hdch)
        self.spi_write_register(Si4432_PREAMBLE_LENGTH, 8) # set preamble length 
        self.spi_write_register(Si4432_SYNC_WORD3, 0x2D)   # first sync byte 
        self.spi_write_register(Si4432_SYNC_WORD2, 0xD4)   # second sync byte 
        # RadioHead doesn't set these!  Hope this is right 
        self.spi_write_register(Si4432_SYNC_WORD1, 0x00)
        self.spi_write_register(Si4432_SYNC_WORD0, 0x00)
        self.spi_write_register(Si4432_HEADER_CONTROL2, 0x22) # por def ault value 
        promiscuous = 0xFF   # this is por def ault 
        self.spi_write_register(Si4432_HEADER_ENABLE3, promiscuous)
        # RadioHead doesn't set these!  Hope this is right 
        self.spi_write_register(Si4432_HEADER_ENABLE2, promiscuous)
        self.spi_write_register(Si4432_HEADER_ENABLE1, promiscuous)
        self.spi_write_register(Si4432_HEADER_ENABLE0, promiscuous)


    def load_packet(self, *data, len):
        # reset and clear FIFO 
        self.spi_write_register(Si4432_OPERATING_MODE2, ffclrtx)
        self.spi_write_register(Si4432_OPERATING_MODE2, 0x00)
        # load up the xmit FIFO 
        self.spi_write_register(Si4432_PACKET_LENGTH, len)
        spi_burst_write(Si4432_FIFO_ACCESS, data, len)
        self.spi_write_register(Si4432_PREAMBLE_LENGTH, 8) # set preamble length 
        # enable packet sent interrupt, disable others 
        self.spi_write_register(Si4432_INTERRUPT_ENABLE1, enpksent)
        self.spi_write_register(Si4432_INTERRUPT_ENABLE2, 0x00)
        # clear any pending interrupts 
        self.spi_read_register(Si4432_INTERRUPT_STATUS1)
        self.spi_read_register(Si4432_INTERRUPT_STATUS2)


    # Query the radio for power state information 
    def get_state(self):
        mode = dtmod_mask & self.spi_read_register(Si4432_MODULATION_CONTROL2)
        status = self.spi_read_register(Si4432_CRYSTAL_OSCILLATOR_POR_CONTROL)

        st = status & internal_power_state_mask

        if st == internal_power_state_lp:
            return IDLE
        elif st == internal_power_state_ready:
            return READY
        elif st == internal_power_state_tune:
            return TUNE
        elif st == internal_power_state_tx:
            if mode == dtmod_direct_gpio or mode == dtmod_direct_sdi:
                return XMIT_DIRECT
            else:
                return XMIT_PACKET
        elif st == internal_power_state_rx:
            if mode == dtmod_direct_gpio or mode == dtmod_direct_sdi:
                return RECV_DIRECT
            else:
                return RECV_PACKET

        return SHUTDOWN


    # Set radio state, turn on/off transmitter and receiver 
    def set_state(self, state):
        if state == READY:
            P1OUT |= RXON_PIN | TXON_PIN # turn off recv and xmit 
            self.spi_write_register(Si4432_OPERATING_MODE1, xton)
            self.spi_write_register(Si4432_OPERATING_MODE2, 0x00)
        elif state == TUNE:
            P1OUT |= RXON_PIN | TXON_PIN # turn off recv and xmit 
            self.spi_write_register(Si4432_OPERATING_MODE1, pllon)
            self.spi_write_register(Si4432_OPERATING_MODE2, 0x00)
        elif state == XMIT_DIRECT:
            P1OUT |= RXON_PIN          # turn off receiver 
            P1OUT &= ~TXON_PIN         # turn on transmitter 
            self.spi_write_register(Si4432_OPERATING_MODE1, txon | xton)
            self.spi_write_register(Si4432_OPERATING_MODE2, 0x00)
        elif state == XMIT_PACKET:
            self.init_tx_packet()
            P1OUT |= RXON_PIN          # turn off receiver 
            P1OUT &= ~TXON_PIN         # turn on transmitter 
            self.spi_write_register(Si4432_OPERATING_MODE1, txon | xton)
        elif state == RECV_DIRECT:
            # unimplemented, probably won't 
            self.set_state(READY)
        elif state == RECV_PACKET:
            # not yet tested 
            self.init_rx_packet()
            P1OUT &= ~RXON_PIN         # turn on receiver 
            P1OUT |= TXON_PIN          # turn off transmitter 
            self.spi_write_register(Si4432_OPERATING_MODE1, rxon | xton)
