package {{package}};

import {{Entitypackage}};
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface {{entityName}}Repository extends JpaRepository<{{entityName}}, String> {
	public List<{{entityName}}> findByName(String name);
}
