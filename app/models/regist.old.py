# 회원 가입 모델.
# DB 테이블과 1:1 같은 게 아니라, 비즈니스 로직이 들어가는 공간이라는 것에 신경쓸 것.
# mongoDB로 할 꺼라서 스키마는 신경 안써도 됨.

# 정확히 지향하고자 하는 바가 뭐지?
# **웹** 서비스를 만드는 데 빠르고 유지보수 가능하고 확장 가능하도록.
# Procedual하게? OOP하게? 왜?
# MSA라고 생각해 보자. 사실상 "collection(table)" 을 하나만 다룬다.
# 그러면 리소스는 `User` 하나만 있으면 된다. 
# 도메인은 리소스가 뭘 하고자 하는지에 대한 이야기다.
# 회원 가입과 로그인은 전혀 다른 행위이고, 컬렉션의 데이터만 공유할 뿐이다.
# 데이터를 다룰때는 모델에서, 절차는 서비스 혹은 컨트롤러에서 다룬다.

# 됐다. 너무 복잡하다.
# 그냥 procedual하게 하자.

"""
# 가입 시도
regist = Regist(email=email)
if regist.exist_email():
    return regist.EXIST_EMAIL
regist.attempt()

# 가입 완료
user = Regist(email=email).first()
if user is None:
    return regist.NOT_EXIST_EMAIL

if user.match_regist_auth_key(auth_key):
    user.regist_auth_complete()
else:


"""

class Regist3:
    def __init__(self, email):
        self.email = email        

    def exist_email(self):
        return db.user.count(email=self.email) > 0
    
    def attempt(self):
        regist_auth_key = generate_random_key()
        db.user.insert(email=email, regist_auth_key=regist_auth_key)
    
    def first(self):
        user = db.user.find_one(email=email)
        for k, v in user.items():
            setattr(self, k,v)
    


# user.py
class Regist2:
    # 묵시적으로 내부 `email`을 들고 있는 게 나은가? 아니면 파라미터로 입력받는 게 나은가?
    # 모든 메소드가 `email`을 사용한다면 묵시적으로 들고 있어도 되지만, 그렇지 않다면 굳이 들고 있어야 하는 이유는 무언가?
    # OK. 꼭 필요한 경우가 아니면 멤버 변수를 쓰지 말자.
    # 꼭 필요하다는 건, 여러 메소드에서 "상태"를 기반으로 뭔가를 해야 할 때.
    # 회원 가입의 식별자는 email이므로, email만 멤버 변수로 가진다.

    EXIST_EMAIL = "EXIST_EMAIL"
    REGIST_SUCCESS = "REGIST_SUCCESS"

    NOT_EXIST_EMAIL = "NOT_EXIST_EMAIL"
    REGIST_COMPLETE = "REGIST_COMPLETE"
    INVALID_REGIST_AUTH_KEY = "INVALID_REGIST_AUTH_KEY"

    def __init__(self, email):
        self.email = email
        self.regist_auth_key = None
        self._last_result = None
    
    def if_not_exist(self):
        self._last_result = db.user.count(email=email) == 0
        return self
    
    def attempt(self):
        self.regist_auth_key = generate_random_key()
        db.user.insert(self)

    # Regist().if_exist().if_match_auth_key(regist_auth_key).complete()
    def if_exist(self):
        self._last_result = db.user.count(email=self.email)> 0
        return self
    
    def if_match_auth_key(self,regist_auth_key) : 
        user = db.user.first(email=self.email)
        if user is None:
            return Regist2.NOT_EXIST_EMAIL
        

    def complete(self):
        



    # Regist().attempt(email=email)    
    # Regist(email).attempt()
    # Regist(email).if_not_exist().attempt()    
    # Regist().attempt_if_not_exist(email)
    #def attempt(self)

"""
resource | domain | 메소드
회원 | 회원가입 | 회원가입 시도 | regist_try
회원 | 회원가입 | 회원가입 인증 | regist_complete
회원 | 로그인 | 로그인 시도 | login_try
회원 | 로그인 | 로그인 시도 | login_try
"""

# user.py
class Regist:
    self.
    class Attempt:
        def __init__(self, email):
            self.email = email
            
    
    class Auth:
        def __init__(self, email):


