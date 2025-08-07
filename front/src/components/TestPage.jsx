import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import config from '../config';

const TestPage = () => {
    const { sectionId } = useParams();
    const navigate = useNavigate();
    const [questions, setQuestions] = useState([]);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [showResult, setShowResult] = useState(false);

    useEffect(() => {
        fetch(`${config.API_BASE_URL}/api/sections/${sectionId}/tests/`)
            .then(response => response.json())
            .then(data => setQuestions(data));
    }, [sectionId]);

    const handleAnswerClick = (answer) => {
        setSelectedAnswer(answer);
        setShowResult(true);
    };

    const handleNextQuestion = () => {
        setSelectedAnswer(null);
        setShowResult(false);
        if (currentQuestionIndex < questions.length - 1) {
            setCurrentQuestionIndex(currentQuestionIndex + 1);
        } else {
            navigate('/');
        }
    };

    if (questions.length === 0) {
        return <div>Loading...</div>;
    }

    const currentQuestion = questions[currentQuestionIndex];

    return (
        <div>
            <h1>{currentQuestion.text}</h1>
            <ul>
                {currentQuestion.answers.map(answer => {
                    const isCorrect = answer.is_correct;
                    const isSelected = selectedAnswer && selectedAnswer.id === answer.id;
                    let className = '';
                    if (showResult) {
                        if (isCorrect) {
                            className = 'correct';
                        } else if (isSelected) {
                            className = 'incorrect';
                        }
                    }
                    return (
                        <li
                            key={answer.id}
                            className={className}
                            onClick={() => !showResult && handleAnswerClick(answer)}
                        >
                            {answer.text}
                        </li>
                    );
                })}
            </ul>
            {showResult && (
                <button onClick={handleNextQuestion}>
                    {currentQuestionIndex < questions.length - 1 ? 'Next' : 'Finish'}
                </button>
            )}
        </div>
    );
};

export default TestPage;
