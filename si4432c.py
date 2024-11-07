BIT0 = 1 << 0
BIT1 = 1 << 1
BIT2 = 1 << 2
BIT3 = 1 << 3
BIT4 = 1 << 4
BIT5 = 1 << 5
BIT6 = 1 << 6
BIT7 = 1 << 7


"""***************** Status ******************"""

Si4432_DEVICE_TYPE = 0x00
device_type_code = 0x08   

Si4432_VERSION_CODE = 0x01
revision_B1 = 0x06        

Si4432_DEVICE_STATUS = 0x02
ffovfl = BIT7            
ffunfl = BIT6            
rxffem = BIT5            
headerr = BIT4            
freqerr = BIT3            
cpsidle = 0x00            
cpsrx = 0x01            
cpstx = 0x02            


"""***************** Interrupts ******************"""

"""
 * The Si4430/31/32 is capable of generating an interrupt signal when
 * certain events occur. The chip notifies the microcontroller that an
 * interrupt event has occurred by setting the nIRQ output pin LOW =
 * 0.  This interrupt signal will be generated when any one (or more)
 * of the interrupt events (corresponding to the Interrupt Status
 * bits) shown below occur.  The nIRQ pin will remain low until the
 * microcontroller reads the Interrupt Status Register(s) (Registers
 * 03h-04h) containing the active Interrupt Status bit.  The nIRQ
 * output signal will then be reset until the next change in status is
 * detected.  The interrupts must be enabled by the corresponding
 * enable bit in the Interrupt Enable Registers (Registers 05h-06h).
 * All enabled interrupt bits will be cleared when the microcontroller
 * reads the interrupt status register.  If the interrupt is not
 * enabled when the event occurs it will not trigger the nIRQ pin, but
 * the status may still be read at anytime in the Interrupt Status
 * registers.
"""

Si4432_INTERRUPT_STATUS1 = 0x03
ifferr = BIT7         
itxffsfull = BIT6         
itxffaem = BIT5         
irxffafull = BIT4         
iext = BIT3         
ipksent = BIT2         
ipkvalid = BIT1         
icrcerror = BIT0         

Si4432_INTERRUPT_STATUS2 = 0x04
iswdet = BIT7         
ipreaval = BIT6         
ipreminval = BIT5         
irssi = BIT4         
iwut = BIT3         
ilbd = BIT2         
ichiprdy = BIT1         
ipor = BIT0         

Si4432_INTERRUPT_ENABLE1 = 0x05
enfferr = BIT7        
entxffafull = BIT6        
entxffaem = BIT5        
enrxffafull = BIT4        
enext = BIT3        
enpksent = BIT2        
enpkvalid = BIT1        
encrcerror = BIT0        

Si4432_INTERRUPT_ENABLE2 = 0x06
enswdet = BIT7        
enpreaval = BIT6        
enpreainval = BIT5        
enrssi = BIT4        
enwut = BIT3        
enlbd_ie2 = BIT2        
enchiprdy = BIT1        
enport = BIT0        


"""************ Operating mode and function control ***********"""

Si4432_OPERATING_MODE1 = 0x07
swres = BIT7        
enlbd_mode1 = BIT6        
enwt = BIT5        
x32ksel = BIT4        
txon = BIT3        
rxon = BIT2        
pllon = BIT1        
xton = BIT0        

Si4432_OPERATING_MODE2 = 0x08
antdiv = (BIT7|BIT6|BIT5) 
rxmpk = BIT4            
autotx = BIT3            
enldm = BIT2            
ffclrrx = BIT1            
ffclrtx = BIT0            

""" fiddle with the crystal load capacitance """
Si4432_OSCILLATOR_LOAD_CAPACITANCE = 0x09
xtalshift = BIT7          
xlc_mask = 0x7F          

""" fiddle with the clock """
Si4432_UC_OUTPUT_CLOCK = 0x0a
clktl = (BIT7|BIT6)       
enlfc = BIT5             
mclk30mhz = 0          
mclk15mhz = 1          
mclk10mhz = 2          
mclk4mhz = 3          
mclk3mhz = 4          
mclk2mhz = 5          
mclk1mhz = 6          
mclk32768khz = 7          


"""************ GPIO configuration ***********"""

Si4432_GPIO_CONFIGURATION0 = 0x0b
pup0 = BIT5               
output_power_on_reset = 0x00

