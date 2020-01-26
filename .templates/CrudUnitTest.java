package {{package}};

import {{Entitypackage}};
import {{Servicepackage}};

import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.extern.slf4j.Slf4j;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
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

    @Test
    public void {{entityName}}CreateTest() throws Exception {
        // Create Test {{entityName}} Object
        {{entityName}} created = CreateAndSave();
        // Remove the Created {{entityName}}
        RemoveOne(created.getId());
    }

    @Test
    public void {{entityName}}ReadTest() throws Exception {
        // Create Test {{entityName}} Object
        {{entityName}} saved = CreateAndSave();
        // Get {{entityName}} using API and verify returned One
        MvcResult mvcgResult = mockMvc.perform(
                get("{{mapping}}/{id}", saved.getId())
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                {% for field in entity.fields | sort(attribute='name') %} .andExpect(MockMvcResultMatchers.jsonPath("{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {% endfor %}
                .andReturn();
        // Verify Getted {{entityName}} using Service
        ObjectMapper mapper = new ObjectMapper();
        {{entityName}} getted = mapper.readValue(mvcgResult.getResponse().getContentAsByteArray(), {{entityName}}.class);
        {{entityName}} found = service.getOne(getted.getId());
        assertEquals(found.getId(), getted.getId());

        {% for field in entity.fields | sort(attribute='name') %}  assertEquals(found.get{{field.name[0]|upper}}{{field.name[1:]}}(), getted.get{{field.name[0]|upper}}{{field.name[1:]}}());        
        {% endfor %}

        // Remove the Created {{entityName}}
        RemoveOne(found.getId());
    }

    @Test
    public void {{entityName}}ReadAllTest() throws Exception {
        // Get all          
        mockMvc.perform(
                get("{{mapping}}/all")
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(0)));
        // Create Test {{entityName}} Object
        {{entityName}} saved = CreateAndSave();
        // Get All
        mockMvc.perform(
                get("{{mapping}}/all")
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(1)))
                {% for field in entity.fields | sort(attribute='name') %} .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {% endfor %}                
                .andReturn();
        // Create Another Test {{entityName}} Object
        {{entityName}} saved2 = CreateAndSave();
        // Get all 
        mockMvc.perform(
                get("{{mapping}}/all")
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(2)))
                {% for field in entity.fields | sort(attribute='name') %} .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {% endfor %}
                {% for field in entity.fields | sort(attribute='name') %} .andExpect(MockMvcResultMatchers.jsonPath("$[1].{{field.name}}").value(saved2.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {% endfor %}
                .andReturn();
        // Remove the Created {{entityName}}
        RemoveOne(saved.getId());
        // Remove the Created {{entityName}}
        RemoveOne(saved2.getId());
    }

    @Test
    public void {{entityName}}UpdateTest() throws Exception {
        // Get all          
        mockMvc.perform(
                get("{{mapping}}/all")
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(0)));
        // Create Test {{entityName}} Object
        {{entityName}} saved = CreateAndSave();
        // Get All
        mockMvc.perform(
                get("{{mapping}}/all")
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(1)))
                {% for field in entity.fields | sort(attribute='name') %} .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {% endfor %}
                .andReturn();
        // Update 
        {{entityName}} updt = Update(saved);
        // Get Update on Server          
        MvcResult mvcResult = mockMvc.perform(
                put("{{mapping}}/{id}", saved.getId())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(asJsonString(updt))
        )
                .andExpect(status().isOk())
                .andDo(print())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                {% for field in entity.fields | sort(attribute='name') %} .andExpect(MockMvcResultMatchers.jsonPath("{{field.name}}").value(updt.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {% endfor %}
                .andReturn();
        // Verify Getted {{entityName}}using Service
        ObjectMapper mapper = new ObjectMapper();
        {{entityName}} getted = mapper.readValue(mvcResult.getResponse().getContentAsByteArray(), {{entityName}}.class);
        {{entityName}} found = service.getOne(getted.getId());
        assertEquals(found.getId(), getted.getId());
        {% for field in entity.fields | sort(attribute='name') %}  assertEquals(found.get{{field.name[0]|upper}}{{field.name[1:]}}(), getted.get{{field.name[0]|upper}}{{field.name[1:]}}());        
        {% endfor %}
    }

    @Test
    public void {{entityName}}DeleteTest() throws Exception {
        // Get all          
        mockMvc.perform(
                get("{{mapping}}/all")
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(0)));
        // Create Test {{entityName}} Object
        {{entityName}} saved = CreateAndSave();
        // Get All
        mockMvc.perform(
                get("{{mapping}}/all")
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(1)))
                {% for field in entity.fields | sort(attribute='name') %} .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {% endfor %}
                .andReturn();
        // Create Another Test {{entityName}} Object
        {{entityName}} saved2 = CreateAndSave();
        // Get all          
        mockMvc.perform(
                get("{{mapping}}/all")
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(2)))
                {% for field in entity.fields | sort(attribute='name') %} .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {% endfor %}
                {% for field in entity.fields | sort(attribute='name') %} .andExpect(MockMvcResultMatchers.jsonPath("$[1].{{field.name}}").value(saved2.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {% endfor %}
                .andReturn();
        // Remove  first one 
        RemoveOne(saved.getId());
        // Get all          
        mockMvc.perform(
                get("{{mapping}}/all")
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(1)))
                {% for field in entity.fields | sort(attribute='name') %} .andExpect(MockMvcResultMatchers.jsonPath("$[0].{{field.name}}").value(saved2.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                {% endfor %}
                .andReturn();
        // Remove  last one 
        RemoveOne(saved2.getId());        
        // Get all          
        mockMvc.perform(
                get("{{mapping}}/all")
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.jsonPath("$", hasSize(0)));
    }

    public {{entityName}} CreateAndSave() throws IOException, Exception {
        // Create  {{entityName}}       
        {{entityName}} ent = Create();
        // Create {{entityName}} using API and verify returned One
        MvcResult mvcResult = mockMvc.perform(
                post("{{mapping}}/new")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(asJsonString(ent))
        )
                .andExpect(status().isCreated())
                .andDo(print())
                .andExpect(MockMvcResultMatchers.content().contentType(MediaType.APPLICATION_JSON))Adde
                .andExpect(MockMvcResultMatchers.jsonPath("id").isNotEmpty())
                {% for field in entity.fields | sort(attribute='name') %} .andExpect(MockMvcResultMatchers.jsonPath("{{field.name}}").value(ent.get{{field.name[0]|upper}}{{field.name[1:]}}()))
                .andReturn();
        // Verify Created {{entityName}} using Service
        ObjectMapper mapper = new ObjectMapper();
        {{entityName}} saved = mapper.readValue(mvcResult.getResponse().getContentAsByteArray(), {{entityName}}.class);
        {{entityName}} found = service.getOne(saved.getId());
        assertEquals(found.getId(), saved.getId());
        {% for field in entity.fields | sort(attribute='name') %}  assertEquals(found.get{{field.name[0]|upper}}{{field.name[1:]}}(), getted.get{{field.name[0]|upper}}{{field.name[1:]}}());        
        {% endfor %}
        // return 
        return saved;
    }

    private void RemoveOne(String id) throws Exception{
        mockMvc.perform(
                delete("{{mapping}}/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .accept(MediaType.APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andReturn();        
    }
    private {{entityName}} Create() {
        {{entityName}} ent = new {{entityName}}();
        return Update(ent);
    }

    private {{entityName}} Update({{entityName}} old) {        
        {% for field in entity.fields | sort(attribute='name') %}{% if 'int' == field.type %}
                old.set{{field.name[0]|upper}}{{field.name[1:] }}(HelperTests.randomInteger());        
                {% elif 'String' == field.type %}
                old.set{{field.name[0]|upper}}{{field.name[1:] }}(HelperTests.randomString(30));        
                {% elif 'double' == field.type %}
                old.set{{field.name[0]|upper}}{{field.name[1:] }}(HelperTests.randomdouble());        
                {% else %}                        
                old.set{{field.name[0]|upper}}{{field.name[1:] }}(HelperTests.randomString(30));        // TODO Field field.name is not updated !!                 
        {% endif %}{% endfor %}          
        return old;
    }

    private String asJsonString(final Object obj) {
        try {
            return new ObjectMapper().writeValueAsString(obj);
        } catch (JsonProcessingException e) {
            log.error(e.getMessage() + "Error to map object ");
            throw new RuntimeException(e);
        }
    }
}
