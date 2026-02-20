import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { OrganizationProvider } from './contexts/OrganizationContext'
import PrivateRoute from './components/PrivateRoute'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Projects from './pages/Projects'
import Tasks from './pages/Tasks'
import Billing from './pages/Billing'
import Analytics from './pages/Analytics'
import Layout from './components/Layout'

function App() {
  return (
    <AuthProvider>
      <OrganizationProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Layout />
              </PrivateRoute>
            }
          >
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="projects" element={<Projects />} />
            <Route path="tasks" element={<Tasks />} />
            <Route path="billing" element={<Billing />} />
            <Route path="analytics" element={<Analytics />} />
          </Route>
        </Routes>
      </OrganizationProvider>
    </AuthProvider>
  )
}

export default App
