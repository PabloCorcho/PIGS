# This module includes the basic instruction for constructing the source items when creating the .ski file

# The basic hierarchy of the SKIRT built-in sources 
source = {
    'ImportedSource':{
        'CellSource':{},
        'MeshSource':{},
    'ParticleSource':{}},
        'NormalizedSource':{
            'GeometricSource':{},
            'SpecialtySource':{
                'CenteredSource':{
                    'CubicalBackgroundSource':{},
                    'SphericalBackgroundSource':{},
                    'StellarSurfaceSource'},
                'PointSource':{}}}
            }

class Source(object):
    pass

class ImportedSource(Source):
    raise NameError('Not implemented yet')

################################
# Normalized class and subclasses
################################

class NormalizedSource(Source):
    def __init__(self, params):
        pass

# Geometric sources 

class GeometricSource(NormalizedSource):
    pass


# Sr. Krtxo
