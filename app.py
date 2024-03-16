from flask import Flask, jsonify, request
from Models import db, Book, ShoppingCart, Wallet, Librarian
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Initialize SQLAlchemy instance

# Exception handling for database errors
@app.errorhandler(SQLAlchemyError)
def handle_database_error(e):
    db.session.rollback()
    return jsonify({'error': f'Database error occurred: {str(e)}'}), 500


    



# Exception handling for database errors
def handle_database_error(e):
    db.session.rollback()
    return jsonify({'error': 'Database error occurred'}), 500

# Error handling for not found error
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

# Error handling for bad request error
@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad request'}), 400

# Error handling for method not allowed error
@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({'error': 'Method not allowed'}), 405

# Error handling for internal server error
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Route to add a book by the librarian
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    if 'name' not in data or 'author' not in data or 'price' not in data or 'quantity' not in data or 'category' not in data:
        return jsonify({'error': 'Incomplete data provided'}), 400
    try:
        book = Book(name=data['name'], author=data['author'], price=data['price'], quantity=data['quantity'], category=data['category'])
        db.session.add(book)
        db.session.commit()
        return jsonify({'message': 'Book added successfully'}), 201
    except SQLAlchemyError as e:
        return handle_database_error(e)

# Route to view all books by the librarian
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        'id': book.id,
        'name': book.name,
        'author': book.author,
        'price': book.price,
        'quantity': book.quantity,
        'category': book.category
    } for book in books])

# Route to remove a book by the librarian
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    except SQLAlchemyError as e:
        return handle_database_error(e)

# Route to change quantity of a book by the librarian
@app.route('/books/<int:book_id>', methods=['PUT'])
def change_quantity(book_id):
    data = request.json
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        if 'quantity' not in data:
            return jsonify({'error': 'Quantity not provided'}), 400
        book.quantity = data['quantity']
        db.session.commit()
        return jsonify({'message': 'Quantity updated successfully'})
    except SQLAlchemyError as e:
        return handle_database_error(e)

# Route to add a book to the shopping cart
@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    if 'book_id' not in data or 'quantity' not in data:
        return jsonify({'error': 'Incomplete data provided'}), 400
    try:
        book = Book.query.get(data['book_id'])
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        cart_item = ShoppingCart(book_id=data['book_id'], quantity=data['quantity'])
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item added to cart successfully'}), 201
    except SQLAlchemyError as e:
        return handle_database_error(e)

# Route to view items in the shopping cart
@app.route('/cart', methods=['GET'])
def view_cart():
    cart_items = ShoppingCart.query.all()
    return jsonify([{
        'book_id': item.book_id,
        'quantity': item.quantity
    } for item in cart_items])
    
    
# Route to update an item in the shopping cart
@app.route('/cart/<int:cart_id>', methods=['PUT'])
def update_cart_item(cart_id):
    data = request.json
    try:
        cart_item = ShoppingCart.query.get(cart_id)
        if not cart_item:
            return jsonify({'error': 'Item not found in cart'}), 404
        if 'quantity' not in data:
            return jsonify({'error': 'Quantity not provided'}), 400
        cart_item.quantity = data['quantity']
        db.session.commit()
        return jsonify({'message': 'Cart item updated successfully'})
    except SQLAlchemyError as e:
        return handle_database_error(e)
    
    
# Route to remove an item from the shopping cart
@app.route('/cart/<int:cart_id>', methods=['DELETE'])
def remove_from_cart(cart_id):
    try:
        cart_item = ShoppingCart.query.get(cart_id)
        if not cart_item:
            return jsonify({'error': 'Item not found in cart'}), 404
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item removed from cart successfully'})
    except SQLAlchemyError as e:
        return handle_database_error(e)

# Route to add a librarian
@app.route('/librarian', methods=['POST'])
def add_librarian():
    data = request.json
    if 'name' not in data:
        return jsonify({'error': 'Name not provided'}), 400
    try:
        librarian = Librarian(name=data['name'])
        db.session.add(librarian)
        db.session.commit()
        return jsonify({'message': 'Librarian added successfully'}), 201
    except SQLAlchemyError as e:
        return handle_database_error(e)

