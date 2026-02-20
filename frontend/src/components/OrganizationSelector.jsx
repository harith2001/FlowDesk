import { useState } from 'react'
import { useOrganization } from '../contexts/OrganizationContext'

const OrganizationSelector = () => {
  const { organizations, currentOrg, switchOrganization, createOrganization } =
    useOrganization()
  const [showModal, setShowModal] = useState(false)
  const [showCreate, setShowCreate] = useState(false)
  const [newOrgName, setNewOrgName] = useState('')
  const [newOrgSlug, setNewOrgSlug] = useState('')

  const handleCreate = async (e) => {
    e.preventDefault()
    const result = await createOrganization(newOrgName, newOrgSlug)
    if (result.success) {
      setShowCreate(false)
      setNewOrgName('')
      setNewOrgSlug('')
    } else {
      alert(result.error?.detail || 'Failed to create organization')
    }
  }

  return (
    <>
      <div className="relative">
        <button
          onClick={() => setShowModal(!showModal)}
          className="px-4 py-2 bg-primary-50 text-primary-700 rounded-md text-sm font-medium hover:bg-primary-100"
        >
          {currentOrg?.name || 'Select Org'} ▼
        </button>
        {showModal && (
          <div className="absolute right-0 mt-2 w-64 bg-white rounded-md shadow-lg z-50 border">
            <div className="py-1">
              {organizations.map((org) => (
                <button
                  key={org.id}
                  onClick={() => {
                    switchOrganization(org)
                    setShowModal(false)
                  }}
                  className={`w-full text-left px-4 py-2 text-sm hover:bg-gray-100 ${
                    currentOrg?.id === org.id ? 'bg-primary-50 text-primary-700' : ''
                  }`}
                >
                  {org.name}
                </button>
              ))}
              <button
                onClick={() => {
                  setShowCreate(true)
                  setShowModal(false)
                }}
                className="w-full text-left px-4 py-2 text-sm text-primary-600 hover:bg-gray-100 border-t"
              >
                + Create New Organization
              </button>
            </div>
          </div>
        )}
      </div>

      {showCreate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96">
            <h2 className="text-xl font-bold mb-4">Create Organization</h2>
            <form onSubmit={handleCreate}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Name
                </label>
                <input
                  type="text"
                  value={newOrgName}
                  onChange={(e) => setNewOrgName(e.target.value)}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Slug
                </label>
                <input
                  type="text"
                  value={newOrgSlug}
                  onChange={(e) => setNewOrgSlug(e.target.value)}
                  className="w-full px-3 py-2 border rounded-md"
                  required
                />
              </div>
              <div className="flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreate(false)
                    setNewOrgName('')
                    setNewOrgSlug('')
                  }}
                  className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}

export default OrganizationSelector
