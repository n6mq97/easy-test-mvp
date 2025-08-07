import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import TestPage from './components/TestPage';
import './App.css';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/test/:sectionId" element={<TestPage />} />
            </Routes>
        </Router>
    );
}

export default App;
