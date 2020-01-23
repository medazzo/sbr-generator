# ----------------------------------------------- 
# Generated Files  Containing temples as variables 
# ----------------------------------------------- 

templates = { 
    'Application.java' :  """package {{package}};

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@SpringBootApplication
public class Application {

    public static final String EMAIL_TEMPLATE_ENCODING = "UTF-8";

    public static void main(final String[] args) {
        SpringApplication.run(Application.class, args);
    }


} """,
    'application.yaml' :  """spring:
  profiles:
    active: "dev"
  main:
    banner-mode: "off"
  output:
    ansi:
      enabled: DETECT

server:
  servlet:
    context-path: {{project.restPath}}/{{project.version}}
---

spring:
  profiles: dev
  datasource:
    url: {{dbDev.url}}
    username: {{dbDev.username}}
    password: {{dbDev.password}}
    driverClassName: {{dbDev.driverClassName}}
  jpa:
    generate-ddl: true
    properties:
      hibernate:
        default_schema: public
        dialect: {{dbDev.dialect}}
    hibernate:
      ddl-auto: {{dbDev.ddlauto}}
    show-sql: true
  jackson:
    serialization:
      FAIL_ON_EMPTY_BEANS: False
---

spring:
  profiles: test
  datasource:
    url: {{dbTest.url}}
    username: {{dbTest.username}}
    password: {{dbTest.password}}
    driverClassName: {{dbTest.driverClassName}}
    jpa:
      generate-ddl: true
      properties:
        hibernate:
          default_schema: public
          dialect: {{dbTest.dialect}}
      hibernate:
        ddl-auto: {{dbTest.ddlauto}}
      show-sql: true
    jackson:
      serialization:
        FAIL_ON_EMPTY_BEANS: False
---

spring:
  profiles: prod
  datasource:
    url: {{dbProd.url}}
    username: {{dbProd.username}}
    password: {{dbProd.password}}
    driverClassName: {{dbProd.driverClassName}}
    jpa:
      generate-ddl: true
      properties:
        hibernate:
          default_schema: public
          dialect: {{dbProd.dialect}}
      hibernate:
        ddl-auto: {{dbProd.ddlauto}}
      show-sql: true
    jackson:
      serialization:
        FAIL_ON_EMPTY_BEANS: False """,
    'BaseEntity.java' :  """package {{package}};

import java.io.Serializable;
import java.util.Date;

import javax.persistence.*;

import org.hibernate.annotations.GenericGenerator;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;
import io.swagger.annotations.ApiModelProperty;

@Getter
@Setter
@AllArgsConstructor
@ToString
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
@JsonIgnoreProperties(value = {"createdAt", "updatedAt"}, allowGetters = true)
public abstract class BaseEntity implements Serializable {

    @Id
    @GeneratedValue(generator = "system-uuid", strategy = GenerationType.IDENTITY)
    @GenericGenerator(name = "system-uuid", strategy = "uuid2")
    @ApiModelProperty(hidden = true)
    protected String Id;

    @Version
    @ApiModelProperty(hidden = true)
    private Integer version;

    @Column(nullable = false, updatable = false)
    @Temporal(TemporalType.TIMESTAMP)
    @CreatedDate
    @ApiModelProperty(hidden = true)
    private Date createdAt;

    @Column(nullable = false)
    @Temporal(TemporalType.TIMESTAMP)
    @LastModifiedDate
    @ApiModelProperty(hidden = true)
    private Date updatedAt;


    protected String name;

    protected BaseEntity(){
    	this.createdAt = new Date();
    	this.updatedAt = new Date();
    }
} """,
    'controller.java' :  """package {{package}};

import {{Entitypackage}};
import {{projectPackage}}.exceptions.ResourceBadParameterException;
import {{projectPackage}}.exceptions.ResourceNotFoundException;
import {{Servicepackage}};
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import lombok.extern.slf4j.Slf4j;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;

@Slf4j
@Controller
@Api( value = "{{entityName}}" , description="API for CRUD on {{entityName}}.", tags = { "{{entityName}}" })
@RequestMapping(path = "{{mapping}}")
public class {{entityName}}Controller   implements IController<{{entityName}}> {

    @Autowired
    private {{entityName}}Service service;

    @PostMapping("/new")
    @ResponseBody
    @Override
    @ApiOperation(value = "Create a new  {{entityName}} ", nickname = "CreateNew{{entityName}}" ,
 tags = { "{{entityName}}" })
    public ResponseEntity<{{entityName}}> create(@RequestBody {{entityName}} n) {
        if (n == null) {
            throw new ResourceBadParameterException("{{entityName}}", "new", n);
        }
        log.debug(" -->  Will create a new {{entityName}} ");
        {{entityName}} nu = service.create(n);
        return new ResponseEntity<{{entityName}}>(nu, HttpStatus.CREATED);
    }

    @GetMapping("/all")
    @ResponseBody
    @Override
    @ApiOperation(value = "Get all stored {{entityName}} !", nickname = "GetAll{{entityName}}" ,
 tags = { "{{entityName}}" })
    public List<{{entityName}}> getAll() {
        log.debug(" -->  Will Get All {{entityName}}'s'");
        return service.getAll();
    }

    @GetMapping("/all/{id}")
    @ResponseBody
    @Override
    @ApiOperation(value = "Get all stored {{entityName}} using some extra ID( user/group ID or some other ID)", 
        nickname = "GetAll{{entityName}}BySomeID" , tags = { "{{entityName}}" })
    public List<{{entityName}}> getAllBySomeId(String id) {
        if (id == null) {
            throw new ResourceNotFoundException("{{entityName}}", "some id", id);
        }
        log.debug(" -->  Will all {{entityName}}'s' by some id " + id);
        return service.getAllBySomeId(id);
    }

    @GetMapping(path = "/{id}")
    @ResponseBody
    @Override
    @ApiOperation(value = "Get stored {{entityName}} using his unique ID", nickname = "GetOne{{entityName}}ById" ,
 tags = { "{{entityName}}" })
    public {{entityName}} getOne(@PathVariable String id) {
        if (id == null) {
            throw new ResourceNotFoundException("{{entityName}}", "id", id);
        }
        log.debug(" -->  Will get one  {{entityName}} with id " + id);
        return service.getOne(id);
    }

    @PutMapping(path = "/{id}")
    @ResponseBody
    @Override
    @ApiOperation(value = "Update the stored {{entityName}} using his unique ID",
         nickname = "UpdateOne{{entityName}}ById" , tags = { "{{entityName}}" })
    public {{entityName}} update(@PathVariable String id, @RequestBody {{entityName}} n) {
        if (n == null) {
            throw new ResourceNotFoundException("{{entityName}}", "object", n);
        }
        if (id == null) {
            throw new ResourceNotFoundException("{{entityName}}", "id", id);
        }
        if (n.getId() == id) {
            throw new ResourceBadParameterException("{{entityName}}", "id", id);
        }
        log.debug(" -->  Will update one with id " + id);
        return service.update(n);
    }

    @DeleteMapping("/{id}")
    @ResponseBody
    @Override
    @ApiOperation(value = "Removing the stored {{entityName}} using his unique ID", 
        nickname = "RemoveOne{{entityName}}ById" , tags = { "{{entityName}}" })
    public void delete(@PathVariable String id) {
        if (id == null) {
            throw new ResourceNotFoundException("{{entityName}}", "id", id);
        }
        log.debug(" --> Will remove one with id " + id);
        service.deleteone(id);
    }
} """,
    'entity.java' :  """package {{package}} ;

import javax.persistence.*;
import javax.validation.constraints.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.*;
import lombok.extern.slf4j.Slf4j;

/**
 * {{entity.comment}}
 */
@Slf4j
@Getter
@Setter
@AllArgsConstructor
@ToString
@Entity
public class {{entity.name}} extends BaseEntity {
   {% for field in entity.fields | sort(attribute='name') %}
    /** {{field.comment}} */
    {% for annot in field.annotations  %}
    {{annot}}{% endfor %}
    private {{field.type}} {{field.name}};
   {% endfor %}
    public {{entity.name}}() {
        super();        
    }    
} """,
    'icontroller.java' :  """package {{package}};

import java.util.List;

import org.springframework.http.ResponseEntity;

public interface IController<T> {

    public ResponseEntity<T> create(T n);

    public List<T> getAll();

    public List<T> getAllBySomeId(String id);

    public T getOne(String id);

    public T update(String id, T n);

    public void delete(String id);

} """,
    'IService.java' :  """package {{package}};

import java.util.List;

public interface IService<T> {

    public T create(T n);

    public List<T> getAll();

    public List<T> getAllBySomeId(String id);

    public T getOne(String id);

    public T update(T n);

    public void deleteone(String id);
} """,
    'log4j2.xml' :  """{% raw %}<?xml version="1.0" encoding="UTF-8"?>
<Configuration>
    <Properties>
        <Property name="LOG_PATTERN">
            %d{yyyy-MM-dd HH:mm:ss.SSS} %5p ${hostName} --- [%15.15t] %-40.40c{1.} : %m%n%ex
        </Property>
        <Property name="LOG_PATTERN_2">
            %style{%d{ISO8601}}{black} %highlight{%-5level }[%style{%t}{bright,blue}] %style{%C{1.}}{bright,yellow}:
            %msg%n%throwable
        </Property>
    </Properties>
    <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
            <PatternLayout pattern="${LOG_PATTERN}"/>
        </Console>{% endraw %}
        <RollingFile name="RollingFile"
                     fileName="/usr/share/tomcat/{{logger.projectName}}/logs/{{logger.projectName}}-logger-log4j2.log"
                     filePattern="/usr/share/tomcat/{{logger.projectName}}/logs/$${date:yyyy-MM}/{{logger.projectName}}-logger-log4j2-%d{-dd-MMMM-yyyy}-%i.log.gz">
            <PatternLayout>
                <pattern>%d %p %C{1.} [%t] %m%n</pattern>
            </PatternLayout>
            <Policies>
                <!-- rollover on startup, daily and when the file reaches 
                    10 MegaBytes -->
                <OnStartupTriggeringPolicy/>
                <SizeBasedTriggeringPolicy
                        size="10 MB"/>
                <TimeBasedTriggeringPolicy/>
            </Policies>
        </RollingFile>
    </Appenders>

    <Loggers>
        <!-- LOG everything at INFO level -->
        <Root level="{{logger.RootLoggerLevel}}">
            <AppenderRef ref="Console"/>
            <AppenderRef ref="RollingFile"/>
        </Root>
        {% for logg in logger.Loggers %}
        <Logger name="{{logg.name}}" level="{{logg.level}}"></Logger>{% endfor %}
    </Loggers>

</Configuration> """,
    'MyErrorController.java' :  """package {{package}};

import org.springframework.http.*;
import org.springframework.stereotype.Controller;
import org.springframework.boot.web.servlet.error.ErrorController;
import org.springframework.web.bind.annotation.*;
import lombok.extern.slf4j.Slf4j;
import javax.servlet.*;
import javax.servlet.http.*;

@Slf4j
@Controller
public class MyErrorController implements ErrorController {

  @RequestMapping("/error")
  @ResponseBody
  public String handleError(HttpServletRequest request) {
      Integer statusCode = (Integer) request.getAttribute("javax.servlet.error.status_code");
      Exception exception = (Exception) request.getAttribute("javax.servlet.error.exception");
      return String.format("<html><body><h2>{{project.name}}-{{project.version}}:  Error Page</h2><div>Status code: <b>%s</b></div>"
                      + "<div>Exception Message: <b>%s</b></div><body></html>",
              statusCode, exception==null? "N/A": exception.getMessage());
  }

  @Override
  public String getErrorPath() {
      return "/error";
  }
} """,
    'pom.xml' :  """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.2.0.BUILD-SNAPSHOT</version>
        <relativePath/>
        <!-- lookup parent from repository -->
    </parent>
    <groupId>{{pom.package}}</groupId>
    <artifactId>{{pom.name}}</artifactId>
    <version>{{pom.version}}</version>
    <name>{{pom.longName}}</name>
    <description>{{pom.description}}</description>
    <url>{{pom.url}}</url>
    <packaging>war</packaging>
    <properties>
        <java.version>11</java.version>
        <start-class>{{pom.package}}.Application</start-class>
    </properties>
    <profiles>
        <profile>
            <id>dev</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <properties>
                <springProfile>dev</springProfile>
            </properties>
            <dependencies>
                <dependency>
                    <groupId>com.h2database</groupId>
                    <artifactId>h2</artifactId>
                    <version>1.4.199</version>
                    <scope>runtime</scope>
                </dependency>
            </dependencies>
        </profile>
        <profile>
            <id>prod</id>
            <properties>
                <springProfile>prod</springProfile>
            </properties>
            <activation>
                <activeByDefault>false</activeByDefault>
            </activation>
        </profile>
        <profile>
            <id>test</id>
            <properties>
                <springProfile>test</springProfile>
            </properties>
            <activation>
                <activeByDefault>false</activeByDefault>
            </activation>
        </profile>
    </profiles>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
            <exclusions>
                <exclusion>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-starter-logging</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <!-- Swagger -->
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger2</artifactId>
            <version>2.6.1</version>
            <scope>compile</scope>
        </dependency>
        <!-- Swagger UI -->
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger-ui</artifactId>
            <version>2.6.1</version>
            <scope>compile</scope>
        </dependency>
        <dependency>
            <groupId>com.itextpdf</groupId>
            <artifactId>html2pdf</artifactId>
            <version>2.1.3</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-log4j2</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-thymeleaf</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt</artifactId>
            <version>0.9.0</version>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
        </dependency>
        <dependency>
            <groupId>org.jetbrains</groupId>
            <artifactId>annotations</artifactId>
            <version>17.0.0</version>
            <scope>compile</scope>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.6</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>test</scope>
            <version>1.4.199</version>
        </dependency>
        <dependency>
            <groupId>org.apache.httpcomponents</groupId>
            <artifactId>httpclient</artifactId>
            <version>4.5.6</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <artifactId>maven-antrun-plugin</artifactId>
                <executions>
                    <execution>
                        <phase>generate-resources</phase>
                        <goals>
                            <goal>run</goal>
                        </goals>
                        <configuration>
                            <tasks>
                                <echo>current active profile: ${springProfile}</echo>
                            </tasks>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-checkstyle-plugin</artifactId>
                <configuration>
                    <configLocation>google_checks.xml</configLocation>
                </configuration>
                <version>2.17</version>
            </plugin>
            <plugin>
                <groupId>org.apache.tomcat.maven</groupId>
                <artifactId>tomcat7-maven-plugin</artifactId>
                <version>2.2</version>
                <configuration>
                    <url>http://localhost:8080/manager/text</url>
                    <server>TomcatServer</server>
                    <path>{{pom.restPath}}</path>
                </configuration>
            </plugin>
            <plugin>
                <groupId>pl.project13.maven</groupId>
                <artifactId>git-commit-id-plugin</artifactId>
                <version>2.2.4</version>
                <executions>
                    <execution>
                        <id>get-the-git-infos</id>
                        <goals>
                            <goal>revision</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <dotGitDirectory>${project.basedir}/.git</dotGitDirectory>
                    <prefix>git</prefix>
                    <verbose>true</verbose>
                    <generateGitPropertiesFile>true</generateGitPropertiesFile>
                    <generateGitPropertiesFilename>${project.build.outputDirectory}/git.properties
                    </generateGitPropertiesFilename>
                    <format>json</format>
                    <gitDescribe>
                        <skip>false</skip>
                        <always>false</always>
                        <dirty>-dirty</dirty>
                    </gitDescribe>
                    <excludeProperties>
                        <excludeProperty>git.commit.*</excludeProperty>
                        <excludeProperty>git.remote.origin.url</excludeProperty>
                    </excludeProperties>
                    <failOnNoGitDirectory>false</failOnNoGitDirectory>
                    <failOnUnableToExtractRepoInfo>false</failOnUnableToExtractRepoInfo>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.0</version>
                <configuration>
                    <source>11</source>
                    <target>11</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
    <repositories>
        <repository>
            <id>spring-snapshots</id>
            <name>Spring Snapshots</name>
            <url>https://repo.spring.io/snapshot</url>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </repository>
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
        </repository>
    </repositories>
    <pluginRepositories>
        <pluginRepository>
            <id>spring-snapshots</id>
            <name>Spring Snapshots</name>
            <url>https://repo.spring.io/snapshot</url>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </pluginRepository>
        <pluginRepository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
        </pluginRepository>
    </pluginRepositories>
</project> """,
    'README.md' :  """
# {{project.name}} - {{project.version}}

**{{project.longname}}**
**{{project.description}}**

**{{project.longname}}**
Information URL      :**{{project.url}}** <br/>
Source code packages : **{{project.package}}** <br/>
Deployed at          :**{{project.restPath}} / {{project.version}}** <br/>

## Pre-Install

### What needed for installation 
* Maven
* Java 11
* postgreSQL

### Maven
```
sudo apt get install maven
```
### JAVA 11
```
sudo add-apt-repository ppa:openjdk-r/ppa
sudo apt-get update -q
sudo apt install -y openjdk-11-jdk
sudo apt install -y openjdk-11-jre
```
Verify the installation with:
```
java -version
```
### Postgresql

```
sudo apt install postgresql postgresql-contrib
```
More info in setting [users](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)

Postgres Database and user configuration
```
user@user-VirtualBox:~/Documents/ebill$ psql -h localhost -U postgres -d postgres
Password for user postgres: 
psql (10.6 (Ubuntu 10.6-0ubuntu0.18.04.1), server 11.2 (Debian 11.2-1.pgdg90+1))
postgres=#
postgres=# create database "essDB";
CREATE DATABASE
postgres=# create user "easin" with password 'Easin';
CREATE ROLE
postgres=# grant ALL on database "essDB" to "easin";
GRANT

```
## Server

To compile

```
 mvn clean package
```
To run

```
mvn spring-boot:run
```

## Swagger docs 

It Can be found under <br/>
 [http://localhost:8080{{project.restPath}}/{{project.version}}/swagger-ui.html](http://localhost:8080{{project.restPath}}/{{project.version}}/swagger-ui.html)

OR json format under <br/>
 [http://localhost:8080{{project.restPath}}/{{project.version}}/v2/api-docs](http://localhost:8080{{project.restPath}}/{{project.version}}/v2/api-docs)

where **{{project.restPath}}/{{project.version}}** can be found and modified in file  **[application.yaml](src/main/resources/application.yaml)** :
```
server:
  servlet:
    context-path: /serverTest/0.0.1-SNAP
``` """,
    'Repository.java' :  """package {{package}};

import {{Entitypackage}};
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface {{entityName}}Repository extends JpaRepository<{{entityName}}, String> {
	public List<{{entityName}}> findByName(String name);
} """,
    'RequestLoggingFilterConfig.java' :  """package {{package}};

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.filter.CommonsRequestLoggingFilter;

@Configuration
public class RequestLoggingFilterConfig {

    private final int MAX_PAYLOAD_LOG_BUFFER_LENGTH = 10000;

    @Bean
    public CommonsRequestLoggingFilter logFilter() {

        CommonsRequestLoggingFilter filter = new CommonsRequestLoggingFilter();
        filter.setIncludeQueryString(true);
        filter.setIncludePayload(true);
        filter.setMaxPayloadLength(MAX_PAYLOAD_LOG_BUFFER_LENGTH);
        filter.setIncludeHeaders(false);
        filter.setAfterMessageSuffix(" ============== DONE =============== ");
        filter.setBeforeMessagePrefix(" =========== STARTING  =========== ");
        return filter;
    }
} """,
    'ResourceBadParameterException.java' :  """package {{package}};

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@Getter
@Setter
@ToString
@ResponseStatus(value = HttpStatus.BAD_REQUEST)
public class ResourceBadParameterException extends RuntimeException {

    private static final long serialVersionUID = -1517971622745346451L;
    private String resourceName;
    private String fieldName;
    private Object fieldValue;

    public ResourceBadParameterException(String resourceName, String fieldName, Object fieldValue) {
        super(String.format("%s Bad request with parmeter %s : '%s'", resourceName, fieldName, fieldValue));
        this.resourceName = resourceName;
        this.fieldName = fieldName;
        this.fieldValue = fieldValue;
    }

} """,
    'ResourceNotFoundException.java' :  """package {{package}};

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@Getter
@Setter
@ToString
@ResponseStatus(value = HttpStatus.NOT_FOUND)
public class ResourceNotFoundException extends RuntimeException {
	/**
	 * 
	 */
	private static final long serialVersionUID = -1517971622745346451L;
	private String resourceName;
	private String fieldName;
	private Object fieldValue;
	public ResourceNotFoundException( String message) {
		super(message);
		this.resourceName = "";
		this.fieldName = "";
		this.fieldValue = "";
	}
	
	public ResourceNotFoundException( String resourceName, String fieldName, Object fieldValue) {
	    super(String.format("%s not found with %s : '%s'", resourceName, fieldName, fieldValue));
	    this.resourceName = resourceName;
	    this.fieldName = fieldName;
	    this.fieldValue = fieldValue;
	}

} """,
    'Service.java' :  """package {{package}};


import {{package}}.IService;
import {{projectPackage}}.exceptions.ResourceBadParameterException;
import {{projectPackage}}.exceptions.ResourceNotFoundException;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import {{Entitypackage}};
import {{Repositorypackage}};
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
public class {{entityName}}Service  implements IService<{{entityName}}> {

    @Autowired
    private {{entityName}}Repository erepo;


    @Override
    public {{entityName}} create({{entityName}} n) {
        log.info("Saving new  {{entityName}} .. " + n.toString());
        return erepo.save(n);
    }

    @Override
    public List<{{entityName}}> getAll() {
        log.info("Getting All  .. ");
            return erepo.findAll();
    }

    @Override
    public List<{{entityName}}> getAllBySomeId(String id) {
        log.info("Getting All by some id  ..  " + id);
        // Todo correctly
        return erepo.findAll();
    }

    @Override
    public {{entityName}} getOne(String id) {
        log.info("Getting one with id   .. " + id);
        {{entityName}} cm = erepo.findById(id).orElseThrow(() -> new ResourceNotFoundException("{{entityName}}", "id", id));
        return cm;
    }

    @Override
    public void deleteone(String id) {
        log.info("Deleting one with id   .. " + id);
        if (id == null) {
            throw new ResourceNotFoundException("{{entityName}}", "id", id);
        }
        if (this.erepo.existsById(id)) {
            {{entityName}} cm = erepo.findById(id).orElseThrow(() -> new ResourceNotFoundException("{{entityName}}", "id", id));

            erepo.deleteById(id);
        } else {
            throw new ResourceNotFoundException("{{entityName}}", "id", id);
        }
    }

    @Override
    public {{entityName}} update({{entityName}} n) {
        if (n == null) {
            throw new ResourceNotFoundException("{{entityName}}", "id", n);
        }
        log.info("Updating one  {{entityName}}   .. " + n.toString());
        return erepo.findById(n.getId()).map(found -> {
            {% for field in entity.fields | sort(attribute='name') %}found.set{{field.name[0]|upper}}{{field.name[1:] }}(n.get{{field.name[0]|upper}}{{field.name[1:]}}());
            {% endfor %}
            return erepo.save(found);
        }).orElseThrow(() -> {
            throw new ResourceNotFoundException("{{entityName}}", "id", n.getId());
        });
    }
} """,
    'StatusController.java' :  """package {{package}};

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

@Controller
@RequestMapping(path = "/status")
public class StatusController {

    @RequestMapping(value = "/version", method = RequestMethod.GET, produces = "application/json")
    @ResponseBody
    public Map<String, String> versionInformation() throws IOException {
        return readGitProperties();
    }

    private Map<String, String> readGitProperties() {
        ClassLoader classLoader = getClass().getClassLoader();
        Map<String, String> ll = new HashMap<String, String>();
        try {
            InputStream inputStream = classLoader.getResourceAsStream("git.properties");
            JsonNode node = new ObjectMapper().readTree(inputStream);
            JsonNode jsnode;
            jsnode = node.get("git.branch");
            ll.put("branch", jsnode.textValue());
            jsnode = node.get("git.build.time");
            ll.put("build_time", jsnode.textValue());
            jsnode = node.get("git.build.user.email");
            ll.put("email", jsnode.textValue());
            jsnode = node.get("git.build.version");
            ll.put("version", jsnode.textValue());
            jsnode = node.get("git.closest.tag.name");
            /* next fies are setting issue ..  not really needed !
            ll.put("closest_tag", jsnode.textValue());
            jsnode = node.get("git.commit.id.abbrev");
            ll.put("short_hash", jsnode.textValue());
            jsnode = node.get("git.commit.time");
            ll.put("commit_time", jsnode.textValue());*/
        } catch (IOException e1) {
            e1.printStackTrace();
        }
        return ll;
    }
} """,
    'SwaggerConfiguration.java' :  """package {{project.package}};

import static springfox.documentation.builders.PathSelectors.regex;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

@Configuration
@EnableSwagger2
public class SwaggerConfiguration {
    @Bean
    public Docket api() { 
        return new Docket(DocumentationType.SWAGGER_2)  
          .select()                                  
          .apis(RequestHandlerSelectors.basePackage("{{project.package}}"))
          .paths(regex("{{ApiPrefix}}.*"))
          .build();                                           
    }
} """,
    'WebInitializer.java' :  """package {{package}};

import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class WebInitializer extends SpringBootServletInitializer {

    @Override
    protected final  SpringApplicationBuilder configure
        (final SpringApplicationBuilder application) {
        log.warn(" .. .. .. .. .Initilizing App  .. .. ... .. .. ");
        return application.sources(Application.class);
    }
} """}
