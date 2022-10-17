#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: EE417_Midterm_Project_AM_KellyHo
# Author: Kelly Ho
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="EE417_Midterm_Project_AM_KellyHo")
        _icon_path = "C:\Program Files\GNURadio-3.7\share\icons\hicolor\scalable/apps\gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 768000
        self.resamp_factor = resamp_factor = 16
        self.message_amp = message_amp = 1.2
        self.carrier_amp = carrier_amp = 0.5

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_scopesink2_1 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title='Scope Plot',
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Counts',
        )
        self.Add(self.wxgui_scopesink2_1.win)
        self.wxgui_fftsink2_1 = fftsink2.fft_sink_f(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate/resamp_factor,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_1.win)
        _message_amp_sizer = wx.BoxSizer(wx.VERTICAL)
        self._message_amp_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_message_amp_sizer,
        	value=self.message_amp,
        	callback=self.set_message_amp,
        	label='message_amp',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._message_amp_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_message_amp_sizer,
        	value=self.message_amp,
        	callback=self.set_message_amp,
        	minimum=0,
        	maximum=10,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_message_amp_sizer)
        self.gr_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 48000, 0.5, 0)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcf(resamp_factor, (firdes.low_pass(1,samp_rate,samp_rate/(2*resamp_factor), 2000)), 48000, samp_rate)
        _carrier_amp_sizer = wx.BoxSizer(wx.VERTICAL)
        self._carrier_amp_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_carrier_amp_sizer,
        	value=self.carrier_amp,
        	callback=self.set_carrier_amp,
        	label='carrier_amp',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._carrier_amp_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_carrier_amp_sizer,
        	value=self.carrier_amp,
        	callback=self.set_carrier_amp,
        	minimum=0,
        	maximum=1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_carrier_amp_sizer)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\kelly\\OneDrive\\Desktop\\EE417_Midterm_Project_Audio.wav', True)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, 16)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((1.2, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((0.3, ))
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((1, ))
        self.band_pass_filter_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	1, samp_rate/resamp_factor, 500, 6000, 400, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_1 = audio.sink(48000, '', True)
        self.analog_agc_xx_0 = analog.agc_cc(6.25e-4, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.wxgui_fftsink2_1, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_scopesink2_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.gr_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_1.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_1.set_sample_rate(self.samp_rate/self.resamp_factor)
        self.gr_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.resamp_factor), 2000)))
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate/self.resamp_factor, 500, 6000, 400, firdes.WIN_HAMMING, 6.76))

    def get_resamp_factor(self):
        return self.resamp_factor

    def set_resamp_factor(self, resamp_factor):
        self.resamp_factor = resamp_factor
        self.wxgui_fftsink2_1.set_sample_rate(self.samp_rate/self.resamp_factor)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.resamp_factor), 2000)))
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate/self.resamp_factor, 500, 6000, 400, firdes.WIN_HAMMING, 6.76))

    def get_message_amp(self):
        return self.message_amp

    def set_message_amp(self, message_amp):
        self.message_amp = message_amp
        self._message_amp_slider.set_value(self.message_amp)
        self._message_amp_text_box.set_value(self.message_amp)

    def get_carrier_amp(self):
        return self.carrier_amp

    def set_carrier_amp(self, carrier_amp):
        self.carrier_amp = carrier_amp
        self._carrier_amp_slider.set_value(self.carrier_amp)
        self._carrier_amp_text_box.set_value(self.carrier_amp)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
