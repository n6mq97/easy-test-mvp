import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import config from '../config';

const HomePage = () => {
    const [sections, setSections] = useState([]);
    const [jsonInput, setJsonInput] = useState('');

    useEffect(() => {
        fetch(`${config.API_BASE_URL}/api/sections/`)
            .then(response => response.json())
            .then(data => setSections(data));
    }, []);

    const handleJsonSubmit = () => {
        try {
            const tests = JSON.parse(jsonInput);
            fetch(`${config.API_BASE_URL}/api/tests/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(tests),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                setJsonInput('');
                // Refresh sections
                fetch(`${config.API_BASE_URL}/api/sections/`)
                    .then(response => response.json())
                    .then(data => setSections(data));
            });
        } catch (error) {
            console.error('Error parsing JSON:', error);
        }
    };

    return (
        <div>
            <h1>Easy Test</h1>
            <div>
                <h2>Add Tests (JSON)</h2>
                <textarea
                    rows="10"
                    cols="50"
                    value={jsonInput}
                    onChange={(e) => setJsonInput(e.target.value)}
                    placeholder='Paste JSON here'
                ></textarea>
                <br />
                <button onClick={handleJsonSubmit}>Add Tests</button>
            </div>
            <div>
                <h2>Sections</h2>
                <ul>
                    {sections.map(section => (
                        <li key={section.id}>
                            <Link to={`/test/${section.id}`}>{section.name}</Link>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default HomePage;
