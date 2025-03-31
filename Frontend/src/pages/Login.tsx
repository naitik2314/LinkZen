import React from 'react';
interface LoginProps {
  onLogin: () => void;
}
const Login: React.FC<LoginProps> = ({
  onLogin
}) => {
  return <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-8 max-w-md w-full">
        <h1 className="text-2xl font-semibold text-gray-800 text-center mb-6">
          LinkCat
        </h1>
        <h2 className="text-lg text-gray-600 text-center mb-8">
          Sign in to your account
        </h2>
        <form onSubmit={e => {
        e.preventDefault();
        onLogin();
      }}>
          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input type="email" id="email" className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500" placeholder="you@example.com" required />
          </div>
          <div className="mb-6">
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input type="password" id="password" className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500" placeholder="••••••••" required />
          </div>
          <button type="submit" className="w-full py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors">
            Sign In
          </button>
        </form>
        <div className="mt-6 text-center">
          <a href="#" className="text-sm text-blue-500 hover:text-blue-600">
            Forgot password?
          </a>
        </div>
        <div className="mt-8 pt-6 border-t border-gray-200 text-center">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <a href="#" className="text-blue-500 hover:text-blue-600">
              Sign up
            </a>
          </p>
        </div>
      </div>
    </div>;
};
export default Login;