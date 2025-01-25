import { useState, useEffect} from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { Menu, MenuItem } from 'semantic-ui-react';
import './Main.css'

const VITE_REACT_APP_SERVER = import.meta.env.VITE_REACT_APP_SERVER

const NavBar = ({cookies, setCookie, removeCookie}) => {
    const navigate = useNavigate()
    const [activeItem, setActiveItem] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userName, setUserName] = useState('Anynymous')

    const logoutURL = `${VITE_REACT_APP_SERVER}/logout/`

    useEffect(() => {
        if(cookies.token && cookies.username) {
          setIsLoggedIn(true);
          setUserName(cookies.username);
        }else {
            setIsLoggedIn(false);
        }
      }, [cookies.token, cookies.username]);

    const handleLogin = () => {
        navigate("/login");
    };
    
    const handleLogout = async () => {
        if (cookies.token) {
            await fetch(logoutURL, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    'Authorization': `Bearer ${cookies.refreshToken}`,
                 }
            });
            removeCookie("token");
            removeCookie("refreshToken");
            removeCookie("username");

            setIsLoggedIn(false);
            setUserName("Anonymous");
            navigate("/login");
        }
    };
    
    const handleLoginLogout = () => {
        if (isLoggedIn) {
            handleLogout();
        } else {
            handleLogin();
        }
    };

    return (
        <>
        <nav className='navbar-position'>
            <Menu stackable size='massive'>
                <MenuItem header>
                {isLoggedIn ? `Welcome, ${userName}` : 'Welcome, Guest'}
                </MenuItem>
                <Menu.Menu position="right">
                <MenuItem
                name={isLoggedIn ? 'logout' : 'login'}
                active={activeItem === (isLoggedIn ? 'logout' : 'login')}
                onClick={() => {
                    handleLoginLogout();
                    setActiveItem(isLoggedIn ? 'logout' : 'login');
                }}
                >
                    {isLoggedIn ? 'Logout' : 'Login'}
                </MenuItem>
                </Menu.Menu>
            </Menu>
        </nav>
        <Outlet context={{ cookies, setCookie, removeCookie }}/>
        </>
    );
};

export default NavBar;
