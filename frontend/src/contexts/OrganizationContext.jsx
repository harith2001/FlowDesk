import { createContext, useContext, useState, useEffect } from 'react'
import api from '../services/api'

const OrganizationContext = createContext(null)

export const useOrganization = () => {
  const context = useContext(OrganizationContext)
  if (!context) {
    throw new Error('useOrganization must be used within OrganizationProvider')
  }
  return context
}

export const OrganizationProvider = ({ children }) => {
  const [organizations, setOrganizations] = useState([])
  const [currentOrg, setCurrentOrg] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchOrganizations()
  }, [])

  const fetchOrganizations = async () => {
    try {
      setLoading(true)
      const response = await api.get('/organizations/organizations/')
      setOrganizations(response.data.results || response.data)
      if (response.data.results?.length > 0 || response.data.length > 0) {
        const orgs = response.data.results || response.data
        const savedSlug = localStorage.getItem('currentOrgSlug')
        const org = orgs.find((o) => o.slug === savedSlug) || orgs[0]
        setCurrentOrg(org)
        updateApiHeader(org.slug)
      }
    } catch (error) {
      console.error('Failed to fetch organizations:', error)
    } finally {
      setLoading(false)
    }
  }

  const updateApiHeader = (slug) => {
    if (slug) {
      api.defaults.headers.common['X-Organization-Slug'] = slug
      localStorage.setItem('currentOrgSlug', slug)
    }
  }

  const switchOrganization = (org) => {
    setCurrentOrg(org)
    updateApiHeader(org.slug)
  }

  const createOrganization = async (name, slug) => {
    try {
      const response = await api.post('/organizations/organizations/', {
        name,
        slug,
      })
      const newOrg = response.data
      setOrganizations([...organizations, newOrg])
      switchOrganization(newOrg)
      return { success: true, organization: newOrg }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || 'Failed to create organization',
      }
    }
  }

  return (
    <OrganizationContext.Provider
      value={{
        organizations,
        currentOrg,
        switchOrganization,
        createOrganization,
        fetchOrganizations,
        loading,
      }}
    >
      {children}
    </OrganizationContext.Provider>
  )
}
