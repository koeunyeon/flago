from collections.abc import MutableMapping
import validators # pip install validators



from functools import wraps
def valid_wrap(param):
    def wrapper(func):
        @wraps(func)
        def decorator(self, *args, **kwargs):
            key = None
            if 'key' in kwargs.keys():
                key = kwargs['key']
            elif len(args) > 0:
                key = args[0]                        
            else:
                self._add_validation_fail("INVALID_KEY_FUNC", "VALIDATION :: INVALID_KEY :: " + func.__name__)
                return self

            if key not in self.__dict__.keys():
                self._add_validation_fail(key, "VALIDATION :: KEY_NOT_EXIST :: " + func.__name__)
                return self

            validation_message = "VALIDATION :: " + param
            validation_message += " :: " + str(getattr(self, key))
            try:
                result = func(self, *args, **kwargs)
                if not result:
                    self._add_validation_fail(key, validation_message)
            except Exception as ex:                
                self._add_validation_fail(key, validation_message)

            return self
            
        return decorator
    return wrapper

class Magic:
    def __init__(self, **kwargs):        
        self._data = dict()
        self._validation_results = dict()

        self.__dict__.update(kwargs)
        
        for key, val in kwargs.items():
            self._append_self_data(key, val)        
        
    def __getattr__(self, key):
        if key in self.__dict__.keys():
            return self.__dict__[key]
        return None

    def _append_self_data(self, key, val):
        if key not in ['_data', "_validation_results"]:
            self._data[key] = val
    
    def __setattr__(self, key, val):
        super().__setattr__(key, val)

        self._append_self_data(key, val)
    
    def __str__(self):
        return str(self.__dict__)

    def __len__(self):
        return len(self._data)
    
    def items(self):
        return self._data
    
    def v_filter_keys(self, *keys):        
        remove_keys = list(filter(lambda x:x not in keys , self._data.keys()))
        for key in remove_keys:
            super().__delattr__(key)
        return self


    def _add_validation_fail(self, key, message):
        if key not in self._validation_results.keys():
            self._validation_results[key] = []
        self._validation_results[key].append(message)
    
    @valid_wrap("BETWEEN")
    def v_between(self, key, min=None, max=None):
        return validators.between(self.__dict__[key], min=min, max=max)
    
    @valid_wrap("DOMAIN")
    def v_domain(self, key):        
        return validators.domain(self.__dict__[key])

    @valid_wrap("EMAIL")
    def v_email(self, key):
        return validators.email(self.__dict__[key])

    @valid_wrap("IVAN")
    def v_ivan(self, key):
        return validators.ivan(self.__dict__[key])
    
    @valid_wrap("IPV4")
    def v_ipv4(self, key):
        return validators.ipv4(self.__dict__[key])
    
    @valid_wrap("IPV6")
    def v_ipv6(self, key):
        return validators.ipv6(self.__dict__[key])

    @valid_wrap("LENGTH")
    def v_length(self, key, min=None, max=None):
        return validators.length(self.__dict__[key], min=min, max=max)

    @valid_wrap("MAC_ADDRESS")
    def v_mac_address(self, key):
        return validators.mac_address(self.__dict__[key])

    @valid_wrap("SLUG")
    def v_slug(self, key):
        return validators.slug(self.__dict__[key]) 
    
    @valid_wrap("TRUE")
    def v_true(self, key):
        return validators.truthy(self.__dict__[key]) 
    
    @valid_wrap("URL")
    def v_url(self, key, public=False):
        ret = validators.url(self.__dict__[key], public=public) 
        if ret:
            return True
        return False # ValidationFailure 반환하기 때문에 단순하게 False 리턴

    @valid_wrap("UUID")
    def v_uuid(self, key):
        return validators.uuid(self.__dict__[key])
        
    def v_result(self):
        return self._validation_results
    
    def v_is_validate(self):
        return len(self._validation_results) == 0


"""
ed = Magic(a="a")
print ("init value", ed.a)
print ("not assign value", ed.b)
ed.c = "c"
print ("assign value", ed.c)
ed.v_filter_keys("a","b")
print ("after filter", ed)

ed.email = "aaa@bbb.com"
ed.v_email("email")
ed.email2 = ""
ed.v_email("email2")
print ("email", ed.v_result())

ed.between = 3
ed.v_between("between", 1, 5)

ed.between2 = 3
ed.v_between("between2", 1, max=2)
ed.v_email("between")

print ("between", ed.v_result())

ed.domain = "aaa.com"
ed.domain2 = None

ed.v_domain("domain")
ed.v_domain("domain2")
ed.v_domain("")

print ("domain", ed.v_result())
"""