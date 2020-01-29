#!/usr/bin/python
# # -*- coding: utf-8 -*-

# Copyright (C) 2019 EASYSOFT-IN
# All rights exclusively reserved for EASYSOFT-IN,
# unless otherwise expressly agreed.

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# This file contains class for easin Args Manager
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys, argparse
from easinAnalyser import ConfigLoader, Analyser
from easinModels import Project, Helper
import pprint, os, shutil
import jinja2
from jinja2 import Environment, BaseLoader
from easinTemplates import templates
DefaultOutput_Dir = "./tmp-out"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Generator Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Generator:
    """A Generator   class"""
    Entity_Template         = "entity.java"
    EntityRepo_Template     = "Repository.java"
    Controller_Template     = "controller.java"
    Authorities_Template    = "AuthoritiesConstants.java"
    log4j2_Template         = "log4j2.xml"
    pom_Template            = "pom.xml"
    properties_Template     = "application.yaml"
    application_Template    = "Application.java"
    logginFilter_Template   = "RequestLoggingFilterConfig.java"
    SwaggerConfig_Template  = "SwaggerConfiguration.java"
    webInitializer_Template = "WebInitializer.java"
    BaseEntity_Template     = "BaseEntity.java"
    IController_Template    = "icontroller.java"
    IService_Template       = "IService.java"
    Service_Template        = "Service.java"
    ExceptionBad_Template   = "ResourceBadParameterException.java"
    ExceptionNot_Template   = "ResourceNotFoundException.java"
    ErrorControl_Template   = "MyErrorController.java"
    StatusControl_Template  = "StatusController.java"
    READMEFILE_Template     = "README.md"
    CrudTest_Template       = "CrudUnitTest.java"
    HelperTests_Template    = "HelperTests.java"

    Template_Dir            = "templates"
    def __init__(self, outputDir=None, verbose=False, tests=False, security=True, project = None,entities=list(), conf=None):
        # Setup some params        
        if not isinstance(project, Project):
            Helper.logger.critical('project must be of Project type !.')
            raise TypeError('project must be of Project type !.')
        if not outputDir:
            Helper.logger.critical('The output Dir  must be non null')
            raise TypeError('The output Dir  must be non null')
        self.__project = project
        self.outputDir = outputDir
        self.verbose = verbose
        self.tests = tests
        self.security = security
        self.entities = entities
        self.controllers = list()
        self.configuration = conf        
        # check output Directory
        if self.outputDir is DefaultOutput_Dir:
            self.outputDir = './' + self.__project.name + '-' + self.__project.version
        # clean folder Output directory
        if os.path.exists(self.outputDir) and os.path.isdir(self.outputDir):
            shutil.rmtree(self.outputDir)
        # Re create folders
        os.makedirs(self.outputDir + Project.JAVA_Dir)
        self.__srcdir = self.outputDir + Project.JAVA_Dir + self.__project.package.replace(".", "/")
        os.makedirs(self.outputDir + Project.Resources_Dir)
        self.__testdir = self.outputDir + Project.Test_Dir + self.__project.package.replace(".", "/")        
        os.makedirs(self.__testdir)        
        #  prepare template loader
        self.__pathTemplate = os.getcwd() + "/" + Generator.Template_Dir
        loader = jinja2.FileSystemLoader(searchpath=self.__pathTemplate)
        self.templateEnv = jinja2.Environment(loader=loader)

    def GenerateAll(self):
        Helper.logger.info("Generate Base ==>   ")
        self.__GenerateBase()
        Helper.logger.info("Generate Entities ==>   ")
        self.__GenerateEntity()    
        Helper.logger.info("Generate configurations ==>   ")
        self.__GenerateConfiguration()
        if self.tests:
            Helper.logger.info("Generate tests ==>   ")
            self.__GenerateTests()
        if self.security:
            Helper.logger.info("Generate Security ==>   ")
            self.__GenerateSecurity()

    def __GenerateEntity(self):              
        #loop in entities
        for ent in self.entities:            
            # Generate
            Helper.logger.debug("> Generating Classes for Entity {} .".format(ent.name))
            output = self.templateEntity.render(package=self.__project.package+"."+Project.Entities_folder,entity=ent).encode("utf-8")
            f = open(self.entityDirs+'/'+ent.name+'.java', 'wb')
            f.write(output)
            f.close()
            # Generate
            Helper.logger.debug("> Generating Repository for Entity {} .".format(ent.name))            
            output = self.templateRepo.render(package=self.__project.package+"."+Project.Repositories_folder,
                                         Entitypackage=self.__project.package+"."+Project.Entities_folder+"."+ent.name,
                                         entityName=ent.name).encode("utf-8")
            f = open(self.entityRepoDirs+'/'+ent.name+Project.Repository_prepend+'.java', 'wb')
            f.write(output)
            f.close()
            # Generate
            Helper.logger.debug("> Generating Controller for Entity {} .".format(ent.name))            
            output = self.templateController.render(projectPackage=self.__project.package,
                                               package=self.__project.package+"."+Project.Controllers_folder,
                                               Entitypackage=self.__project.package+"."+Project.Entities_folder+"."+ent.name,
                                               Servicepackage=self.__project.package + "." + Project.Services_folder + "." + ent.name+Project.Service_prepend,
                                               entityName=ent.name,
                                               mapping=Project.ApiPrefix+ent.name.lower()).encode("utf-8")
            f = open(self.controllersDirs + '/' + ent.name +Project.Controller_prepend + '.java', 'wb')
            f.write(output)
            f.close()
            # Generate
            Helper.logger.debug("> Generating Service for Entity {} .".format(ent.name))            
            output = self.templateService.render(projectPackage=self.__project.package,
                                            package=self.__project.package+"."+Project.Services_folder,
                                            Entitypackage=self.__project.package+"."+Project.Entities_folder+"."+ent.name,
                                            Repositorypackage=self.__project.package + "." + Project.Repositories_folder + "." + ent.name+Project.Repository_prepend,
                                            Servicepackage=self.__project.package + "." + Project.Services_folder + "." + ent.name+Project.Service_prepend,
                                            entityName=ent.name,
                                            entity=ent).encode("utf-8")
            f = open(self.servicesDirs + '/' + ent.name + Project.Service_prepend+'.java', 'wb')
            f.write(output)
            f.close()            
        
    def __GenerateBase(self):
        # Preparing templates
        self.templateEntity = Environment(loader=BaseLoader()).from_string(templates[Generator.Entity_Template])
        self.templateRepo = Environment(loader=BaseLoader()).from_string(templates[Generator.EntityRepo_Template])
        self.templateController = Environment(loader=BaseLoader()).from_string(templates[Generator.Controller_Template])
        self.templateService = Environment(loader=BaseLoader()).from_string(templates[Generator.Service_Template])
        # Creating dir's for entities , repositories, controllers, services
        self.entityDirs = self.__srcdir + '/' + Project.Entities_folder
        os.makedirs(self.entityDirs)        
        self.entityRepoDirs = self.__srcdir + '/' + Project.Repositories_folder
        os.makedirs(self.entityRepoDirs)        
        self.controllersDirs = self.__srcdir + '/' + Project.Controllers_folder
        os.makedirs(self.controllersDirs)        
        self.servicesDirs = self.__srcdir + '/' + Project.Services_folder
        os.makedirs(self.servicesDirs)        
        self.securityDirs = self.__srcdir + '/' + Project.Security_folder
        os.makedirs(self.securityDirs)  
        # Generate
        Helper.logger.debug("> Generating Base entity file ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.BaseEntity_Template])
        output = template.render(package=self.__project.package + "." + Project.Entities_folder).encode("utf-8")
        f = open(self.entityDirs + '/' + Generator.BaseEntity_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.IController_Template])
        Helper.logger.debug("> Generating IController .")
        output = template.render(package=self.__project.package + "." +Project.Controllers_folder).encode("utf-8")
        f = open(self.controllersDirs + '/IController.java', 'wb')
        f.write(output)
        f.close()
        # Generate
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.IService_Template])
        Helper.logger.debug("> Generating IService .")
        packageService = self.__project.package + "." + Project.Services_folder
        output = template.render(package=self.__project.package + "." +Project.Services_folder).encode("utf-8")
        f = open(self.servicesDirs + '/IService.java', 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating error Controller file ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.ErrorControl_Template])
        output = template.render(package=self.__project.package + "." + Project.Controllers_folder,
                                    project=self.__project).encode("utf-8")
        f = open(self.controllersDirs + '/' + Generator.ErrorControl_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating Status Controller file ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.StatusControl_Template])
        output = template.render(package=self.__project.package + "." + Project.Controllers_folder).encode("utf-8")
        f = open(self.controllersDirs + '/' + Generator.StatusControl_Template, 'wb')
        f.write(output)
        f.close()          

    def __GenerateConfiguration(self):
        exceptionDirs = self.__srcdir + '/' + Project.Exceptions_folder
        os.makedirs(exceptionDirs)        
        # Generate xml logging configuration
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.log4j2_Template])
        Helper.logger.debug("> Generating Configuration logger ..")
        # Generate
        output = template.render(logger=self.configuration).encode("utf-8")
        f = open(self.outputDir + Project.Resources_Dir + Generator.log4j2_Template, 'wb')
        f.write(output)
        f.close()
        # Generate configurations file
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.properties_Template])
        Helper.logger.debug("> Generating Configurations file ..")
        # Generate
        output = template.render(project=self.__project).encode("utf-8")
        f = open(self.outputDir + Project.Resources_Dir + Generator.properties_Template, 'wb')
        f.write(output)
        f.close()
        # Generate pom configuration
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.pom_Template])
        Helper.logger.debug("> Generating Configuration pom ..")
        # Generate
        output = template.render(pom=self.__project).encode("utf-8")
        f = open(self.outputDir + '/' + Generator.pom_Template, 'wb')
        f.write(output)
        f.close()
        # Generate some java files
        Helper.logger.debug("> Generating application  files ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.application_Template])
        output = template.render(package=self.__project.package).encode("utf-8")
        f = open(self.__srcdir  + '/' + Generator.application_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating Swagger Config files ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.SwaggerConfig_Template])
        output = template.render(ApiPrefix=Project.ApiPrefix, project=self.__project).encode("utf-8")
        f = open(self.__srcdir + '/' + Generator.SwaggerConfig_Template, 'wb')
        f.write(output)
        f.close()
    	# Generate
        Helper.logger.debug("> Generating Logging Filter files ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.logginFilter_Template])
        output = template.render(package=self.__project.package).encode("utf-8")
        f = open(self.__srcdir + '/' + Generator.logginFilter_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating Web Initializer files ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.webInitializer_Template])
        output = template.render(package=self.__project.package).encode("utf-8")
        f = open(self.__srcdir + '/' + Generator.webInitializer_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating Web Exceptions files ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.ExceptionBad_Template])
        output = template.render(package=self.__project.package + "." + Project.Exceptions_folder).encode("utf-8")
        f = open(exceptionDirs + '/' + Generator.ExceptionBad_Template, 'wb')
        f.write(output)
        f.close()
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.ExceptionNot_Template])
        output = template.render(package=self.__project.package + "." + Project.Exceptions_folder).encode("utf-8")
        f = open(exceptionDirs + '/' + Generator.ExceptionNot_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating Read ME File .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.READMEFILE_Template])
        output = template.render(project=self.__project).encode("utf-8")
        f = open(self.outputDir + '/' + Generator.READMEFILE_Template, 'wb')
        f.write(output)
        f.close()

    def __GenerateTests(self):
        #loop in entities
        for ent in self.entities: 
            # Generate
            Helper.logger.debug("> Generating Crud tests file for Entity {} .".format(ent.name))
            template = Environment(loader=BaseLoader()).from_string(templates[Generator.CrudTest_Template])
            output = template.render(   package=self.__project.package ,
                                        Entitypackage=self.__project.package+"."+Project.Entities_folder+"."+ent.name,
                                        Servicepackage=self.__project.package + "." + Project.Services_folder + "." + ent.name+Project.Service_prepend,
                                        ServiceBasepackage=self.__project.package+"."+Project.Services_folder,
                                        EntityBasepackage=self.__project.package+"."+Project.Entities_folder,
                                        entityName=ent.name,
                                        mapping=Project.ApiPrefix+ent.name.lower(),
                                        entity=ent).encode("utf-8")
            f = open(self.__testdir + '/' + ent.name + Generator.CrudTest_Template, 'wb')
            f.write(output)
            f.close()        
        # Generate
        Helper.logger.debug("> Generating Helper test file ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.HelperTests_Template])
        output = template.render(package=self.__project.package).encode("utf-8")
        f = open(self.__testdir + '/' + Generator.HelperTests_Template, 'wb')
        f.write(output)
        f.close()           

    def __GenerateSecurity(self):
        # Generate
        Helper.logger.debug("> Generating Authorities file .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.Authorities_Template])
        output = template.render(   package=self.__project.package +".securit" ,
                                    roles=self.__project.securityRoles).encode("utf-8")
        f = open(self.securityDirs + '/' +Generator.Authorities_Template, 'wb')
        f.write(output)
        f.close()

    """ To string type method """
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# The Main function
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def main(argv):
    # Check Parameter
    parser = argparse.ArgumentParser(
        prog='SBR Generator',
        description='SBR generator: Generate Spring Boot Rest source code.')
    parser.add_argument('-v', '--mode-verbose', dest='verbose', action='store_true', help='Enable verbose traces')
    parser.add_argument('-t', '--enable-tests', dest='tests', action='store_true', help='Enable tests')
    parser.add_argument('-s', '--disable-security', dest='security', action='store_false', help='Disable security')
    parser.add_argument('-c', '--config-file', dest='configfile', action='store',
                        help='The Yaml config file ', required=True)
    parser.add_argument('-o', '--outputDir', dest='outputDir', action='store',default=DefaultOutput_Dir,
                        help='The Output folder where to store generated source code', )
    args = parser.parse_args()
    Helper.logger.info("[  ok ] verbose     : '{}'     ".format(args.verbose))
    Helper.logger.info("[  ok ] tests       : '{}'     ".format(args.tests))
    Helper.logger.info("[  ok ] security    : '{}'     ".format(args.security))
    Helper.logger.info("[  ok ] configfile  : '{}'   ".format(args.configfile))
    Helper.logger.info("[  ok ] outputDir   : '{}'     ".format(args.outputDir))
    # Load configuration
    econ = ConfigLoader(args.configfile, args.verbose)
    if args.verbose:
        pp = pprint.PrettyPrinter(indent=4)
        Helper.logger.info("The config Project is ==>   ")
        pp.pprint(econ.configuration['project'])
    # Analyse Configuration
    Helper.logger.info("Analysing Configuration ..   ")
    analyser = Analyser(econ.project, econ.configuration)
    # Generate ...
    Helper.logger.info("Generate ..   ")
    gen = Generator(args.outputDir, args.verbose, args.tests, args.security, econ.project, analyser.AllEntities, analyser.Configuration)
    gen.GenerateAll()    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# The Default function
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
    main(sys.argv[1:])
