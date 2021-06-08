#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# PARAMETER FILE FOR MAKING SKIRT .SKI FILES
# =============================================================================

# =============================================================================
# BASIC PROPERTIES 
# =============================================================================
Basics = {
        'userLevel':'Regular',
        'simulationMode':'NoMedium',
        'numPackets':'1e7',
        'units':'ExtragalacticUnits',
        'fluxOutputStyle': 'Wavelength'        
         }

# =============================================================================
# SOURCES 
# =============================================================================
Sources = dict()
Sources['SourceSystem'] = { 
                            'minWavelength': '0.09 micron',
                            'maxWavelength': '100 micron',
                            'wavelengths': '0.55 micron',
                            'sourceBias': '0.5'
                            }
# Number of different sources 
Sources['n_sources'] = 4
# Sources' geometry (DO NOT CHANGE)
Sources['Geometry'] = {'geometry': 'RingGeometry',
                       'ringRadius': ['500', '1000', '1500', '2000'],
                       'width': ['300', '300', '300', '300'], 
                       'heigh': ['150', '150', '150', '150'],
                       'units': 'pc'
                       }
# 1. Folder containing each source SED numbered from 1_*.txt to n_*^.txt
#    Each file must contain: 
#        Column 1 --> wavelength, 
#        Column 2 --> Specific luminosity per unit wavelength
# 
Sources['SED'] = {'folder': 'sources_sed',
                  'normalization': {'type':'LuminosityNormalization',
                                    'wavelength':'0.55 micron',
                                    'unitStyle': 'wavelengthmonluminosity',
                                    'specificLuminosity':'1 Lsun/micron'
                                    },
                  'wavelengthBiasDistribution': {
                      'type':'WavelengthDistribution',
                      'LogWavelengthDistribution':{
                                              'minWavelength':'0.0001 micron',
                                              'maxWavelength':'1e3 micron'
                                                   }
                                                 }
                  }                  
# =============================================================================
# INSTRUMENTS
# =============================================================================
Instruments = dict()
Instruments['InstrumentSystem'] = {'defaultWavelengthGrid':'LogWavelengthGrid',
                                    'minWavelength':'0.4 micron',
                                    'maxWavelength':'0.7 micron',
                                    'numWavelengths':'200'}

Instruments['instruments']={
                         1:{'type':'SEDInstrument',
                         'instrumentName':'instrument_sed', 
                         'distance':'1 Mpc',
                         'inclination':'0 deg',
                         'azimuth':'0',
                         'roll':'0 deg',
                         'radius':'0 pc',
                         'recordComponents':'true', 
                         'numScatteringLevels':'0', 
                         'recordPolarization':'false', 
                         'recordStatistics':'false'},
                         2:{'type':'FrameInstrument',
                         'instrumentName':'instrument_camera', 
                         'distance':'1 Mpc',
                         'inclination':'0 deg',
                         'azimuth':'0',
                         'roll':'0 deg',
                         'fieldOfViewX':'10 kpc',
                         'numPixelsX':'300',
                         'centerX':'0 kpc',
                         'fieldOfViewY':'10 kpc',
                         'numPixelsY':'300',
                         'centerY':'0 kpc',                                                 
                         'recordComponents':'true', 
                         'numScatteringLevels':'0', 
                         'recordPolarization':'false', 
                         'recordStatistics':'false'}
                            }
