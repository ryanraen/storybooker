import * as React from 'react';
import { createRoot } from 'react-dom/client';
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider } from '@mui/material/styles';
import { BrowserRouter, Routes, Route } from "react-router";

import App from './pages/App';
import Dashboard from './pages/Dashboard';
import Generate from './pages/Generate'
import History from './pages/History'
import Examples from './pages/Examples'
import Login from './pages/Login'

import homeTheme from './themes/homeTheme';

const rootElement = document.getElementById('root');
const root = createRoot(rootElement);

root.render(
    <React.StrictMode>
        <ThemeProvider theme={homeTheme}>
            <CssBaseline />
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<App />} /> 
                    <Route path="login" element={<Login />} /> 
                    <Route path="dashboard" element={<Dashboard />}>
                        <Route index element={<Generate />} />
                        <Route path="generate" element={<Generate />} />
                        <Route path="history" element={<History />} />
                    </Route>
                    <Route path="/examples" element={<Examples />} />
                </Routes>
            </BrowserRouter>
        </ThemeProvider>
    </React.StrictMode>,
);
