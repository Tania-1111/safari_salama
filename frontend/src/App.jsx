import { Routes, Route } from 'react-router-dom'
import PrivateRoute from './auth/PrivateRoute'
import Login from './pages/Login'
import Register from './pages/Register'
import GuardianDashboard from './pages/GuardianDashboard'
import AdminDashboard from './pages/AdminDashboard'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/guardian" element={
        <PrivateRoute>
          <GuardianDashboard />
        </PrivateRoute>
      } />
      <Route path="/admin" element={
        <PrivateRoute>
          <AdminDashboard />
        </PrivateRoute>
      } />
    </Routes>
  )
}

export default App
