import React from 'react';
import Sidebar from './Sidebar';
interface LayoutProps {
  children: React.ReactNode;
  onNavigate: (page: string) => void;
  currentPage: string;
}
const Layout: React.FC<LayoutProps> = ({
  children,
  onNavigate,
  currentPage
}) => {
  return <div className="flex h-screen bg-gray-50">
      <Sidebar onNavigate={onNavigate} currentPage={currentPage} />
      <main className="flex-1 overflow-y-auto p-6">{children}</main>
    </div>;
};
export default Layout;