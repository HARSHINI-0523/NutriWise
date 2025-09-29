import React from 'react';
import './App.css';
import {createBrowserRouter,RouterProvider} from 'react-router-dom';

// Import all components
import Home from './components/home/home';
import Login from './components/login/login';
import RootLayout from './RootLayout'
import Profile from './components/profile/profile';
import { UserLoginProvider } from './contexts/UserLoginContext';

function App() {
  const router=createBrowserRouter([
    {
      path:'/',
      element:<RootLayout/>,
      children:[
        {index:true,element:<Home/>},
        {path:"/login",element:<Login/>},
        { path: "/profile", element: <Profile /> } 
      ]
    }
  ])
  return (
    <UserLoginProvider>
        <RouterProvider router={router} />
    </UserLoginProvider>
  );
}

export default App;
