#!/usr/bin/python
# # -*- coding: utf-8 -*-

# Copyright (C) 2019 EASYSOFT-IN
# All rights exclusively reserved for EASYSOFT-IN,
# unless otherwise expressly agreed.

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# This file contains class for easin config loader and analyser
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from enum import Enum, unique
import yaml
import pprint
from easinModels import Entity, Configuration
from easinModels import Project
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Analyser Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Analyser:
    """A Analyser checkers and helps class"""
    def __init__(self, project=None, config=None):
        if not isinstance(project, Project):
            raise TypeError('project must be of Project type !.')
        self.Configuration = Configuration(project, config)
        self.AllEntities = list()
        for ent in config['entities']:
            e = Entity(project, ent['name'], ent['comment'], ent['fields'])
            self.AllEntities.append(e)
        # re-checks for links
        for ent in self.AllEntities:
            ent.checkforLinks(self.AllEntities)
        print("{} Entities  has been Analysed .".format(len(self.AllEntities)))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  ConfigLoader Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class ConfigLoader:
    """A Configuration loader  class"""
    """ configfile : the path of configuration file """

    def __init__(self, configfile=None, verbose=False):
        if not configfile:
            raise TypeError('configfile  must be non null')
        # Setup params
        self.configuration = None
        self.verbose = verbose
        self.file = None
        self.configfile = configfile
        try:
            self.file = open(self.configfile, 'r')
        except FileNotFoundError:
            raise FileNotFoundError("Wrong file or file path for config file @ {} ".format(self.configfile))
        self.configuration = yaml.safe_load(self.file)
        pp = pprint.PrettyPrinter(indent=4)
        self.project = Project(self.configuration['project']['name'], self.configuration['project']['package'],
                               self.configuration['project']['version'], self.configuration['project']['longname'],
                               self.configuration['project']['description'], self.configuration['project']['url'],
                               self.configuration['project']['restPath']);
        print("Config  loaded correctly ..")
        if self.verbose: pp.pprint(self.configuration)
