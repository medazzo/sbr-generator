package {{package}};

import {{Entitypackage}};
import {{Servicepackage}};
{%- if security %}
import {{packageAuth}}.AuthToken ;
{%-endif %}
{%- for field in entity.fields %}{%- if field.foreignKey  %}
import {{EntityBasepackage}}.{{field.foreignEntity}};              
{%-endif %} {% endfor %}     
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
    private AuthToken auth ;
    Map<String, Object> hm = new HashMap<>();
    @Autowired
    private ObjectMapper mapper;

    {% if security  %}
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
        String body = "{\\\"username\\\":\\\"nonexistentuser\\\", \\\"password\\\":\\\password \\\"}";
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

    @Test
    public void {{entityName}}CreateTest() throws Exception {
        log.debug(" in {{entityName}}  CreateTest !.");
        {%- if security  %}                 
        auth = DoAdminAuthentication() ;
        {%- endif  %} 
        // check Get all is empty     
        CheckAllEmpty();
        // Create Test {{entityName}} Object
        {{entityName}} created = CreateAndSave(hm);
        // Remove the Created {{entityName}}
        RemoveOne( created.getId());
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
        {{entityName}} saved = CreateAndSave( hm);
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
        RemoveOne( found.getId());
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
        {{entityName}} saved = CreateAndSave(hm);
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
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(1)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %}
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}                
                .andReturn();
        // Create Another Test {{entityName}} Object
        {{entityName}} saved2 = CreateAndSave(  hm);
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
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(2)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %} 
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                {%- for field in entity.fields %} {% if not field.foreignKey  %} 
                .andExpect(MockMvcResultMatchers.jsonPath("$[1].{{field.name}}").value(saved2.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                .andReturn();
        // Remove the Created {{entityName}}
        RemoveOne( saved.getId());
        // Remove the Created {{entityName}}
        RemoveOne( saved2.getId());
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
        {{entityName}} saved = CreateAndSave( hm);
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
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(1)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %} 
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                .andReturn();
        // Update 
        {{entityName}} updt = Update(saved, hm);
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
         RemoveOne( getted.getId());
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
        {{entityName}} saved = CreateAndSave( hm);
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
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(1)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %} 
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                .andReturn();
        // Create Another Test {{entityName}} Object
        {{entityName}} saved2 = CreateAndSave( hm);
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
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(2)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %} 
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                {%- for field in entity.fields %} {% if not field.foreignKey  %} 
                .andExpect(MockMvcResultMatchers.jsonPath("$[1].{{field.name}}").value(saved2.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                .andReturn();
        // Remove  first one 
        RemoveOne( saved.getId());
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
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(1)))
                {%- for field in entity.fields %} {% if not field.foreignKey  %} 
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved2.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {%-endif %} {% endfor %}
                .andReturn();
        // Remove  last one 
        RemoveOne(saved2.getId());        
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
{%- if 'User' == entity.name %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(2)));
{%- else %}
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(0)));
{%- endif %}                

    }
    /**
    * 
    */
    public {{entityName}} CreateAndSave(Map<String, Object> hm) throws IOException, Exception {
        log.debug(" Will CreateAndSave {{entityName}}  !.");
        // Create  {{entityName}}       
        {{entityName}} ent = Create(hm);
        // Create {{entityName}} using API and verify returned One
        MvcResult mvcResult = mockMvc.perform(
                post("{{mapping}}/new")
                {%- if security  %}                 
                .header("Authorization", "Bearer "+auth.getToken())
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
        {{entityName}} saved = mapper.readValue(mvcResult.getResponse().getContentAsByteArray(), {{entityName}}.class);
        {{entityName}} found = service.getOne(saved.getId());
        assertEquals(found.getId(), saved.getId());
        {%- for field in entity.fields %} {% if not field.foreignKey  %} 
        assertEquals(found.get{{field.name[0]|upper}}{{field.name[1:]}}(), saved.get{{field.name[0]|upper}}{{field.name[1:]}}());        
        {%-endif %} {% endfor %}// return         
        return found;
    }
    /**
     * 
     */
    public  void RemoveOne(String id) throws Exception{  
        log.debug(" Will RemoveOne {{entityName}}  !.");
        mockMvc.perform(
                delete("{{mapping}}/{id}", id)
                {%- if security  %}                 
                .header("Authorization", "Bearer "+auth.getToken())
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
    private {{entityName}} Create(Map<String, Object> hm) throws  Exception{
        {{entityName}} ent = new {{entityName}}();
        return Update(ent,hm);
    }
    /**
     * 
     */
    private {{entityName}} Update({{entityName}} old, Map<String, Object> hm) throws Exception  {        
        {%- if 'User' == entity.name %}
        // Add extra for User        
        old.setLogin(HelperTests.randomString(10));  
        old.setPassword(HelperTests.randomString(10)); 
        old.setFirstName(HelperTests.randomString(10));
        old.setLastName(HelperTests.randomString(10));
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
        old.set{{field.name[0]|upper}}{{field.name[1:]}}(HelperTests.randomString(100));                        
                        {%- endif %} 
                {%- else %}          
                        {%- if field.foreignKey  %}
        //String Field referring foreignKey of type  {{field.foreignEntity}} , so let's create one !        
        old.set{{field.name[0]|upper}}{{field.name[1:]}}(({{field.foreignEntity}})hm.get("{{field.foreignEntity}}"));
                        {%- else %}
        old.set{{field.name[0]|upper}}{{field.name[1:]}}(new {{field.type}}());  //TODO {{field.type }} Not supported type yet : easy to do!                
                        {%- endif %}                 
                {%- endif %}
        {%- endfor %}          
        return old;
    }
    
    @PostConstruct
    @Before
    public void setUp() throws Exception {
        mapper.registerModule(new JavaTimeModule());
        log.debug(" in  setUp Test {{entityName}}  !.");
        {%- for field in entity.fields %}{% if field.foreignKey  %}
        //String Field referring foreignKey of type  {{field.foreignEntity}} , so let's create one !
        {{field.foreignEntity}}CrudUnitTest {{field.foreignEntity}}tst = new {{field.foreignEntity}}CrudUnitTest();
        {{field.foreignEntity}} fk{{field.foreignEntity}} = {{field.foreignEntity}}tst.CreateAndSave(hm);      
        hm.put("{{field.foreignEntity}}",fk{{field.foreignEntity}});        
        {%-endif %} {% endfor %}          
    }

    @After
    public void tearDown() throws Exception {
        log.debug(" in  tearDown Test {{entityName}}  !.");
        {%- for field in entity.fields %}{%- if field.foreignKey  %}
        //String Field referring foreignKey of type  {{field.foreignEntity}} , so let's remove it once done wuth test !        
        {{field.foreignEntity}} dep{{field.foreignEntity}} = ({{field.foreignEntity}}) hm.get("{{field.foreignEntity}}");
        {{field.foreignEntity}}CrudUnitTest  {{field.foreignEntity}}tst = new {{field.foreignEntity}}CrudUnitTest();
        {{field.foreignEntity}}tst.RemoveOne(dep{{field.foreignEntity}}.getId());        
        hm.remove("{{field.foreignEntity}}");        
        {%-endif %} {% endfor %}                  
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
}
