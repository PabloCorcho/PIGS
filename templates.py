#I'm writing here some templates for different geometries in skirt.
#These lines are meant to be replaced in the main code if a different geometry is desired.

#####################
#SOURCES
#####################

### POINT SOURCES ###
point_source_template = {'PointSource':{ #This line indicates the type of source it is. Inside this dictionary you have ALL parameters needed for that source
		            'positionX': ['0 pc'], #All lists here must have length equal to 'n_stellarZones' (in this case, you only have 1 stellar zone)
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
		                'FileSED':{'filename':get_from_folder('input_data/primary_source')}}, #Here a link to your folder, starting from the folder where the script is run
		            'normalization':{
		                'type':'LuminosityNormalization',
		                'SpecificLuminosityNormalization':{
		                        'wavelength':get_norm_wavelength('input_data/primary_source', 'nm'), #It will check the third line of 'fileSED', check if units are correct in your file
		                        'unitStyle':'neutralmonluminosity',
		                        'specificLuminosity':get_norm('input_data/primary_source', 'erg/s')} #It will check the fourth line of 'fileSED', check if units are correct in your file
		                }
		            }
                    }

### SHELL SOURCES ###
shell_source_template = {'GeometricSource':{ #This line indicates the type of source it is. Inside this dictionary you have ALL parameters needed for that source
		                'velocityMagnitude':'0 km/s', 
		                'sourceWeight':"1", 
		                'wavelengthBias':"0.5",
		                
		                'geometry':{
		                    'type':'Geometry',
		                    'ShellGeometry':{
				            'minRadius': minRadius_list, #All lists (here labelled as a variable) here must have length equal to 'n_gasSources'. 
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
		                            'wavelength':get_norm_wavelength('input_data/gas_regions', 'nm'), #It will check the third line of 'fileSED', check if units are correct in your file
		                            'unitStyle':'neutralmonluminosity',
		                            'specificLuminosity':get_norm('input_data/gas_regions', 'erg/s')} #It will check the fourth line of 'fileSED',check if units are correct in your file
		                    }
		                }
		            }

#####################
#MEDIA
#####################
### SHELL MEDIA ###
shell_medium_template = {'GeometricMedium':{ #This line indicates the type of medium it is. Inside this dictionary you have ALL parameters needed for that medium
                                'velocityMagnitude':'0 km/s', 
                                'magneticFieldStrength':'0 uG',
                                
                                'geometry':{
                                    'type':'Geometry',
                                    'ShellGeometry':{
                                    'minRadius': minRadius_list, #All lists (here labelled as a variable) here must have length equal to 'n_gasSources'. 
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
                                            'mass':get_mass_norm('input_data/gas_props','Msun') #It will check the third line of 'MeanFileDustMix', check if units are correct in your file
                                    }
                                }
                            }
                        }
