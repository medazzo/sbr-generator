/*   Copyright (C) 2019 EASYSOFT-IN                                 */
/*   All rights exclusively reserved for EASYSOFT-IN,               */
/*   unless otherwise expressly agreed.                             */
/*                                                                  */
/*   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *    */
/*   This is a Generated source code file                           */
/*   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *    */
package {{package}};

import {{Entitypackage}};
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface {{entityName}}Repository extends JpaRepository<{{entityName}}, String> {
	public List<{{entityName}}> findByName(String name);
}
