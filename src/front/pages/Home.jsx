import React, { useEffect } from "react"
import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const Home = () => {

	const { store, dispatch } = useGlobalReducer()

	const loadMessage = async () => {
		try {
			const backendUrl = import.meta.env.VITE_BACKEND_URL

			if (!backendUrl) throw new Error("VITE_BACKEND_URL is not defined in .env file")

			const response = await fetch(backendUrl + "/api/hello")
			const data = await response.json()

			if (response.ok) dispatch({ type: "set_hello", payload: data.message })

			return data

		} catch (error) {
			if (error.message) throw new Error(
				`Could not fetch the message from the backend.
				Please check if the backend is running and the backend port is public.`
			);
		}

	}

	useEffect(() => {
		loadMessage()
	}, [])

	return (
		<div className="text-center mt-5">
			<h1 className="display-4">Holaaa Ehiber , no me ha dado tiempo a hacer más cosas, hasta aqui llegué , valore usted si pasa esto por alto y me da el titulo </h1>
			<p className="lead">
				<img src={rigoImageUrl} className="img-fluid rounded-circle mb-3" alt="Rigo Baby" />
			</p>
			<div className="alert alert-info">
				{store.message ? (
					<span>Hola Ehiber</span>
				) : (
					<span className="text-danger">
						Arriba tienes el botón para loguearte,para loguearte , pincha en el backend y crea un usuario , hay uno por defecto , usuario : fillaux33@gmail.com contraseña : 123456 , una vez logueado , vuelve a esta página y recarga para ver el mensaje secreto que viene del backend , si no ves el mensaje es que algo ha ido mal , revisa la consola del navegador para más detalles
					</span>
				)}
			</div>
		</div>
	);
}; 