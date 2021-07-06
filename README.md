# Python Interface for Generating .ski fileS (PIGS)

## Overview

This code allows to build and run complex models of SKIRT (https://skirt.ugent.be/root/_landing.html) based on built-in geometry classes.

### Installation and python dependencies

First, download to your local folder the code
```
git clone https://github.com/PabloCorcho/PIGS
cd PIGS
```
Then, check that the following packages are installed 
```
os
numpy
flatten_dict
glob
```

# Basic tutorial

In this simple tutorial you will learn how to generate .ski files by using PIGS. 

## Understanding SKIRT

The elements for running SKIRT can be divided into five different classes:

- **Simulation properties**
	- Number of launched photons. 
	- Simulation mode: Only extinction, secondary emission from dust, etc... (only tested using 'simulationMode':"ExtinctionOnly").
	- Units.
	- Cosmology.

- **Photon sources**
	- Sources with built-in geometries (e.g. shell, ring, point).
	- Sources coming from snapshots.
- **Media sources**
	- Media with built-in geometries (e.g. shell, ring, point).
	- Media coming from snapshots.
- **Instruments**
	- How the resulting emission is stored.
- **Probes**
	- Some additional parameters can be stored as "probes" for further sanity checks or deeper physical analysis.

## Creating the input parameter file

The best way to create a .ski configuration file is using the one provided in this example as template. 

PIGS uses nested dictionaries to build the XML configuration file. WARNING: It is extremelly important to keep the hierarchy of each dictionary as reported by SKIRT doc (https://skirt.ugent.be/skirt9/annotated.html).

- **Basics** 

This dictionary contains all the parameters relevant for writing the *Simulation properties*. 

- **Sources**
	- Generating individual sources. 
	
	When trying to generate specific sources that will consist of a single class, the user must create a dictionary containing all the properties requered for that source. 
	```
	my_source = dict()
	
	my_source['param_i'] = 'foo'
	
	"""All the parameters are set...""
	```
	Once the dictionary is built, the user must include it to the Sources dictionary within the sources nested-dict:
	```
	Sources['SourceSystem']['sources']['KIND_OF_SOURCE NUMBER'] = my_source
	```
	It is crucial that the keyword set for denoting this new sources corresponds to the specific kind of source according to SKIRT, followed always by a number. For example, if I would like to include a point-like source, you should use the following syntax:
	```
	Sources['SourceSystem']['sources']['PointSource 1'] = my_point_source
	```
	
	- Generating sequences of source.
	
	It is also possible to include a set of sources that share several properties (e.g. geometrical distribution) but presenting some specific differences. In this case the code will require the user to declare the number of sources and two dictionaries: a template source dictionary (including all the properties required for SKIRT) and a dictionary containing those properties that differ from one source to another. 
	
	For example, if we would like to model a set of sources consisting of concentric sphericall shells we must define the following *template* dictionary:
	```
	shell_template = {'velocityMagnitude':'0 km/s', 'sourceWeight':"1", 'wavelengthBias':"0.5",
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
                                'wavelength':None,
                            'unitStyle':'neutralmonluminosity',
                            'specificLuminosity': None}
                            }
           }
	```
	In this case the template items common for all the individual sources are filled with the corresponding value whereas those items that will vary are set to `None`.
	
	Now we declare the dictionary containing the individual features. 
	
	```
	n_sources = 5
	
	different_properties = {'geometry':{
                            'ShellGeometry':{
                            'minRadius': ['0.1 pc', '20 pc', '40 pc', '60 pc', '80 pc'],
                            'maxRadius': ['20 pc', '40 pc', '60 pc', '80 pc', '100 pc'], 
                            'exponent': ['0']*5
                            }},
                        'sed':{'FileSED':{'filename':get_from_folder('example_data/gas_regions')}},
                        'normalization':{'SpecificLuminosityNormalization':{
                            'wavelength':get_norm_wavelength('example_data/gas_regions', 'nm'),
                            'specificLuminosity':get_norm('example_data/gas_regions', 'erg/s')}
                                        }
                        }
	```
	
	By default, there is always one single value for each key in every dictionary, therefore the code will interpret *lists or arrays* as sets of *different sources*. 
	
	In addition, in this particular example the functions
	```
	get_from_folder('path')
	get_norm_wavelength('path', 'units')
	get_norm_wavelength('path', 'units')
	```
	are used to set the corresponding SEDs, normalization and normalization wavelength for every source within an specific folder.
	
	**Warning** It is important to include the kind of source (i.e. `"GeometricSource"`) at the loop responsible for including each source (line 137 of current ski_params.py).  
	
- **Media**
	Similar to **Sources**
	
- **Instruments**

- **Probes**
 
## Calling PIGS

Once the parameter file is created, simply import the `pigs` module from src and create and object `SkirtFile`. 	
	
	
	
