import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import ChatsPage from './components/ChatsPage'
import ChatMessages from './components/ChatsPage'
import { Link } from 'react-router-dom';
import { AuthProvider } from "./context/auth";
import { UserProvider } from "./context/user";
import { useAuth } from "./utils/hooks.js";
import TopNav from "./components/TopNav";
import Login from "./components/Login";
import Registration from './components/Registration.jsx';
import Profile from './components/Profile.jsx';
import HomePage from './components/HomePage.jsx';


const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
}

function ErrorPage() {
  return (
    <>
      <h1>an error has occurred</h1>
      <p>contact site admin for support</p>
    </>
  );
}


function Home(){
  const { isLoggedIn, logout } = useAuth();
  return(
    <div className="max-w-4/5 mx-auto text-center px-4 py-8">
      <div className="py-2">
        logged in: {isLoggedIn.toString()}
      </div>
    </div>
  );

}

function Header() {
  return (
    <header>
      <TopNav />
    </header>
  );
}

function LoggedInRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ChatsPage />} />
      <Route path="/chats/:chatId" element={<ChatMessages />} />
      <Route path="/chats" element={<ChatsPage />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/register" element={<Registration />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}


function LoggedOutRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Registration />} />
      <Route path="*" element={<Login />} />
    </Routes>
  );
}

function Main() {
  const { isLoggedIn } = useAuth();

  return (
    <main className="max-h-main min-h-screen">
      {isLoggedIn ? 
      <LoggedInRoutes /> : 
      <LoggedOutRoutes />}
    </main>
  );
}

function App() {
  const className = [
    "h-100vh",
    "bg-gray-700 text-white",
    "flex flex-col",
  ].join(" ");

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <UserProvider>
            <div className={className}>
              <Header />
              <Main />
            </div>
          </UserProvider>
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App
