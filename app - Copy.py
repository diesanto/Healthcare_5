from flask import Flask
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_paginate import Pagination, get_page_parameter, get_page_args
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'xxxxxxxx'

username = 'root'
password = ''
server = 'localhost'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{username}:{password}@{server}/car_dealership'.format(username, password, server)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/healthcare_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Memanggil SQLAlchemy
db = SQLAlchemy(app)

class Categories(db.Model):
    CategoryID = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.String(20), index=True, unique=True)
    Description = db.Column(db.String(20))
    Picture = db.Column(db.String(20))
    
    def to_json(self):
        return {
            'CategoryID': self.CategoryID,
            'CategoryName': self.CategoryName,
            'Description': self.Description,
            'Picture': self.Picture
        }


class Suppliers(db.Model):
    SupplierID = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String(40), index=True, unique=True)
    ContactName = db.Column(db.String(30))
    ContactTitle = db.Column(db.String(30))
    Address = db.Column(db.String(60))
    City = db.Column(db.String(15))
    Region = db.Column(db.String(15))
    PostalCode = db.Column(db.String(10))
    Country = db.Column(db.String(15))
    Phone = db.Column(db.String(24))
    Fax = db.Column(db.String(24))
    HomePage = db.Column(db.Text)
    
    def to_json(self):
        return {
            'SupplierID': self.SupplierID,
            'CompanyName': self.CompanyName,
            'ContactName': self.ContactName,
            'ContactTitle': self.ContactTitle,
            'Address': self.Address,
            'City': self.City,
            'Region': self.Region,
            'PostalCode': self.PostalCode,
            'Country': self.Country,
            'Phone': self.Phone,
            'Fax': self.Fax,
            'HomePage': self.HomePage
        }

class Customers(db.Model):
    CustomerID = db.Column(db.String(5), primary_key=True)
    CompanyName = db.Column(db.String(40), index=True, unique=True)
    ContactName = db.Column(db.String(30))
    ContactTitle = db.Column(db.String(30))
    Address = db.Column(db.String(60))
    City = db.Column(db.String(15))
    Region = db.Column(db.String(15))
    PostalCode = db.Column(db.String(10))
    Country = db.Column(db.String(15))
    Phone = db.Column(db.String(24))
    Fax = db.Column(db.String(24))
    
    def to_json(self):
        return {
            'CustomerID': self.CustomerID,
            'CompanyName': self.CompanyName,
            'ContactName': self.ContactName,
            'ContactTitle': self.ContactTitle,
            'Address': self.Address,
            'City': self.City,
            'Region': self.Region,
            'PostalCode': self.PostalCode,
            'Country': self.Country,
            'Phone': self.Phone,
            'Fax': self.Fax
        }

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/categories_list')
def categories_list():
    categories = Categories.query.all()

    return render_template('categories/categories_list.html', categories = categories)

@app.route('/categories_add', methods=['GET', 'POST'])
def categories_add():
    if request.method == 'POST':        
        categories = Categories(CategoryName = request.form['CategoryName'], 
                        Description = request.form['Description'])

        db.session.add(categories)
        db.session.commit()
        flash('You have successfully added a category.')
        
        return redirect(url_for('categories_list'))

    return render_template('categories/categories_form.html', action = url_for('categories_add'), title = 'Add categories')


@app.route('/categories_update/<int:CategoryID>', methods=['GET', 'POST'])
def categories_update(CategoryID):
    category = Categories.query.get_or_404(CategoryID)

    if request.method == 'POST':        
        category.CategoryName = request.form['CategoryName']
        category.Description = request.form['Description']

        db.session.add(category)
        db.session.commit()
        flash('You have successfully update a category.')

        return redirect(url_for('categories_list'))

    return render_template('categories/categories_form.html', category = category, action = url_for('categories_update', CategoryID=category.CategoryID), title = 'Update categories')

@app.route('/categories_delete/<int:CategoryID>', methods=['GET'])
def categories_delete(CategoryID):
    category = Categories.query.get_or_404(CategoryID)
    
    db.session.delete(category)
    db.session.commit()

    return redirect(url_for('categories_list'))

@app.route('/suppliers_list/', methods=['GET'], defaults={"page": 1})
@app.route('/suppliers_list/<int:page>', methods=['GET'])
def suppliers_list(page):
    per_page = 10
    suppliers = Suppliers.query.paginate(page, per_page, error_out = False)

    return render_template('suppliers/suppliers_list.html', suppliers = suppliers)

