#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Convention_AM
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


class Convention_AM(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Convention_AM")
        _icon_path = "C:\Program Files\GNURadio-3.7\share\icons\hicolor\scalable/apps\gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.volume = volume = 1
        self.samp_rate = samp_rate = 768000
        self.resamp_factor = resamp_factor = 16
        self.noise = noise = 0.05
        self.carrier_freq = carrier_freq = 48000

        ##################################################
        # Blocks
        ##################################################
        _volume_sizer = wx.BoxSizer(wx.VERTICAL)
        self._volume_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	label='volume',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._volume_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	minimum=0,
        	maximum=2,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_volume_sizer)
        _noise_sizer = wx.BoxSizer(wx.VERTICAL)
        self._noise_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_noise_sizer,
        	value=self.noise,
        	callback=self.set_noise,
        	label='noise',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._noise_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_noise_sizer,
        	value=self.noise,
        	callback=self.set_noise,
        	minimum=0,
        	maximum=0.1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_noise_sizer)
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
        self.wxgui_fftsink2_1_0 = fftsink2.fft_sink_f(
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
        self.Add(self.wxgui_fftsink2_1_0.win)
        self.low_pass_filter_0 = filter.fir_filter_fff(resamp_factor, firdes.low_pass(
        	1, samp_rate, 17000, 100, firdes.WIN_HAMMING, 6.76))
        self.gr_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, carrier_freq, 0.8, 0)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\kelly\\OneDrive\\Desktop\\Midterm Project\\EE417_Midterm_Project_Audio.wav', True)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('C:\\Users\\kelly\\OneDrive\\Desktop\\E E 417\\Midterm Project\\Conventional AM\\Convention_AM_Recovered_Noise.wav', 1, samp_rate/resamp_factor, 16)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, 16)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((0.8, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((volume, ))
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((1, ))
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, carrier_freq, 1, 0)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, noise, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_fftsink2_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_scopesink2_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_xx_1, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.gr_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_const_vxx_0, 0))

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self._volume_slider.set_value(self.volume)
        self._volume_text_box.set_value(self.volume)
        self.blocks_multiply_const_vxx_0.set_k((self.volume, ))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_1.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_1_0.set_sample_rate(self.samp_rate/self.resamp_factor)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 17000, 100, firdes.WIN_HAMMING, 6.76))
        self.gr_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_resamp_factor(self):
        return self.resamp_factor

    def set_resamp_factor(self, resamp_factor):
        self.resamp_factor = resamp_factor
        self.wxgui_fftsink2_1_0.set_sample_rate(self.samp_rate/self.resamp_factor)

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self._noise_slider.set_value(self.noise)
        self._noise_text_box.set_value(self.noise)
        self.analog_noise_source_x_0.set_amplitude(self.noise)

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.gr_sig_source_x_0.set_frequency(self.carrier_freq)
        self.analog_sig_source_x_0.set_frequency(self.carrier_freq)


def main(top_block_cls=Convention_AM, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
