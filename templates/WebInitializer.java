/*   Copyright (C) 2019 EASYSOFT-IN                                 */
/*   All rights exclusively reserved for EASYSOFT-IN,               */
/*   unless otherwise expressly agreed.                             */
/*                                                                  */
/*   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *    */
/*   This is a Generated source code file                           */
/*   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *    */
package {{package}};

import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class WebInitializer extends SpringBootServletInitializer {

    @Override
    protected final  SpringApplicationBuilder configure
        (final SpringApplicationBuilder application) {
        log.warn(" .. .. .. .. .Initilizing App  .. .. ... .. .. ");
        return application.sources(Application.class);
    }
}
