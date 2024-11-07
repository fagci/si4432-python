#!/usr/bin/env python3

from si4432 import Si4432

from time import sleep

with Si4432(0,0) as si:
    print(si.reset())
    print(si.check())


    si.reg_write(0x1F, 0x00);







    si.configure_gpio()
    si.reg_write(0x7, 0x0B);
    #si.reg_write(0x09, 0x64)
    si.set_frequency(434225000)
    sleep(1)
    si.reg_write(0x7, 0x00);
    

