import React from 'react';
import { ExternalLinkIcon, StarIcon } from 'lucide-react';
interface LinkCardProps {
  title: string;
  description: string;
  url: string;
  source: string;
  isFavorite?: boolean;
}
const LinkCard: React.FC<LinkCardProps> = ({
  title,
  description,
  url,
  source,
  isFavorite = false
}) => {
  return <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-lg font-medium text-gray-900">{title}</h3>
        <button className={`p-1 rounded-full ${isFavorite ? 'text-yellow-500' : 'text-gray-300 hover:text-gray-400'}`}>
          <StarIcon size={18} fill={isFavorite ? 'currentColor' : 'none'} />
        </button>
      </div>
      <p className="text-gray-600 text-sm mb-3">{description}</p>
      <div className="flex items-center justify-between">
        <span className="text-xs text-gray-500">{source}</span>
        <a href={url} target="_blank" rel="noopener noreferrer" className="flex items-center text-blue-500 text-sm hover:text-blue-600">
          Visit <ExternalLinkIcon size={14} className="ml-1" />
        </a>
      </div>
    </div>;
};
export default LinkCard;