import { createContext, useContext, useState } from "react";

const getToken = () => sessionStorage.getItem("pony_express_token");
const storeToken = (token) => sessionStorage.setItem("pony_express_token", token);
const clearToken = () => sessionStorage.removeItem("pony_express_token");

const AuthContext = createContext();

function AuthProvider({ children }) {
    const [token, setToken] = useState(getToken());
  
    const login = (tokenData) => {
      setToken(tokenData.access_token);
      storeToken(tokenData.access_token);
    };
  
    const logout = () => {
      setToken(null);
      clearToken();
    };
  
    const isLoggedIn = !!token;
  
    const contextValue = {
      login,
      token,
      isLoggedIn,
      logout,
    };
  
    return (
      <AuthContext.Provider value={contextValue}>
        {children}
      </AuthContext.Provider>
    );
  }
  
  
  export { AuthContext, AuthProvider };