package {{package}};

import org.springframework.http.*;
import org.springframework.stereotype.Controller;
import org.springframework.boot.web.servlet.error.ErrorController;
import org.springframework.web.bind.annotation.*;
import lombok.extern.slf4j.Slf4j;
import javax.servlet.*;
import javax.servlet.http.*;

@Slf4j
@Controller
public class MyErrorController implements ErrorController {

  @RequestMapping("/error")
  @ResponseBody
  public String handleError(HttpServletRequest request) {
      Integer statusCode = (Integer) request.getAttribute("javax.servlet.error.status_code");
      Exception exception = (Exception) request.getAttribute("javax.servlet.error.exception");
      return String.format("<html><body><h2>{{project.name}}-{{project.version}}:  Error Page</h2><div>Status code: <b>%s</b></div>"
                      + "<div>Exception Message: <b>%s</b></div><body></html>",
              statusCode, exception==null? "N/A": exception.getMessage());
  }

  @Override
  public String getErrorPath() {
      return "/error";
  }
}
