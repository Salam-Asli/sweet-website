from flask import Blueprint, jsonify, request
from .models import db, Product, Order, User
from sqlalchemy import or_

main = Blueprint('main', __name__)

@main.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'stock': p.stock
    } for p in products])

@main.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock
    })

@main.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully', 'id': new_product.id}), 201

@main.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

from sqlalchemy.exc import IntegrityError

@main.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        # Check if there are any orders associated with this product
        orders = Order.query.filter_by(product_id=product_id).first()
        if orders:
            return jsonify({'message': 'Cannot delete product. It has associated orders.'}), 400

        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Cannot delete product. It has associated orders.'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the product', 'error': str(e)}), 500

@main.route('/api/products/search', methods=['GET'])
def search_products():
    query = request.args.get('q')
    if query:
        products = Product.query.filter(or_(
            Product.name.ilike(f'%{query}%'),
            Product.description.ilike(f'%{query}%')
        )).all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'stock': p.stock
        } for p in products])
    return jsonify({'message': 'No search query provided'}), 400

@main.route('/api/products/inventory', methods=['GET'])
def get_product_inventory():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'stock': p.stock
    } for p in products])

@main.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        orders = Order.query.all()
        return jsonify([{
            'id': o.id,
            'user_id': o.user_id,
            'product_id': o.product_id,
            'quantity': o.quantity,
            'total_price': o.total_price,
            'status': o.status
        } for o in orders]), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred while fetching orders', 'error': str(e)}), 500

@main.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(
        user_id=data['user_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        total_price=data['total_price']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully', 'id': new_order.id}), 201

@main.route('/api/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': o.id,
        'product_id': o.product_id,
        'quantity': o.quantity,
        'total_price': o.total_price,
        'status': o.status
    } for o in orders])

@main.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.json
    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify({'message': 'Order status updated successfully'})

@main.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'id': new_user.id}), 201

@main.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@main.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal server error'}), 500