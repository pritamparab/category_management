import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useCookies } from 'react-cookie';
import Dashboard from './components/Dashboard';
import SignUp from './components/SignUp';
import Login from './components/Login';
import NavBar from './components/NavBar';

const App = () => {
    const [cookies, setCookie, removeCookie] = useCookies(['username', 'token', 'refreshToken']);

    return (
        <Router>
            <Routes>
                <Route element={<NavBar cookies={cookies} setCookie={setCookie} removeCookie={removeCookie}/>}>
                <Route exact path="/" element={<Dashboard />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/login" element={<Login/>} />
                </Route>
            </Routes>
        </Router>
    );
};

export default App;