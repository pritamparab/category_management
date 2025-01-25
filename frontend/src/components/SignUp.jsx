import { useState } from 'react';
import { Form, Input, Button, Message } from 'semantic-ui-react';
import './Main.css';
import { useNavigate } from 'react-router-dom';

const VITE_REACT_APP_SERVER = import.meta.env.VITE_REACT_APP_SERVER;

const SignUp = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(null);
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setSuccess(null);

        try {
            await signup(username, password, firstName, lastName, email);
            setLoading(false);
        } catch (err) {
            setError('An error occurred during signup');
            setLoading(false);
        }
    };

    const signup = async (username, password, firstName, lastName, email = '') => {
        const signupData = {
            username,
            password,
            first_name: firstName,
            last_name: lastName,
            email,
        };

        const response = await fetch(`${VITE_REACT_APP_SERVER}/signup/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(signupData),
        });

        const data = await response.json();
        if (response.ok) {
            setSuccess("User added successfully")
            setTimeout(() => {
                navigate('/login')
            }, 3000);
        }else{
            throw new Error(data.message || 'Failed to sign up');
        }
    };

    return (
        <div className='signup-form'>
        <Form onSubmit={handleSubmit} loading={loading} error={!!error}>
            <Form.Field>
                <label>Username</label>
                <Input
                    type="text"
                    placeholder="Enter username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
            </Form.Field>

            <Form.Field>
                <label>Password</label>
                <Input
                    type="password"
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
            </Form.Field>

            <Form.Field>
                <label>First Name</label>
                <Input
                    type="text"
                    placeholder="Enter first name"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    required
                />
            </Form.Field>

            <Form.Field>
                <label>Last Name</label>
                <Input
                    type="text"
                    placeholder="Enter last name"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    required
                />
            </Form.Field>

            <Form.Field>
                <label>Email (optional)</label>
                <Input
                    type="email"
                    placeholder="Enter email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </Form.Field>

            {success && <Message positive header="Signup success" content={success}/>}
            {error && <Message error header="Signup Error" content={error} />}

            <Form.Field>
                <label>
                    Already have an account?  &nbsp;
                    <a onClick={() => navigate('/login')} style={{cursor:'pointer'}}>Login</a>
                </label>
            </Form.Field>

            <Button primary type="submit">
                Sign Up
            </Button>
            
        </Form>
        </div>
    );
};

export default SignUp;
