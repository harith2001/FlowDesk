import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'
import { useOrganization } from '../contexts/OrganizationContext'

const Dashboard = () => {
  const { currentOrg } = useOrganization()
  const [stats, setStats] = useState({
    activeProjects: 0,
    overdueProjects: 0,
    totalTasks: 0,
    completedTasks: 0,
    completionRate: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (currentOrg) {
      fetchStats()
    }
  }, [currentOrg])

  const fetchStats = async () => {
    try {
      setLoading(true)
      const [projectsRes, tasksRes] = await Promise.all([
        api.get('/analytics/active-projects/'),
        api.get('/analytics/task-completion-rate/'),
      ])
      setStats({
        activeProjects: projectsRes.data.active_projects || 0,
        overdueProjects: projectsRes.data.overdue_projects || 0,
        totalTasks: tasksRes.data.total_tasks || 0,
        completedTasks: tasksRes.data.completed_tasks || 0,
        completionRate: tasksRes.data.completion_rate || 0,
      })
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
      
      {!currentOrg && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <p className="text-yellow-800">
            Please create or select an organization to continue.
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Active Projects"
          value={stats.activeProjects}
          icon="📁"
          link="/projects"
        />
        <StatCard
          title="Overdue Projects"
          value={stats.overdueProjects}
          icon="⚠️"
          link="/projects"
          warning
        />
        <StatCard
          title="Total Tasks"
          value={stats.totalTasks}
          icon="✅"
          link="/tasks"
        />
        <StatCard
          title="Completion Rate"
          value={`${stats.completionRate.toFixed(1)}%`}
          icon="📊"
          link="/tasks"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <QuickActions />
        <RecentActivity />
      </div>
    </div>
  )
}

const StatCard = ({ title, value, icon, link, warning }) => (
  <Link
    to={link}
    className={`bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow ${
      warning ? 'border-l-4 border-yellow-500' : ''
    }`}
  >
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className={`text-2xl font-bold mt-2 ${warning ? 'text-yellow-600' : 'text-gray-900'}`}>
          {value}
        </p>
      </div>
      <span className="text-4xl">{icon}</span>
    </div>
  </Link>
)

const QuickActions = () => (
  <div className="bg-white rounded-lg shadow p-6">
    <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
    <div className="space-y-2">
      <Link
        to="/projects"
        className="block px-4 py-2 bg-primary-50 text-primary-700 rounded-md hover:bg-primary-100"
      >
        + Create New Project
      </Link>
      <Link
        to="/tasks"
        className="block px-4 py-2 bg-primary-50 text-primary-700 rounded-md hover:bg-primary-100"
      >
        + Create New Task
      </Link>
      <Link
        to="/billing"
        className="block px-4 py-2 bg-primary-50 text-primary-700 rounded-md hover:bg-primary-100"
      >
        + Create New Invoice
      </Link>
    </div>
  </div>
)

const RecentActivity = () => (
  <div className="bg-white rounded-lg shadow p-6">
    <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Activity</h2>
    <p className="text-gray-500 text-sm">No recent activity</p>
  </div>
)

export default Dashboard