class Regist:
    def __init__(self):
        self.email = email
        self.regist_auth_key = regist_auth_key

    def regist_try():
        pass
    
    def regist_complete():
        pass


# 회원가입 절차
# 회원 가입 화면을 클릭한다.
# 회원 가입 화면에 이메일 주소를 입력하고 가입 버튼을 누른다.
## 이메일이 이미 있는지 확인한다.
def exist_email(email):
    return db.user.count(email=email) > 0

def generate_random_key(length=10):
    result = ""
    for i in range(length):
        result += random.choice(string.ascii_letters + string.digits)
    return result

class RETURN_MESSAGE:
    EXIST_EMAIL = "EXIST_EMAIL"
    REGIST_SUCCESS = "REGIST_SUCCESS"

    NOT_EXIST_EMAIL = "NOT_EXIST_EMAIL"
    REGIST_COMPLETE = "REGIST_COMPLETE"
    INVALID_REGIST_AUTH_KEY = "INVALID_REGIST_AUTH_KEY"

def regist(email):
    ### 이메일이 이미 있다면 이미 있는 이메일이라는 메세지를 보낸다.
    if exist_email(email):
        return RETURN_MESSAGE.EXIST_EMAIL
    ### 이메일이 없다면 인증키를 생성하고 데이터를 저장한 후 이메일을 보낸다.
    regist_auth_key = generate_random_key()
    db.user.insert(email=email, regist_auth_key=regist_auth_key)
    # send_regist_email(email, regist_auth_key=regist_auth_key)
    return 

def regist_complete(email, regist_auth_key):
    ### 이메일이 없다면 이메일이 없다는 메세지를 보낸다.
    if exist_email(email):
        return RETURN_MESSAGE.NOT_EXIST_EMAIL
    
    ### 인증키가 일치하는지 확인한다.
    user = db.user.first(email=email, regist_auth_key=regist_auth_key)
    if user:        
        user.update(regist_auth_complete="Y")
        return RETURN_MESSAGE.REGIST_COMPLETE

    return RETURN_MESSAGE.INVALID_REGIST_AUTH_KEY


# 미니몽고 사용?
# 몽고를 도입한 이유가, 스키마가 없고, 서비스에서 바로 쓸 수 있게 하려고
# 영속성 레이어니까 객체를 쓰는 게 더 낫다고 생각했는데..


class MGDB:
    USER = "user"

    def __init__(self, collection_name):        
        self.client = MongoClient('localhost', 27017) # by config
        self.db = self.client["database_name_by_config"]
        self.collection_name = collection_name

        self.data = dict()

    def instance(self, **kwargs):
        self.collection = self.db[self.collection_name]
        self.data = kwargs
        return self.collection
    
    def first(self, **kwargs):
        pass

    def all(self, **kwargs):
        pass

    def save(self):
        self.collection.save(self.data)
    
    @classmethod
    def USERS(**kwargs):
        return MGDB(MGDB.USER).instance(**kwargs)

def attempt(email):
    user = MGDB.USERS().first(email=email)
    # user = MGDB(MGDB.USER).first(email=email)
    
    if user:
        return RETURN_MESSAGE.EXIST_EMAIL
    
    user.insert(dict(
        email=email, 
        regist_auth_yn='Y', 
        regist_date = datetime.datetime.now()
        )
    )

    return RETURN_MESSAGE.REGIST_SUCCESS

def complete(email, regist_auth_key):
    user = MGDB.USERS().first(email=email, regist_auth_key=regist_auth_key)
    if not user:
        return RETURN_MESSAGE.INVALID_REGIST_AUTH_KEY
    
    user.regist_auth_complete = "Y"
    user.save()

    return RETURN_MESSAGE.REGIST_COMPLETE



def attempt(email):
    user = db.user.first(email=email)
    if user:
        return "EXIST EMAIL"

    regist_auth_key = "asdasdSA"
    db.user.save(email=email, regist_auth_key=regist_auth_key, regist_auth_date=datetime.datetime.now())


def complete(email, regist_auth_key):
    user = db.user.first(email=email, regist_auth_key=regist_auth_key)
    if user is None:
        return "NOT EXIST EMAIL OR REGIST KEY IS INVALID"
    
    user.update(regist_auth_complete='Y')
    

