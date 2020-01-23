

# SBR-Generator

Spring Boot Rest Generator is a  python Library used to generate source code modules starting from config files .
The Generated source code is a CRUD Rest Spring Boot Server.  

## How to install 
It's a node binary , can be installed by 
```
npm install -g sbr-generator
```
### Prerequisites
To work correctly nsbr need some python modules to be installed :   
```
pip install jinja2
pip install pyyaml
pip install coloredlogs
```
## How To use 
sbr need a config file , you can use the example one    
```
~$ sbrgen  -h 
usage: SBR Generator [-h] [-v] -c CONFIGFILE [-o OUTPUTDIR]

SBR generator: Generate Spring Boot Rest source code.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbose traces
  -c CONFIGFILE, --config CONFIGFILE
                        The Yaml config file
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        The Output folder where to store generated source code

~$ cd examples 
~$ sbrgen  -h  -c config.yaml
...
```
This will generate the next folder :
```
$ tree serverTest-0.0.1-SNAP/
serverTest-0.0.1-SNAP/
├── pom.xml
├── README.md
└── src
    └── main
        ├── java
        │   └── com
        │       └── easin
        │           └── serverTest
        │               ├── Application.java
        │               ├── controllers
        │               │   ├── AddressController.java
        │               │   ├── CompanyController.java
        │               │   ├── IController.java
        │               │   ├── LegalController.java
        │               │   ├── MyErrorController.java
        │               │   ├── StatusController.java
        │               │   └── UserController.java
        │               ├── entities
        │               │   ├── Address.java
        │               │   ├── BaseEntity.java
        │               │   ├── Company.java
        │               │   ├── Legal.java
        │               │   └── User.java
        │               ├── exceptions
        │               │   ├── ResourceBadParameterException.java
        │               │   └── ResourceNotFoundException.java
        │               ├── repositories
        │               │   ├── AddressRepository.java
        │               │   ├── CompanyRepository.java
        │               │   ├── LegalRepository.java
        │               │   └── UserRepository.java
        │               ├── RequestLoggingFilterConfig.java
        │               ├── services
        │               │   ├── AddressService.java
        │               │   ├── CompanyService.java
        │               │   ├── IService.java
        │               │   ├── LegalService.java
        │               │   └── UserService.java
        │               ├── SwaggerConfiguration.java
        │               └── WebInitializer.java
        └── resources
            ├── application.yaml
            └── log4j2.xml

12 directories, 31 files
```

## How to use Generated source code 

The generated source code is a spring boot rest maven project wit ha read me file , ready to use : 
To build and Run server :
```
cd testServer-0.0.1/
mvn clean package
mvn spring-boot:run

```
# Configuration File

The Configuration is a yaml file having multiple.

## database section
it defines the database sectin in profile test, dev and prod
```yaml
database:
  test:
    url: jdbc:h2:mem:test;DB_CLOSE_ON_EXIT=FALSE
    dialect: org.hibernate.dialect.H2Dialect
    driverClassName: org.h2.Driver
    username: easin
    password: ''
    ddlauto: create
  dev:
    url: jdbc:h2:~/database.h2;DB_CLOSE_ON_EXIT=FALSE
    dialect: org.hibernate.dialect.H2Dialect
    driverClassName: org.h2.Driver
    username: easin
    password: ''
    ddlauto: update
  prod:
    url: jdbc:postgresql://localhost:5432/essDB
    dialect: org.hibernate.dialect.PostgreSQL82Dialect
    driverClassName: org.postgresql.Driver
    username: easin
    password: Easin
    ddlauto: update
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

## entitys section
This section is used to generate java package responsible for entity's : @Entity class and  JpaRepository for each one , also it schould generate action script definition foe theses entity to be used in front end 
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
Starting from defined entity's , entity's , controller's ,repository's will be generated

# Next steps
## generate tests
Python will be generated  under src/test/python based on templates of Enity.py and Crud.py from esserver and exec maven plugin to run it 
like described in :
https://blog.berczuk.com/2009/12/continuous-integration-of-python-code.html
and  https://www.mojohaus.org/exec-maven-plugin/usage.html
## Security layer
security will be based on role and user's token as done in esserver 
## mail 
to do later , very later et maibe not needed 
 