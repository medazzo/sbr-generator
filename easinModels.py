#!/usr/bin/python
# # -*- coding: utf-8 -*-

# Copyright (C) 2019 EASYSOFT-IN
# All rights exclusively reserved for EASYSOFT-IN,
# unless otherwise expressly agreed.

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# This file contains class for easin generator with some checkers helpers
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from enum import Enum, unique
import coloredlogs, logging

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Helper Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Helper:
    # Create a logger object.
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG',
                        logger=logger,
                        fmt='%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s')

    def __init__(self):
        logger.debug("= = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        logger.info(" - - - Testing color")
        logger.warning(" - - - Testing color")
        logger.error(" - - - Testing color")
        logger.critical(" - - - Testing color")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Project Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Project:
    """ A Project definition class"""
    Service_prepend         = "Service"    
    Controller_prepend      = "Controller"
    Repository_prepend      = "Repository"

    Security_folder         = "security"
    Entities_folder         = "entities"
    Repositories_folder     = "repositories"
    Exceptions_folder       = "exceptions"
    Controllers_folder      = "controllers"
    Services_folder         = "services"

    ApiPrefix                = "/api/"

    JAVA_Dir                = "/src/main/java/"
    Test_Dir                = "/src/test/java/"
    Resources_Dir           = "/src/main/resources/"
    def __init__(self, projectConf=None):
        self.projectConf = projectConf
        if "name" not in self.projectConf:
            Helper.logger.critical('project must have name !.')
            raise TypeError('project must have name !.')
        self.name = self.projectConf['name']
        if "package" not in self.projectConf:
            Helper.logger.critical('project must have package !.')
            raise TypeError('project must have package !.')
        self.package = self.projectConf['package']
        if "version" not in self.projectConf:
            Helper.logger.critical('project must have version !.')
            raise TypeError('project must have version !.')
        self.version = self.projectConf['version']
        if "longname" not in self.projectConf:
            Helper.logger.critical('project must have longname !.')
            raise TypeError('project must have longname !.')
        self.longname = self.projectConf['longname']
        if "description" not in self.projectConf:
            Helper.logger.critical('project must have description !.')
            raise TypeError('project must have description !.')
        self.description = self.projectConf['description']
        if "url" not in self.projectConf:
            Helper.logger.critical('project must have url !.')
            raise TypeError('project must have url !.')
        self.url = self.projectConf['url']
        if "restPath" not in self.projectConf:
            Helper.logger.critical('project must have restPath !.')
            raise TypeError('project must have restPath !.')
        self.restPath = self.projectConf['restPath']
        self.securityRoles = []
        if "extraroles" in self.projectConf["security"]:
            roles = self.projectConf['security'] ['extraroles']            
            for r in roles: 
                if r.upper().startswith ("ROLE") :
                    Helper.logger.critical('Role string must not  start with ROLE !.')
                    raise TypeError('Role string must not  start with ROLE !.')
                self.securityRoles.append(r.upper())
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Logger Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Logger:
    """ A Logger definition class"""
    def __init__(self, name=None, level=None):
        self.name = name
        self.level = level

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Database Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Database:
    """ A Database definition class"""
    def __init__(self, url=None, dialect=None, driverClassName=None, username=None, password=None, ddlauto=None):
        self.url = url
        self.dialect = dialect
        self.driverClassName = driverClassName
        self.username = username
        self.password = password
        self.ddlauto = ddlauto

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Field Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Field:
    """ A Fields definition class"""
    def __init__(self, name=None, type="String", comment=None, annotations=list()):
        if not isinstance(annotations, list):
            Helper.logger.critical('annotations must be a list of strings: '+annotations+'  !.' )
            raise TypeError('annotations must be a list of strings: '+annotations+'  !.' )
        self.name = name
        self.type = type
        self.foreignKey= False
        self.foreignEntity= None
        self.comment = comment
        self.annotations = annotations

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Configuration Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Configuration():
    """ A Configuration definition class"""
    def __init__(self, project=None, config=None):
        self.project = project
        self.name=project.name
        self.RootLoggerLevel = config['logging']['RootLoggerLevel']
        self.Loggers = list()
        for fi in config['logging']['Loggers']:
            f = Logger(fi['name'], fi['level'])
            self.Loggers.append(f)
        Helper.logger.info("> > {} Loggers  has been Analysed .".format(len(self.Loggers)))
        # Setup extra DB  params
        self.databaseProd = Database(config['database']['prod']['url'], config['database']['prod']['dialect'],
                                    config['database']['prod']['driverClassName'], config['database']['prod']['username'],
                                    config['database']['prod']['password'], config['database']['prod']['ddlauto'])
        self.databaseDev = Database(config['database']['dev']['url'], config['database']['dev']['dialect'],
                                    config['database']['dev']['driverClassName'], config['database']['dev']['username'],
                                    config['database']['dev']['password'], config['database']['dev']['ddlauto'])
        self.databaseTest = Database(config['database']['test']['url'], config['database']['test']['dialect'],
                                    config['database']['test']['driverClassName'], config['database']['test']['username'],
                                    config['database']['test']['password'], config['database']['test']['ddlauto'])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Entity Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Entity():
    """ A Entity definition class"""
    def __init__(self, project, name=None, comment=None,  fieldsconfig=list()):
        self.project = project
        self.name = name[0].upper()+name[1:]
        self.fields = list()
        self.fieldsconfig = fieldsconfig
        self.comment = comment
        if not isinstance(fieldsconfig, list):
            Helper.logger.critical('fields must be a list of Field')
            raise TypeError('fields must be a list of Field')
        Helper.logger.info("> Analysing Entity {} ..".format(self.name))
        for fi in self.fieldsconfig:
            f =  Field(fi['name'], fi['type'],fi['comment'], fi['annotations'])
            self.fields.append(f)            
        Helper.logger.debug("> > {} Field's  has been Analysed .".format(len(self.fields)))
    
    """ Function will loop into fields and replace entity name by id """
    def checkforLinks(self, othersEntitys):
        Helper.logger.debug("> > {} Rechecking Fields for links to others entity.".format(len(self.fields)))
        for field in self.fields:
            for ent in othersEntitys:
                if ent.name == field.type :
                    Helper.logger.warn("> > Entity {} , Field {} is having relation with Entity {} .. Updating ..".format(self.name ,field.name, field.type))
                    field.foreignKey= True
                    field.foreignEntity= ent.name

