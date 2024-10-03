import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const ProductList = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/api/products')
      .then(response => setProducts(response.data))
      .catch(error => console.error('Error fetching products:', error));
  }, []);

  return (
    <div>
      <h2>Our Products</h2>
      {products.map(product => (
        <div key={product.id}>
          <h3>{product.name}</h3>
          <p>{product.description}</p>
          <p>Price: ${product.price}</p>
          <p>In Stock: {product.stock}</p>
        </div>
      ))}
    </div>
  );
};

const OrderForm = () => {
  const [order, setOrder] = useState({
    user_id: 1,
    product_id: '',
    quantity: 1,
    total_price: 0
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    axios.post('http://localhost:5000/api/orders', order)
      .then(response => alert('Order placed successfully!'))
      .catch(error => console.error('Error placing order:', error));
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Place an Order</h2>
      <div>
        <label>Product ID:
          <input 
            type="number" 
            value={order.product_id} 
            onChange={e => setOrder({...order, product_id: e.target.value})}
          />
        </label>
      </div>
      <div>
        <label>Quantity:
          <input 
            type="number" 
            value={order.quantity} 
            onChange={e => setOrder({...order, quantity: e.target.value})}
          />
        </label>
      </div>
      <button type="submit">Place Order</button>
    </form>
  );
};

function App() {
  return (
    <div className="App">
      <h1>Sweet Store</h1>
      <ProductList />
      <OrderForm />
    </div>
  );
}

export default App;