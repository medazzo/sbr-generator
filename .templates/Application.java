package {{package}};

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
{%- if security  %}
import org.springframework.context.annotation.Bean;
import {{EntitypackageUser}};
import {{ServicepackageUser}};
import {{RepositorypackageUser}};
import org.springframework.beans.factory.annotation.Autowired;
import {{SecurityPackage}}.AuthoritiesConstants;
{%- endif  %}
import lombok.extern.slf4j.Slf4j;

@Slf4j
@SpringBootApplication
public class Application {

    public static final String EMAIL_TEMPLATE_ENCODING = "UTF-8";

    public static void main(final String[] args) {
        SpringApplication.run(Application.class, args);
    }

{%- if security  %}
    @Autowired
    UserRepository repo;

    @Bean
    public CommandLineRunner demoData() {
        return args -> {
            User u = new User();
            u.setEmail("admin@admin.com");
            u.setLogin("admin");
            u.setPassword("admin");
            u.setFirstName("Mr admin");
            u.setLastName("admin com");
            u.setActivated(true);
            u.setLangKey("EN");
            u.setMainRole(AuthoritiesConstants.ADMIN);
            try {
                repo.save(u);
            } catch (Exception e) {
                log.warn("Admin user seems to be already created   .. "
                        + e.getMessage());
            }
        };
    }
{%- endif  %}

}
