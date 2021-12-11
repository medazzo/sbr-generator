package {{package}};

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@Getter
@Setter
@ToString
@ResponseStatus(value = HttpStatus.NOT_FOUND)
public class ResourceNotFoundException extends RuntimeException {
	/**
	 * 
	 */
	private static final long serialVersionUID = -1517971622745346451L;
	private String resourceName;
	private String fieldName;
	private Object fieldValue;
	public ResourceNotFoundException( String message) {
		super(message);
		this.resourceName = "";
		this.fieldName = "";
		this.fieldValue = "";
	}
	
	public ResourceNotFoundException( String resourceName, String fieldName, Object fieldValue) {
	    super(String.format("%s not found with %s : '%s'", resourceName, fieldName, fieldValue));
	    this.resourceName = resourceName;
	    this.fieldName = fieldName;
	    this.fieldValue = fieldValue;
	}

}
