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
        'numPackets':'1e8',
        'units':'ExtragalacticUnits',
        'fluxOutputStyle': 'Wavelength'        
         }

# =============================================================================
# SOURCES 
# =============================================================================
Sources = dict()
Sources['SourceSystem'] = { 
                            'minWavelength': '0.01 micron',
                            'maxWavelength': '100 micron',
                            'wavelengths': '0.55 micron',
                            'sourceBias': '0.5'
                            }
# Number of different sources 
Sources['n_sources'] = 25

# Sources' geometry (DO NOT CHANGE)
Sources['Geometry'] = {'geometry': 'RingGeometry',
                       'ringRadius': ['0.001',  '1',  '2',  '3',  '4',  '5',  '6',  
                                      '7',  '8',  '9', '10', '11', '12', '13',
                                      '14', '15', '16', '17', '18', '19', '20',
                                      '21', '22', '23', '24'],
                       'width': ['0.5']*25, 
                       'heigh': ['0.15']*25,
                       'units': 'kpc'
                       }
# 1. Folder containing each source SED numbered from 1_*.txt to n_*^.txt
#    Each file must contain: 
#        Column 1 --> wavelength, 
#        Column 2 --> Specific luminosity per unit wavelength
# 

#todo: read norm from file
Sources['SED'] = {'folder': '../mw_zones',
                  'normalization': {'type':'LuminosityNormalization',                                    
                                    'unitStyle': 'wavelengthmonluminosity',                                    
                                    'unit':'erg/s/Angstrom'
                                    },
                  'wavelengthBiasDistribution': {
                      'type':'WavelengthDistribution',
                      'LogWavelengthDistribution':{
                                              'minWavelength':'0.01 micron',
                                              'maxWavelength':'100 micron'
                                                   }
                                                 }
                  }                  
# =============================================================================
# INSTRUMENTS
# =============================================================================
Instruments = dict()
Instruments['InstrumentSystem'] = {'defaultWavelengthGrid':'LogWavelengthGrid',
                                    'minWavelength':'0.01 micron',
                                    'maxWavelength':'10 micron',
                                    'numWavelengths':'100'}

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
                         'instrumentName':'instrument_camera_fo', 
                         'distance':'1 Mpc',
                         'inclination':'0 deg',
                         'azimuth':'0',
                         'roll':'0 deg',
                         'fieldOfViewX':'30 kpc',
                         'numPixelsX':'300',
                         'centerX':'0 kpc',
                         'fieldOfViewY':'30 kpc',
                         'numPixelsY':'300',
                         'centerY':'0 kpc',                                                 
                         'recordComponents':'true', 
                         'numScatteringLevels':'0', 
                         'recordPolarization':'false', 
                         'recordStatistics':'false'},
                         3:{'type':'FrameInstrument',
                         'instrumentName':'instrument_camera_eo', 
                         'distance':'1 Mpc',
                         'inclination':'90 deg',
                         'azimuth':'0',
                         'roll':'0 deg',
                         'fieldOfViewX':'30 kpc',
                         'numPixelsX':'300',
                         'centerX':'0 kpc',
                         'fieldOfViewY':'30 kpc',
                         'numPixelsY':'300',
                         'centerY':'0 kpc',                                                 
                         'recordComponents':'true', 
                         'numScatteringLevels':'0', 
                         'recordPolarization':'false', 
                         'recordStatistics':'false'}
                            }

# =============================================================================
# PROBES
# =============================================================================

Probes = dict()

Probes['probes'] = {
    1:{'type':'InstrumentWavelengthGridProbe',
       'probeName':'wgrids'},
    2:{'type':'LuminosityProbe',
       'probeName':'source_lum',
       'wavelengthGrid':{'type':'LogWavelengthGrid',
                         'minWavelength':'0.01 micron',
                         'maxWavelength':'100 micron',
                         'numWavelengths':'100'
                         }}
    
    }