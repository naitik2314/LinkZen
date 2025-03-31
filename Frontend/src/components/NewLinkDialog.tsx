import React, { useState } from 'react';

interface NewLinkDialogProps {
  onSave: (link: string) => void;
  onClose: () => void;
}

const NewLinkDialog: React.FC<NewLinkDialogProps> = ({ onSave, onClose }) => {
  const [link, setLink] = useState('');

  const handleSave = () => {
    onSave(link);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-lg font-semibold mb-4">Add New Link</h2>
        <input
          type="text"
          value={link}
          onChange={(e) => setLink(e.target.value)}
          placeholder="Enter new link"
          className="w-full mb-4 px-3 py-2 border rounded-md"
        />
        <div className="flex justify-end space-x-2">
          <button onClick={onClose} className="px-4 py-2 bg-gray-300 rounded-md">
            Cancel
          </button>
          <button onClick={handleSave} className="px-4 py-2 bg-blue-500 text-white rounded-md">
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default NewLinkDialog;
