import React, { useState } from 'react';
import './styles/App.css';
import axios from "axios";

function App() {
  const [topic, setTopic] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [results, setResults] = useState([]);
  const [message, setMessage] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!topic || !difficulty) {
      setMessage("Please enter your topic and difficulty!");
      return;
    }
  
    try {
      const response = await axios.post("http://localhost:3000/learning_assistant", {
        topic,
        difficulty,
      }, {
        timeout: 20000 
      });

      setResults(response.data.results);
      setMessage("")

    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>Hi😊 I am your learning assistant!</h1>
        <p>Please enter the topic and difficulty you want to learn, and I will give you five related repositories in GitHub.</p>
      </header>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Topic: </label>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
        </div>
        <div>
          <label>Difficulty: </label>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
          >
            <option value="">Select Difficulty</option>
            <option value="Beginner">Beginner</option>
            <option value="Intermediate">Intermediate</option>
            <option value="Advanced">Advanced</option>
          </select>
        </div>
        <button type="submit">Submit</button>
      </form>
      {message && <p>{message}</p>}
      <br />
      <br />
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Stars⭐</th>
            <th>Justification</th>
            <th>URL</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result) => (
            <tr key={result.id}>
              <td>{result.name}</td>
              <td>{result.stars}</td>
              <td>{result.justification}</td>
              <td>
                <a href={result.url} target="_blank" rel="noopener noreferrer">
                  View Repository
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;


