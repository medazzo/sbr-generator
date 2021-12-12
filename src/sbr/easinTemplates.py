# ----------------------------------------------------
# Generated Files  Containing templates as variables
# ---------------------------------------------------

templates = {
    "Application.java": """package {{package}};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@SpringBootApplication
@ComponentScan("{{package}}")
public class Application {

    public static final String EMAIL_TEMPLATE_ENCODING = "UTF-8";

    public static void main(final String[] args) {
        SpringApplication.run(Application.class, args);
    }

} """,
    "application.yaml": """spring:
  profiles:
    active: "dev"
  thymeleaf:
    prefix: classpath:/templates/
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
    url: jdbc:h2:/tmp/{{project.name}}/sbr-gen-database.h2;DB_CLOSE_ON_EXIT=FALSE
    username: easin
    password:
    driverClassName: org.h2.Driver
  jpa:
    generate-ddl: true
    properties:
      hibernate:
        default_schema: public
        dialect: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: update
    show-sql: true
  jackson:
    serialization:
      FAIL_ON_EMPTY_BEANS: False
debug: true
logging:
  level:
    org:
      springframework:
        web: DEBUG
      hibernate: DEBUG
      boot:
        autoconfigure:
          logging: INFO
---

spring:
  profiles: test
  datasource:
    url: jdbc:h2:mem:test;DB_CLOSE_ON_EXIT=FALSE
    username: easin
    password:
    driverClassName: org.h2.Driver
    jpa:
      generate-ddl: true
      properties:
        hibernate:
          default_schema: public
          dialect: org.hibernate.dialect.H2Dialect
      hibernate:
        ddl-auto: create-drop
      show-sql: true
    jackson:
      serialization:
        FAIL_ON_EMPTY_BEANS: False
debug: true
logging:
  level:
    org:
      springframework:
        web: DEBUG
      hibernate: DEBUG
      boot:
        autoconfigure:
          logging: INFO
---

spring:
  profiles: prod
  datasource:
    url: jdbc:postgresql://localhost:5432/essDB
    username: easin
    password: Easin
    driverClassName: org.postgresql.Driver
    jpa:
      generate-ddl: true
      properties:
        hibernate:
          default_schema: public
          dialect: org.hibernate.dialect.PostgreSQL82Dialect
      hibernate:
        ddl-auto: none
      show-sql: true
    jackson:
      serialization:
        FAIL_ON_EMPTY_BEANS: False """,
    "AuthenticationController.java": """package {{package}};

import {{Securitypackage}}.TokenProvider;
import {{EntitypackageUser}};
import {{Securitypackage}}.api.AuthToken;
import {{Securitypackage}}.api.LoginUser;
import {{ServicepackageUser}};
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

@CrossOrigin(origins = "*", maxAge = 3600)
@RestController
@RequestMapping("{{mapping}}")
public class AuthenticationController {

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private TokenProvider jwtTokenUtil;

    @Autowired
    private UserService userService;

    @RequestMapping(value = "/token", method = RequestMethod.POST)
    public ResponseEntity<?> register(@RequestBody LoginUser loginUser) throws AuthenticationException {

        final Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        loginUser.getEmail(),
                        loginUser.getPassword()
                )
        );
        SecurityContextHolder.getContext().setAuthentication(authentication);
        final String token = jwtTokenUtil.generateToken(authentication);

        User user = userService.GetUserByUsername(authentication.getName());
        return ResponseEntity.ok(new AuthToken(token, user));
    }
} """,
    "AuthoritiesConstants.java": """package {{package}};

/**
 * Constants for Spring Security authorities.
 */
public final class AuthoritiesConstants {

    public static final String ADMIN = "ROLE_ADMIN";

    public static final String USER = "ROLE_USER";
{% for role in roles  %}
    public static final String {{role}} = "ROLE_{{role}}";
{% endfor %}

}
 """,
    "AuthToken.java": """package {{package}};

import {{EntitypackageUser}};
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class AuthToken {

    private String token;
    private User user;

} """,
    "BaseEntity.java": """package {{package}};

import java.io.Serializable;
import java.util.Date;

import javax.persistence.*;

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

    @Version
    @ApiModelProperty(hidden = true)
    private Integer version = 1;

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
    "CommandInitializer.java": """package {{package}};

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Component
class CommandInitializer implements CommandLineRunner {

    @Override
    public void run(String... args) throws Exception {
        log.warn("Preparing some stuff to do before run applications .. ");
    }
} """,
    "Constants.java": """package {{package}};

public class Constants {

    public static final long ACCESS_TOKEN_VALIDITY_SECONDS = 2 * 60 * 60;
    public static final String SIGNING_KEY = "{{key}}";
    public static final String TOKEN_PREFIX = "Bearer ";
    public static final String HEADER_STRING = "Authorization";
    public static final String AUTHORITIES_KEY = "scopes";
    public static final int QUOTATIONS_COUNT_EXPIRES_DAY = 60;
    public static final String LOGIN_REGEX = "^[_.@A-Za-z0-9-]*$";
    public static final String SYSTEM_ACCOUNT = "system";
    public static final String DEFAULT_LANGUAGE = "en";
    public static final String ANONYMOUS_USER = "anonymoususer";

    private Constants() {
    }

} """,
    "controller.java": """package {{package}};

import {{Entitypackage}};
import {{projectPackage}}.exceptions.ResourceBadParameterException;
import {{projectPackage}}.exceptions.ResourceNotFoundException;
import {{Servicepackage}};
{%- if security  %}
import org.springframework.security.access.prepost.PreAuthorize;
{%- endif  %}
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
    @ApiOperation(value = "Create a new  {{entityName}} ", nickname = "CreateNew{{entityName}}", tags = { "{{entityName}}" })
 {%- if security %}
 {%- if 'User' != entityName %}
    @PreAuthorize("hasAnyRole('ADMIN', 'USER'{%- for role in roles  %}, '{{role}}'{%- endfor %})")
 {%- endif  %}
 {%- endif  %}
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
 {%- if security  %}
    @PreAuthorize("hasAnyRole('ADMIN', 'USER'{%- for role in roles  %}, '{{role}}'{%- endfor %})")
 {%- endif  %}
    public List<{{entityName}}> getAll() {
        log.debug(" -->  Will Get All {{entityName}}'s'");
        return service.getAll();
    }

    @GetMapping("/all/{id}")
    @ResponseBody
    @Override
    @ApiOperation(value = "Get all stored {{entityName}} using some extra ID( user/group ID or some other ID)", nickname = "GetAll{{entityName}}BySomeID", tags = { "{{entityName}}" })
{%- if security  %}
    @PreAuthorize("hasAnyRole('ADMIN', 'USER'{%- for role in roles  %}, '{{role}}'{%- endfor %})")
{%- endif  %}
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
    @ApiOperation(value = "Get stored {{entityName}} using his unique ID", nickname = "GetOne{{entityName}}ById", tags = { "{{entityName}}" })
 {%- if security  %}
     @PreAuthorize("hasAnyRole('ADMIN', 'USER'{%- for role in roles  %}, '{{role}}'{%- endfor %})")
 {%- endif  %}
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
    @ApiOperation(value = "Update the stored {{entityName}} using his unique ID", nickname = "UpdateOne{{entityName}}ById" , tags = { "{{entityName}}" })
{%- if security  %}
    @PreAuthorize("hasAnyRole('ADMIN', 'USER'{%- for role in roles  %}, '{{role}}'{%- endfor %})")
{%- endif  %}
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
    @ApiOperation(value = "Removing the stored {{entityName}} using his unique ID", nickname = "RemoveOne{{entityName}}ById" , tags = { "{{entityName}}" })
{%- if security  %}
    @PreAuthorize("hasAnyRole('ADMIN', 'USER'{%- for role in roles  %}, '{{role}}'{%- endfor %})")
{%- endif  %}
    public void delete(@PathVariable String id) {
        if (id == null) {
            throw new ResourceNotFoundException("{{entityName}}", "id", id);
        }
        log.debug(" --> Will remove one with id " + id);
        service.deleteone(id);
    }
} """,
    "CrudUnitTest.java": """package {{package}};