Si4432_GPIO_CONFIGURATION1 = 0x0c
pup1 = BIT5               
output_inverted_power_on_reset = 0x00

Si4432_GPIO_CONFIGURATION2 = 0x0d
pup2 = BIT5               
output_microcontroller_clock = 0x00

""" the following apply to all GPIO_CONFIGURATIONx registers """
output_wakeup_timer = 0x01
output_low_battery_detect = 0x02
input_direct_digital = 0x03
input_external_interrupt_falling_edge = 0x04
input_external_interrupt_rising_edge = 0x05
input_external_interrupt_state_change = 0x06
input_adc_analog = 0x07
output_direct_digital = 0x0A
output_reference_voltage = 0x0E
output_txrx_data_clock = 0x0F
input_tx_direct_modulation_data = 0x10
input_external_retransmission_request = 0x11
output_tx_state = 0x12
output_tx_fifo_almost_full = 0x13
output_rx_data = 0x14
output_rx_state = 0x15
output_rx_fifo_almost_full = 0x16
output_antenna_diversity_switch_1 = 0x17
output_antenna_diversity_switch_2 = 0x18
output_valid_preamble_detected = 0x19
output_invalid_preamble_detected = 0x1A
output_sync_word_detected = 0x1B
output_clear_channel = 0x1C
output_vdd = 0x1D

Si4432_IO_PORT_CONFIGURATION = 0x0e
extitst2 = BIT6           
extitst1 = BIT5           
extitst0 = BIT4           
itsdo = BIT3           
dio2 = BIT2           
dio1 = BIT1           
dio0 = BIT0           

""" analog to digital converter """
Si4432_ADC_CONFIGURATION = 0x0f
Si4432_ADC_SENSOR_AMP_OFFSET = 0x10
Si4432_ADC_VALUE = 0x11

""" temperature sensor """
Si4432_TEMPERATURE_SENSOR_CALIBRATION = 0x12
Si4432_TEMPERATURE_VALUE_OFFSET = 0x13

""" wake-up timer """
Si4432_WAKEUP_TIMER_PERIOD1 = 0x14
Si4432_WAKEUP_TIMER_PERIOD2 = 0x15
Si4432_WAKEUP_TIMER_PERIOD3 = 0x16
Si4432_WAKEUP_TIMER_VALUE1 = 0x17
Si4432_WAKEUP_TIMER_VALUE2 = 0x18

""" low duty cycle  """
Si4432_LDC_MODE_DURATION = 0x19

""" battery """
Si4432_LOW_BATTERY_DETECTOR_THRESHOLD = 0x1a
Si4432_BATTERY_VOLTAGE_LEVEL = 0x1b

""" IF filter bandwidth -- see table in AN440 """
Si4432_IF_FILTER_BANDWIDTH = 0x1c

""" automatic frequency control """
Si4432_AFC_LOOP_GEARSHIFT_OVERRIDE = 0x1d
Si4432_AFC_TIMING_CONTROL = 0x1e

""" clock recovery """
Si4432_CLOCK_RECOVERY_GEARSHIFT_OVERRIDE = 0x1f
Si4432_CLOCK_RECOVERY_OVERSAMPLING_RATIO = 0x20
Si4432_CLOCK_RECOVERY_OFFSET2 = 0x21
Si4432_CLOCK_RECOVERY_OFFSET1 = 0x22
Si4432_CLOCK_RECOVERY_OFFSET0 = 0x23
Si4432_CLOCK_RECOVERY_TIMING_LOOP_GAIN1 = 0x24
Si4432_CLOCK_RECOVERY_TIMING_LOOP_GAIN0 = 0x25

""" Received signal strength indicator """
Si4432_RSSI = 0x26
Si4432_RSSI_THRESHOLD = 0x27

""" antenna diversity """
Si4432_ANTENNA_DIVERSITY1 = 0x28
Si4432_ANTENNA_DIVERSITY2 = 0x29

""" more automatic frequency control """
Si4432_AFC_LIMIT = 0x2a
Si4432_AFC_CORRECTION_READ = 0x2b

""" on-off keyed """
Si4432_OOK_COUNTER_VALUE_1 = 0x2c
Si4432_OOK_COUNTER_VALUE_2 = 0x2d
Si4432_SLICER_PEAK_HOLD = 0x2e

