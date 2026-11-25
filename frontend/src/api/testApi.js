import apiClient from './client'

export const checkBackendHealth = async () => {

    try {

        const response = await apiClient.get('/health')

        console.log('Backend Response:', response.data)

        return response.data

    } catch (error) {

        console.error('Backend Connection Failed:', error)

        throw error

    }

}