@app.route('/suppliers_add', methods=['GET', 'POST'])
def suppliers_add():
    if request.method == 'POST':        
        suppliers = Suppliers(SupplierID = request.form['SupplierID'], 
                        CompanyName = request.form['CompanyName'],
                        ContactName = request.form['ContactName'],
                        ContactTitle = request.form['ContactTitle'],
                        Address = request.form['Address'],
                        City = request.form['City'],
                        Region = request.form['Region'],
                        PostalCode = request.form['PostalCode'],
                        Country = request.form['Country'],
                        Phone = request.form['Phone'],
                        Fax = request.form['Fax'],
                        HomePage = request.form['HomePage'])

        db.session.add(suppliers)
        db.session.commit()
        flash('You have successfully added a Supplier.')
        
        return redirect(url_for('suppliers_list'))

    return render_template('suppliers/suppliers_form.html', action = url_for('suppliers_add'), title = 'Add suppliers')

@app.route('/suppliers_update/<int:SupplierID>', methods=['GET', 'POST'])
def suppliers_update(SupplierID):
    supplier = Suppliers.query.get_or_404(SupplierID)

    if request.method == 'POST':        
        supplier.CompanyName = request.form['CompanyName']
        supplier.ContactName = request.form['ContactName']
        supplier.ContactTitle = request.form['ContactTitle']
        supplier.Address = request.form['Address']
        supplier.City = request.form['City']
        supplier.Region = request.form['Region']
        supplier.PostalCode = request.form['PostalCode']
        supplier.Country = request.form['Country']
        supplier.Phone = request.form['Phone']
        supplier.Fax = request.form['Fax']
        supplier.HomePage = request.form['HomePage']

        db.session.add(supplier)
        db.session.commit()
        flash('You have successfully update a supplier.')

        return redirect(url_for('suppliers_list'))

    return render_template('suppliers/suppliers_form.html', supplier = supplier, action = url_for('suppliers_update', SupplierID=supplier.SupplierID), title = 'Update suppliers')

@app.route('/suppliers_delete/<int:SupplierID>', methods=['GET'])
def suppliers_delete(SupplierID):
    supplier = Suppliers.query.get_or_404(SupplierID)
    
    db.session.delete(supplier)
    db.session.commit()

    return redirect(url_for('suppliers_list'))

@app.route('/customers_list', methods=['GET'])
def customers_list():

    search = False
    q = request.args.get('q')
    if q:
        search = True
    
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    # page = request.args.get(get_page_parameter(), type=int, default=1)
    # page = int(request.args.get('page', 1))
    # per_page = 10
    # offset = (page - 1) * per_page

    query = Customers.query
    
    customers = query.limit(per_page).offset(offset) 

    pagination = Pagination(page=page, per_page=per_page, total=query.count(), search=search, record_name='customers', css_framework='bootstrap3')

    return render_template('customers/customers_list.html', customers = customers, pagination = pagination)

@app.route('/customers_add', methods=['GET', 'POST'])
def customers_add():
    if request.method == 'POST':        
        customers = Customers(CustomerID = request.form['CustomerID'], 
                        CompanyName = request.form['CompanyName'],
                        ContactName = request.form['ContactName'],
                        ContactTitle = request.form['ContactTitle'],
                        Address = request.form['Address'],
                        City = request.form['City'],
                        Region = request.form['Region'],
                        PostalCode = request.form['PostalCode'],
                        Country = request.form['Country'],
                        Phone = request.form['Phone'],
                        Fax = request.form['Fax'])

        db.session.add(customers)
        db.session.commit()
        flash('You have successfully added a Customer.')
        
        return redirect(url_for('customers_list'))

    return render_template('customers/customers_form.html', action = url_for('customers_add'), title = 'Add customers')

@app.route('/customers_update/<string:CustomerID>', methods=['GET', 'POST'])
def customers_update(CustomerID):
    customer = Customers.query.get_or_404(CustomerID)

    if request.method == 'POST':        
        customer.CompanyName = request.form['CompanyName']
        customer.ContactName = request.form['ContactName']
        customer.ContactTitle = request.form['ContactTitle']
        customer.Address = request.form['Address']
        customer.City = request.form['City']
        customer.Region = request.form['Region']
        customer.PostalCode = request.form['PostalCode']
        customer.Country = request.form['Country']
        customer.Phone = request.form['Phone']
        customer.Fax = request.form['Fax']

        db.session.add(customer)
        db.session.commit()
        flash('You have successfully update a customer.')

        return redirect(url_for('customers_list'))

    return render_template('customers/customers_form.html', customer = customer, action = url_for('customers_update', CustomerID=customer.CustomerID), title = 'Update customers')