""" packet stuff """
Si4432_DATA_ACCESS_CONTROL = 0x30
enpacrx = BIT7           
lsbfrst = BIT6           
crcdonly = BIT5           
skip2ph = BIT4           
enpactx = BIT3           
encrc = BIT2           
crc_ccitt = 0          
crc_ibm_16 = 1          
crc_iec_16 = 2          
crc_biacheva = 3          

Si4432_EZMAC_STATUS = 0x31
rxcrc1 = BIT6           
pksrch = BIT5           
pkrx = BIT4           
pkvalid = BIT3           
crcerror = BIT2           
pktx = BIT1           
pksent = BIT0           

Si4432_HEADER_CONTROL1 = 0x32
bcen_mask = 0xF0          
hdch_mask = 0x0F          

Si4432_HEADER_CONTROL2 = 0x33
skipsyn = BIT7     
hdlen_mask = ( BIT6 | BIT5 | BIT4 ) 
fixpklen = BIT3     
synclen_mask = ( BIT2 | BIT1 ) 
prealen = BIT0     

Si4432_PREAMBLE_LENGTH = 0x34
Si4432_PREAMBLE_DETECTION_CONTROL1 = 0x35
Si4432_SYNC_WORD3 = 0x36
Si4432_SYNC_WORD2 = 0x37
Si4432_SYNC_WORD1 = 0x38
Si4432_SYNC_WORD0 = 0x39
Si4432_TRANSMIT_HEADER3 = 0x3a
Si4432_TRANSMIT_HEADER2 = 0x3b
Si4432_TRANSMIT_HEADER1 = 0x3c
Si4432_TRANSMIT_HEADER0 = 0x3d
Si4432_PACKET_LENGTH = 0x3e
Si4432_CHECK_HEADER3 = 0x3f
Si4432_CHECK_HEADER2 = 0x40
Si4432_CHECK_HEADER1 = 0x41
Si4432_CHECK_HEADER0 = 0x42
Si4432_HEADER_ENABLE3 = 0x43
Si4432_HEADER_ENABLE2 = 0x44
Si4432_HEADER_ENABLE1 = 0x45
Si4432_HEADER_ENABLE0 = 0x46
Si4432_RECEIVED_HEADER3 = 0x47
Si4432_RECEIVED_HEADER2 = 0x48
Si4432_RECEIVED_HEADER1 = 0x49
Si4432_RECEIVED_HEADER0 = 0x4a
Si4432_RECEIVED_PACKET_LENGTH = 0x4b
Si4432_ANALOG_TEST_BUS_SELECT = 0x50
Si4432_DIGITAL_TEST_BUS_SELECT = 0x51
Si4432_TX_RAMP_CONTROL = 0x52
Si4432_PLL_TUNE_TIME = 0x53
Si4432_CALIBRATION_CONTROL = 0x55
Si4432_MODEM_TEST = 0x56
Si4432_CHARGE_PUMP_TEST = 0x57
Si4432_CHARGE_PUMP_CURRENT_TRIMMING = 0x58
Si4432_DIVIDER_CURRENT_TRIMMING = 0x59
Si4432_VCO_CURRENT_TRIMMING = 0x5a
Si4432_VCO_CALIBRATION = 0x5b
Si4432_SYNTHESIZER_TEST = 0x5c
Si4432_BLOCK_ENABLE_OVERRIDE1 = 0x5d
Si4432_BLOCK_ENABLE_OVERRIDE2 = 0x5e
Si4432_BLOCK_ENABLE_OVERRIDE3 = 0x5f
Si4432_CHANNEL_FILTER_COEFFICIENT_ADDRESS = 0x60
Si4432_CHANNEL_FILTER_COEFFICIENT_VALUE = 0x61

""" power-on reset  """
Si4432_CRYSTAL_OSCILLATOR_POR_CONTROL = 0x62
internal_power_state_mask = (BIT7|BIT6|BIT5)
internal_power_state_lp = 0x00
internal_power_state_ready = 0x20
internal_power_state_tune = 0x60
internal_power_state_tx = 0x40
internal_power_state_rx = 0xE0
clkhyst = BIT4           
enbias2x = BIT3           
enamp2x = BIT2           
bufovr = BIT1           
enbuf = BIT0           

