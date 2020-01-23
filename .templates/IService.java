package {{package}};

import java.util.List;

public interface IService<T> {

    public T create(T n);

    public List<T> getAll();

    public List<T> getAllBySomeId(String id);

    public T getOne(String id);

    public T update(T n);

    public void deleteone(String id);
}
