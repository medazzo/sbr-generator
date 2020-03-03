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
@RequestMapping(path = "/status")
public class StatusController {

    @RequestMapping(value = "/version", method = RequestMethod.GET, produces = "application/json")
    @ResponseBody
    public Map<String, String> versionInformation() throws IOException {
    	  Map<String, String> ll = new HashMap<String, String>();
			ll.put("Server status ", " Working fine !!");
        //readGitProperties(ll);
        return  ll;        
    }
/* Removed because git plugin is taken too munch time on booting : 
    private Map<String, String> readGitProperties(Map<String, String> ll) {
        ClassLoader classLoader = getClass().getClassLoader();        
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
            // next fies are setting issue ..  not really needed !
            // ll.put("closest_tag", jsnode.textValue());
            // jsnode = node.get("git.commit.id.abbrev");
            // ll.put("short_hash", jsnode.textValue());
            // jsnode = node.get("git.commit.time");
            // ll.put("commit_time", jsnode.textValue());
        } catch (IOException e1) {
            e1.printStackTrace();
        }
        return ll;
    }*/
}
