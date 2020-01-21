/*   Copyright (C) 2019 EASYSOFT-IN                                 */
/*   All rights exclusively reserved for EASYSOFT-IN,               */
/*   unless otherwise expressly agreed.                             */
/*                                                                  */
/*   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *    */
/*   This is a Generated source code file                           */
/*   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *    */
package {{package}};

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@Getter
@Setter
@ToString
@ResponseStatus(value = HttpStatus.BAD_REQUEST)
public class ResourceBadParameterException extends RuntimeException {

    private static final long serialVersionUID = -1517971622745346451L;
    private String resourceName;
    private String fieldName;
    private Object fieldValue;

    public ResourceBadParameterException(String resourceName, String fieldName, Object fieldValue) {
        super(String.format("%s Bad request with parmeter %s : '%s'", resourceName, fieldName, fieldValue));
        this.resourceName = resourceName;
        this.fieldName = fieldName;
        this.fieldValue = fieldValue;
    }

}
