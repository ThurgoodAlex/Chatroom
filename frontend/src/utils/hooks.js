import { useContext } from "react";
import { AuthContext } from "../context/auth.jsx";
import { UserContext } from "../context/user.jsx";
import api from "./api.js";

const useApi = () => {
  const { token } = useAuth();
  return api(token);
}

const useApiWithoutToken = () => {
  return api();
}

// custom hooks
const useAuth = () => useContext(AuthContext);
const useUser = () => useContext(UserContext);

export {
  useApi,
  useApiWithoutToken,
  useAuth,
  useUser,
};