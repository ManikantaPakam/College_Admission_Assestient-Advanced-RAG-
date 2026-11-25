import apiClient from './client'

// Registration API
export const registerUser = async (userData) => {
    const response = await apiClient.post(
        '/api/v1/auth/register',
        userData
    )

    return response.data
}

// Login API
export const loginUser = async (credentials) => {
    const response = await apiClient.post(
        '/api/v1/auth/login',
        credentials
    )

    return response.data
}