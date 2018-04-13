# set_freq
Simple GUI demo for pyLMS7002M and Glade 

Just testing putting LimeSDR controls from pyLMS7002M in an easy gui whipped up in Glade.
Hit the transmit toggle button to turn power on / off by setting :

  limeSDR.LMS7002.TxTSP['A'].loadDCIQ(0x0, 0x0)<br/>
  limeSDR.LMS7002.TRF['A'].LOSS_MAIN_TXPAD_TRF = 31<br/>

for 'off' and to 

  limeSDR.LMS7002.TxTSP['A'].loadDCIQ(0x7FFF, 0x8000)<br/>
  limeSDR.LMS7002.TRF['A'].LOSS_MAIN_TXPAD_TRF = 0<br/>

for 'on'.
Three other spin boxes allow changing the frequency as well as the above DCIQ and LOSS. 

