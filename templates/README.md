
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
```
