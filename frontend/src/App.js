import logo from './logo.svg';
import './App.css';
import Classifier from './index.jsx';
import Detector from './detector';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        
        {/* <div>
        <Classifier />
        </div> */}
        <div>
          <Detector/>
        </div>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
