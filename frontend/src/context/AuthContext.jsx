import { createContext, useContext, useState } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {

    const [accessToken, setAccessToken] = useState(null)

    const login = (token) => {
        setAccessToken(token)
    }

    const logout = () => {
        setAccessToken(null)
    }

    const isAuthenticated = Boolean(accessToken)

    return (
        <AuthContext.Provider
            value={{
                accessToken,
                login,
                logout,
                isAuthenticated
            }}
        >
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    return useContext(AuthContext)
}