import React, { useState } from 'react';

const CreateWorkspace = () => {
  const [workspaceName, setWorkspaceName] = useState('');

  const handleCreateWorkspace = () => {
    // TODO: Implement workspace creation logic
    console.log(`Creating workspace: ${workspaceName}`);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="p-8 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Create a New Workspace</h2>
        <input
          type="text"
          placeholder="Enter workspace name"
          value={workspaceName}
          onChange={(e) => setWorkspaceName(e.target.value)}
          className="w-full px-3 py-2 mb-4 border border-gray-300 rounded-md"
        />
        <button
          onClick={handleCreateWorkspace}
          className="w-full px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600"
        >
          Create Workspace
        </button>
      </div>
    </div>
  );
};

export default CreateWorkspace;
