from flago.flago_do import FlagoDo

db = FlagoDo()
db.init_uri()

# insert
sample = db.user.insert(name='sample', nice='to meet you', korean='한글 테스트')
print ("insert", sample)

# select
sample_select = db.user.find(sample._id)
print ('select', sample_select)

# update
sample_update = db.user.find(sample._id).save(gender=25)
print ('update', sample_update)

# all
all = db.user.all()
for row in all:
    print ('all', row)


all = db.user.all(name='sample')
for row in all:
    print ('all term', row)
