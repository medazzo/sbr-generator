package {{package}};

public class Constants {

    public static final long ACCESS_TOKEN_VALIDITY_SECONDS = 2 * 60 * 60;
    public static final String SIGNING_KEY = "{{key}}";
    public static final String TOKEN_PREFIX = "Bearer ";
    public static final String HEADER_STRING = "Authorization";
    public static final String AUTHORITIES_KEY = "scopes";
    public static final int QUOTATIONS_COUNT_EXPIRES_DAY = 60;
    public static final String LOGIN_REGEX = "^[_.@A-Za-z0-9-]*$";
    public static final String SYSTEM_ACCOUNT = "system";
    public static final String DEFAULT_LANGUAGE = "en";
    public static final String ANONYMOUS_USER = "anonymoususer";

    private Constants() {
    }

}
