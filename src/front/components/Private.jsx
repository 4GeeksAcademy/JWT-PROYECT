import { Navigate } from "react-router-dom";

function Private({ children }) {
  // Verificamos si el usuario está logueado
  const user = JSON.parse(localStorage.getItem("user"));

  if (!user || !user.loggedIn) {
    // Si no está logueado, redirige al login
    return <Navigate to="/login" />;
  }

  return <>{children}</>; // Renderiza contenido privado
}

export default Private;
