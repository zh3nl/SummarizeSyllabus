import './App.css';
import FileUploader from './components/FileUploader';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';

function App() {
  return (
    <div>
      <FileUploader />
    </div>
  );
}

export default App;
