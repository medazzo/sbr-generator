package {{package}}y;

/**
 * Constants for Spring Security authorities.
 */
public final class AuthoritiesConstants {

    public static final String ADMIN = "ROLE_ADMIN";

    public static final String USER = "ROLE_USER";
{% for role in roles  %}
    public static final String {{role}} = "ROLE_{{role}}";
{% endfor %}
    private AuthoritiesConstants() {
    }
}
