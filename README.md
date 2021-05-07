# SBR-Generator

[![Build Status](https://travis-ci.org/medazzo/sbr-generator.svg?branch=master)](https://travis-ci.org/medazzo/sbr-generator)
[![npm version](https://badge.fury.io/js/sbr-generator.svg)](https://badge.fury.io/js/sbr-generator)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmedazzo%2Fsbr-generator.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmedazzo%2Fsbr-generator?ref=badge_shield)

SBR generator is a Spring Boot Rest Generator npm binary cli used to generate source code modules starting from config file.<br/>

The Generated source code is a CRUD Rest Spring Boot Server, ready to build and run .  

## How to install
It's a node package with CLI (command line interface) binary , can be installed by
```
npm install -g sbr-generator
```
### Prerequisites
To work correctly *SBR* needs python to be installed .
All needed python mudules with be installed automatically when installing *SBR*.

## How To use
To Generate a ready to use Spring boot Rest Server , *SBR* need a configuration file
You can start by using the example one    
```
~$ sbrgen  -h
usage: SBR Generator [-h] [-v] [-t] [-s] -c CONFIGFILE [-o OUTPUTDIR]

SBR generator: Generate Spring Boot Rest source code.

optional arguments:
  -h, --help            show this help message and exit
  -v, --mode-verbose    Enable verbose traces
  -t, --enable-tests    Enable tests
  -s, --disable-security
                        Disable security
  -c CONFIGFILE, --config-file CONFIGFILE
                        The Yaml config file
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        The Output folder where to store generated source code

```
Additionally , *SBR* support :
* Verobse mode using *-v*
* Disabling Security based on spring role and JWT token mode using *-s*
* Enabling generating tests using  *-t*

Like Below, to generate project with security enabled and tests using example config file :
```
~$ sbrgen  -v -t -c  examples/config.yaml

```
This will generate the next folder strcutue :
```
$  tree serverTest-0.0.1-SNAP/
serverTest-0.0.1-SNAP/
├── pom.xml
├── README.md
└── src
    ├── main
    │   ├── java
    │   │   └── com
    │   │       └── easin
    │   │           └── serverTest
    │   │               ├── Application.java
    │   │               ├── conf
    │   │               │   └── ....java
    │   │               ├── controllers    
    │   │               │   └── ....java
    │   │               ├── entities    
    │   │               │   └── ...java
    │   │               ├── exceptions    
    │   │               │   └── ...java
    │   │               ├── repositories    
    │   │               │   └── ....java
    │   │               ├── security
    │   │               │   ├── api
    │   │               │   │   └── ...java
    │   │               │   └── ...java
    │   │               └── services
    │   │                   └── ...java
    │   └── resources
    │       ├── application.yaml
    │       ├── data.sql
    │       └── log4j2.xml
    └── test
        └── java
            └── com
                └── easin
                    └── serverTest
                        └── ...java

```

## How to use Generated source code

The generated source code is a spring boot rest maven project with a read me file ,a complete project ready to use :

To build and Run   :
```
cd testServer-0.0.1/
mvn clean package -Dmaven.test.skip=true
mvn spring-boot:run -Dmaven.test.skip=true

```

To Run  Crud unit tests ( already generated ):

```
cd testServer-0.0.1/
mvn test
```

# Configuration File

The Configuration is a yaml file having 3 sections : project, logging  and entities.

## project section
Contains all project specific data used in the pom file and the Readme and in sourec conde generations ..
```yaml
project:
    longname: Easy Soft IN Selling Server # the project long name used in the pom files and the Readme     
    description: Easin Selling Server     # a description for the project
    url: http://easysoft-in.com           # the url of the project
    name: serverTest                      # the short name
    restPath: /serverTest                 # the rest base path generated
    package: com.easin.serverTest         # the package of the project
    version: 0.0.1-SNAP                   # the version of the prpoject
    security:                             # security data if activated to generate
      extraroles:                         # security extra roles (*SBR* already manage admin and user) please do not prefix roles with ROLE_ !      
        - "PROVIDER"
        - "CONSUMER"
```

## logging section
it will be used to generate the **src/main/resources/log4j2.xml** file , extra configuration need to be added manually to the file .
```yaml
logging:
  RootLoggerLevel: trace
  Loggers:
    - name: com.easin
      level: trace
    - name: org.springframework.web.client.RestTemplate
      level: trace
    - name: org.apache.catalina.filters.RequestDumperFilter
      level: trace
```

## entitiess section
This section is used to generate java package  for entity's, services, controllers,  and beyond : @Entity class and  JpaRepository for each one ..
**User**: be Aware that the *User* entity is specific as it already managed by *SBR*, when using it on your entity, *SBR* will merge your fiels and his.

```yaml
entities:
  - name: User
    comment: Class representing the User parameters
    fields:
      - name: mail
        type: String
        comment: the official Mail of the User
        annotations:
          - "@Email"
      - name: phone
        type: String
        comment: the official Phone number of the User
        annotations:  []
      - name: name
        comment: name of the User
        annotations:
          - "@Column(nullable = false)"
        type: String
  - name: Company
    crudRest: true
    baseclass: BaseEntity
    comment: Class representing the company parameters
    fields:
      - name: user
        comment: User created
        annotations:
          - '@JoinColumn(name="user_id", insertable=false, updatable=false)'
          - "@ManyToOne(targetEntity = User.class, fetch = FetchType.EAGER)"
          - "@JsonIgnore"
          - "@ToString.Exclude"
        type: User

```

## How it's Works

*SBR* is using python and jinja2 Template machine..
*SBR* will also generate **Swapper html api** pages on :<br/>
http://localhost:8080/project.name/project.version/swagger-ui.html
<br/>OR json format under <br/>
http://localhost:8080/project.name/project.version/v2/api-docs


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmedazzo%2Fsbr-generator.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmedazzo%2Fsbr-generator?ref=badge_large)