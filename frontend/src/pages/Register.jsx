import { useState } from 'react'
import { Link, useNavigate } from 'react-router'
import { registerUser } from '../api/auth'

function Register() {

    const navigate = useNavigate()

    const [showPassword, setShowPassword] = useState(false)
    const [message, setMessage] = useState('')
    const [loading, setLoading] = useState(false)

    const handleRegister = async (event) => {

        event.preventDefault()

        const form = event.currentTarget
        const formData = new FormData(form)

        const username = formData.get('username')
        const email = formData.get('email')
        const password = formData.get('password')
        const confirmPassword = formData.get('confirmPassword')

        setMessage('')

        if (password !== confirmPassword) {
            setMessage('Passwords do not match.')
            return
        }

        try {

            setLoading(true)

            const userData = {
                username,
                email,
                password
            }

            // Call FastAPI Register API
            await registerUser(userData)

            // Registration successful
            navigate('/login', {
                replace: true,
                state: {
                    message: 'Registration successful! Please login.'
                }
            })

        } catch (error) {

            const detail = error.response?.data?.detail

            const errorMessage = Array.isArray(detail)
                ? detail.map(item => item.msg).join(', ')
                : detail || 'Registration failed. Please try again.'

            setMessage(errorMessage)

        } finally {

            setLoading(false)

        }
    }

    return (

        <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4 py-8">

            <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl">

                <h1 className="text-center text-3xl font-bold text-blue-600">
                    Create Account
                </h1>

                <p className="mt-2 text-center text-gray-500">
                    Register to access your AI assistant
                </p>

                <form onSubmit={handleRegister} className="mt-8 space-y-5">

                    <div>
                        <label className="mb-2 block text-sm font-medium text-gray-700">
                            Username
                        </label>

                        <input
                            type="text"
                            name="username"
                            placeholder="Enter your username"
                            minLength={3}
                            maxLength={100}
                            required
                            className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:border-blue-500"
                        />
                    </div>

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
                            placeholder="Create password"
                            minLength={8}
                            maxLength={128}
                            required
                            className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:border-blue-500"
                        />
                    </div>

                    <div>
                        <label className="mb-2 block text-sm font-medium text-gray-700">
                            Confirm Password
                        </label>

                        <input
                            type={showPassword ? 'text' : 'password'}
                            name="confirmPassword"
                            placeholder="Confirm password"
                            minLength={8}
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
                        {loading ? 'Creating Account...' : 'Create Account'}
                    </button>

                </form>

                {message && (
                    <p className="mt-4 text-center text-sm text-red-600">
                        {message}
                    </p>
                )}

                <p className="mt-6 text-center text-sm text-gray-600">
                    Already have an account?

                    <Link
                        to="/login"
                        className="ml-2 font-semibold text-blue-600 hover:underline"
                    >
                        Login
                    </Link>
                </p>

            </div>

        </div>
    )
}

export default Register