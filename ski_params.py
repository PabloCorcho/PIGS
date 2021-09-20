#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 11:12:18 2021

@author: pablo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.get_sed import get_from_folder, get_norm, get_norm_wavelength, get_optdepth_norm, get_optdepth_wavelength, get_mass_norm
from flatten_dict import flatten, unflatten
import numpy as np

n_StellarZones = 1
n_GasZones = 15
n_wavelengths = '400'
minRadius_list = ['10.0 pc','12.0 pc','14.0 pc','16.0 pc','18.0 pc','20.0 pc','22.0 pc','24.0 pc','26.0 pc','28.0 pc','30.0 pc','32.0 pc','34.0 pc','36.0 pc','38.0 pc']
maxRadius_list = ['12.0 pc','14.0 pc','16.0 pc','18.0 pc','20.0 pc','22.0 pc','24.0 pc','26.0 pc','28.0 pc','30.0 pc','32.0 pc','34.0 pc','36.0 pc','38.0 pc','40.0 pc']

def iterate_over_dict(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            for pair in iterate_over_dict(value):
                yield (key, *pair)
        else:
            # If value is not dict type then yield the value
            yield (key, value)

def translate_dictionary(my_dict,ii):
        new_dict = dict()
        for prop_jj in iterate_over_dict(my_dict):
            keywords = tuple( [prop_jj[elem] for elem in range(0,len(prop_jj)-1)] )
            value = prop_jj[-1]
            if isinstance(value,(list,np.ndarray)):
                value = value[ii]
            elif value is None:
                value = {}
            new_dict[keywords] = value
        new_dict = unflatten(new_dict)
        dict_type = list(new_dict.keys())[0]
        return [new_dict[dict_type],dict_type]

              
# =============================================================================
# PARAMETER FILE FOR MAKING SKIRT .SKI FILES
# =============================================================================
class SkiParams(object):
    def __init__(self):    
            # =============================================================================
            # BASIC PROPERTIES 
            # =============================================================================
            Basics = {
                    'MonteCarloSimulation':{
                        'userLevel':"Expert",
                        'simulationMode':"ExtinctionOnly",
                        'numPackets':"1e7",
                    'random':{
                        'type':'Random',
                        'Random':{'seed':'0'}
                                },        
                    'units':{
                        'type':'Units',
                        'ExtragalacticUnits':{'fluxOutputStyle': 'Neutral'}
                            },
                    'cosmology':{
                        'type':'Cosmology',
                        'LocalUniverseCosmology':{}
                                }
                    }
                    }
            self.Basics = Basics
            # =============================================================================
            # SOURCES 
            # =============================================================================
            Sources = dict()
            
            # Basic properties 
            Sources['SourceSystem'] = {
                                        'minWavelength': '0.1 nm',
                                        'maxWavelength': '1e9 nm',
                                        'wavelengths': '550 nm',
                                        'sourceBias': '0.5'
                                        }
            
            Sources['SourceSystem']['sources'] = {'type':'Source'}
            
            # STELLAR SOURCES
            
            starSource_properties = {'PointSource':{
                                        'positionX': ['0 pc'],
                                        'positionY': ['0 pc'],
                                        'positionZ': ['0 pc'],
                                        'velocityX': ['0 km/s'],
                                        'velocityY': ['0 km/s'],
                                        'velocityZ': ['0 km/s'],
                                        'sourceWeight': '1',
                                        'wavelengthBias':'0.5',
                                        'angularDistribution': {
                                            'type':'AngularDistribution',
                                            'IsotropicAngularDistribution':None #This is to copy '{}' in the dictionary
                                            },
                                        'polarizationProfile': {
                                            'type': 'PolarizationProfile',
                                            'NoPolarizationProfile':None
                                            },
                                            
                                        'sed':{ 'type':'SED',
                                            'FileSED':{'filename':get_from_folder('input_data/primary_source')}},
                                        'normalization':{
                                            'type':'LuminosityNormalization',
                                            'SpecificLuminosityNormalization':{
                                                    'wavelength':get_norm_wavelength('input_data/primary_source', 'nm'),
                                                    'unitStyle':'neutralmonluminosity',
                                                    'specificLuminosity':get_norm('input_data/primary_source', 'erg/s')}
                                            }
                                        }
                                    }
            
            for ii in range(n_StellarZones):
                translated_stellarSource = translate_dictionary(starSource_properties,ii)
                source_ii  = translated_stellarSource[0]
                source_key = translated_stellarSource[1]
                number_ii = str(ii+1).zfill(3)
                Sources['SourceSystem']['sources'][(source_key+" {}").format(number_ii)] = source_ii
                
            
            # GAS SOURCES
            
            n_GasSources = n_GasZones
            
            #Mario: 0.0 pc is not allowed by skirt
            gasSource_properties = {'GeometricSource':{
                                        'velocityMagnitude':'0 km/s', 
                                        'sourceWeight':"1", 
                                        'wavelengthBias':"0.5",
                                        
                                        'geometry':{
                                            'type':'Geometry',
                                            'ShellGeometry':{
                                            'minRadius': minRadius_list,
                                            'maxRadius': maxRadius_list, 
                                            'exponent': ['0']*n_GasSources
                                                }
                                            },
                                        'sed':{
                                            'type':'SED',
                                            'FileSED':{'filename':get_from_folder('input_data/gas_regions')}
                                            },
                                        'normalization':{
                                            'type':'LuminosityNormalization',
                                            'SpecificLuminosityNormalization':{
                                                    'wavelength':get_norm_wavelength('input_data/gas_regions', 'nm'),
                                                    'unitStyle':'neutralmonluminosity',
                                                    'specificLuminosity':get_norm('input_data/gas_regions', 'erg/s')}
                                            }
                                        }
                                    }
            
            for ii in range(n_GasSources):
                translated_gasSource = translate_dictionary(gasSource_properties,ii)
                source_ii  = translated_gasSource[0]
                source_key = translated_gasSource[1]
                number_ii = str(ii+1).zfill(3)
                Sources['SourceSystem']['sources'][(source_key+" {}").format(number_ii)] = source_ii
            
            
            self.Sources = Sources    
            # =============================================================================
            # MEDIUM SYSTEM
            # =============================================================================
                    
            Media = dict()
            
            # Basic properties 
            Media['MediumSystem'] = { 'numDensitySamples':'100',
                                       'photonPacketOptions':{'type':'PhotonPacketOptions',
                                                              'PhotonPacketOptions':{
                                                                  'forceScattering':True,
                                                                  'minWeightReduction':1e4,
                                                                  'minScattEvents':'0',
                                                                  'pathLengthBias':'0.5'}},
                   'extinctionOnlyOptions':{'type':'ExtinctionOnlyOptions',
                                            'ExtinctionOnlyOptions':{
                                                'storeRadiationField':'true',
                                                'radiationFieldWLG':{'type':'DisjointWavelengthGrid',
                                                                 'LogWavelengthGrid':{
                                                                     'minWavelength':'0.0001 micron',
                                                                     'maxWavelength':'1e6 micron',
                                                                     'numWavelengths': n_wavelengths #200
                                                                                     }
                                                                 }}
                                            },
                   'dynamicStateOptions':{'type':'DynamicStateOptions', 
                                          'DynamicStateOptions':{'hasDynamicState':True,
                                                                 'minIterations':'1',
                                                                 'maxIterations':'10',
                                                                 'iterationPacketsMultiplier':'1',
                                                                 'recipes':{'type':'DynamicStateRecipe',
                                                                            'ClearDensityRecipe':{
                                                                                'maxNotConvergedCells':'0', 
                                                                                'fieldStrengthThreshold':'1e9'
                                                                                } 
                                                                            }
                                                                 }
                                          }
                                        }
            
            Media['MediumSystem']['media'] = {'type':'Medium'}
            
            # GAS CONTINUUM MEDIA (several mediums sharing the same geometry)
            
            n_media = n_GasZones
            
            gasMedia_properties = {'GeometricMedium':{
                                        'velocityMagnitude':'0 km/s', 
                                        'magneticFieldStrength':'0 uG',
                                        
                                        'geometry':{
                                            'type':'Geometry',
                                            'ShellGeometry':{
                                            'minRadius': minRadius_list,
                                            'maxRadius': maxRadius_list, 
                                            'exponent': ['0']*n_GasSources
                                                }
                                            },
                                        'materialMix':{
                                            'type':'MaterialMix',
                                            'MeanFileDustMix':{'filename':get_from_folder('input_data/gas_props')}
                                            },
                                        'normalization':{
                                            'type':'MaterialNormalization',
                                            'MassMaterialNormalization':{
                                                    'mass':get_mass_norm('input_data/gas_props','Msun')
                                            }
                                        }
                                    }
                                }
            
            for ii in range(n_media): 
                translated_gasMedia = translate_dictionary(gasMedia_properties,ii)
                medium_ii  = translated_gasMedia[0]
                medium_key = translated_gasMedia[1]
                number_ii = str(ii+1).zfill(3)
                Media['MediumSystem']['media'][(medium_key+" {}").format(number_ii)] = medium_ii 
               
                
            units = ' pc'    
            Media['MediumSystem']['grid'] = {'type':'SpatialGrid',
                               'Cylinder2DSpatialGrid': {'maxRadius':'40'+units, 
                                                         'minZ':'-40'+units,
                                                         'maxZ':'40'+units,
                                                         'meshRadial':{'type':'Mesh',
                                                                       'LinMesh':{'numBins':400}},
                                                         'meshZ':{'type':'MoveableMesh',
                                                                  'LinMesh':{'numBins':200}}
                                                         }
                               }       
            
            self.Media = Media
            # =============================================================================
            # INSTRUMENTS
            # =============================================================================
            Instruments = dict()
             
            Instruments['InstrumentSystem'] = {'defaultWavelengthGrid':{
                'type':'WavelengthGrid',
                'LogWavelengthGrid':{
                    'minWavelength':'0.0001 micron',
                    'maxWavelength':'1e6 micron',
                    'numWavelengths':n_wavelengths} #200
                }
                                               }
            
            Instruments['InstrumentSystem']['instruments']={
                                    'type':'Instrument',
                                     'SEDInstrument 1':{
                                             'instrumentName':'ised', 
                                             'distance':'1 Mpc',
                                             'inclination':'0 deg',
                                             'azimuth':'0',
                                             'roll':'0 deg',
                                             'radius':'0 pc',
                                             'recordComponents':'true', 
                                             'numScatteringLevels': '0', 
                                             'recordPolarization':'false', 
                                             'recordStatistics':'false',
                                             'wavelengthGrid':{'type':'WavelengthGrid',
                                                               'LogWavelengthGrid':{
                                                                       'minWavelength':'0.0001 micron',
                                                                       'maxWavelength':'1e6 micron',
                                                                       'numWavelengths':n_wavelengths #200
                                                                                   }
                                                       }
                                         },
                                     # 2:{'type':'FrameInstrument',
                                     # 'instrumentName':'instrument_camera_fo', 
                                     # 'distance':'1 Mpc',
                                     # 'inclination':'0 deg',
                                     # 'azimuth':'0',
                                     # 'roll':'0 deg',
                                     # 'fieldOfViewX':'30 kpc',
                                     # 'numPixelsX':'300',
                                     # 'centerX':'0 kpc',
                                     # 'fieldOfViewY':'30 kpc',
                                     # 'numPixelsY':'300',
                                     # 'centerY':'0 kpc',                                                 
                                     # 'recordComponents':'true', 
                                     # 'numScatteringLevels':'0', 
                                     # 'recordPolarization':'false', 
                                     # 'recordStatistics':'false'},
                                     # 3:{'type':'FrameInstrument',
                                     # 'instrumentName':'instrument_camera_eo', 
                                     # 'distance':'1 Mpc',
                                     # 'inclination':'90 deg',
                                     # 'azimuth':'0',
                                     # 'roll':'0 deg',
                                     # 'fieldOfViewX':'30 kpc',
                                     # 'numPixelsX':'300',
                                     # 'centerX':'0 kpc',
                                     # 'fieldOfViewY':'30 kpc',
                                     # 'numPixelsY':'300',
                                     # 'centerY':'0 kpc',                                                 
                                     # 'recordComponents':'true', 
                                     # 'numScatteringLevels':'0', 
                                     # 'recordPolarization':'false', 
                                     # 'recordStatistics':'false'}
                                        }
            self.Instruments = Instruments
            # =============================================================================
            # PROBES
            # =============================================================================
            
            Probes = dict()
            
            Probes['ProbeSystem'] = {
                'probes':{'type':'Probe',    
                'LuminosityProbe 1':{
                                    'probeName':'source_lum',
                                    'wavelengthGrid':{'type':'WavelengthGrid',
                                     'LogWavelengthGrid':{
                                     'minWavelength':'0.1 nm',
                                     'maxWavelength':'1e6 nm',
                                     'numWavelengths':n_wavelengths #200
                                                          }
                                     }
                                    },
                'SpatialGridConvergenceProbe 1':{'probeName':"conv",
                                                 'wavelength':"0.55 micron"
                                                 },
                'RadiationFieldAtPositionsProbe 1':{
                    'probeName':"nuJnu",
                    'filename':"input_data/MeanIntensity_Positions/BStar_HighRes.txt",
                    'useColumns':"",
                    'writeWavelengthGrid':"false"
                                                },
                'InstrumentWavelengthGridProbe 1':{'probeName':"grid"},    
                'RadiationFieldWavelengthGridProbe 1':{'probeName':"radGrid"}                        
                        }
                }    
            self.Probes = Probes
        
        
