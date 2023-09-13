from config import db,app


class Product(db.Model):
    __tablename__ = 'PRODUCT_INFO'
    id = db.Column('prod_id',db.Integer(),primary_key=True)
    name = db.Column('prod_name',db.String(30))
    qty = db.Column('prod_qty', db.Integer())
    category = db.Column('prod_category', db.String(30))
    vendor = db.Column('prod_vendor', db.String(30))
    price = db.Column('prod_price', db.Float())

#Product(id,name,qty,category,vendor,price)



with app.app_context():
    db.create_all()
    print('Tables created...!')