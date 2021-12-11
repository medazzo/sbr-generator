package {{package}};


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
}
