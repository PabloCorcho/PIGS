#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 11:12:18 2021

@author: pablo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.get_sed import get_from_folder, get_norm, get_norm_wavelength, get_optdepth_norm, get_optdepth_wavelength
from flatten_dict import flatten, unflatten

def iterate_over_dict(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            for pair in iterate_over_dict(value):
                yield (key, *pair)
        else:
            # If value is not dict type then yield the value
            yield (key, value)
                
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
            
            # point source
            point_source = dict()
            
            units = 'pc'
            point_source['positionX'] = '0' +' '+ units
            point_source['positionY'] = '0' +' '+ units
            point_source['positionZ'] = '0' +' '+ units
            
            units = 'km/s'
            point_source['velocityX'] = '0' +' '+ units
            point_source['velocityY'] = '0' +' '+ units
            point_source['velocityZ'] = '0' +' '+ units
            
            point_source['sourceWeight'] = '1'
            point_source['wavelengthBias'] = '0.5'
            
            point_source['angularDistribution'] = {'type':'AngularDistribution',
                                                   'IsotropicAngularDistribution':{}}
            point_source['polarizationProfile'] = {'type':'PolarizationProfile',
                                                   'NoPolarizationProfile':{}}
            
            point_source['sed'] = {'type':'SED',               
                                   'FileSED':{'filename':'input_data/primary_source/Primary_Source_0.stab'}}
            
            point_source['normalization'] = {'type':'LuminosityNormalization',
                                   'SpecificLuminosityNormalization':{
                                       'wavelength':'0.548602 micron',
                                       'unitStyle':'neutralmonluminosity',
                                       'specificLuminosity':'5.247375259612887e+31 erg/s'}
                                           }
            
            Sources['SourceSystem']['sources']['PointSource 001'] = point_source
            
            # continuum sources (several sources sharing the same geometry)
            
            n_sources = 15
            
            #Mario: 0.0 pc is not allowed by skirt
            different_properties = {'geometry':{
                                        'ShellGeometry':{
                                        'minRadius': ['0.01 pc','0.4 pc','0.8 pc','1.2 pc','1.6 pc','2.0 pc','2.4 pc','2.8 pc','3.2 pc','3.6 pc','4.0 pc','4.4 pc','4.8 pc','5.2 pc','5.6 pc'],
                                        'maxRadius': ['0.4 pc','0.8 pc','1.2 pc','1.6 pc','2.0 pc','2.4 pc','2.8 pc','3.2 pc','3.6 pc','4.0 pc','4.4 pc','4.8 pc','5.2 pc','5.6 pc','6.0 pc'], 
                                        'exponent': ['0']*n_sources
                                        }},
                                    'sed':{'FileSED':{'filename':get_from_folder('example_data/gas_regions')}},
                                    'normalization':{'SpecificLuminosityNormalization':{
                                        'wavelength':get_norm_wavelength('example_data/gas_regions', 'nm'),
                                        'specificLuminosity':get_norm('example_data/gas_regions', 'erg/s')}
                                                    }
                                    }
            # example including common values (nonshared values will be filled with 'None')
            template = {'velocityMagnitude':'0 km/s', 'sourceWeight':"1", 'wavelengthBias':"0.5",
                       'geometry':{'type':'Geometry',
                                   'ShellGeometry':{
                                       'minRadius':None, 'maxRadius':None, 'exponent':None
                                                   }
                                  },
                       'sed':{'type':'SED',
                              'FileSED':{'filename':None}
                             },
                       'normalization':{'type':'LuminosityNormalization',
                                        'SpecificLuminosityNormalization':{
                                            'wavelength':'0.548602 micron',
                                        'unitStyle':'neutralmonluminosity',
                                        'specificLuminosity': None}
                                        }
                       }
            
            
            for ii in range(n_sources):            
                source_ii = flatten(template.copy())
                for prop_jj in iterate_over_dict(different_properties):
                    elem = 0
                    keywords = []        
                    while elem < len(prop_jj)-1:
                        keywords.append(prop_jj[elem])            
                        elem += 1
                    #print(prop_jj[-1],tuple(keywords))
                    source_ii[tuple(keywords)] = prop_jj[-1][ii]
                    #Mario: If an error happens with the line above, check that you have the same number of files as n_sources
                    #       I'm not sure if dummy files are allowed because they are going to be overwritten with the correct values before needed.
                                    
                source_ii = unflatten(source_ii)
                # source_ii['kind'] = kind
                number_ii = str(ii+1).zfill(3)
                Sources['SourceSystem']['sources']['GeometricSource {}'.format(number_ii)] = source_ii
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
                                                                     'numWavelengths':'200'
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
            
            # continuum mediums (several mediums sharing the same geometry)
            
            n_media = n_sources
            
            #Mario: 0.0 pc is not allowed by skirt
            different_properties = {'geometry':{
                                        'ShellGeometry':{
                                        'minRadius': ['0.01 pc','0.4 pc','0.8 pc','1.2 pc','1.6 pc','2.0 pc','2.4 pc','2.8 pc','3.2 pc','3.6 pc','4.0 pc','4.4 pc','4.8 pc','5.2 pc','5.6 pc'],
                                        'maxRadius': ['0.4 pc','0.8 pc','1.2 pc','1.6 pc','2.0 pc','2.4 pc','2.8 pc','3.2 pc','3.6 pc','4.0 pc','4.4 pc','4.8 pc','5.2 pc','5.6 pc','6.0 pc'], 
                                        'exponent': ['0']*n_media
                                        }},
                                    'materialMix':{'MeanFileDustMix':{'filename':get_from_folder('example_data/gas_props')}},
                                    'normalization':{'OpticalDepthMaterialNormalization':{
                                        'wavelength':get_optdepth_wavelength('example_data/gas_props','nm'),
                                        'opticalDepth':get_optdepth_norm('example_data/gas_props')}
                                                    }
                                    }
            # example including common values (nonshared values will be filled with 'None')
            template = {
                       'velocityMagnitude':'0 km/s', 'magneticFieldStrength':'0 uG',           
                       'geometry':{'type':'Geometry',
                                   'ShellGeometry':{
                                       'minRadius':None, 'maxRadius':None, 'exponent':None
                                                   }
                                  },
                       'materialMix':{'type':'MaterialMix',
                              'MeanFileDustMix':{'filename':None}
                             },
                       'normalization':{'type':'MaterialNormalization',
                                        'OpticalDepthMaterialNormalization':{
                                                                    'axis':'X',
                                                            'wavelength':'0.548602 micron',
                                                            'opticalDepth':None,                            
                                                                            }
                                        }
                       }
                        
            for ii in range(n_media):            
                medium_ii = flatten(template.copy())
                for prop_jj in iterate_over_dict(different_properties):
                    elem = 0
                    keywords = []        
                    while elem < len(prop_jj)-1:
                        keywords.append(prop_jj[elem])            
                        elem += 1
                    #print(prop_jj[-1])
                    medium_ii[tuple(keywords)] = prop_jj[-1][ii]
                    #Mario: It has the same issues as sources_ii
                                    
                medium_ii = unflatten(medium_ii)    
                number_ii = str(ii+1).zfill(3)
                Media['MediumSystem']['media']['GeometricMedium {}'.format(number_ii)] = medium_ii           
              
                
            units = ' pc'    
            Media['MediumSystem']['grid'] = {'type':'SpatialGrid',
                               'Cylinder2DSpatialGrid': {'maxRadius':'100'+units, 
                                                         'minZ':'-100'+units,
                                                         'maxZ':'100'+units,
                                                         'meshRadial':{'type':'Mesh',
                                                                       'LinMesh':{'numBins':200}},
                                                         'meshZ':{'type':'MoveableMesh',
                                                                  'LinMesh':{'numBins':100}}
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
                    'numWavelengths':'200'}
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
                                                                       'numWavelengths':'200'
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
                                     'numWavelengths':'200'
                                                          }
                                     }
                                    },
                'SpatialGridConvergenceProbe 1':{'probeName':"conv",
                                                 'wavelength':"0.55 micron"
                                                 },
                'RadiationFieldAtPositionsProbe 1':{
                    'probeName':"nuJnu",
                    'filename':"input_data/MeanIntensity_Positions.txt",
                    'useColumns':"",
                    'writeWavelengthGrid':"false"
                                                },
                'InstrumentWavelengthGridProbe 1':{'probeName':"grid"},    
                'RadiationFieldWavelengthGridProbe 1':{'probeName':"radGrid"}                        
                        }
                }    
            self.Probes = Probes
