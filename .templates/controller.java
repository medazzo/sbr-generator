package {{package}};

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
    @ApiOperation(value = "Create a new  {{entityName}} ", nickname = "CreateNew{{entityName}}" ,
 tags = { "{{entityName}}" })
 {%- if security  %}
    @PreAuthorize("hasAnyRole('ADMIN', 'USER'{%- for role in roles  %}, '{{role}}'{%- endfor %})")
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
    @ApiOperation(value = "Get all stored {{entityName}} using some extra ID( user/group ID or some other ID)",
        nickname = "GetAll{{entityName}}BySomeID" , tags = { "{{entityName}}" })
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
    @ApiOperation(value = "Get stored {{entityName}} using his unique ID", nickname = "GetOne{{entityName}}ById" ,
 tags = { "{{entityName}}" })
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
    @ApiOperation(value = "Update the stored {{entityName}} using his unique ID",
         nickname = "UpdateOne{{entityName}}ById" , tags = { "{{entityName}}" })
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
    @ApiOperation(value = "Removing the stored {{entityName}} using his unique ID",
        nickname = "RemoveOne{{entityName}}ById" , tags = { "{{entityName}}" })
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
}
