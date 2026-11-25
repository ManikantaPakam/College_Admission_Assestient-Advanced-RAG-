import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router'
import { loginUser } from '../api/auth'
import { useAuth } from '../context/AuthContext'

function Login() {
    const navigate = useNavigate()
    const location = useLocation()

    const { login } = useAuth()

    const [showPassword, setShowPassword] = useState(false)
    const [message, setMessage] = useState(
        location.state?.message || ''
    )
    const [loading, setLoading] = useState(false)

    const handleLogin = async (event) => {
        event.preventDefault()

        const form = event.currentTarget
        const formData = new FormData(form)

        const email = formData.get('email')
        const password = formData.get('password')

        setMessage('')

        try {
            setLoading(true)

            const credentials = {
                email,
                password
            }

            const response = await loginUser(credentials)

            console.log('Login successful')

            login(response.access_token)

            navigate('/chat', {
                replace: true
            })

        } catch (error) {
            console.error('Login Error:', error)

            const detail = error.response?.data?.detail

            const errorMessage = Array.isArray(detail)
                ? detail.map(item => item.msg).join(', ')
                : detail || error.message || 'Login failed.'

            setMessage(errorMessage)

        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4">

            <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl">

                <h1 className="text-center text-3xl font-bold text-blue-600">
                    Welcome Back
                </h1>

                <p className="mt-2 text-center text-gray-500">
                    Login to your account
                </p>

                <form onSubmit={handleLogin} className="mt-8 space-y-5">

                    <div>
                        <label className="mb-2 block text-sm font-medium text-gray-700">
                            Email Address
                        </label>

                        <input
                            type="email"
                            name="email"
                            placeholder="Enter your email"
                            required
                            className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:border-blue-500"
                        />
                    </div>

                    <div>
                        <label className="mb-2 block text-sm font-medium text-gray-700">
                            Password
                        </label>

                        <input
                            type={showPassword ? 'text' : 'password'}
                            name="password"
                            placeholder="Enter your password"
                            required
                            className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:border-blue-500"
                        />

                        <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="mt-2 text-sm text-blue-600"
                        >
                            {showPassword ? 'Hide Password' : 'Show Password'}
                        </button>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full rounded-lg bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 disabled:opacity-50"
                    >
                        {loading ? 'Logging in...' : 'Login'}
                    </button>

                </form>

                {message && (
                    <p className="mt-4 text-center text-sm text-red-600">
                        {message}
                    </p>
                )}

                <p className="mt-6 text-center text-sm text-gray-600">
                    Don't have an account?

                    <Link
                        to="/register"
                        className="ml-2 font-semibold text-blue-600 hover:underline"
                    >
                        Register
                    </Link>
                </p>

            </div>
        </div>
    )
}

export default Login
