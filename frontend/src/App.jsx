import React from 'react';
import './App.css';
import {createBrowserRouter,RouterProvider} from 'react-router-dom';

// Import all components
import Home from './components/home/home';
import Login from './components/login/login';
import RootLayout from './RootLayout'
import Profile from './components/profile/profile';
import UserDetailsForm from './components/userDetailsForm/userDetailsForm';
import { UserLoginProvider } from './contexts/UserLoginContext';
import ProtectedRoute from './components/protectedRoute/protectedRoute';

function App() {
  const router=createBrowserRouter([
    {
      path:'/',
      element:<RootLayout/>,
      children:[
        {index:true,element:<Home/>},
        {path:"/login",element:<Login/>},
      ]
    },
    {
      element: <ProtectedRoute />,
      children: [
        {
          path: "/profile",
          element: <Profile />,
        },
        {
          path: "/user-details-form",
          element: <UserDetailsForm />,
        },
      ],
    }
  ])
  return (
    <UserLoginProvider>
        <RouterProvider router={router} />
    </UserLoginProvider>
  );
}

export default App;
