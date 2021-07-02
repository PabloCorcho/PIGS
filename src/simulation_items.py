# Geometry items
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
            'ShellGeometry':['minRadius', 'maxRadius', 'exponent

                ']
                }
        }

# Angular distribution used to describe the anisotropic distribution of a point source

angular_distribution = {
        'AxAngularDistribution':['ConicalAngularDistribution', 'LaserAngularDistribution', 'NetzerAngularDistribution'],
        'IsotropicAngularDistribution':None,
        }
