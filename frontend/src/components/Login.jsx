import React, { useState, useEffect } from 'react';
import { useNavigate, useOutletContext } from 'react-router-dom';
import { FormField, Button, Form, Message } from 'semantic-ui-react'

const VITE_REACT_APP_SERVER = import.meta.env.VITE_REACT_APP_SERVER;

const Login = () => {
    const { cookies, setCookie, removeCookie } = useOutletContext()
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const loginURL = `${VITE_REACT_APP_SERVER}/login/`;
    const refreshURL = `${VITE_REACT_APP_SERVER}/login/refresh/`;

    const handleLogin = async(e) => {
        e.preventDefault();
        setError(null)
        try {
            const response = await fetch(loginURL, {
                method: 'POST',
                cors: 'no-cors',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            if (response.ok) {
                const data = await response.json();
                setCookie('token', data.access, {maxAge: 36000});
                setCookie('refreshToken', data.refresh, {maxAge: 70000});
                setCookie('username', data.username, {maxAge: 70000});
                navigate('/');
            } else {
                setError('Login failed. Check your credentials.')
            }
        } catch (error) {
            setError('Login failed, Please try again.');
        }
    };

    const refreshAccessToken = async () => {
        try {
            const response = await fetch(refreshURL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: cookies.refreshToken }),
            });
            if (response.ok) {
                const data = await response.json();
                setCookie('token', data.access, { path: '/' });
            } else {
                console.warn('Refresh token expired. Logging out.');
                handleLogout();
            }
        } catch (error) {
            console.error('Token refresh error:', error);
            handleLogout();
        }
    };

    const handleLogout = () => {
        removeCookie('token');
        removeCookie('refreshToken');
        navigate('/login');
    };

    useEffect(() => {
        if (cookies?.refreshToken) {
            const interval = setInterval(() => {
                refreshAccessToken();
            }, 14 * 60 * 1000);
            return () => clearInterval(interval);
        }
    }, [cookies?.refreshToken]);

    return (
    <div className='loginForm' size="huge">
        <Form onSubmit={handleLogin} error={!!error}>
            <FormField>
                <label>Username</label>
                <input
                type="text"
                placeholder="Enter username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                />
            </FormField>
            <FormField>
                <label>Last Name</label>
                <input
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                />
            </FormField>

            {error && <Message error header="Login Error" content={error} />}

            <FormField>
                <label>
                    Don't have an account?  &nbsp;
                    <a onClick={() => navigate('/signup')} style={{cursor:'pointer'}}>Signup</a>
                </label>
            </FormField>

            <Button type='submit' primary>Submit</Button>
        </Form>
    </div> 
    );
};

export default Login;