import {{Entitypackage}};
import {{Servicepackage}};
{%- if security %}
import {{packageSecurity}}.api.AuthToken ;
import java.util.Date;
import {{packageSecurity}}.AuthoritiesConstants ;
import org.springframework.security.crypto.bcrypt.BCrypt;
{%-endif %}
{%- for field in entity.fields %}{%- if field.foreignKey  %}
import {{EntityBasepackage}}.{{field.foreignEntity}};
import {{ServiceBasepackage}}.{{field.foreignEntity}}Service;
{%-endif %} {% endfor %}
import {{packageConstants}}.Constants;
import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.extern.slf4j.Slf4j;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import org.junit.After;
import org.junit.Before;
import static org.hamcrest.Matchers.hasSize;
import static org.junit.Assert.assertEquals;
import org.junit.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.runner.RunWith;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import javax.annotation.PostConstruct;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase.Replace;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;

@RunWith(SpringRunner.class)
@ExtendWith(SpringExtension.class)
@SpringBootTest()
@AutoConfigureMockMvc
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace=Replace.NONE)
@Slf4j
public class {{entityName}}CrudUnitTest {

    @Autowired
    private MockMvc mockMvc;
    @Autowired
    private {{entityName}}Service service;
{%- for field in entity.fields  %}{%- if field.foreignKey  %}
    @Autowired
    private {{field.foreignEntity}}Service fk{{field.foreignEntity}}service;
{%-endif %} {% endfor %}
{%- if security %}
    private AuthToken auth ;
{%-endif %}
    Map<String, Object> hm = new HashMap<>();
    @Autowired
    private ObjectMapper mapper;

    {%- if security  %}
    public  AuthToken DoUserAuthentication() throws Exception {
        String body = "{\\\"email\\\":\\\"{{uemail}}\\\",\\\"password\\\":\\\"{{upassword}}\\\"}";
        log.debug(" Try to authenticate  user '{{uemail}}'' with his password '{{upassword}}'.");
        MvcResult result = mockMvc.perform(
                    post("/api/auth/token")
                    .contentType(MediaType.APPLICATION_JSON)
                    .accept(MediaType.APPLICATION_JSON)
                    .content(body))
                .andExpect(status().isOk()).andReturn();

        // Verify Getted {{entityName}} using Service
        AuthToken authGetted = mapper.readValue(result.getResponse().getContentAsByteArray(),AuthToken.class);
        log.debug(" >>> User '{{uemail}}'' has been authenticated , his tomen is  '"+ authGetted.getToken() +"'.");
        return authGetted;
    }

    public  AuthToken DoAdminAuthentication() throws Exception {
        String body = "{\\\"email\\\":\\\"{{aemail}}\\\", \\\"password\\\":\\\"{{apassword}}\\\"}";
        log.debug(" Try to authenticate  Admin '{{aemail}}'' with his password '{{apassword}}'.");
        MvcResult result = mockMvc.perform(
                    post("/api/auth/token")
                    .contentType(MediaType.APPLICATION_JSON)
                    .accept(MediaType.APPLICATION_JSON)
                    .content(body))
                .andExpect(status().isOk()).andReturn();

        // Verify Getted {{entityName}} using Service
        AuthToken authGetted = mapper.readValue(result.getResponse().getContentAsByteArray(),AuthToken.class);
        log.debug(" >>> Admin '{{uemail}}'' has been authenticated , his tomen is  '"+ authGetted.getToken() +"'.");
        return authGetted;
    }

    @Test
    public void nonexistentUserCannotGetToken() throws Exception {
        String body = "{\\\"username\\\":\\\"nonexistentuser\\\", \\\"password\\\":\\\\password \\\"}";
        mockMvc.perform(
                    post("/v2/token")
                    .contentType(MediaType.APPLICATION_JSON)
                    .accept(MediaType.APPLICATION_JSON)
                    .content(body))
                .andExpect(status().isUnauthorized())
                .andReturn();
        log.debug(" Try to authenticate  non Existant User !.");
    }
    {%- endif  %}

{%- if security %}
{%- if 'User' == entity.name%}

