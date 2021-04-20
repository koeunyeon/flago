from pymongo import MongoClient # pip install pymongo
from bson.objectid import ObjectId # NEVER INSTALL BSON. It's embed on pymongo

# Flask Mongo Document Object
class FlagoDoRow:
    def __init__(self, collection):
        self._collection = collection
    
    def __getattr__(self, name):            
        if name in self._data.keys():
            return self._data[name]
        return None

    def first(self, **kwargs):
        if '_id' in kwargs.keys() and type(kwargs['_id']) != ObjectId:
            kwargs['_id'] = ObjectId(kwargs['_id'])
        
        result = self._collection.find_one(kwargs)        
        self._data = result
        self._id = str(self._data['_id'])
        
        return self
    
    def find(self, _id):
        return self.first(_id=_id)

    def all(self, **kwargs):
        if '_id' in kwargs.keys() and type(kwargs['_id']) != ObjectId:
            kwargs['_id'] = ObjectId(kwargs['_id'])

        results = self._collection.find(kwargs)        
        return_datas = []
        for row in results:            
            new_row = FlagoDoRow(self._collection)            
            new_row._data = row
            new_row._id = str(row['_id'])
            return_datas.append(new_row)
        return return_datas
    
    def insert(self, *largs, **kwargs):
        if len(largs) == 1 and len(kwargs) == 0:
            kwargs = largs[0]
            
        insert_id = self._collection.insert_one(kwargs).inserted_id
        return self.find(insert_id)
        return self
    
    # 관련 필드만 추가/수정
    def update(self, _id, **kwargs):
        if type(_id) != ObjectId:
            _id = ObjectId(_id)
        
        self._data.update(kwargs)
        self._collection.update({'_id' : _id}, self._data)
        return self.find(_id)
    
    # 통채로 데이터를 바꿔버림.
    def change(self, _id, **kwargs):
        if type(_id) != ObjectId:
            _id = ObjectId(_id)
        
        self._collection.update({'_id' : _id}, kwargs)
        return self.find(_id)

    def save(self, **kwargs):
        if self._id is None:
            return self.insert(**kwargs)
        else:
            return self.update(self._id, **kwargs)

    def __str__(self):        
        self._data.update({"_id": self._id })
        return str(self._data)


class FlagoDo:
    def __init__(self):
        self._mongo_uri = None
        self._dbname = None

        self._client = None
        self._db = None

    def init_uri(self, uri="localhost:27017/", dbname="sample_db"):
        # uri example
        # host:port
        # localhost:27017/
        self._mongo_uri = uri
        self._dbname = dbname

        self._client = MongoClient("mongodb://" + uri)
        self._db = self._client[dbname]        
    
    def init_app(self, app):
        uri = app.config['MONGO_URI']
        dbname = app.config['MONGO_DBNAME']
        self.init_uri(uri, dbname)

    # set collection name or get attribute
    
    def __getattr__(self, name):
        self._collection = self._db[name]            
        return FlagoDoRow(self._collection)
    
    
        
        