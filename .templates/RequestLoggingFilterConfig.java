package {{package}};

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.filter.CommonsRequestLoggingFilter;

@Configuration
public class RequestLoggingFilterConfig {

    private final int MAX_PAYLOAD_LOG_BUFFER_LENGTH = 10000;

    @Bean
    public CommonsRequestLoggingFilter logFilter() {

        CommonsRequestLoggingFilter filter = new CommonsRequestLoggingFilter();
        filter.setIncludeQueryString(true);
        filter.setIncludePayload(true);
        filter.setMaxPayloadLength(MAX_PAYLOAD_LOG_BUFFER_LENGTH);
        filter.setIncludeHeaders(false);
        filter.setAfterMessageSuffix(" ============== DONE =============== ");
        filter.setBeforeMessagePrefix(" =========== STARTING  =========== ");
        return filter;
    }
}
