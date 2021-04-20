import sys
import traceback

import importlib
from flask import request, render_template
from jinja2.exceptions import TemplateNotFound
from .flago_magic import Magic

#from ..endpoints#

def _bind_error(message, path):
    return message +  ". error in " + path

def _get_func_name(func_name):
    if func_name.startswith("__"):
        return "index"
    if request.method in ['POST', 'PUT', "DELETE"]:
        func_name = func_name + "_" + request.method.lower()
        
    return func_name
    

def request_bind(path=""):
    if path == "/favicon/ico":
        return
        
    module_name = "index"
    func_name = "index"
    request_path = "index"
    params = []
    passing_data = dict()

    # default. /ep/index.py/index()
    if path == "":
        module_name = "index"    
    elif "/" not in path: # /ep/모듈.py.index()
        module_name = path
    else: # /ep/모듈.py/함수명
        split_path = path.split("/")
        module_name = split_path[0]
        func_name = _get_func_name(split_path[1])     
        request_path = split_path[1]
        
        #if request.mimetype == "text/html":
        passing_data = request.form
        
        print (request.mimetype, request.accept_mimetypes, request.content_type)

        if len(split_path) >= 2:
            params = split_path[2:]

    m = None
    import_module_name = "app.ep."     + module_name
    if import_module_name in sys.modules.keys():
        m = sys.modules[import_module_name]
    else:
        m = importlib.import_module("...ep." + module_name, package=__name__)
    if hasattr(m, func_name):
        func = getattr(m, func_name)        
        if callable(func):            
            try:                
                result = None
                if 'data' in list(func.__code__.co_varnames):
                    func_param_data = Magic(**passing_data)
                    result = func(*params, data=func_param_data)
                else:
                    result = func(*params)

                # text/html
                template_path = "/".join([module_name, request_path]) + ".html"
                
                
                # {}, template_path
                if result is None:                    
                    result = Magic()

                # result, template_path
                elif len(result) == 1:
                    if type(result) == str:
                        return result
                                    
                elif len(result) == 2:
                    if type(result) != Magic:                        
                        template_path = result[1]
                        result = result[0]
                
                try:
                    return render_template(template_path, items=result.items(), validation_results = result.v_result())
                except TemplateNotFound as ex:
                    return "TEMPLATE NOT FOUND"
                # return render_template(template_path)
                # application/json
            except Exception as ex:
                print ("Exception in callable : ", ex)
                traceback.print_exc()
                return _bind_error("callable error", path)
    
    return _bind_error("not match endpoint", path)