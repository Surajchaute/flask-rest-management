from product_info import *
from flask import request,jsonify
import json
from flask_jwt_extended import \
    create_access_token,\
    create_refresh_token,\
    jwt_required,\
    JWTManager,\
    get_jwt_identity

@app.route('/api/generate/token',methods = ['POST'])
def generate_jwt_tokens():
    req_body =  request.get_json()
    username,password = req_body.get('username'),req_body.get('password')
    if username=='python' and password=='webdev':
        credentials = (username,password)       #identity
        access_token = create_access_token(identity = credentials)
        refresh_token = create_refresh_token(identity = credentials)
        return jsonify({"ACCESS-TOKEN":access_token,"REFRESH-TOKEN":refresh_token})
    else:
        return jsonify({"ERROR" : "Invalid Credentails"}),401

@app.route('/api/generate/accesstoken')
@jwt_required(refresh=True)
def obtain_accesstoken_frm_refreshtoken():
    credentials = get_jwt_identity()
    access_token = create_access_token(identity=credentials)
    return jsonify({"ACCESS-TOKEN": access_token})

@app.route("/api/v1/product",methods = ['POST'])    #http://localhost:5000/api/v1/product -- POST
@jwt_required()
def add_new_product():
    jsondata = request.get_json()      # req madhn mala json
    try:
        pr = Product(id = jsondata.get('PRODUCT_ID'),
                name = jsondata.get('PRODUCT_NAME'),
                qty = jsondata.get('PRODUCT_QTY'),
                category = jsondata.get('PRODUCT_CATEGORY'),
                vendor = jsondata.get('PRODUCT_VENDOR'),
                price = jsondata.get('PRODUCT_PRICE'))
        db.session.add(pr)
        db.session.commit()
        return jsonify({"SUCCESS" : "PRODUCT SUCCESSFULLY ADDED...!"}),201
    except BaseException as b:
        print(b.args)
        return jsonify({"ERROR": "PROBLEM IN PRODUCT ADD....!"}), 200

@app.route("/api/v1/product/<int:pid>",methods = ['PUT'])
@jwt_required()
def update_product(pid):
    prod = Product.query.filter_by(id=pid).first()
    if prod:
        jsondata = request.get_json()  # req madhn mala json
        try:
            prod.name = jsondata.get('PRODUCT_NAME')
            prod.price = jsondata.get('PRODUCT_PRICE')
            prod.qty = jsondata.get('PRODUCT_QTY')
            prod.category = jsondata.get('PRODUCT_CATEGORY')
            prod.vendor = jsondata.get('PRODUCT_VENDOR')
            db.session.commit()
            return jsonify({"SUCCESS": "PRODUCT SUCCESSFULLY UPDATED...!"}), 201
        except BaseException as b:
            print(b.args)
            return jsonify({"ERROR": "PROBLEM IN PRODUCT UPDATE....!"}), 200
    else:
        return json.dumps({"ERROR": "No PRODUCT WITH GIVEN ID..CANNOT UPDATE..!"})


@app.route("/api/v1/product/<int:pid>",methods=['DELETE'])
@jwt_required()
def delete_product(pid):
    prod = Product.query.filter_by(id=pid).first()
    if prod:
        db.session.delete(prod)
        db.session.commit()
        return json.dumps({"SUCCESS": "Product DELETED.!"})
    else:
        return json.dumps({"ERROR": "No PRODUCT WITH GIVEN ID..CANNOT DELETE..!"})

@app.route("/api/v1/product/<int:pid>",methods = ['PATCH'])
def modify_product(pid):
    pass

@app.route("/api/v1/product/<int:pid>",methods = ['GET'])
@jwt_required()
def search_product(pid):
    prod = Product.query.filter_by(id=pid).first()
    if prod:
        return json.dumps({"PRODUCT-ID":prod.id,
                               "PRODUCT-NAME":prod.name,
                               "PRODUCT-CATEGORY":prod.category,
                               "PRODUCT-PRICE":prod.price,
                               "PRODUCT-QTY":prod.qty,
                               "PRODUCT-VENDOR":prod.vendor})
    else:
        return json.dumps({"ERROR" : "No PRODUCT WITH GIVEN ID..!"})

@app.route("/api/v1/product",methods = ['GET'])
@jwt_required()
def list_products():
    prodlist = Product.query.all()
    prod_json_list = []
    for prod in prodlist:
        prod_json_list.append({"PRODUCT-ID":prod.id,
                               "PRODUCT-NAME":prod.name,
                               "PRODUCT-CATEGORY":prod.category,
                               "PRODUCT-PRICE":prod.price,
                               "PRODUCT-QTY":prod.qty,
                               "PRODUCT-VENDOR":prod.vendor})
    if prod_json_list:
        return json.dumps(prod_json_list)
    else:
        return json.dumps({"ERROR" : "NO PRODUCTS..."}),200

