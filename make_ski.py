#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 17:48:40 2021

@author: pablo
"""


from src import pigs

# =============================================================================
# Create the SKIRT .ski file
# =============================================================================
pigs.SkirtFile('ski_params', output_path='my_skirt_file')