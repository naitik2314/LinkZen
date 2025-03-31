import React from 'react';
import { PlusIcon } from 'lucide-react';
const Settings: React.FC = () => {
  return <div>
      <h1 className="text-2xl font-semibold text-gray-800 mb-6">Settings</h1>
      <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6 mb-6">
        <h2 className="text-lg font-medium text-gray-800 mb-4">
          Account Settings
        </h2>
        <div className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input type="email" id="email" defaultValue="user@example.com" className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500" />
          </div>
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
              Name
            </label>
            <input type="text" id="name" defaultValue="John Doe" className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500" />
          </div>
          <button className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors">
            Save Changes
          </button>
        </div>
      </div>
      <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
        <h2 className="text-lg font-medium text-gray-800 mb-4">
          Category Management
        </h2>
        <div className="space-y-3 mb-4">
          <div className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded-md">
            <span>Development</span>
            <button className="text-gray-400 hover:text-gray-600">Edit</button>
          </div>
          <div className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded-md">
            <span>Design</span>
            <button className="text-gray-400 hover:text-gray-600">Edit</button>
          </div>
          <div className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded-md">
            <span>Bookmarks</span>
            <button className="text-gray-400 hover:text-gray-600">Edit</button>
          </div>
        </div>
        <button className="flex items-center text-blue-500 hover:text-blue-600">
          <PlusIcon size={16} className="mr-1" />
          <span>Add New Category</span>
        </button>
      </div>
    </div>;
};
export default Settings;