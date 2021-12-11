package {{package}} ;

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
}
