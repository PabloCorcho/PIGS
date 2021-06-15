#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 15:20:20 2021

@author: pablo
"""

import importlib
from glob import glob
from numpy import sort
from os import path, getcwd

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
            output = output_path
        else:
            output = path.join(getcwd(), 'skirt_config_file.ski')
            
        self.skifile = open(output, 'w+')
            
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

        print('File saved at ', output)
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
        
        
        # self.sources_sed_paths = glob(self.params.Sources['SED']['folder']+'/*')
        # print(self.sources_sed_paths)
        for ii in range(self.params.Sources['n_sources']):
            source_sed_path = path.join(self.params.Sources['SED']['folder'], 
                                        '{}.dat'.format(ii+1))            
            with open(source_sed_path, 'r') as f:
                all_lines = f.readlines()                
                norm_wavelength = float(all_lines[2].split(' ')[3])
                normalization = float(all_lines[3].split(' ')[2])
                print(ii, normalization, norm_wavelength)
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
            self.source_lines.append('                            <FileSED filename="{}/{}.dat"/>'.format(
                self.params.Sources['SED']['folder'], ii+1))
            self.source_lines.append('                        </sed>')
            self.source_lines.append('                        <normalization type="{}">'.format(
                self.params.Sources['SED']['normalization']['type']))
            self.source_lines.append('                            <SpecificLuminosityNormalization wavelength="{} Angstrom"'.format(
                norm_wavelength))
            self.source_lines.append('unitStyle="{}" specificLuminosity="{} {}"/>'.format(
                self.params.Sources['SED']['normalization']['unitStyle'],
                normalization,
                self.params.Sources['SED']['normalization']['unit']))
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
                            
            instrument_details += '/>'
            self.inst_lines.append(instrument_details)            
        
        self.inst_lines.append('                </instruments>')
        self.inst_lines.append('            </InstrumentSystem>')
        self.inst_lines.append('        </instrumentSystem>')            
            
        for line in self.inst_lines:
            self.skifile.write(line+'\n')
                    
    def make_probes(self):
        self.probe_lines = [
            '        <probeSystem type="ProbeSystem">',
            '            <ProbeSystem>',
            '                <probes type="Probe">',
            
            ]
        
        for key_i in list(self.params.Probes['probes'].keys()):
            probe_i = self.params.Probes['probes'][key_i]
            probe_i_keys = list(probe_i.keys())            
            probe_details = '<{} '.format(probe_i['type'])
            print(probe_details)
            for key_j in probe_i_keys[1:]:
                print(key_j)
                if key_j=='wavelengthGrid':
                    probe_details += '>\n                        <wavelengthGrid type="WavelengthGrid">'
                    probe_details += '\n                            <LogWavelengthGrid minWavelength="{}" maxWavelength="{}"  numWavelengths="{}" '.format(
                        probe_i[key_j]['minWavelength'],
                        probe_i[key_j]['maxWavelength'],
                        probe_i[key_j]['numWavelengths']
                        )
                    probe_details +='/>\n                        </wavelengthGrid>'
                    # probe_details += '{}/>'.format(probe_i['type'])
                else:
                    probe_details += key_j+'='+'"{}" '.format(probe_i[key_j])                            
                    # probe_details += '/>'
            
            if probe_i['type']=='InstrumentWavelengthGridProbe':
                probe_details += '/>'                
            elif probe_i['type']=='LuminosityProbe':
                probe_details += '\n                    </LuminosityProbe>'                            
            self.probe_lines.append(probe_details)            
            
        self.probe_lines.append('                </probes>')
        self.probe_lines.append('            </ProbeSystem>')
        self.probe_lines.append('        </probeSystem>')            
            
        for line in self.probe_lines:
            self.skifile.write(line+'\n')
        
# ...

if __name__ == '__main__':
    skirtfile = SkirtFile('ski_params', 
                          output_path='../test1/skirt_config_file.ski')