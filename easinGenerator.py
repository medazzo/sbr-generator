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
import uuid 
import bcrypt
from jinja2 import Environment, BaseLoader
from easinTemplates import templates

DefaultOutput_Dir = "./tmp-out"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Generator Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Generator:
    """A Generator   class"""
    Entity_Template = "entity.java"
    EntityRepo_Template = "Repository.java"
    Controller_Template = "controller.java"
    AuthenticationController_Template= "AuthenticationController.java"
    log4j2_Template = "log4j2.xml"
    pom_Template = "pom.xml"
    Data_Template = "data.sql"
    properties_Template = "application.yaml"
    application_Template = "Application.java"
    CommandInitializer_Template = "CommandInitializer.java"
    LoggingFilter_Template = "RequestLoggingFilterConfig.java"
    SwaggerConfig_Template = "SwaggerConfiguration.java"
    webInitializer_Template = "WebInitializer.java"
    BaseEntity_Template = "BaseEntity.java"
    IController_Template = "IController.java"
    IService_Template = "IService.java"
    Service_Template = "Service.java"
    ExceptionBad_Template = "ResourceBadParameterException.java"
    ExceptionNot_Template = "ResourceNotFoundException.java"
    ErrorControl_Template = "MyErrorController.java"
    StatusControl_Template = "StatusController.java"
    READMEFILE_Template = "README.md"
    CrudTest_Template = "CrudUnitTest.java"
    HelperTests_Template = "HelperTests.java"
    Constants_Template = "Constants.java"
    Authorities_Template = "AuthoritiesConstants.java"
    WebSecurityConfig_Template = "WebSecurityConfig.java"
    TokenProvider_Template = "TokenProvider.java"
    RestConfig_Template = "RestConfig.java"
    JwtAuthenticationEntryPoint_Template = "JwtAuthenticationEntryPoint.java"
    JwtAuthenticationFilter_Template = "JwtAuthenticationFilter.java"
    UserService_Template = "UserService.java"
    UserEntity_Template = "User.java"
    AuthToken_Template = "AuthToken.java"
    LoginUser_Template = "LoginUser.java"
    Template_Dir = ".templates"

    def __init__(self, outputDir=None, verbose=False, tests=False, security=True, project=None, entities=list(),
                 conf=None):
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
        #  prepare template loader
        self.__pathTemplate = os.getcwd() + "/" + Generator.Template_Dir
        loader = jinja2.FileSystemLoader(searchpath=self.__pathTemplate)
        self.templateEnv = jinja2.Environment(loader=loader)

    def generate(self):
        Helper.logger.info("Generate Base ==>   ")
        self.__GenerateBase()
        Helper.logger.info("Generate Entities ==>   ")
        self.__GenerateEntity()
        Helper.logger.info("Generate configurations ==>   ")
        self.__GenerateConfiguration()
        if self.security:
            Helper.logger.info("Generate Security ==>   ")
            self.__GenerateSecurity()
        if self.tests:
            Helper.logger.info("Generate tests ==>   ")
            self.__GenerateTests()

    def __GenerateEntity(self):
        # loop in entities
        for ent in self.entities:
            # Generate
            Helper.logger.debug("> Generating Classes for Entity {} .".format(ent.name))
            output = self.templateEntity.render(package=self.__project.package + "." + Project.Entities_folder,
                                                entity=ent).encode("utf-8")
            f = open(self.entityDirs + '/' + ent.name + '.java', 'wb')
            f.write(output)
            f.close()
            # Generate
            Helper.logger.debug("> Generating Repository for Entity {} .".format(ent.name))
            output = self.templateRepo.render(package=self.__project.package + "." + Project.Repositories_folder,
                                              Entitypackage=self.__project.package + "." + Project.Entities_folder + "." + ent.name,
                                              entityName=ent.name).encode("utf-8")
            f = open(self.entityRepoDirs + '/' + ent.name + Project.Repository_prepend + '.java', 'wb')
            f.write(output)
            f.close()
            # Generate
            Helper.logger.debug("> Generating Controller for Entity {} .".format(ent.name))
            output = self.templateController.render(projectPackage=self.__project.package,
                                                    security = self.security,
                                                    roles=self.__project.securityRoles,
                                                    package=self.__project.package + "." + Project.Controllers_folder,
                                                    Entitypackage=self.__project.package + "." + Project.Entities_folder + "." + ent.name,
                                                    Servicepackage=self.__project.package + "." + Project.Services_folder + "." + ent.name + Project.Service_prepend,
                                                    entityName=ent.name,
                                                    mapping=Project.ApiPrefix + ent.name.lower()).encode("utf-8")
            f = open(self.controllersDirs + '/' + ent.name + Project.Controller_prepend + '.java', 'wb')
            f.write(output)
            f.close()
            # Generate
            Helper.logger.debug("> Generating Service for Entity {} .".format(ent.name))
            output = self.templateService.render(projectPackage=self.__project.package,
                                                 package=self.__project.package + "." + Project.Services_folder,
                                                 Entitypackage=self.__project.package + "." + Project.Entities_folder + "." + ent.name,
                                                 Repositorypackage=self.__project.package + "." + Project.Repositories_folder + "." + ent.name + Project.Repository_prepend,
                                                 Servicepackage=self.__project.package + "." + Project.Services_folder + "." + ent.name + Project.Service_prepend,
                                                 entityName=ent.name,
                                                 entity=ent).encode("utf-8")
            f = open(self.servicesDirs + '/' + ent.name + Project.Service_prepend + '.java', 'wb')
            f.write(output)
            f.close()
            if ent.name == "User":
                # Generate and overwrite the user entity, repositories and service
                Helper.logger.debug("> Generating User Class  {} .".format(ent.name))
                templateUserEntity = Environment(loader=BaseLoader()).from_string(templates[Generator.UserEntity_Template])
                output = templateUserEntity.render( package=self.__project.package + "." + Project.Entities_folder,
                                                    configConstants=self.__project.package + "." + Project.Conf_folder ,
                                                    entity=ent).encode("utf-8")
                f = open(self.entityDirs + '/' + ent.name + '.java', 'wb')
                f.write(output)
                f.close()
                if self.security:
                    # Generate and overwrite the user service
                    Helper.logger.debug("> Generating User  Service file  for security profile.")
                    template = Environment(loader=BaseLoader()).from_string(templates[Generator.UserService_Template])
                    output = template.render(projectPackage=self.__project.package,
                                             package=self.__project.package + "." + Project.Services_folder,
                                             Repositorypackage=self.__project.package + "." + Project.Repositories_folder + "." + ent.name + Project.Repository_prepend,
                                             Entitypackage=self.__project.package + "." + Project.Entities_folder + ".User",
                                             entity=ent,
                                             Repopackage=self.__project.package + "." + Project.Repositories_folder+".User" + Project.Repository_prepend).encode("utf-8")
                    f = open(self.servicesDirs + '/' + Generator.UserService_Template, 'wb')
                    f.write(output)
                    f.close()

    def __GenerateBase(self):
        # key used as salt for password
        self.key = bcrypt.gensalt()
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
        self.appDirs = self.__srcdir + '/' + Project.Conf_folder
        os.makedirs(self.appDirs)
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
        output = template.render(package=self.__project.package + "." + Project.Controllers_folder).encode("utf-8")
        f = open(self.controllersDirs + '/'+Generator.IController_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.IService_Template])
        Helper.logger.debug("> Generating IService .")
        packageService = self.__project.package + "." + Project.Services_folder
        output = template.render(package=self.__project.package + "." + Project.Services_folder).encode("utf-8")
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
        # Generate
        Helper.logger.debug("> Generating Constants config file .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.Constants_Template])
        output = template.render(package=self.__project.package + "." + Project.Conf_folder,
                                 key=self.key.decode()).encode("utf-8")
        f = open(self.appDirs + '/' + Generator.Constants_Template, 'wb')
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
        output = template.render(   pom=self.__project,
                                    startClass=self.__project.package+ '.' + Generator.application_Template[:-5],
                                    security=self.security).encode("utf-8")
        f = open(self.outputDir + '/' + Generator.pom_Template, 'wb')
        f.write(output)
        f.close()
        # Generate some java files
        Helper.logger.debug("> Generating application  files ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.application_Template])
        output = template.render(package=self.__project.package).encode("utf-8")
        f = open(self.__srcdir + '/' + Generator.application_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating Command Initializer  files ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.CommandInitializer_Template])
        output = template.render(package=self.__project.package + '.' + Project.Conf_folder).encode("utf-8")
        f = open(self.appDirs + '/' + Generator.CommandInitializer_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating Swagger Config files ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.SwaggerConfig_Template])
        output = template.render(package=self.__project.package + '.' + Project.Conf_folder,
                                 ApiPrefix=Project.ApiPrefix, 
                                 project=self.__project).encode("utf-8")
        f = open(self.appDirs + '/' + Generator.SwaggerConfig_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating Logging Filter files ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.LoggingFilter_Template])
        output = template.render(package=self.__project.package+ '.' + Project.Conf_folder).encode("utf-8")
        f = open(self.appDirs + '/' + Generator.LoggingFilter_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating Web Initializer files ..")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.webInitializer_Template])
        output = template.render(package=self.__project.package+ '.' + Project.Conf_folder,
                                 Apppackage=self.__project.package+ '.' +  Generator.application_Template[:-5]).encode("utf-8")
        f = open(self.appDirs + '/' + Generator.webInitializer_Template, 'wb')
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
        self.__testdir = self.outputDir + Project.Test_Dir + self.__project.package.replace(".", "/")
        os.makedirs(self.__testdir)
        # loop in entities
        for ent in self.entities:
            # Generate
            Helper.logger.debug("> Generating Crud tests file for Entity {} .".format(ent.name))
            template = Environment(loader=BaseLoader()).from_string(templates[Generator.CrudTest_Template])
            output = template.render(package=self.__project.package,
                                     packageAuth=self.__project.package + "." + Project.Security_folder + "." + Project.Security_api_folder,
                                     security=self.security,
                                     aemail=self.amail,
                                     uemail=self.umail,
                                     apassword=self.apassword,
                                     upassword=self.upassword,
                                     Entitypackage=self.__project.package + "." + Project.Entities_folder + "." + ent.name,
                                     Servicepackage=self.__project.package + "." + Project.Services_folder + "." + ent.name + Project.Service_prepend,
                                     ServiceBasepackage=self.__project.package + "." + Project.Services_folder,
                                     EntityBasepackage=self.__project.package + "." + Project.Entities_folder,
                                     entityName=ent.name,
                                     mapping=Project.ApiPrefix + ent.name.lower(),
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
        self.securityDirs = self.__srcdir + '/' + Project.Security_folder
        os.makedirs(self.securityDirs)
        self.securityApiDirs = self.__srcdir + '/' + Project.Security_folder + '/' + Project.Security_api_folder
        os.makedirs(self.securityApiDirs)
        # Generate
        Helper.logger.debug("> Generating Authorities file .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.Authorities_Template])
        output = template.render(package=self.__project.package + "." + Project.Security_folder,
                                 roles=self.__project.securityRoles).encode("utf-8")
        f = open(self.securityDirs + '/' + Generator.Authorities_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating WebSecurityConfig file .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.WebSecurityConfig_Template])
        output = template.render(package=self.__project.package + "." + Project.Security_folder, project=self.__project).encode("utf-8")
        f = open(self.securityDirs + '/' + Generator.WebSecurityConfig_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating TokenProvider file .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.TokenProvider_Template])
        output = template.render(package=self.__project.package + "." + Project.Security_folder,
                                packageConstants=self.__project.package + "." + Project.Conf_folder).encode("utf-8")
        f = open(self.securityDirs + '/' + Generator.TokenProvider_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating RestConfig file .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.RestConfig_Template])
        output = template.render(package=self.__project.package + "." + Project.Security_folder).encode("utf-8")
        f = open(self.securityDirs + '/' + Generator.RestConfig_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating JwtAuthenticationEntryPoint file .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.JwtAuthenticationEntryPoint_Template])
        output = template.render(package=self.__project.package + "." + Project.Security_folder).encode("utf-8")
        f = open(self.securityDirs + '/' + Generator.JwtAuthenticationEntryPoint_Template, 'wb')
        f.write(output)
        f.close()
        # Generate
        Helper.logger.debug("> Generating JwtAuthenticationFilter file .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.JwtAuthenticationFilter_Template])
        output = template.render(package=self.__project.package + "." + Project.Security_folder,
                                packageConstants=self.__project.package + "." + Project.Conf_folder).encode("utf-8")
        f = open(self.securityDirs + '/' + Generator.JwtAuthenticationFilter_Template, 'wb')
        f.write(output)
        f.close()
        # Generate Auth controller 
        Helper.logger.debug("> Generating Authentication Controller .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.AuthenticationController_Template])        
        output = template.render(package=self.__project.package + "." + Project.Controllers_folder,
                                                EntitypackageUser=self.__project.package + "." + Project.Entities_folder + ".User",
                                                Securitypackage=self.__project.package + "." +  Project.Security_folder,
                                                ServicepackageUser=self.__project.package + "." + Project.Services_folder + ".User" + Project.Service_prepend,
                                                mapping=Project.ApiPrefix + "auth").encode("utf-8")
        f = open(self.controllersDirs + '/' + Generator.AuthenticationController_Template , 'wb')
        f.write(output)
        f.close()     
        # Generate Security Api files
        Helper.logger.debug("> Generating Security Api classe Auth token .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.AuthToken_Template])        
        output = template.render(package=self.__project.package + "." + Project.Security_folder + "." + Project.Security_api_folder,
                                                EntitypackageUser=self.__project.package + "." + Project.Entities_folder + ".User"  ).encode("utf-8")
        f = open(self.securityApiDirs + '/' + Generator.AuthToken_Template , 'wb')
        f.write(output)
        f.close()              
        Helper.logger.debug("> Generating Security Api classe Login User .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.LoginUser_Template])        
        output = template.render(package=self.__project.package + "." + Project.Security_folder + "." + Project.Security_api_folder).encode("utf-8")
        f = open(self.securityApiDirs + '/' + Generator.LoginUser_Template , 'wb')
        f.write(output)
        f.close()              
        # Generate DATA SQL file to be injected in database
        Helper.logger.debug("> Generating  data.sql file .")
        template = Environment(loader=BaseLoader()).from_string(templates[Generator.Data_Template]) 
        passwd =  Helper.randomString(5)
        upasswd =  Helper.randomString(5)    
        # Usinb bcryt for passwords
        pwdhash = bcrypt.hashpw(passwd.encode(), self.key )
        upwdhash = bcrypt.hashpw(upasswd.encode(), self.key )
        mail_prefix = Helper.randomString(5)
        umail_prefix = Helper.randomString(5)
        self.amail = mail_prefix+"_admin@admin.com"
        self.umail = umail_prefix+"_user@user.com"
        self.apassword = passwd
        self.upassword = upasswd
        output = template.render(   uuid=uuid.uuid1() ,
                                    uuuid=uuid.uuid1() ,
                                    password=pwdhash.decode(), 
                                    upassword=upwdhash.decode(), 
                                    passwordclear=passwd,
                                    upasswordclear=upasswd,
                                    login=mail_prefix+"Admin",
                                    ulogin=umail_prefix+"User",
                                    mail=self.amail,
                                    umail=self.umail).encode("utf-8")
        f = open(self.outputDir + Project.Resources_Dir + '/' + Generator.Data_Template , 'wb')
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
    parser.add_argument('-o', '--outputDir', dest='outputDir', action='store', default=DefaultOutput_Dir,
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
    gen = Generator(args.outputDir, args.verbose, args.tests, args.security, econ.project, analyser.AllEntities,
                    analyser.Configuration)
    gen.generate()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# The Default function
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
    main(sys.argv[1:])
