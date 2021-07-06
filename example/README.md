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
	- Generating individual sources. When trying to generate specific sources that will consist of a single class, the user must create a dictionary containing all the properties requered for that source. Once the dictionary is built, the user must include it to the Sources dictionary:
	```
	my_source = dict()
	
	my_source['param_i'] = 'foo'
	
	"""All the parameters are set...""
	
	Sources['SourceSystem']['sources']['KIND_OF_SOURCE NUMBER'] = my_source
	```
		
