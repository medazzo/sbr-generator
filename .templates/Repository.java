package {{package}};

import {{Entitypackage}};
import org.springframework.data.jpa.repository.JpaRepository;
{%- if entityName == "User"  %}
import org.springframework.data.jpa.repository.Query;
{%- endif  %}
import java.util.List;

public interface {{entityName}}Repository extends JpaRepository<{{entityName}}, String> {
{%- if entityName == "User"  %}
   @Query("select u from User u where u.Email = ?1")
   User findByEmail(String Email);
{%- endif  %}
	public List<{{entityName}}> findByName(String name);
}
