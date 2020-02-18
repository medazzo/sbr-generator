package {{package}};

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@SpringBootApplication(exclude = { SecurityAutoConfiguration.class })
public class Application {

    public static final String EMAIL_TEMPLATE_ENCODING = "UTF-8";

    public static void main(final String[] args) {
        SpringApplication.run(Application.class, args);
    }


}
