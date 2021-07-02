# This module includes the basic geometry classes for building the source/medium classes and the corresponding parameters needed to implement them.

# Geometry hierarchy 
# TODO: Complete all geometry classes
geometry ={
        'AxGeometry':{
            'ConicalShellGeometry':{},
            'HyperboloidGeometry':{},
            'HyperboloidShellGeometry':{},
            'MultiGaussianExpansionGeometry':{},
            'ParaboloidGeometry':{},
            'ParaboloidShellGeometry':{},
            'SepAxGeometry':{
                'BrokenExpDiskGeometry':{},
                'ExpDiskGeometry':{},
                'RingGeometry':['ringRadius', 'width', 'height']
                },
            'SpheroidalGeometryDecorator':{},
            'TorusGeometry':{}
            },
        'ClipGeometryDecorator':{},
        'CombineGEometryDecorator':{},
        'GenGeometry':{},
        'OffsetGeometryDecorator':{},
        'SpheGeometry':{
            'SersicGeometry':[],
            'GaussianGeometry':[],
            'ShellGeometry':['minRadius', 'maxRadius', 'exponent']
                }
        }
