package {{package}};

import {{Entitypackage}};
import {{Servicepackage}};
import {{ServiceBasepackage}}.IService;

{%- for field in entity.fields %}{%- if field.foreignKey  %}
import {{EntityBasepackage}}.{{field.foreignEntity}};        
import {{ServiceBasepackage}}.{{field.foreignEntity}}Service;        
{%-endif %} {% endfor %}     
import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.extern.slf4j.Slf4j;
import com.fasterxml.jackson.databind.ObjectMapper;
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

@RunWith(SpringRunner.class)
@ExtendWith(SpringExtension.class)
@SpringBootTest()
@AutoConfigureMockMvc
@ActiveProfiles("test")
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
    Map<String, Object> hm = new HashMap<>();

    @Test
    public void {{entityName}}CreateTest() throws Exception {
        // check Get all is empty     
        CheckAllEmpty(mockMvc);
        // Create Test {{entityName}} Object
        {{entityName}} created = CreateAndSave(mockMvc, service, hm);
        // Remove the Created {{entityName}}
        RemoveOne(mockMvc, created.getId());
        // check Get all is empty     
        CheckAllEmpty(mockMvc);
    }

    @Test
    public void {{entityName}}ReadTest() throws Exception {
        // check Get all is 0
        CheckAllEmpty(mockMvc);
        // Create Test {{entityName}} Object
        {{entityName}} saved = CreateAndSave(mockMvc, service, hm);
        // Get {{entityName}} using API and verify returned One
        MvcResult mvcgResult = mockMvc.perform(
                get("{{mapping}}/{id}", saved.getId())
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
        ObjectMapper mapper = new ObjectMapper();
        {{entityName}} getted = mapper.readValue(mvcgResult.getResponse().getContentAsByteArray(), {{entityName}}.class);
        {{entityName}} found = service.getOne(getted.getId());
        assertEquals(found.getId(), getted.getId());
        {%- for field in entity.fields %} {% if not field.foreignKey  %}
        assertEquals(found.get{{field.name[0]|upper}}{{field.name[1:]}}(), getted.get{{field.name[0]|upper}}{{field.name[1:]}}());        
        {%-endif %} {% endfor %}
        // Remove the Created {{entityName}}
        RemoveOne(mockMvc, found.getId());
        // check Get all is 0
        CheckAllEmpty(mockMvc);
    }

    @Test
    public void {{entityName}}ReadAllTest() throws Exception {
        // Get all          
        CheckAllEmpty(mockMvc);
        // Create Test {{entityName}} Object
        {{entityName}} saved = CreateAndSave(mockMvc, service, hm);
        // Get All
        mockMvc.perform(
                get("{{mapping}}/all")
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
        {{entityName}} saved2 = CreateAndSave(mockMvc, service, hm);
        // Get all 
        mockMvc.perform(
                get("{{mapping}}/all")
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
        RemoveOne(mockMvc, saved.getId());
        // Remove the Created {{entityName}}
        RemoveOne(mockMvc, saved2.getId());
        // check Get all is empty     
        CheckAllEmpty(mockMvc);
    }

    @Test
    public void {{entityName}}UpdateTest() throws Exception {
        // Get all          
        CheckAllEmpty(mockMvc);
        // Create Test {{entityName}} Object
        {{entityName}} saved = CreateAndSave(mockMvc, service, hm);
        // Get All
        mockMvc.perform(
                get("{{mapping}}/all")
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
        ObjectMapper mapper = new ObjectMapper();
        {{entityName}} getted = mapper.readValue(mvcResult.getResponse().getContentAsByteArray(), {{entityName}}.class);
        {{entityName}} found = service.getOne(getted.getId());
        assertEquals(found.getId(), getted.getId());
        {%- for field in entity.fields %} {% if not field.foreignKey  %} 
        assertEquals(found.get{{field.name[0]|upper}}{{field.name[1:]}}(), getted.get{{field.name[0]|upper}}{{field.name[1:]}}());        
        {%-endif %} {% endfor %}
         // Remove the Created {{entityName}}
         RemoveOne(mockMvc, getted.getId());
        // check Get all is empty     
        CheckAllEmpty(mockMvc);
    }

    @Test
    public void {{entityName}}DeleteTest() throws Exception {
        // check Get all is 0
        CheckAllEmpty(mockMvc);
        // Create Test {{entityName}} Object
        {{entityName}} saved = CreateAndSave(mockMvc, service, hm);
        // Get All
        mockMvc.perform(
                get("{{mapping}}/all")
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
        {{entityName}} saved2 = CreateAndSave(mockMvc, service, hm);
        // Get all          
        mockMvc.perform(
                get("{{mapping}}/all")
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
        RemoveOne(mockMvc, saved.getId());
        // Get all          
        mockMvc.perform(
                get("{{mapping}}/all")
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
        RemoveOne(mockMvc, saved2.getId());        
        // check Get all is empty     
        CheckAllEmpty(mockMvc);
    }
    /**
     * 
     */
    public static void CheckAllEmpty(MockMvc mock)  throws  Exception{
        // check Get all is 0
        mock.perform(
                get("{{mapping}}/all")
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(0)));
    }
    /**
    * 
    */
    public static {{entityName}} CreateAndSave(MockMvc mock, IService<{{entityName}}> serv,Map<String, Object> hm) throws IOException, Exception {
        // Create  {{entityName}}       
        {{entityName}} ent = Create(hm);
        // Create {{entityName}} using API and verify returned One
        MvcResult mvcResult = mock.perform(
                post("{{mapping}}/new")
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
        ObjectMapper mapper = new ObjectMapper();
        {{entityName}} saved = mapper.readValue(mvcResult.getResponse().getContentAsByteArray(), {{entityName}}.class);
        {{entityName}} found = serv.getOne(saved.getId());
        assertEquals(found.getId(), saved.getId());
        {%- for field in entity.fields %} {% if not field.foreignKey  %} 
        assertEquals(found.get{{field.name[0]|upper}}{{field.name[1:]}}(), saved.get{{field.name[0]|upper}}{{field.name[1:]}}());        
        {%-endif %} {% endfor %}// return         
        return found;
    }
    /**
     * 
     */
    public  static void RemoveOne(MockMvc mock,String id) throws Exception{
        mock.perform(
                delete("{{mapping}}/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andReturn();        
    }
    /**
     * 
     */
    private static {{entityName}} Create(Map<String, Object> hm) throws  Exception{
        {{entityName}} ent = new {{entityName}}();
        return Update(ent,hm);
    }
    /**
     * 
     */
    private static {{entityName}} Update({{entityName}} old, Map<String, Object> hm) throws Exception  {        
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
    
    @Before
    public void setUp() throws Exception {
        {%- for field in entity.fields %}{% if field.foreignKey  %}
        //String Field referring foreignKey of type  {{field.foreignEntity}} , so let's create one !
        {{field.foreignEntity}} fk{{field.foreignEntity}} = {{field.foreignEntity}}CrudUnitTest.CreateAndSave(mockMvc, fk{{field.foreignEntity}}service, hm);      
        hm.put("{{field.foreignEntity}}",fk{{field.foreignEntity}});        
        {%-endif %} {% endfor %}          
    }

    @After
    public void tearDown() throws Exception {
        {%- for field in entity.fields %}{%- if field.foreignKey  %}
        //String Field referring foreignKey of type  {{field.foreignEntity}} , so let's remove it once done wuth test !        
        {{field.foreignEntity}} dep{{field.foreignEntity}} = ({{field.foreignEntity}}) hm.get("{{field.foreignEntity}}");
        {{field.foreignEntity}}CrudUnitTest.RemoveOne(mockMvc, dep{{field.foreignEntity}}.getId());        
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
