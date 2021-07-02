# PIGS (Python Interface for Generating .ski fileS)

## Overview

This set of scripts allow to build .ski files for running SKIRT (a radiative transfer code) with a large number of sources (with different built-in geometries and/or spectral energy distirbutions). 

Current version is supported under SKIRT 9.
 
### Requirements 

The user must have installed the following python packages:

```
importlib
glob
numpy
os
```

### Basic instructions

Once all the requested parameters are included on a configuration file .py (see ski_params.py for an example) the user will have to create an SkirtFile object. 

This can be done on a separated python script as follows:

```
from pigs import SkirtFile

my_skirtfile = SkirtFile('my_params_config_file_name', output='path_to_folder/filename')
```

Then a .ski file will be created with the name and location provided that can be run on command line:
```
cd path_to_folder/
skirt filename
```

### Configuration files

Following the SKIRT architecture the user must fill the following configuration files

- sources.py (indicating the different sources of radiation)
- medium.py (the medium could be just dust models or interstellar gas)
- basics.py (basic parameters for running the simulation including the instruments and output probes)

