package {{package}};

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

@Controller
@RequestMapping(path = "/api/status")
public class StatusController {

    @RequestMapping(value = "/version", method = RequestMethod.GET, produces = "application/json")
    @ResponseBody
    public Map<String, String> versionInformation() throws IOException {
        return readGitProperties();
    }

    private Map<String, String> readGitProperties() {
        ClassLoader classLoader = getClass().getClassLoader();
        Map<String, String> ll = new HashMap<String, String>();
        try {
            InputStream inputStream = classLoader.getResourceAsStream("git.properties");
            JsonNode node = new ObjectMapper().readTree(inputStream);
            JsonNode jsnode;
            jsnode = node.get("git.branch");
            ll.put("branch", jsnode.textValue());
            jsnode = node.get("git.build.time");
            ll.put("build_time", jsnode.textValue());
            jsnode = node.get("git.build.user.email");
            ll.put("email", jsnode.textValue());
            jsnode = node.get("git.build.version");
            ll.put("version", jsnode.textValue());
            jsnode = node.get("git.closest.tag.name");
            /* next fies are setting issue ..  not really needed !
            ll.put("closest_tag", jsnode.textValue());
            jsnode = node.get("git.commit.id.abbrev");
            ll.put("short_hash", jsnode.textValue());
            jsnode = node.get("git.commit.time");
            ll.put("commit_time", jsnode.textValue());*/
        } catch (IOException e1) {
            e1.printStackTrace();
        }
        return ll;
    }
}
