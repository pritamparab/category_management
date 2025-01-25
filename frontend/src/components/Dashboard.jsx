import { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { Dropdown, Tab, Table, TabPane } from 'semantic-ui-react';
const VITE_REACT_APP_SERVER = import.meta.env.VITE_REACT_APP_SERVER;

const RenderTable = ({type, data}) => {
    const [selectedCategory, setSelectedCategory] = useState('');
    const categories = [...new Set(data?.map((product) => product.category))];

    const categoryOptions = [
        { key: 'all', text: 'All Categories', value: '' },
        ...categories.map((category) => ({
            key: category,
            text: category,
            value: category,
        })),
    ];
    
    const filteredData = type === 'premium'
        ? data
        : selectedCategory
        ? data.filter((product) => product.category === selectedCategory)
        : data;

    const handleCategoryChange = (e, { value }) => {
        setSelectedCategory(value);
    };

    useEffect(() => {
        if (type === 'premium') {
            setSelectedCategory('');
        }
    }, [type]);

    return(
        <>
        {type === "products" && 
        <Dropdown
            placeholder="Select Category"
            fluid
            selection
            options={categoryOptions}
            onChange={handleCategoryChange}
            value={selectedCategory}
        />}
        <Table celled  inverted>
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
            {filteredData?.map((product) => (
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
    </Table>
    </>
    )
}

const Dashboard = () => {
    const { cookies } = useOutletContext()
    const [products, setProducts] = useState([]);
    const [premium, setPremium] = useState([])

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
            setProducts(data.accessible_products)
            if(data.premium_products){
                setPremium(data.premium_products)
            }
        })
        .catch((error) => console.error('Error fetching products:', error));
    }, []);

    return (
    <div style={{padding: '2rem'}}>
        {cookies.token ? 
            <Tab panes={[
                {
                    menuItem: 'Available products',
                    render: () => <TabPane>{products.length > 0 ? <RenderTable type="products" data={products}/> : 'No products available'}</TabPane>
                },
                {
                    menuItem: 'Premium products',
                    render: () => <TabPane>{premium.length > 0 ? <RenderTable type="premium" data={premium}/> : 'Premium products not available'}</TabPane>
                }
            ]}
            />:
            <h2>Login to see products</h2>
        }
    </div>
    );
};

export default Dashboard;