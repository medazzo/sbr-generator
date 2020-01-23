package {{package}} ;

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
}

