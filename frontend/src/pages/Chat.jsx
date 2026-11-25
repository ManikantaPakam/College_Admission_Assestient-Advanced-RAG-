import { useState } from 'react'
import { useNavigate } from 'react-router'
import { useAuth } from '../context/AuthContext'
import apiClient from '../api/client'

function Chat() {
    const navigate = useNavigate()

    const { accessToken, logout } = useAuth()

    const [question, setQuestion] = useState('')
    const [messages, setMessages] = useState([])
    const [loading, setLoading] = useState(false)

    const handleLogout = () => {
        logout()
        navigate('/login', { replace: true })
    }

    const handleNewChat = () => {
        setMessages([])
        setQuestion('')
    }

    const handleSendMessage = async (event) => {
        event.preventDefault()

        if (!question.trim() || loading) return

        const userQuestion = question.trim()

        setMessages(prev => [
            ...prev,
            {
                role: 'user',
                content: userQuestion
            }
        ])

        setQuestion('')
        setLoading(true)

        try {
            const response = await apiClient.post(
                '/api/v1/chat',
                {
                    question: userQuestion
                },
                {
                    headers: {
                        Authorization: `Bearer ${accessToken}`
                    }
                }
            )

            setMessages(prev => [
                ...prev,
                {
                    role: 'assistant',
                    content: response.data.answer,
                    sources: response.data.sources || []
                }
            ])

        } catch (error) {
            console.error('Chat API Error:', error)

            const detail = error.response?.data?.detail

            setMessages(prev => [
                ...prev,
                {
                    role: 'assistant',
                    content: Array.isArray(detail)
                        ? detail.map(item => item.msg).join(', ')
                        : detail || 'Unable to get an answer. Please try again.'
                }
            ])

        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="flex h-screen bg-slate-950 text-white">

            {/* Sidebar */}
            <aside className="hidden w-64 flex-col border-r border-slate-800 bg-slate-900 p-5 md:flex">

                <h1 className="text-xl font-bold text-blue-400">
                    Admission AI
                </h1>

                <button
                    onClick={handleNewChat}
                    className="mt-8 rounded-lg bg-blue-600 px-4 py-3 text-sm font-semibold hover:bg-blue-700"
                >
                    + New Chat
                </button>

                <div className="mt-auto">
                    <button
                        onClick={handleLogout}
                        className="w-full rounded-lg border border-red-500 px-4 py-3 text-red-400 hover:bg-red-500 hover:text-white"
                    >
                        Logout
                    </button>
                </div>

            </aside>

            {/* Main Chat Area */}
            <main className="flex flex-1 flex-col">

                {/* Header */}
                <header className="flex items-center justify-between border-b border-slate-800 px-6 py-5">

                    <div>
                        <h2 className="text-lg font-semibold">
                            College Admission Assistant
                        </h2>

                        <p className="text-xs text-slate-400">
                            AI-powered admission support
                        </p>
                    </div>

                    <button
                        onClick={handleLogout}
                        className="rounded-lg bg-red-600 px-4 py-2 text-sm md:hidden"
                    >
                        Logout
                    </button>

                </header>

                {/* Messages */}
                <section className="flex-1 overflow-y-auto px-4 py-8 md:px-12">

                    {messages.length === 0 && (
                        <div className="flex h-full flex-col items-center justify-center text-center">

                            <h2 className="text-3xl font-bold">
                                Welcome to Admission AI
                            </h2>

                            <p className="mt-4 max-w-lg text-slate-400">
                                Ask questions about college admissions,
                                eligibility, courses, fees and application procedures.
                            </p>

                            <div className="mt-8 grid gap-3 text-sm md:grid-cols-2">

                                <div className="rounded-xl border border-slate-700 p-4">
                                    What are the admission requirements?
                                </div>

                                <div className="rounded-xl border border-slate-700 p-4">
                                    What documents are required?
                                </div>

                                <div className="rounded-xl border border-slate-700 p-4">
                                    Explain the eligibility criteria.
                                </div>

                                <div className="rounded-xl border border-slate-700 p-4">
                                    What are the available courses?
                                </div>

                            </div>

                        </div>
                    )}

                    <div className="mx-auto max-w-4xl space-y-6">

                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={`flex ${
                                    message.role === 'user'
                                        ? 'justify-end'
                                        : 'justify-start'
                                }`}
                            >
                                <div
                                    className={`max-w-[85%] rounded-2xl p-4 ${
                                        message.role === 'user'
                                            ? 'bg-blue-600'
                                            : 'bg-slate-800'
                                    }`}
                                >

                                    <p className="whitespace-pre-wrap text-sm leading-7">
                                        {message.content}
                                    </p>

                                    {message.sources?.length > 0 && (
                                        <div className="mt-4 border-t border-slate-600 pt-3">

                                            <h4 className="mb-2 text-xs font-semibold text-blue-300">
                                                Sources
                                            </h4>

                                            {message.sources.map((source, sourceIndex) => (
                                                <p
                                                    key={sourceIndex}
                                                    className="mb-1 text-xs text-slate-300"
                                                >
                                                    {typeof source === 'string'
                                                        ? source
                                                        : source.source || source.filename || JSON.stringify(source)}
                                                </p>
                                            ))}

                                        </div>
                                    )}

                                </div>
                            </div>
                        ))}

                        {loading && (
                            <div className="text-sm text-slate-400">
                                Admission AI is thinking...
                            </div>
                        )}

                    </div>

                </section>

                {/* Message Input */}
                <footer className="border-t border-slate-800 p-4 md:px-12">

                    <form
                        onSubmit={handleSendMessage}
                        className="mx-auto flex max-w-4xl gap-3"
                    >

                        <input
                            type="text"
                            value={question}
                            onChange={(event) => setQuestion(event.target.value)}
                            placeholder="Ask your admission-related question..."
                            className="flex-1 rounded-xl border border-slate-700 bg-slate-900 px-5 py-4 text-sm outline-none focus:border-blue-500"
                        />

                        <button
                            type="submit"
                            disabled={loading || !question.trim()}
                            className="rounded-xl bg-blue-600 px-6 font-semibold hover:bg-blue-700 disabled:opacity-50"
                        >
                            Send
                        </button>

                    </form>

                    <p className="mt-3 text-center text-xs text-slate-500">
                        College Admission AI Assistant
                    </p>

                </footer>

            </main>

        </div>
    )
}

export default Chat