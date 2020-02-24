package {{package}};

import org.springframework.boot.CommandLineRunner;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
{%- if security  %}
import org.springframework.context.annotation.Bean;
import {{EntitypackageUser}};
import {{ServicepackageUser}};
import org.springframework.beans.factory.annotation.Autowired;
import {{SecurityPackage}}.AuthoritiesConstants;
{%- endif  %}
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Component
class CommandInitializer implements CommandLineRunner {

{%- if security  %}
    @Autowired
    private UserService service;
{%- endif  %}

    @Override
    public void run(String... args) throws Exception {
        log.warn("Preparing some stuff to do before run applications .. ");
{%- if security  %}
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
            service.create(u);
            // check it ?
            service.getAll().forEach((us) -> {
                    log.info("{}", us);
                });
        } catch (Exception e) {
            log.warn("Admin user seems to be already created   .. "
                    + e.getMessage());
        }
    }
{%- endif  %}

}
