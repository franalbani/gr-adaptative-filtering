#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# Copyright 2015 Francisco Albani.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

class lms_filter_ff(gr.sync_block):
    """
    docstring for block lms_filter_ff
    """
    def __init__(self, w0, mu):
        # Initial filter taps:
        # This also sets the filter size.
        self.w  = w0
        # Step:
        self.mu = mu

        gr.sync_block.__init__(self,
            name    =   "lms_filter_ff",
            in_sig  =   [numpy.float32, numpy.float32],
            out_sig =   [numpy.float32, numpy.float32])


    def work(self, input_items, output_items):
        # Referencei signal:
        r = input_items[0]
        # Filter input:
        x = input_items[1]
        # Filter output:
        y = output_items[0]
        # Error:
        e = output_items[1]
        
        N = len(x)
        L = len(self.w)
            
        for i in range(N):
            _x = x[i:i+L] # TODO: check orientation.
            # x --> [LTI w] --> y
            y[i] = sum(self.w * _x)
            e[i] = r[i] - y[i]
            # Taps update:
            self.w = self.w + self.mu * e[i] * _x

        # TODO: avoid boundary effects saving the state of the filter.

        return len(output_items[0])