Si4432_RC_OSCILLATOR_COARSE_CALIBRATION = 0x63
Si4432_RC_OSCILLATOR_FINE_CALIBRATION = 0x64
Si4432_LDO_CONTROL_OVERRIDE = 0x65
Si4432_LDO_LEVEL_SETTINGS = 0x66
Si4432_DELTA_SIGMA_ADC_TUNING1 = 0x67
Si4432_DELTA_SIGMA_ADC_TUNING2 = 0x68
Si4432_AGC_OVERRIDE1 = 0x69
Si4432_AGC_OVERRIDE2 = 0x6a
Si4432_GFSK_FIR_FILTER_COEFFICIENT_ADDRESS = 0x6b
Si4432_GFSK_FIR_FILTER_COEFFICIENT_VALUE = 0x6c

""" transmit power """
Si4432_TX_POWER = 0x6d
lna_sw = BIT3        
txpow_mask = (BIT2|BIT1|BIT0)
txpow_max = 0x07        
txpow_17dbm = 0x06
txpow_14dbm = 0x05
txpow_11dbm = 0x04
txpow_08dbm = 0x03
txpow_05dbm = 0x02
txpow_02dbm = 0x01
txpow_min = 0x00        

""" transmission data rate """
Si4432_TX_DATA_RATE1 = 0x6e
Si4432_TX_DATA_RATE0 = 0x6f
""" 8590 decimal, 0x218E in these registers gives 4096.03 kbps """

""" modulation """
Si4432_MODULATION_CONTROL1 = 0x70
txdtrtscale = BIT5        
enphpwdn = BIT4        
manppol = BIT3        
enmaninv = BIT2        
enmanch = BIT1        
enwhite = BIT0        

""" more modulation """
Si4432_MODULATION_CONTROL2 = 0x71
tx_data_clock_config_mask = (BIT7|BIT6) 
tx_data_clock_none = 0x00 
tx_data_clock_gpio = 0x40 
tx_data_clock_sdo = 0x80 
tx_data_clock_nirq = 0xC0 
dtmod_mask = (BIT5|BIT4)  
dtmod_direct_gpio = 0x00 
dtmod_direct_sdi = 0x10 
dtmod_fifo = 0x20 
dtmod_pn9 = 0x30 
eninv = BIT3              
freq_deviation_msb = BIT2 
modtyp_mask = (BIT1|BIT0) 
modtyp_unmodulated = 0    
modtyp_ook = 1    
modtyp_fsk = 2    
modtyp_gfsk = 3    

""" frequency deviation """
Si4432_FREQUENCY_DEVIATION = 0x72

""" frequency offset """
Si4432_FREQUENCY_OFFSET1 = 0x73
Si4432_FREQUENCY_OFFSET2 = 0x74

""" frequency band select """
Si4432_FREQUENCY_BAND = 0x75
sbsel = BIT6              
hbsel = BIT5              
fb_mask = 0x1F            
""" Choose sbsel = 1, hbsel = 0, fb = 19, 0x13 for frequency band 430
   MHz.  Then value is (sbsel|0x13) """

""" carrier frequency """
Si4432_NOMINAL_CARRIER_FREQUENCY1 = 0x76
Si4432_NOMINAL_CARRIER_FREQUENCY0 = 0x77
""" Spreadsheet gives fc = 0x76C0 = 30400 => carrier = 434.75 MHz"""

""" frequency hopping """
Si4432_FREQUENCY_HOPPING_CHANNEL = 0x79
Si4432_FREQUENCY_HOPPING_STEP_SIZE = 0x7a

""" tx FIFO  """
Si4432_TX_FIFO_CONTROL1 = 0x7c
txafthr_mask = 0x1F       
Si4432_TX_FIFO_CONTROL2 = 0x7d
txaethr_mask = 0x1F       

""" rx FIFO """
Si4432_RX_FIFO_CONTROL = 0x7e
txafthr_mask = 0x1F       
Si4432_FIFO_ACCESS = 0x7f





SHUTDOWN = 1
IDLE = 2
STANDBY = 3
SLEEP = 4
SENSOR = 5
READY = 6
TUNE = 7
XMIT_DIRECT = 8
XMIT_PACKET = 9
RECV_DIRECT = 10
RECV_PACKET = 11