# Route to get all librarians
@app.route('/librarian', methods=['GET'])
def get_librarians():
    librarians = Librarian.query.all()
    return jsonify([{
        'id': librarian.id,
        'name': librarian.name
    } for librarian in librarians])

# Route to update a librarian
@app.route('/librarian/<int:librarian_id>', methods=['PUT'])
def update_librarian(librarian_id):
    data = request.json
    try:
        librarian = Librarian.query.get(librarian_id)
        if not librarian:
            return jsonify({'error': 'Librarian not found'}), 404
        if 'name' in data:
            librarian.name = data['name']
        db.session.commit()
        return jsonify({'message': 'Librarian updated successfully'})
    except SQLAlchemyError as e:
        return handle_database_error(e)

# Route to delete a librarian
@app.route('/librarian/<int:librarian_id>', methods=['DELETE'])
def delete_librarian(librarian_id):
    try:
        librarian = Librarian.query.get(librarian_id)
        if not librarian:
            return jsonify({'error': 'Librarian not found'}), 404
        db.session.delete(librarian)
        db.session.commit()
        return jsonify({'message': 'Librarian deleted successfully'})
    except SQLAlchemyError as e:
        return handle_database_error(e)

# Route to create a new wallet
@app.route('/wallet', methods=['POST'])
def create_wallet():
    data = request.json
    if 'balance' not in data:
        return jsonify({'error': 'Balance not provided'}), 400
    try:
        wallet = Wallet(balance=data['balance'])
        db.session.add(wallet)
        db.session.commit()
        return jsonify({'message': 'Wallet created successfully'}), 201
    except SQLAlchemyError as e:
        return handle_database_error(e)

# Route to get all wallets
@app.route('/wallet', methods=['GET'])
def get_wallets():
    wallets = Wallet.query.all()
    return jsonify([{
        'id': wallet.id,
        'balance': wallet.balance
    } for wallet in wallets])

# Route to update a wallet
@app.route('/wallet/<int:wallet_id>', methods=['PUT'])
def update_wallet(wallet_id):
    data = request.json
    try:
        wallet = Wallet.query.get(wallet_id)
        if not wallet:
            return jsonify({'error': 'Wallet not found'}), 404
        if 'balance' in data:
            wallet.balance = data['balance']
        db.session.commit()
        return jsonify({'message': 'Wallet updated successfully'})
    except SQLAlchemyError as e:
        return handle_database_error(e)

# Route to delete a wallet
@app.route('/wallet/<int:wallet_id>', methods=['DELETE'])
def delete_wallet(wallet_id):
    try:
        wallet = Wallet.query.get(wallet_id)
        if not wallet:
            return jsonify({'error': 'Wallet not found'}), 404
        db.session.delete(wallet)
        db.session.commit()
        return jsonify({'message': 'Wallet deleted successfully'})
    except SQLAlchemyError as e:
        return handle_database_error(e)


# Add your dummy data function
def add_dummy_data():
    # Add books
    book1 = Book(name="Book1", author="Author1", price=20, quantity=10, category="Fiction")
    book2 = Book(name="Book2", author="Author2", price=25, quantity=15, category="Non-fiction")
    db.session.add(book1)
    db.session.add(book2)

    # Add librarians
    librarian1 = Librarian(name="Book1")
    librarian2 = Librarian(name="Book2")
    db.session.add(librarian1)
    db.session.add(librarian2)

    # Add wallets
    wallet1 = Wallet(balance=100)
    wallet2 = Wallet(balance=150)
    db.session.add(wallet1)
    db.session.add(wallet2)

    # Commit changes
    db.session.commit()

# Add your routes and other application logic...

# Run the application if executed directly
if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Add dummy data
        add_dummy_data()

    # Run the Flask app
    app.run(debug=True)
