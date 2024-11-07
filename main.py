#!/usr/bin/env python3

from si4432 import Si4432

from time import sleep

with Si4432(0,0) as si:
    si.reset()
    if not si.check():
        print('Chip npt detected')
        exit(255)

    si.configure_gpio()
    si.set_power(0)

    si.set_frequency(434000000)

    si.enable_tx()
    sleep(2)
    si.disable_tx()
    

