import { Routes, Route, Navigate } from 'react-router'

import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Chat from './pages/Chat'

import ProtectedRoute from './routes/ProtectedRoute'

function App() {

    return (

        <Routes>

            <Route path="/" element={<Home />} />

            <Route path="/login" element={<Login />} />

            <Route path="/register" element={<Register />} />

            <Route element={<ProtectedRoute />}>

                <Route path="/chat" element={<Chat />} />

            </Route>

            <Route path="*" element={<Navigate to="/" replace />} />

        </Routes>

    )
}

export default App