import React, { useState, useEffect } from 'react';
import LinkCard from '../components/LinkCard';
import { SearchIcon, PlusIcon } from 'lucide-react';

interface LinkData {
  id: number;
  title: string;
  description: string;
  url: string;
  source: string;
  isFavorite: boolean;
}

const Dashboard: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [links, setLinks] = useState<LinkData[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/links')
      .then(response => response.json())
      .then(data => {
        // Map the API response to the format used by LinkCard.
        // API returns: id, url, category, subcategory, isFavorite, createdAt.
        // Here we use url as title, and a combination of category and subcategory as description.
        const mappedLinks = data.map((link: any) => ({
          id: link.id,
          title: link.short_description, // Change this title to short description of the link
          // description: `${link.category} - ${link.subcategory}`,
          description: link.description,
          url: link.url,
          source: link.category,
          isFavorite: link.isFavorite,
        }));
        setLinks(mappedLinks);
      })
      .catch(error => console.error('Error fetching links:', error));
  }, []);

  const filteredLinks = links.filter(link =>
    link.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    link.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-800">All Links</h1>
        <div className="relative">
          <input
            type="text"
            placeholder="Search links..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            className="pl-10 pr-4 py-2 border border-gray-200 rounded-md w-64 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
          <SearchIcon size={18} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredLinks.map(link => (
          <LinkCard
            key={link.id}
            title={link.title}
            description={link.description}
            url={link.url}
            source={link.source}
            isFavorite={link.isFavorite}
          />
        ))}
      </div>
      {filteredLinks.length === 0 && (
        <div className="text-center py-10">
          <p className="text-gray-500">
            No links found. Try a different search term.
          </p>
        </div>
      )}
      <button className="fixed bottom-6 right-6 md:hidden p-4 bg-blue-500 hover:bg-blue-600 text-white rounded-full shadow-lg">
        <PlusIcon size={24} />
      </button>
    </div>
  );
};

export default Dashboard;