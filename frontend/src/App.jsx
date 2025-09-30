import React from 'react';
import './App.css';
import {createBrowserRouter,RouterProvider} from 'react-router-dom';

// Import all components
import Home from './components/home/home';
import Login from './components/login/login';
import RootLayout from './RootLayout'
import Profile from './components/profile/profile';
import UserDetailsForm from './components/userDetailsForm/userDetailsForm';
import ProtectedRoute from './components/protectedRoute/protectedRoute';
import UploadReport from './components/uploadReport/UploadReport.jsx';

//Contexts
import { UserLoginProvider } from './contexts/UserLoginContext';
import { ToastProvider } from './contexts/ToastContext.jsx';
import { SidebarProvider } from './contexts/SidebarContext.jsx';

function App() {

  const ReportsPage = () => <h1>Reports Content</h1>;
const DietPlansPage = () => <h1>Diet Plans Content</h1>;
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
       
            { path: "/reports/my", element: <ReportsPage /> },
            { path: "/reports/upload", element: <UploadReport /> },
            { path: "/reports/analysis", element: <ReportsPage /> },

            
            { path: "/diet-plans/generate", element: <DietPlansPage /> },
            { path: "/diet-plans/weekly", element: <DietPlansPage /> },
      ],
    }
  ])
  return (
    <UserLoginProvider>
      <ToastProvider>
        <SidebarProvider>
        <RouterProvider router={router} />
        </SidebarProvider>
        </ToastProvider>
    </UserLoginProvider>
  );
}

export default App;