@app.route('/customers_delete/<string:CustomerID>', methods=['GET'])
def customers_delete(CustomerID):
    customer = Customers.query.get_or_404(CustomerID)
    
    db.session.delete(customer)
    db.session.commit()

    return redirect(url_for('customers_list'))


class Products(db.Model):
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(40), index=True, unique=True)
    SupplierID = db.Column(db.Integer, db.ForeignKey('suppliers.SupplierID'))
    CategoryID = db.Column(db.Integer, db.ForeignKey('categories.CategoryID'))
    QuantityPerUnit = db.Column(db.String(20))
    UnitPrice = db.Column(db.Float)
    UnitsInStock = db.Column(db.SmallInteger)
    UnitsOnOrder = db.Column(db.SmallInteger)
    ReorderLevel = db.Column(db.SmallInteger)
    Discontinued = db.Column(db.SmallInteger)
    
    def to_json(self):
        return {
            'ProductID': self.ProductID,
            'ProductName': self.ProductName,
            'SupplierID': self.SupplierID,
            'CategoryID': self.CategoryID,
            'QuantityPerUnit': self.QuantityPerUnit,
            'UnitPrice': self.UnitPrice,
            'UnitsInStock': self.UnitsInStock,
            'UnitsOnOrder': self.UnitsOnOrder,
            'ReorderLevel': self.ReorderLevel,
            'Discontinued': self.Discontinued
        }

@app.route('/products_list/', methods=['GET'], defaults={"page": 1})
@app.route('/products_list/<int:page>', methods=['GET'])
def products_list(page):
    per_page = 10
    products = Products.query \
                .join(Categories, Products.CategoryID == Categories.CategoryID) \
                .join(Suppliers, Products.SupplierID == Suppliers.SupplierID) \
                .add_columns(Products.ProductID, Products.ProductName, Products.UnitPrice, Categories.CategoryName, Suppliers.CompanyName) \
                .paginate(page, per_page, error_out = False)

    return render_template('products/products_list.html', products = products)

@app.route('/products_add', methods=['GET', 'POST'])
def products_add():
    categories = db.session.query(Categories.CategoryID, Categories.CategoryName).all()
    suppliers = Suppliers.query.add_columns(Suppliers.SupplierID, Suppliers.CompanyName).all()

    if request.method == 'POST':        
        products = Products(ProductID = request.form['ProductID'],
                            ProductName = request.form['ProductName'],
                            SupplierID = request.form['SupplierID'],
                            CategoryID = request.form['CategoryID'],
                            QuantityPerUnit = request.form['QuantityPerUnit'],
                            UnitPrice = request.form['UnitPrice'],
                            UnitsInStock = request.form['UnitsInStock'],
                            UnitsOnOrder = request.form['UnitsOnOrder'],
                            ReorderLevel = request.form['ReorderLevel'],
                            Discontinued = request.form['Discontinued'])

        db.session.add(products)
        db.session.commit()
        flash('You have successfully added a Products.')
        
        return redirect(url_for('products_list'))

    return render_template('products/products_form.html', categories = categories, suppliers = suppliers, action = url_for('products_add'), title = 'Add products')

@app.route('/products_update/<int:ProductID>', methods=['GET', 'POST'])
def products_update(ProductID):
    categories = db.session.query(Categories.CategoryID, Categories.CategoryName).all()
    suppliers = Suppliers.query.add_columns(Suppliers.SupplierID, Suppliers.CompanyName).all()
    product = Products.query.get_or_404(ProductID)

    if request.method == 'POST':        
        product.ProductID = request.form['ProductID']
        product.ProductName = request.form['ProductName']
        product.SupplierID = request.form['SupplierID']
        product.CategoryID = request.form['CategoryID']
        product.QuantityPerUnit = request.form['QuantityPerUnit']
        product.UnitPrice = request.form['UnitPrice']
        product.UnitsInStock = request.form['UnitsInStock']
        product.UnitsOnOrder = request.form['UnitsOnOrder']
        product.ReorderLevel = request.form['ReorderLevel']
        product.Discontinued = request.form['Discontinued']

        db.session.add(product)
        db.session.commit()
        flash('You have successfully update a product.')

        return redirect(url_for('products_list'))

    return render_template('products/products_form.html', product = product, categories = categories, suppliers = suppliers, action = url_for('products_update', ProductID=product.ProductID), title = 'Update products')

@app.route('/products_delete/<string:ProductID>', methods=['GET'])
def products_delete(ProductID):
    product = Products.query.get_or_404(ProductID)
    
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('products_list'))

if __name__ == '__main__':
    app.run(debug = True)