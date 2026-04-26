from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ryx123'
app.config['MYSQL_DB'] = 'shoes_catalog'

mysql = MySQL(app)


@app.route('/products', methods=['GET'])
def get_products():
    q = request.args.get('q', '')
    cur = mysql.connection.cursor()
    if q:
        cur.execute("""
            SELECT * FROM products
            ORDER BY CASE WHEN name LIKE %s THEN 0 ELSE 1 END, name
        """, (q + '%',))
    else:
        cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    cur.close()
    return jsonify([{
        'id': r[0], 'name': r[1], 'description': r[2],
        'price': float(r[3]), 'image_url': r[4]
    } for r in rows])


@app.route('/products', methods=['POST'])
def add_product():
    d = request.get_json()
    if not d:
        return jsonify({'error': 'No data provided'}), 400

    name        = d.get('name', '').strip()
    description = d.get('description', '').strip()
    price       = d.get('price')
    image_url   = d.get('image_url', '').strip()

    if not name or not description or not image_url:
        return jsonify({'error': 'All fields are required'}), 400
    if not price or float(price) <= 0:
        return jsonify({'error': 'Price must be positive'}), 400

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO products (name, description, price, image_url) VALUES (%s,%s,%s,%s)",
        (name, description, float(price), image_url)
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Product added'}), 201


if __name__ == '__main__':
    app.run(debug=True)