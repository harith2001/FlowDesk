import { useEffect, useState } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import api from '../services/api'
import { useOrganization } from '../contexts/OrganizationContext'

const Analytics = () => {
  const { currentOrg } = useOrganization()
  const [revenueData, setRevenueData] = useState([])
  const [productivityData, setProductivityData] = useState([])
  const [taskStats, setTaskStats] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (currentOrg) {
      fetchAnalytics()
    }
  }, [currentOrg])

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      const [revenueRes, productivityRes, taskRes] = await Promise.all([
        api.get('/analytics/revenue-per-month/'),
        api.get('/analytics/user-productivity/'),
        api.get('/analytics/task-completion-rate/'),
      ])
      
      setRevenueData(revenueRes.data || [])
      setProductivityData(productivityRes.data || [])
      setTaskStats(taskRes.data || {})
    } catch (error) {
      console.error('Failed to fetch analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  const formatRevenueData = revenueData.map(item => ({
    month: `${item.year}-${String(item.month).padStart(2, '0')}`,
    revenue: parseFloat(item.total) || 0,
  }))

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Analytics</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Task Completion Rate</h2>
          <div className="text-4xl font-bold text-primary-600">
            {taskStats.completion_rate?.toFixed(1) || 0}%
          </div>
          <div className="text-sm text-gray-600 mt-2">
            {taskStats.completed_tasks || 0} of {taskStats.total_tasks || 0} tasks completed
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">User Productivity</h2>
          {productivityData.length > 0 ? (
            <div className="space-y-2">
              {productivityData.slice(0, 5).map((item) => (
                <div key={item.user_id} className="flex justify-between">
                  <span className="text-sm text-gray-600">User #{item.user_id}</span>
                  <span className="text-sm font-medium">{item.completed_tasks} tasks</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-sm">No productivity data available</p>
          )}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Revenue Per Month</h2>
        {formatRevenueData.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={formatRevenueData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="revenue" stroke="#3b82f6" name="Revenue ($)" />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-gray-500 text-center py-8">No revenue data available</p>
        )}
      </div>
    </div>
  )
}

export default Analytics
