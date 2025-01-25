import { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { Table } from 'semantic-ui-react';
const VITE_REACT_APP_SERVER = import.meta.env.VITE_REACT_APP_SERVER;

const Dashboard = () => {
    const { cookies } = useOutletContext()
    const [products, setProducts] = useState([]);

    useEffect(() => {
        fetch(`${VITE_REACT_APP_SERVER}/get_products/`,{
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${cookies.token}`,
                'Content-Type': 'application/json',
            },
        })
        .then((response) => response.json())
        .then((data) => {
            setProducts(data)
        })
        .catch((error) => console.error('Error fetching products:', error));
    }, []);

    return (
    <div style={{padding: '2rem'}}>
        <h2>{cookies.token && 'Products Available'}</h2>
        {cookies.token ? 
        <Table celled>
            <Table.Header>
                <Table.Row>
                <Table.HeaderCell>ID</Table.HeaderCell>
                <Table.HeaderCell>Title</Table.HeaderCell>
                <Table.HeaderCell>Price</Table.HeaderCell>
                <Table.HeaderCell>Description</Table.HeaderCell>
                <Table.HeaderCell>Category</Table.HeaderCell>
                <Table.HeaderCell>Image</Table.HeaderCell>
                </Table.Row>
            </Table.Header>

            <Table.Body>
                {products?.map((product) => (
                <Table.Row key={product.id}>
                    <Table.Cell>{product.id}</Table.Cell>
                    <Table.Cell>{product.title}</Table.Cell>
                    <Table.Cell>${product.price}</Table.Cell>
                    <Table.Cell>{product.description}</Table.Cell>
                    <Table.Cell>{product.category}</Table.Cell>
                    <Table.Cell>
                    <img
                        src={product.image_url}
                        alt={product.title}
                        style={{ width: '100px', height: 'auto' }}
                    />
                    </Table.Cell>
                </Table.Row>
                ))}
            </Table.Body>
        </Table>:
        <h2>Login to see products</h2>
        }
    </div>
    );
};

export default Dashboard;