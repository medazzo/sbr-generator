package {{package}} ;

import javax.persistence.*;
import javax.validation.constraints.*;
import lombok.*;
import lombok.extern.slf4j.Slf4j;
import io.swagger.annotations.ApiModelProperty;
import io.swagger.annotations.ApiModel;
import org.hibernate.annotations.GenericGenerator;

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
}

