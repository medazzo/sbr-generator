package {{package}};

import {{projectPackage}}.exceptions.ResourceNotFoundException;

import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import javax.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import {{Entitypackage}};
import {{Repositorypackage}};

import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service(value = "userService")
public class UserService  implements  UserDetailsService, IService<User> {

    @Autowired
    private UserRepository erepo;

    @Autowired
     private BCryptPasswordEncoder bcryptEncoder;

     public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
     log.debug(" >>>>>>>>>>>>>> looking for user with email  " + email);
     User user = erepo.findByEmail(email);

     if (user == null) {
         log.error(" UsernameNotFoundException : user not found with email " + email);
         throw new UsernameNotFoundException("Invalid email or password.");
     }
     log.info(" >>>>>>>>>>>>>> Found user is   " + getAuthority(user));
     UserDetails urd = new org.springframework.security.core.userdetails.User(user.getEmail(), user.getPassword(), getAuthority(user));
     return urd;
 }

 public User GetUserByUsername(String email) throws UsernameNotFoundException {
     log.debug(" >>>>>>>>>>>>>> looking for user with email  " + email);
     User user = erepo.findByEmail(email);

     if (user == null) {
         log.error(" UsernameNotFoundException : user not found with email " + email);
         throw new UsernameNotFoundException("Invalid email or password.");
     }

     return user;
 }

 @Transactional
 protected Set<SimpleGrantedAuthority> getAuthority(User user) {
     Set<SimpleGrantedAuthority> authorities = new HashSet<>();
     authorities.add(new SimpleGrantedAuthority(user.getMainRole()));
     return authorities;
 }


    @Override
    public User create(User n) {
        log.info("Saving new  User .. " + n.toString());
        return erepo.save(n);
    }

    @Override
    public List<User> getAll() {
        log.info("Getting All  .. ");
            return erepo.findAll();
    }

    @Override
    public List<User> getAllBySomeId(String id) {
        log.info("Getting All by some id  ..  " + id);
        // Todo correctly
        return erepo.findAll();
    }

    @Override
    public User getOne(String id) {
        log.info("Getting one with id   .. " + id);
        User cm = erepo.findById(id).orElseThrow(() -> new ResourceNotFoundException("User", "id", id));
        return cm;
    }

    @Override
    public void deleteone(String id) {
        log.info("Deleting one with id   .. " + id);
        if (id == null) {
            throw new ResourceNotFoundException("User", "id", id);
        }
        if (this.erepo.existsById(id)) {
            User cm = erepo.findById(id).orElseThrow(() -> new ResourceNotFoundException("User", "id", id));

            erepo.deleteById(id);
        } else {
            throw new ResourceNotFoundException("User", "id", id);
        }
    }

    @Override
    public User update(User n) {
        if (n == null) {
            throw new ResourceNotFoundException("User", "id", n);
        }
        log.info("Updating one  User   .. " + n.toString());
        return erepo.findById(n.getId()).map(found -> {
            {% for field in entity.fields | sort(attribute='name') %}found.set{{field.name[0]|upper}}{{field.name[1:] }}(n.get{{field.name[0]|upper}}{{field.name[1:]}}());
            {% endfor %}
            return erepo.save(found);
        }).orElseThrow(() -> {
            throw new ResourceNotFoundException("User", "id", n.getId());
        });
    }
}
