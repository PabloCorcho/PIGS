#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 17:48:40 2021

@author: pablo
"""


from src import pigs
from ski_params_v2 import SkiParams


# =============================================================================
# Create the SKIRT .ski file
# =============================================================================
params = SkiParams()
pigs.SkirtFile(params, output_path='my_skirt_file')