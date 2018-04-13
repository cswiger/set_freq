#!/usr/bin/python

# get radio library
from pyLMS7002M import *

# import gtk  -- gtk 2.24
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk as gtk

class lmsgui:
  def on_window1_destroy(self, object, data=None):
    print "quit with cancel"
    self.limeSDR.LMS7002_Reset()                             # reset the LMS7002M
    gtk.main_quit()

  def on_gtk_quit_activate(self, menuitem, data=None):
    print "quit from menu"
    self.limeSDR.LMS7002_Reset()                             # reset the LMS7002M
    gtk.main_quit()

  def radio_control_f(self,user_data):
    if (user_data.get_active()):
       self.TxTSP.loadDCIQ(0x7FFF, 0x8000)
       self.TRF.LOSS_MAIN_TXPAD_TRF = 0
       self.builder.get_object("DCIQ_val").set_value(32767)
       self.builder.get_object("Loss_val").set_value(0)
    else:
       self.TxTSP.loadDCIQ(0x0, 0x0)
       self.TRF.LOSS_MAIN_TXPAD_TRF = 31
       self.builder.get_object("DCIQ_val").set_value(0)
       self.builder.get_object("Loss_val").set_value(31)

  def freq_change(self,adj):
       self.lms7002.SX['T'].setFREQ(adj.get_value() * 1e6)

  def DCIQ_change(self,adj):
       iq = int(adj.get_value())
       self.TxTSP.loadDCIQ(iq, iq)

  def loss_change(self,adj):
       self.TRF.LOSS_MAIN_TXPAD_TRF = int(adj.get_value())

  def __init__(self):
    self.gladefile = "set_freq.glade" # store the file name
    self.builder = gtk.Builder() # create an instance of the gtk.Builder
    self.builder.add_from_file(self.gladefile) # add the xml file to the Builder

    self.builder.connect_signals({"gtk_main_quit" : gtk.main_quit,
                                "on_window1_destroy" : gtk.main_quit,
                                "radio_control_f" : self.radio_control_f,
                                "Frequency_val_value_changed_cb" : self.freq_change,
                                "DCIQ_val_value_changed_cb" : self.DCIQ_change,
                                "Loss_val_value_changed_cb" : self.loss_change})

    self.window = self.builder.get_object("window1") # This gets the 'window1' object
    self.window.show() # this shows the 'window1' object

    # radio functions
    self.limeSDR = LimeSDR()
    self.limeSDR.LMS7002_Reset()                             # reset the LMS7002M
    self.lms7002 = self.limeSDR.getLMS7002()                      # get the LMS7002M object
    self.lms7002.MIMO = 'MIMO'

    # Initial configuration
    self.lms7002.CGEN.setCLK(80e6)

    self.lms7002.SX['T'].setFREQ(435 * 1e6)

    # Configure TxTSP in test mode, DC output
    self.TxTSP = self.lms7002.TxTSP['A']
    self.TxTSP.TSGMODE = 'DC'
    self.TxTSP.INSEL = 'TEST'
    self.TxTSP.CMIX_BYP = 'BYP'
    self.TxTSP.GFIR1_BYP = 'BYP'
    self.TxTSP.GFIR2_BYP = 'BYP'
    self.TxTSP.GFIR3_BYP = 'BYP'
    self.TxTSP.GC_BYP = 'BYP'
    self.TxTSP.DC_BYP = 'BYP'
    self.TxTSP.PH_BYP = 'BYP'
    self.TxTSP.loadDCIQ(0x0, 0x0)

    # Configure TRF
    self.TRF = self.lms7002.TRF['A']
    self.TRF.LOSS_MAIN_TXPAD_TRF = 31
    self.TRF.EN_LOOPB_TXPAD_TRF = 0
    self.TRF.L_LOOPB_TXPAD_TRF = 0
    self.TRF.PD_TLOBUF_TRF = 0



if __name__ == "__main__":
  main = lmsgui() # create an instance of our class
  gtk.main() # run the darn thing
