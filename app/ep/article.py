# GET /article/create => /templates/article/create.html
# GET /article/create.json => {}

from .. import db
from flask import redirect

def index():
    return

# GET /article/create => /templates/article/create.html
def create():
    return # equals return {}, None == dict(), template/article/create.html || {}

# POST /article/create
def create_post(data):
    data = data.v_filter_keys("title", "content").v_true("title").v_true("content").v_length("title", 4, 10).v_length("content", 10, 100)

    if data.v_is_validate():
        article = db.article.insert(data.items())        
        print (article)
        redirect("/article/read/" + article._id)
    return data # equals return data, None == data, template/article/create.html || data {items : {...}, validation_results : {...}}


def edit(id):
    print ("edit run")
    return