    @Test
    public void UserCreateAndAuthenticateTest() throws Exception {
        log.debug(" in {{entityName}}  Create And Authenticate Test !.");
        auth = DoAdminAuthentication() ;
        // check Get all is empty
        CheckAllEmpty();
        // Create Test User Object
         User user = Create();
         log.debug(" Will CreateAndSave {{entityName}}  !." +user.toString());
         log.warn( " !!!!!! the generated entity sent to server is ################### >" + asJsonString(user));
         // Create {{entityName}} using API and verify returned One
         MvcResult mvcResult = mockMvc.perform(
                 post("{{mapping}}/new")
                 .contentType(MediaType.APPLICATION_JSON)
                 .content(asJsonString(user)))
                 .andExpect(status().isCreated())
                 .andDo(print())
                 .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                 .andExpect(MockMvcResultMatchers.jsonPath("id").isNotEmpty())
                 {%- for field in entity.fields %} {% if not field.foreignKey  %}
                 .andExpect(MockMvcResultMatchers.jsonPath("{{field.name}}").value(user.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                 {%-endif %} {% endfor %}
                 .andReturn();
         // Verify Created {{entityName}} using Service
         User saved = mapper.readValue(mvcResult.getResponse().getContentAsByteArray(), User.class);
         User found = service.getOne(saved.getId());
         assertEquals(found.getId(), saved.getId());
         {%- for field in entity.fields %} {% if not field.foreignKey  %}
         assertEquals(found.get{{field.name[0]|upper}}{{field.name[1:]}}(), saved.get{{field.name[0]|upper}}{{field.name[1:]}}());
         {%-endif %} {% endfor %}// return
        // Get {{entityName}} using API and verify returned One
        MvcResult mvcgResult = mockMvc.perform(
                get("{{mapping}}/{id}", found.getId())
                .header("Authorization", "Bearer "+auth.getToken())
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("{{field.name}}").value(found.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                .andReturn();
        // Do Created {{entityName}} authentication
        log.warn(" =====>  =====>  =====>  =====> Will start to Login created USER !!!!!!!!!");
        String body = "{\\\"email\\\":\\\""+user.getEmail()+"\\\", \\\"password\\\":\\\""+user.getPassword()+"\\\"}";
        log.debug(" Try to Created USer '"+user.getEmail()+"' with his password '"+user.getPassword()+"'.");
        log.warn(" =====>  =====>  =====>  =====> Will start to Login created USER !!!!!!!!!");
        MvcResult result = mockMvc.perform(
                    post("/api/auth/token")
                    .contentType(MediaType.APPLICATION_JSON)
                    .accept(MediaType.APPLICATION_JSON)
                    .content(body))
                .andExpect(status().isOk()).andReturn();
        log.warn(" =====>  =====>  =====>  =====> Done try to Login created USER !!!!!!!!!");
        log.warn(" =====>  =====>  =====>  =====> Done try to Login created USER !!!!!!!!!");
        // Verify Getted {{entityName}} using Service
        AuthToken authGetted = mapper.readValue(result.getResponse().getContentAsByteArray(),AuthToken.class);
        log.debug(" >>> User '"+user.getEmail()+"' has been authenticated , his token is  '"+ authGetted.getToken() +"'.");
        // Remove the Created {{entityName}}
        RemoveOne( saved.getId(), mockMvc, auth);
        // check Get all is empty
        CheckAllEmpty();
    }
{%- endif  %}
{%- endif  %}
    @Test
    public void {{entityName}}CreateTest() throws Exception {
        log.debug(" in {{entityName}}  CreateTest !.");
        {%- if security  %}
        auth = DoAdminAuthentication() ;
        {%- endif  %}
        // check Get all is empty
        CheckAllEmpty();
        // Create Test {{entityName}} Object
{%- if security %}
        {{entityName}} created = CreateAndSave(mockMvc, mapper, service, auth);
{%- else %}
        {{entityName}} created = CreateAndSave(mockMvc, mapper, service);
{%- endif %}
        // Remove the Created {{entityName}}
{%- if security  %}
        RemoveOne( created.getId(), mockMvc, auth);
{%- else  %}
        RemoveOne( created.getId(), mockMvc);
{%- endif  %}
        // check Get all is empty
        CheckAllEmpty();
    }

    @Test
    public void {{entityName}}ReadTest() throws Exception {
        log.debug(" in {{entityName}}  ReadTest !.");
        {%- if security  %}
        auth = DoAdminAuthentication() ;
        {%- endif  %}

        // check Get all is 0
        CheckAllEmpty();
        // Create Test {{entityName}} Object
{%- if security %}
        {{entityName}} saved = CreateAndSave(mockMvc, mapper, service, auth);
{%- else %}
        {{entityName}} saved = CreateAndSave(mockMvc, mapper, service);
{%- endif %}
        // Get {{entityName}} using API and verify returned One
        MvcResult mvcgResult = mockMvc.perform(
                get("{{mapping}}/{id}", saved.getId())
                {%- if security  %}
                .header("Authorization", "Bearer "+auth.getToken())
                {%- endif  %}
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                .andReturn();
        // Verify Getted {{entityName}} using Service
        {{entityName}} getted = mapper.readValue(mvcgResult.getResponse().getContentAsByteArray(), {{entityName}}.class);
        {{entityName}} found = service.getOne(getted.getId());
        assertEquals(found.getId(), getted.getId());
        {%- for field in entity.fields %} {% if not field.foreignKey  %}
        assertEquals(found.get{{field.name[0]|upper}}{{field.name[1:]}}(), getted.get{{field.name[0]|upper}}{{field.name[1:]}}());
        {%-endif %} {% endfor %}
        // Remove the Created {{entityName}}
{%- if security  %}
        RemoveOne( found.getId(), mockMvc, auth);
{%- else  %}
        RemoveOne( found.getId(), mockMvc);
{%- endif  %}

        // check Get all is 0
        CheckAllEmpty();
    }

    @Test
    public void {{entityName}}ReadAllTest() throws Exception {
        log.debug(" in {{entityName}}  ReadAllTest !.");
        {%- if security  %}
        auth = DoAdminAuthentication() ;
        {%- endif  %}
        // Get all
        CheckAllEmpty();
        // Create Test {{entityName}} Object
{%- if security %}
        {{entityName}} saved = CreateAndSave(mockMvc, mapper, service, auth);
{%- else %}
        {{entityName}} saved = CreateAndSave(mockMvc, mapper, service);
{%- endif %}
        // Get All
        mockMvc.perform(
                get("{{mapping}}/all")
                {%- if security  %}
                .header("Authorization", "Bearer "+auth.getToken())
                {%- endif  %}
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
{%- if 'User' == entity.name and security is sameas true %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(3)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[2].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
{%- else %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(1)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
{%- endif %}
                .andReturn();
        // Create Another Test {{entityName}} Object
{%- if security %}
        {{entityName}} saved2 = CreateAndSave(mockMvc, mapper, service, auth);
{%- else %}
        {{entityName}} saved2 = CreateAndSave(mockMvc, mapper, service);
{%- endif %}
        // Get all
        mockMvc.perform(
                get("{{mapping}}/all")
                {%- if security  %}
                .header("Authorization", "Bearer "+auth.getToken())
                {%- endif  %}
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
{%- if 'User' == entity.name and security is sameas true  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(4)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[2].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[3].{{field.name}}").value(saved2.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
{%- else %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(2)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[1].{{field.name}}").value(saved2.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
{%- endif %}
                .andReturn();
        // Remove the Created {{entityName}}
{%- if security  %}
        RemoveOne( saved.getId(), mockMvc, auth);
{%- else  %}
        RemoveOne( saved.getId(), mockMvc);
{%- endif  %}
        // Remove the Created {{entityName}}
{%- if security  %}
        RemoveOne( saved2.getId(), mockMvc, auth);
{%- else  %}
        RemoveOne( saved2.getId(), mockMvc);
{%- endif  %}
        // check Get all is empty
        CheckAllEmpty();
    }

    @Test
    public void {{entityName}}UpdateTest() throws Exception {
        log.debug(" in {{entityName}}  UpdateTest !.");
        {%- if security  %}
        auth = DoAdminAuthentication() ;
        {%- endif  %}
        // Get all
        CheckAllEmpty();
        // Create Test {{entityName}} Object
{%- if security %}
        {{entityName}} saved = CreateAndSave(mockMvc, mapper, service, auth);
{%- else %}
        {{entityName}} saved = CreateAndSave(mockMvc, mapper, service);
{%- endif %}
        // Get All
        mockMvc.perform(
                get("{{mapping}}/all")
                {%- if security  %}
                .header("Authorization", "Bearer "+auth.getToken())
                {%- endif  %}
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
{%- if 'User' == entity.name  and security is sameas true %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(3)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[2].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
{%- else %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(1)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
{%- endif %}
                .andReturn();
        // Update
        {{entityName}} updt = Update(saved);
        // Get Update on Server
        MvcResult mvcResult = mockMvc.perform(
                put("{{mapping}}/{id}", saved.getId())
                {%- if security  %}
                .header("Authorization", "Bearer "+auth.getToken())
                {%- endif  %}
                .contentType(MediaType.APPLICATION_JSON)
                .content(asJsonString(updt))
        )
                .andExpect(status().isOk())
                .andDo(print())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("id").value(updt.getId()))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("{{field.name}}").value(updt.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                .andReturn();
        // Verify Getted {{entityName}}using Service
        {{entityName}} getted = mapper.readValue(mvcResult.getResponse().getContentAsByteArray(), {{entityName}}.class);
        {{entityName}} found = service.getOne(getted.getId());
        assertEquals(found.getId(), getted.getId());
        {%- for field in entity.fields %} {% if not field.foreignKey  %}
        assertEquals(found.get{{field.name[0]|upper}}{{field.name[1:]}}(), getted.get{{field.name[0]|upper}}{{field.name[1:]}}());
        {%-endif %} {% endfor %}
         // Remove the Created {{entityName}}
 {%- if security  %}
         RemoveOne( getted.getId(), mockMvc, auth);
 {%- else  %}
         RemoveOne( getted.getId(), mockMvc);
 {%- endif  %}
        // check Get all is empty
        CheckAllEmpty();
    }

    @Test
    public void {{entityName}}DeleteTest() throws Exception {
        log.debug(" in {{entityName}}  DeleteTest !.");
        {%- if security  %}
        auth = DoAdminAuthentication() ;
        {%- endif  %}
        // check Get all is 0
        CheckAllEmpty();
        // Create Test {{entityName}} Object
{%- if security %}
        {{entityName}} saved = CreateAndSave(mockMvc, mapper, service, auth);
{%- else %}
        {{entityName}} saved = CreateAndSave(mockMvc, mapper, service);
{%- endif %}
        // Get All
        mockMvc.perform(
                get("{{mapping}}/all")
                {%- if security  %}
                .header("Authorization", "Bearer "+auth.getToken())
                {%- endif  %}
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
{%- if 'User' == entity.name  and security is sameas true %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(3)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[2].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
{%- else %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(1)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
{%- endif %}
                .andReturn();
        // Create Another Test {{entityName}} Object
{%- if security %}
        {{entityName}} saved2 = CreateAndSave(mockMvc, mapper, service, auth);
{%- else %}
        {{entityName}} saved2 = CreateAndSave(mockMvc, mapper, service);
{%- endif %}
        // Get all
        mockMvc.perform(
                get("{{mapping}}/all")
                {%- if security  %}
                .header("Authorization", "Bearer "+auth.getToken())
                {%- endif  %}
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
{%- if 'User' == entity.name  and security is sameas true %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(4)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[2].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[3].{{field.name}}").value(saved2.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
{%- else %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(2)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[1].{{field.name}}").value(saved2.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
{%- endif %}
                .andReturn();
        // Remove  first one
{%- if security  %}
        RemoveOne( saved.getId(), mockMvc, auth);
{%- else  %}
        RemoveOne( saved.getId(), mockMvc);
{%- endif  %}

        // Get all
        mockMvc.perform(
                get("{{mapping}}/all")
                {%- if security  %}
                .header("Authorization", "Bearer "+auth.getToken())
                {%- endif  %}
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
{%- if 'User' == entity.name  and security is sameas true %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(3)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[2].{{field.name}}").value(saved2.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
{%- else %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(1)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved2.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
{%-endif %}
                .andReturn();
        // Remove  last one
{%- if security  %}
        RemoveOne( saved2.getId(), mockMvc, auth);
{%- else  %}
        RemoveOne( saved2.getId(), mockMvc);
{%- endif  %}
        // check Get all is empty
        CheckAllEmpty();
    }
    /**
     *
     */
    public void CheckAllEmpty()  throws  Exception{
{%- if 'User' == entity.name %}
        log.debug(" Will CheckAllEmpty in {{entityName}} (Well, not realyy empty, but contains only 2 : since we already have 2 user: admin + user) !.");
{%- else %}
    log.debug(" Will CheckAllEmpty in {{entityName}}  !.");
{%- endif %}
        // check Get all is 0
        mockMvc.perform(
                get("{{mapping}}/all")
                {%- if security  %}
                .header("Authorization", "Bearer "+auth.getToken())
                {%- endif  %}
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
{%- if 'User' == entity.name  and security is sameas true %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(2)));
{%- else %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(0)));
{%- endif %}

    }
    /**
    *
    */
{%- if security  %}
    public static {{entityName}} CreateAndSave(MockMvc movc, ObjectMapper mapp, {{entityName}}Service srvc, AuthToken authent) throws IOException, Exception {
{%- else %}
    public static {{entityName}} CreateAndSave(MockMvc movc, ObjectMapper mapp, {{entityName}}Service srvc) throws IOException, Exception {
{%- endif %}
        // Create  {{entityName}}
        {{entityName}} ent = Create();
        log.debug(" Will CreateAndSave {{entityName}}  !." +ent.toString());
        log.warn( " !!!!!! the generated entity sent to server is ################### >" + asJsonString(ent));
        // Create {{entityName}} using API and verify returned One
        MvcResult mvcResult = movc.perform(
                post("{{mapping}}/new")
                {%- if security  %}
                .header("Authorization", "Bearer "+authent.getToken())
                {%- endif  %}
                .contentType(MediaType.APPLICATION_JSON)
                .content(asJsonString(ent))
        )
                .andExpect(status().isCreated())
                .andDo(print())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("id").isNotEmpty())
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("{{field.name}}").value(ent.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                .andReturn();
        // Verify Created {{entityName}} using Service
        {{entityName}} saved = mapp.readValue(mvcResult.getResponse().getContentAsByteArray(), {{entityName}}.class);
        {{entityName}} found = srvc.getOne(saved.getId());
        assertEquals(found.getId(), saved.getId());
        {%- for field in entity.fields %} {% if not field.foreignKey  %}
        assertEquals(found.get{{field.name[0]|upper}}{{field.name[1:]}}(), saved.get{{field.name[0]|upper}}{{field.name[1:]}}());
        {%-endif %} {% endfor %}// return
        return found;
    }
    /**
     *
     */
{%- if security  %}
    public static  void RemoveOne(String id, MockMvc movc, AuthToken authent) throws Exception{
{%- else %}
    public static  void RemoveOne(String id, MockMvc movc) throws Exception{
{%- endif %}
        log.debug(" Will RemoveOne {{entityName}}  !.");
        movc.perform(
                delete("{{mapping}}/{id}", id)
                {%- if security  %}
                .header("Authorization", "Bearer "+authent.getToken())
                {%- endif  %}
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andReturn();
    }
    /**
     *
     */
    public static {{entityName}} Create() throws  Exception{
        {{entityName}} ent = new {{entityName}}();
        return Update(ent);
    }
    /**
     *
     */
    public static  {{entityName}} Update({{entityName}} old) throws Exception  {
        {%- if 'User' == entity.name %}
        // Add extra for User
        old.setFirstName(HelperTests.randomString(10));
        old.setLastName(HelperTests.randomString(10));
        {%- if security  %}
        old.setPassword(HelperTests.randomString(7));
        old.setMainRole(AuthoritiesConstants.ADMIN);
        {%- endif  %}
        old.setEmail(HelperTests.randomString(10)+"@blabla.com");
        old.setLangKey("EN");
        old.setImageUrl(HelperTests.randomString(10));
        old.setActivated(true);
        {%- endif %}
        {%- for field in entity.fields | sort(attribute='name') %}
                {%- if ('int' == field.type) or ('Integer' == field.type) %}
        old.set{{field.name[0]|upper}}{{field.name[1:]}}(HelperTests.randomInteger(50));
                {%- elif ('double' == field.type) or ('Double' == field.type)  %}
        old.set{{field.name[0]|upper}}{{field.name[1:]}}(HelperTests.randomdouble());
                {%- elif 'String' == field.type %}
                        {%- if '@Email' in field.annotations  %}
        old.set{{field.name[0]|upper}}{{field.name[1:] }}(HelperTests.randomMail());
                        {#- To add support here  for more annotations #}
                        {%- else %}
        old.set{{field.name[0]|upper}}{{field.name[1:]}}(HelperTests.randomString(10));
                        {%- endif %}
                {%- else %}
                        {%- if field.foreignKey  %}
        //String Field referring foreignKey of type  {{field.foreignEntity}} , so let's create one !
        // not really needed to change foreign keys
        // old.set{{field.name[0]|upper}}{{field.name[1:]}}(({{field.foreignEntity}})hm.get("{{field.foreignEntity}}"));
                        {%- else %}
        old.set{{field.name[0]|upper}}{{field.name[1:]}}(new {{field.type}}());  //TODO {{field.type }} Not supported type yet : easy to do!
                        {%- endif %}
                {%- endif %}
        {%- endfor %}
        log.debug(" ##### Updating {{entityName}} >> "+old);
        return old;
    }

    @PostConstruct
    @Before
    public void setUp() throws Exception {
        mapper.registerModule(new JavaTimeModule());
        log.debug(" in  setUp Test {{entityName}}  !.");
        {%- if security  %}
        auth = DoAdminAuthentication() ;
        {%- endif  %}
        /* could be used : tend to generate tests fails ; depeneds on tests order run !!
        {%- for field in entity.fields %}{% if field.foreignKey  %}
        //String Field referring foreignKey of type  {{field.foreignEntity}} , so let's create one !
{%- if security %}
        {{field.foreignEntity}} fk{{field.foreignEntity}} = {{field.foreignEntity}}CrudUnitTest.CreateAndSave(mockMvc, mapper, fk{{field.foreignEntity}}service, auth);
{%- else %}
        {{field.foreignEntity}} fk{{field.foreignEntity}} = {{field.foreignEntity}}CrudUnitTest.CreateAndSave(mockMvc, mapper, fk{{field.foreignEntity}}service);
{%- endif %}
        hm.put("{{field.foreignEntity}}",fk{{field.foreignEntity}});
        {%-endif %} {% endfor %}
        */
    }

    @After
    public void tearDown() throws Exception {
        log.debug(" in  tearDown Test {{entityName}}  !.");
        /* could be used : tend to generate tests fails ; depeneds on tests order run !!
        {%- for field in entity.fields %}{%- if field.foreignKey  %}
        //String Field referring foreignKey of type  {{field.foreignEntity}} , so let's remove it once done wuth test !
        {{field.foreignEntity}} dep{{field.foreignEntity}} = ({{field.foreignEntity}}) hm.get("{{field.foreignEntity}}");
{%- if security  %}
        {{field.foreignEntity}}CrudUnitTest.RemoveOne(dep{{field.foreignEntity}}.getId(), mockMvc, auth);
{%- else %}
        {{field.foreignEntity}}CrudUnitTest.RemoveOne(dep{{field.foreignEntity}}.getId(), mockMvc);
{%- endif %}
        hm.remove("{{field.foreignEntity}}");
        {%-endif %} {% endfor %}
        */
    }
    /**
     *
     */
    private static String asJsonString(final Object obj) {
        try {
            return new ObjectMapper().writeValueAsString(obj);
        } catch (JsonProcessingException e) {
            log.error(e.getMessage() + "Error to map object ");
            throw new RuntimeException(e);
        }
    }
} """,
    "data.sql": """/* Generated Admin user with mail='{{mail}}' and password='{{passwordclear}}' */
INSERT INTO USER ( ACTIVATED , ACTIVATION_KEY , CREATED_AT , EMAIL , FIRST_NAME , ID , IMAGE_URL , LANG_KEY , LAST_NAME , MAIN_ROLE , NAME , PASSWORD_HASH , PHONE , RESET_DATE , RESET_KEY , UPDATED_AT , VERSION ) VALUES (TRUE, 'ACT-KEY-NOT-NEEDED', NOW(), '{{mail}}', ' Me Admin','{{uuid}}','IMAGE_URL-NOT-NEEDED', 'EN', 'Very strong', 'ROLE_ADMIN','Me Strong Admin', '{{password}}', '0022554411887',NOW() , 'RESET_KEY-NOT-NEEDED' , NOW() , 0);

/* Generated USER with mail='{{umail}}' and password='{{upasswordclear}}' */
INSERT INTO USER ( ACTIVATED , ACTIVATION_KEY , CREATED_AT , EMAIL , FIRST_NAME , ID , IMAGE_URL , LANG_KEY , LAST_NAME , MAIN_ROLE , NAME , PASSWORD_HASH , PHONE , RESET_DATE , RESET_KEY , UPDATED_AT , VERSION ) VALUES (TRUE, 'ACT-KEY-NOT-NEEDED', NOW(), '{{umail}}', ' Me User','{{uuuid}}','IMAGE_URL-NOT-NEEDED', 'EN', 'Very Helpful', 'ROLE_USER','Me Useful User', '{{upassword}}', '0022554411887',NOW() , 'RESET_KEY-NOT-NEEDED' , NOW() , 0); """,
    "entity.java": """package {{package}} ;

import javax.persistence.*;
import javax.validation.constraints.*;
import lombok.*;
import lombok.extern.slf4j.Slf4j;
import io.swagger.annotations.ApiModelProperty;
import io.swagger.annotations.ApiModel;
import org.hibernate.annotations.GenericGenerator;
import java.util.Date;
{%- for field in entity.fields | sort(attribute='name') %}
{%- if field.foreignKey   %}
import {{package}}.{{field.foreignEntity}};
{%- endif %}
{% endfor %}
/**
 * {{entity.comment}}
 */
@ApiModel(description = "{{entity.comment}}")
@Slf4j
@Getter
@Setter
@AllArgsConstructor
@ToString
@Entity
public class {{entity.name}} extends BaseEntity {

    @Id
    @GeneratedValue(generator = "system-uuid", strategy = GenerationType.IDENTITY)
    @GenericGenerator(name = "system-uuid", strategy = "uuid2")
    @ApiModelProperty(hidden = true)
    protected String Id;

{%- for field in entity.fields | sort(attribute='name') %}
    /** {{field.comment}} */
    @ApiModelProperty(value = " {{field.comment}} ")
{%- for annot in field.annotations  %}
    {{annot}}
{%- endfor %}
    private {{field.type}} {{field.name}};
{% endfor %}
    /**
    * default constructor
    */
    public {{entity.name}}() {
        super();
    }
} """,
    "HelperTests.java": """package {{package}} ;


import java.security.SecureRandom;

public class HelperTests {

    private static final String CHAR_LOWER = "abcdefghijklmnopqrstuvwxyz";
    private static final String CHAR_UPPER = CHAR_LOWER.toUpperCase();
    private static final String NUMBER = "0123456789";
    private static final String DATA_FOR_RANDOM_STRING = CHAR_LOWER + CHAR_UPPER + NUMBER;
    private static SecureRandom random = new SecureRandom();

    public static int randomInteger(int bound) {
        return  random.nextInt(bound);
    }

    public static double randomdouble() {
        return  Math.random();
    }

    public static String randomString(int length) {
        if (length < 1) throw new IllegalArgumentException();

        StringBuilder sb = new StringBuilder(length);
        for (int i = 0; i < length; i++) {
			// 0-62 (exclusive), random returns 0-61
            int rndCharAt = random.nextInt(DATA_FOR_RANDOM_STRING.length());
            char rndChar = DATA_FOR_RANDOM_STRING.charAt(rndCharAt);
            sb.append(rndChar);

        }

        return sb.toString();

    }
    public static String randomMail() {
        return randomString(10)+"@"+randomString(7)+".com";

    }

} """,
    "IController.java": """package {{package}};

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
    "IService.java": """package {{package}};

import java.util.List;

public interface IService<T> {

    public T create(T n);

    public List<T> getAll();

    public List<T> getAllBySomeId(String id);

    public T getOne(String id);

    public T update(T n);

    public void deleteone(String id);
} """,
    "JwtAuthenticationEntryPoint.java": """package {{package}};

import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.stereotype.Component;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.Serializable;

@Component
public class JwtAuthenticationEntryPoint implements AuthenticationEntryPoint, Serializable {

    private static final long serialVersionUID = -4265382752632842698L;

    @Override
    public void commence(HttpServletRequest request,
            HttpServletResponse response,
            AuthenticationException authException) throws IOException {
            String error = "{\\\"error\\\": \\\""
              + authException.getMessage()
              + "\\\"}";
            response.setContentType("application/json");
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            response.getOutputStream().println(error);
    }
} """,
    "JwtAuthenticationFilter.java": """package {{package}};

import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.SignatureException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.web.filter.OncePerRequestFilter;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import static {{packageConstants}}.Constants.HEADER_STRING;
import static {{packageConstants}}.Constants.TOKEN_PREFIX;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    @Autowired
    @Qualifier("userService")
    private UserDetailsService userDetailsService;

    @Autowired
    private TokenProvider jwtTokenUtil;

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        String header = req.getHeader(HEADER_STRING);
        String email = null;
        String authToken = null;
        if (header != null && (header.startsWith(TOKEN_PREFIX) || header.startsWith(" " + TOKEN_PREFIX))) {
            authToken = header.replace(TOKEN_PREFIX, "");
            try {
                email = jwtTokenUtil.getEmailFromToken(authToken);
            } catch (IllegalArgumentException e) {
                log.error("an error occured during getting email from token", e);
            } catch (ExpiredJwtException e) {
                log.warn("the token is expired and not valid anymore", e);
            } catch (SignatureException e) {
                log.error("Authentication Failed. email or Password not valid.");
            }
        } else {
            log.warn("couldn't find bearer string, will ignore the header");
        }
        if (email != null && SecurityContextHolder.getContext().getAuthentication() == null) {

            UserDetails userDetails = userDetailsService.loadUserByUsername(email);

            if (jwtTokenUtil.validateToken(authToken, userDetails)) {
                UsernamePasswordAuthenticationToken authentication
                        = jwtTokenUtil.getAuthentication(authToken, SecurityContextHolder.getContext().getAuthentication(),
                                userDetails);
                authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(req));
                log.info("authenticated user " + email + ", setting security context");
                SecurityContextHolder.getContext().setAuthentication(authentication);
            }
        }

        chain.doFilter(req, res);
    }
} """,
    "log4j2.xml": """{% raw %}<?xml version="1.0" encoding="UTF-8"?>
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
            <PatternLayout pattern="${LOG_PATTERN_2}"/>
        </Console>{% endraw %}
        <RollingFile name="RollingFile"
                     pattern="${LOG_PATTERN}"
                     fileName="/tmp/tomcat/{{logger.name}}/logs/logger-log4j2.log"
                     filePattern="/tmp/tomcat/{{logger.name}}/logs/$${date:yyyy-MM}/logger-log4j2-%d{-dd-MMMM-yyyy}-%i.log.gz">
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
    "LoginUser.java": """package {{package}};

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class LoginUser {

    private String email;
    private String password;
} """,
    "MyErrorController.java": """package {{package}};

import org.springframework.stereotype.Controller;
import org.springframework.boot.web.servlet.error.ErrorController;
import org.springframework.web.bind.annotation.*;
import lombok.extern.slf4j.Slf4j;
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
    "pom.xml": """<?xml version="1.0" encoding="UTF-8"?>
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
    <name>{{pom.longname}}</name>
    <description>{{pom.description}}</description>
    <url>{{pom.url}}</url>
    <packaging>war</packaging>
    <properties>
        <java.version>11</java.version>
        <start-class>{{startClass}}</start-class>
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
        {%- if security %}
           <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.security</groupId>
            <artifactId>spring-security-config</artifactId>
        </dependency>
        {%- endif %}
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
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <optional>true</optional>
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
        </dependency>
        <dependency>
            <groupId>org.apache.httpcomponents</groupId>
            <artifactId>httpclient</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    <build>
        <plugins>
<!-- not really needed
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
-->
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
            <!-- Removed : take much time in starting and traces
            <plugin>
                <groupId>pl.project13.maven</groupId>
                <artifactId>git-commit-id-plugin</artifactId>
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
            </plugin> -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
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
    "README.md": """
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
 mvn clean package -Dmaven.test.skip=true
```
To run

```
mvn spring-boot:run  -Dmaven.test.skip=true
```
To Run already generated  CRUD  unt Tests

```
mvn surefire:test
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
    "Repository.java": """package {{package}};

import {{Entitypackage}};
import org.springframework.data.jpa.repository.JpaRepository;
{%- if entityName == "User"  %}
import org.springframework.data.jpa.repository.Query;
{%- endif  %}
import java.util.List;

public interface {{entityName}}Repository extends JpaRepository<{{entityName}}, String> {
{%- if entityName == "User"  %}
   @Query("select u from User u where u.email = ?1")
   User findByEmail(String email);
{%- endif  %}
	public List<{{entityName}}> findByName(String name);
} """,
    "RequestLoggingFilterConfig.java": """package {{package}};

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
    "ResourceBadParameterException.java": """package {{package}};

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
    "ResourceNotFoundException.java": """package {{package}};

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
    "RestConfig.java": """package {{package}};

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Configuration
public class RestConfig {

    @Bean
    public CorsFilter corsFilter() {
        log.info("Filtering CORS...........................................................");
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowCredentials(true);
        config.addAllowedOrigin("*");
        config.setMaxAge(Long.valueOf(3600));
        config.addAllowedHeader("*");
        config.addAllowedHeader("X-Frame-Options");
        config.addAllowedHeader("X-Requested-With");
        config.addAllowedHeader("Content-Type");
        config.addAllowedHeader("Authorization");
        config.addAllowedHeader("Origin");
        config.addAllowedHeader("Accept");
        config.addAllowedHeader("Access-Control-Request-Method");
        config.addAllowedHeader("Access-Control-Request-Headers");
        config.addAllowedMethod("OPTIONS");
        config.addAllowedMethod("GET");
        config.addAllowedMethod("POST");
        config.addAllowedMethod("PUT");
        config.addAllowedMethod("DELETE");
        source.registerCorsConfiguration("/**", config);
        return new CorsFilter(source);
    }
} """,
    "Service.java": """package {{package}};


import {{projectPackage}}.exceptions.ResourceNotFoundException;
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
    "StatusController.java": """package {{package}};

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
    	  Map<String, String> ll = new HashMap<String, String>();
			ll.put("Server status ", " Working fine !!");
        //readGitProperties(ll);
        return  ll;
    }
/* Removed because git plugin is taken too munch time on booting :
    private Map<String, String> readGitProperties(Map<String, String> ll) {
        ClassLoader classLoader = getClass().getClassLoader();
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
            // next fies are setting issue ..  not really needed !
            // ll.put("closest_tag", jsnode.textValue());
            // jsnode = node.get("git.commit.id.abbrev");
            // ll.put("short_hash", jsnode.textValue());
            // jsnode = node.get("git.commit.time");
            // ll.put("commit_time", jsnode.textValue());
        } catch (IOException e1) {
            e1.printStackTrace();
        }
        return ll;
    }*/
} """,
    "SwaggerConfiguration.java": """package {{package}};

import static springfox.documentation.builders.PathSelectors.ant;
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
          .paths(ant("{{ApiPrefix}}**"))
          .build();
    }
} """,
    "TokenProvider.java": """package {{package}};

import io.jsonwebtoken.*;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import java.io.Serializable;
import java.util.Arrays;
import java.util.Collection;
import java.util.Date;
import java.util.function.Function;
import java.util.stream.Collectors;
import static {{packageConstants}}.Constants.ACCESS_TOKEN_VALIDITY_SECONDS;
import static {{packageConstants}}.Constants.AUTHORITIES_KEY;
import static {{packageConstants}}.Constants.SIGNING_KEY;

@Component
public class TokenProvider implements Serializable {

    private static final long serialVersionUID = 8603495511390908974L;

    public String getEmailFromToken(String token) {
        return getClaimFromToken(token, Claims::getSubject);
    }

    public Date getExpirationDateFromToken(String token) {
        return getClaimFromToken(token, Claims::getExpiration);
    }

    public <T> T getClaimFromToken(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = getAllClaimsFromToken(token);
        return claimsResolver.apply(claims);
    }

    private Claims getAllClaimsFromToken(String token) {
        return Jwts.parser()
                .setSigningKey(SIGNING_KEY)
                .parseClaimsJws(token)
                .getBody();
    }

    private Boolean isTokenExpired(String token) {
        final Date expiration = getExpirationDateFromToken(token);
        return expiration.before(new Date());
    }

    public String generateToken(Authentication authentication) {
        final String authorities = authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .collect(Collectors.joining(","));
        return Jwts.builder()
                .setSubject(authentication.getName())
                .claim(AUTHORITIES_KEY, authorities)
                .signWith(SignatureAlgorithm.HS256, SIGNING_KEY)
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + ACCESS_TOKEN_VALIDITY_SECONDS * 1000))
                .compact();
    }

    public Boolean validateToken(String token, UserDetails userDetails) {
        final String email = getEmailFromToken(token);
        return (email.equals(userDetails.getUsername())
                && !isTokenExpired(token));
    }

    UsernamePasswordAuthenticationToken getAuthentication(final String token, final Authentication existingAuth, final UserDetails userDetails) {

        final JwtParser jwtParser = Jwts.parser().setSigningKey(SIGNING_KEY);

        final Jws<Claims> claimsJws = jwtParser.parseClaimsJws(token);

        final Claims claims = claimsJws.getBody();

        final Collection<? extends GrantedAuthority> authorities
                = Arrays.stream(claims.get(AUTHORITIES_KEY).toString().split(","))
                        .map(SimpleGrantedAuthority::new)
                        .collect(Collectors.toList());

        return new UsernamePasswordAuthenticationToken(userDetails, "", authorities);
    }

} """,
    "User.java": """package {{package}} ;

import javax.persistence.*;
import javax.validation.constraints.*;
import lombok.*;
import java.time.Instant;
import lombok.extern.slf4j.Slf4j;
import io.swagger.annotations.ApiModelProperty;
import io.swagger.annotations.ApiModel;
import org.hibernate.annotations.GenericGenerator;
import {{configConstants}}.Constants;
import com.fasterxml.jackson.annotation.JsonIgnore;

/**
 * User definition Class
 */
@ApiModel(description = "User definition Class")
@Slf4j
@Getter
@Setter
@AllArgsConstructor
@ToString
@Entity
public class User extends BaseEntity {

    @Id
    @GeneratedValue(generator = "system-uuid", strategy = GenerationType.IDENTITY)
    @GenericGenerator(name = "system-uuid", strategy = "uuid2")
    @ApiModelProperty(hidden = true)
    protected String Id;

{%- for field in entity.fields | sort(attribute='name') %}
{%- if field.name|upper not in ['LOGIN','PASSWORD','FIRSTNAME','LASTNAME','EMAIL','ACTIVATED','LANGKEY','IMAGEURL','ACTIVATIONKEY','RESETKEY','RESETDATE','MAINROLE'] %}
    /** {{field.comment}} */
    @ApiModelProperty(value = " {{field.comment}} ")
{%- for annot in field.annotations  %}
    {{annot}}
{%- endfor %}
    private {{field.type}} {{field.name}};
{% endif %}
{% endfor %}

{%- if security %}
    @NotNull
    @Size(min = 7, max = 128)
    @Column(name = "password_hash", length = 60, nullable = false)
    private String password;
{%- endif %}
    @Size(max = 50)
    @Column(name = "first_name", length = 50)
    private String firstName;

    @Size(max = 50)
    @Column(name = "last_name", length = 50)
    private String lastName;

    @Email
    @Size(min = 5, max = 254)
    @Column(length = 254, unique = true)
    private String email;

    @NotNull
    @Column(nullable = false)
    private boolean activated = false;

    @Size(min = 2, max = 10)
    @Column(name = "lang_key", length = 10)
    private String langKey;

    @Size(max = 256)
    @Column(name = "image_url", length = 256)
    private String imageUrl;

    @Size(max = 20)
    @Column(name = "activation_key", length = 20)
    @JsonIgnore
    private String activationKey;

    @Size(max = 20)
    @Column(name = "reset_key", length = 20)
    @JsonIgnore
    private String resetKey;

    @Column(name = "reset_date")
    private Instant resetDate = null;
    {%- if security %}
    @NotNull
    {%- else %}
    @JsonIgnore
    {%- endif %}
    private String mainRole;

    /**
    * default constructor
    */
    public User() {
        super();
    }
} """,
    "UserService.java": """package {{package}};

import {{projectPackage}}.exceptions.ResourceNotFoundException;

import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import javax.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import {{packageConstants}}.Constants;
import org.springframework.security.crypto.bcrypt.BCrypt;

import {{Entitypackage}};
import {{Repositorypackage}};

import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service(value = "userService")
public class UserService  implements  UserDetailsService, IService<User> {

    @Autowired
    private UserRepository erepo;

     public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
     log.debug(" >>>>>>>>>>>>>> looking for user with email  " + email);
     User user = erepo.findByEmail(email);

     if (user == null) {
         log.error(" UsernameNotFoundException : user not found with email " + email);
         throw new UsernameNotFoundException("Invalid email or password.");
     }
     log.info(" >>>>>>>>>>>>>> Found user is   " + getAuthority(user));
     UserDetails urd = new org.springframework.security.core.userdetails.User(user.getEmail(), user.getPassword(), getAuthority(user));
     return urd;
 }

 public User GetUserByUsername(String email) throws UsernameNotFoundException {
     log.debug(" >>>>>>>>>>>>>> looking for user with email  " + email);
     User user = erepo.findByEmail(email);

     if (user == null) {
         log.error(" UsernameNotFoundException : user not found with email " + email);
         throw new UsernameNotFoundException("Invalid email or password.");
     }

     return user;
 }

 @Transactional
 protected Set<SimpleGrantedAuthority> getAuthority(User user) {
     Set<SimpleGrantedAuthority> authorities = new HashSet<>();
     authorities.add(new SimpleGrantedAuthority(user.getMainRole()));
     return authorities;
 }


    @Override
    public User create(User n) {
        log.info("Saving new  User .. " + n.toString());
        //Encrypt password , since first time it must bne clear, to be encrypted in DB then.
        n.setPassword(BCrypt.hashpw(n.getPassword(), Constants.SIGNING_KEY));
        return erepo.save(n);
    }

    @Override
    public List<User> getAll() {
        log.info("Getting All  .. ");
            return erepo.findAll();
    }

    @Override
    public List<User> getAllBySomeId(String id) {
        log.info("Getting All by some id  ..  " + id);
        // Todo correctly
        return erepo.findAll();
    }

    @Override
    public User getOne(String id) {
        log.info("Getting one with id   .. " + id);
        User cm = erepo.findById(id).orElseThrow(() -> new ResourceNotFoundException("User", "id", id));
        return cm;
    }

    @Override
    public void deleteone(String id) {
        log.info("Deleting one with id   .. " + id);
        if (id == null) {
            throw new ResourceNotFoundException("User", "id", id);
        }
        if (this.erepo.existsById(id)) {
            User cm = erepo.findById(id).orElseThrow(() -> new ResourceNotFoundException("User", "id", id));

            erepo.deleteById(id);
        } else {
            throw new ResourceNotFoundException("User", "id", id);
        }
    }

    @Override
    public User update(User n) {
        if (n == null) {
            throw new ResourceNotFoundException("User", "id", n);
        }
        log.info("Updating one  User   .. " + n.toString());
        return erepo.findById(n.getId()).map(found -> {
            {% for field in entity.fields | sort(attribute='name') %}found.set{{field.name[0]|upper}}{{field.name[1:] }}(n.get{{field.name[0]|upper}}{{field.name[1:]}}());
            {% endfor %}
            return erepo.save(found);
        }).orElseThrow(() -> {
            throw new ResourceNotFoundException("User", "id", n.getId());
        });
    }
} """,
    "WebInitializer.java": """package {{package}};

import {{Apppackage}};
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
} """,
    "WebSecurityConfig.java": """package {{package}};

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import javax.annotation.Resource;

@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Resource(name = "userService")
    private UserDetailsService userDetailsService;

    @Autowired
    private JwtAuthenticationEntryPoint unauthorizedHandler;

    @Override
    @Bean
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }

    @Autowired
    public void globalUserDetails(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(userDetailsService).passwordEncoder(encoder());
    }

    @Bean
    public JwtAuthenticationFilter authenticationTokenFilterBean() throws Exception {
        return new JwtAuthenticationFilter();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.cors()
            .and()
        	.headers().frameOptions().sameOrigin()
            .and()
            .csrf().disable()
            .authorizeRequests().antMatchers(   "/swagger-ui.html*",
                                                "/webjars/springfox-swagger-ui/**",
                                                "/v2/api-docs*",
                                                "/status/*",
                                                "/api/auth/*",
                                                "/h2-console/**",
                                                "/api/user/new").permitAll()
            .anyRequest().authenticated()
            .and().exceptionHandling().authenticationEntryPoint(unauthorizedHandler)
            .and().sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS);

        http.addFilterBefore(authenticationTokenFilterBean(), UsernamePasswordAuthenticationFilter.class);
    }

    @Bean
    public BCryptPasswordEncoder encoder() {
        return new BCryptPasswordEncoder();
    }

} """,
}
