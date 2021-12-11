package {{package}};

import java.util.List;

import org.springframework.http.ResponseEntity;

public interface IController<T> {

    public ResponseEntity<T> create(T n);

    public List<T> getAll();

    public List<T> getAllBySomeId(String id);

    public T getOne(String id);

    public T update(String id, T n);

    public void delete(String id);

}