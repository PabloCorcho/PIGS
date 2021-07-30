#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 17:17:45 2021

@author: pablo
"""
from glob import glob
from numpy import sort


def get_from_folder(path):
    paths = sort(glob(path+'/*'))    
    return paths

def get_norm(path, units):
    paths = get_from_folder(path)
    all_norms = []
    for path_i in paths:
        with open(path_i, 'r') as f:
                all_lines = f.readlines()                                
                normalization = all_lines[3].split(' ')[2]
                normalization += ' '+units
        f.close()
        all_norms.append(normalization)
    return all_norms
def get_norm_wavelength(path, units):
    paths = get_from_folder(path)
    all_wave_norms = []
    for path_i in paths:
        with open(path_i, 'r') as f:
                all_lines = f.readlines()                
                norm_wavelength = all_lines[2].split(' ')[3]
                norm_wavelength += ' '+units
        f.close()
        all_wave_norms.append(norm_wavelength)
    return all_wave_norms

def get_optdepth_wavelength(path, units):
    paths = get_from_folder(path)
    all_wave_norms = []
    for path_i in paths:
        with open(path_i, 'r') as f:
                all_lines = f.readlines()                
                norm_wavelength = all_lines[4].split(' ')[3]
                norm_wavelength += ' '+units
        f.close()
        all_wave_norms.append(norm_wavelength)
    return all_wave_norms
                
def get_optdepth_norm(path):
    paths = get_from_folder(path)
    all_norms = []
    for path_i in paths:
        with open(path_i, 'r') as f:
                all_lines = f.readlines()                
                norm = float(all_lines[5].split(' ')[2])
        f.close()
        all_norms.append(norm)
    return all_norms                       
                
            

