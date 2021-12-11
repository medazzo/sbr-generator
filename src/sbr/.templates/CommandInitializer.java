package {{package}};

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Component
class CommandInitializer implements CommandLineRunner {

    @Override
    public void run(String... args) throws Exception {
        log.warn("Preparing some stuff to do before run applications .. ");
    }
}
