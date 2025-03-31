import React, { useState } from 'react';
import { BookmarkIcon, ClockIcon, HomeIcon, SettingsIcon, LogOutIcon, PlusIcon, CodeIcon, PaintbrushIcon, StarIcon } from 'lucide-react';
import NewLinkDialog from './NewLinkDialog';
interface SidebarProps {
  onNavigate: (page: string) => void;
  currentPage: string;
}
const Sidebar: React.FC<SidebarProps> = ({ onNavigate, currentPage }) => {
  const [isDialogOpen, setDialogOpen] = useState(false);

  const handleNewLinkClick = () => {
    setDialogOpen(true);
  };

  const handleSaveNewLink = (link: string) => {
    console.log("New link saved:", link);
    // ...add functionality to save the link as needed...
  };

  const categories = [
    { id: 'all', name: 'All', icon: <HomeIcon size={18} /> },
    { id: 'favorites', name: 'Favorites', icon: <StarIcon size={18} /> },
    { id: 'recent', name: 'Recent', icon: <ClockIcon size={18} /> },
    { id: 'development', name: 'Development', icon: <CodeIcon size={18} /> },
    { id: 'design', name: 'Design', icon: <PaintbrushIcon size={18} /> },
    { id: 'bookmarks', name: 'Bookmarks', icon: <BookmarkIcon size={18} /> }
  ];
  return (
    <>
      <aside className="w-64 bg-white border-r border-gray-200 p-4 flex flex-col h-full">
        <div className="flex items-center mb-8">
          <h1 className="text-xl font-semibold text-gray-800">LinkCat</h1>
        </div>
        <div className="mb-6">
          <button
            onClick={handleNewLinkClick}
            className="flex items-center justify-center w-full py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors"
          >
            <PlusIcon size={18} className="mr-2" />
            <span>Add New Link</span>
          </button>
        </div>
        <div className="mb-4">
          <h2 className="text-xs uppercase text-gray-500 font-semibold mb-2 px-2">
            Categories
          </h2>
          <nav>
            <ul>
              {categories.map(category => (
                <li key={category.id}>
                  <button
                    onClick={() =>
                      onNavigate(category.id === 'all' ? 'dashboard' : category.name)
                    }
                    className={`flex items-center w-full px-2 py-2 rounded-md mb-1 ${
                      (category.id === 'all'
                        ? currentPage === 'dashboard'
                        : currentPage === category.name)
                        ? 'bg-blue-50 text-blue-600'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <span className="mr-3">{category.icon}</span>
                    <span>{category.name}</span>
                  </button>
                </li>
              ))}
            </ul>
          </nav>
        </div>
        <div className="mt-auto">
          <h2 className="text-xs uppercase text-gray-500 font-semibold mb-2 px-2">Options</h2>
          <nav>
            <ul>
              <li>
                <button
                  onClick={() => onNavigate('settings')}
                  className={`flex items-center w-full px-2 py-2 rounded-md mb-1 ${currentPage === 'settings' ? 'bg-blue-50 text-blue-600' : 'text-gray-700 hover:bg-gray-100'}`}
                >
                  <SettingsIcon size={18} className="mr-3" />
                  <span>Settings</span>
                </button>
              </li>
              <li>
                <button className="flex items-center w-full px-2 py-2 rounded-md text-gray-700 hover:bg-gray-100">
                  <LogOutIcon size={18} className="mr-3" />
                  <span>Log Out</span>
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </aside>
      {isDialogOpen && (
        <NewLinkDialog
          onSave={handleSaveNewLink}
          onClose={() => setDialogOpen(false)}
        />
      )}
    </>
  );
};
export default Sidebar;