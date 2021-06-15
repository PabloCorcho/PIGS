# PIGS (Python Interface for Generating .ski fileS)

## Overview

This set of scripts allow to build .ski files for running SKIRT (a radiative transfer code) with a large number of sources (with different built-in geometries and/or spectral energy distirbutions). 

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

my_skirtfile = SkirtFile('my_params_config_file_name', output='path/to/storing/folder')
```

Then a .ski file will be created with the name and location provided.
