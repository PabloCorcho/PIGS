#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 15:20:20 2021

@author: pablo
"""

import importlib
from glob import glob
from numpy import sort

class SkirtFile(object):
    """
    This class generates basic .ski files for running SKIRT models with
    built-in geometry configurations. 
    
    input: SKIRTparams (class specifying on a given )
    """
    
    
    def __init__(self, config_file_path, output_path=None):
        self.config_file = config_file_path                
        self.params = self.read_config()
        if output_path:        
            self.skifile = open(output_path, 'w+')
        else:
            self.skifile = open('skirt_config_file.ski', 'w+')
            
        self.skifile.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<!-- A SKIRT parameter file created with pySkirt -->\n'
            )                

        self.make_basics()
        self.make_sources()
        self.make_medium()
        self.make_instruments()
        self.make_probes()
        
        self.skifile.write(             
        '    </MonteCarloSimulation>\n</skirt-simulation-hierarchy>'
                            )

        
    def read_config(self):
        cfg = importlib.import_module(self.config_file)        
        return cfg
    def make_basics(self):
        self.basic_lines =  [
    '<skirt-simulation-hierarchy type="MonteCarloSimulation" format="9" producer="SKIRT v9.0" time="---">',
    '    <MonteCarloSimulation '+'userLevel="{}" simulationMode="{}" numPackets="{}">'.format(
        self.params.Basics['userLevel'],
        self.params.Basics['simulationMode'],
        self.params.Basics['numPackets']),
    '        <random type="Random">',
    '            <Random seed="0"/>',
    '        </random>',
    '        <units type="Units">',
    '            <{} fluxOutputStyle="{}"/>'.format(
        self.params.Basics['units'],
        self.params.Basics['fluxOutputStyle']),
    '        </units>',
    '        <cosmology type="Cosmology">',
    '            <LocalUniverseCosmology/>',
    '        </cosmology>'
    ]
    
        for line in self.basic_lines:
            self.skifile.write(line+'\n')
        
    def make_sources(self):
        self.source_lines = [
    '        <sourceSystem type="SourceSystem">',
    '            <SourceSystem minWavelength="{}" maxWavelength="{}" wavelengths="{}" sourceBias="{}">'.format(
        self.params.Sources['SourceSystem']['minWavelength'],
        self.params.Sources['SourceSystem']['maxWavelength'],
        self.params.Sources['SourceSystem']['wavelengths'],
        self.params.Sources['SourceSystem']['sourceBias']),
    '                <sources type="Source">'
                ]
        
        
        self.sources_sed_paths = sort(
            glob(self.params.Sources['SED']['folder']+'/*'))
        
        for ii in range(self.params.Sources['n_sources']):
            self.source_lines.append(
                '                    <GeometricSource velocityMagnitude="0 km/s" sourceWeight="1" wavelengthBias="0.5">'
                                     )
            self.source_lines.append('                        <geometry type="Geometry">')
            self.source_lines.append('                            <RingGeometry ringRadius="{}" width="{}" height="{}"/>'.format(
                self.params.Sources['Geometry']['ringRadius'][ii]+' '+self.params.Sources['Geometry']['units'],
                self.params.Sources['Geometry']['width'][ii]+' '+self.params.Sources['Geometry']['units'],
                self.params.Sources['Geometry']['heigh'][ii]+' '+self.params.Sources['Geometry']['units']))
            self.source_lines.append('                        </geometry>')
            self.source_lines.append('                        <sed type="SED">')
            self.source_lines.append('                            <FileSED filename="{}"/>'.format(self.sources_sed_paths[ii]))
            self.source_lines.append('                        </sed>')
            self.source_lines.append('                        <normalization type="{}">'.format(
                self.params.Sources['SED']['normalization']['type']))
            self.source_lines.append('                            <SpecificLuminosityNormalization wavelength="{}"'.format(
                self.params.Sources['SED']['normalization']['wavelength']))
            self.source_lines.append('unitStyle="{}" specificLuminosity="{}"/>'.format(
                self.params.Sources['SED']['normalization']['unitStyle'],
                self.params.Sources['SED']['normalization']['specificLuminosity']))
            self.source_lines.append('                        </normalization>')
            self.source_lines.append('                        <wavelengthBiasDistribution type="{}">'.format(
                self.params.Sources['SED']['wavelengthBiasDistribution']['type']))            
            self.source_lines.append('                            <LogWavelengthDistribution minWavelength="{}" maxWavelength="{}"/>'.format(
                self.params.Sources['SED']['wavelengthBiasDistribution']['LogWavelengthDistribution']['minWavelength'],
                self.params.Sources['SED']['wavelengthBiasDistribution']['LogWavelengthDistribution']['maxWavelength']))
            self.source_lines.append('                        </wavelengthBiasDistribution>')
            self.source_lines.append('                    </GeometricSource>')            
            
        self.source_lines.append('                </sources>')
        self.source_lines.append('            </SourceSystem>')
        self.source_lines.append('        </sourceSystem>')        
        for line in self.source_lines:
            self.skifile.write(line+'\n')
                    
    def make_medium(self):
        pass
    def make_instruments(self):
        
        self.inst_lines = [
            '        <instrumentSystem type="InstrumentSystem">',
            '            <InstrumentSystem>',
            '                <defaultWavelengthGrid type="WavelengthGrid">']
        self.inst_lines.append('                    <LogWavelengthGrid minWavelength="{}" maxWavelength="{}" numWavelengths="{}"/>'.format(
            self.params.Instruments['InstrumentSystem']['minWavelength'],
            self.params.Instruments['InstrumentSystem']['maxWavelength'],
            self.params.Instruments['InstrumentSystem']['numWavelengths']))
        self.inst_lines.append('                </defaultWavelengthGrid>')
        
        self.inst_lines.append('                <instruments type="Instrument">')
        for key_i in list(self.params.Instruments['instruments'].keys()):
            instrument_i = self.params.Instruments['instruments'][key_i]
            instrument_i_keys = list(instrument_i.keys())            
            instrument_details = '<{} '.format(instrument_i['type'])
            for key_j in instrument_i_keys[1:]:
                instrument_details += key_j+'='+'"{}" '.format(instrument_i[key_j])
                
            # self.inst_lines.append('                    <{} instrumentName="{}" distance="{}" inclination="{}" azimuth="{}" roll="{}" radius="{}" recordComponents="{}" numScatteringLevels="{}" recordPolarization="{}" recordStatistics="{}">'.format(
            #     self.params.Instruments['instruments'][key_i]['type'],
            #     self.params.Instruments['instruments'][key_i]['instrumentName'],
            #     self.params.Instruments['instruments'][key_i]['distance'],
            #     self.params.Instruments['instruments'][key_i]['inclination'],
            #     self.params.Instruments['instruments'][key_i]['azimuth'],
            #     self.params.Instruments['instruments'][key_i]['roll'],
            #     self.params.Instruments['instruments'][key_i]['radius'],
            #     self.params.Instruments['instruments'][key_i]['recordComponents'],
            #     self.params.Instruments['instruments'][key_i]['numScatteringLevels'],
            #     self.params.Instruments['instruments'][key_i]['recordPolarization'],
            #     self.params.Instruments['instruments'][key_i]['recordStatistics'],))
            instrument_details += '/>'
            self.inst_lines.append(instrument_details)            
        
        self.inst_lines.append('                </instruments>')
        self.inst_lines.append('            </InstrumentSystem>')
        self.inst_lines.append('        </instrumentSystem>')            
            
        for line in self.inst_lines:
            self.skifile.write(line+'\n')
                    
    def make_probes(self):
        pass
    
# ...

if __name__ == '__main__':
    skirtfile = SkirtFile('ski_params')