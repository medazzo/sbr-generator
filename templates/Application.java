/*   Copyright (C) 2019 EASYSOFT-IN                                 */
/*   All rights exclusively reserved for EASYSOFT-IN,               */
/*   unless otherwise expressly agreed.                             */
/*                                                                  */
/*   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *    */
/*   This is a Generated source code file                           */
/*   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *    */
package {{package}};

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@SpringBootApplication
public class Application {

    public static final String EMAIL_TEMPLATE_ENCODING = "UTF-8";

    public static void main(final String[] args) {
        SpringApplication.run(Application.class, args);
    }


}
