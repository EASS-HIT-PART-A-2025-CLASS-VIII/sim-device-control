import './App.css'
import { useState } from 'react'
import ReactComponent from './components/react'
import ViteComponent from './components/vite'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <div className="container">
      
      <div className="left-side">
          <h1>Left Side</h1>
          <h1>Vite + React</h1>
          <div className="card">
            <button onClick={() => setCount((count) => count + 1)}>
              count is {count}
            </button>
            <p>
              Edit <code>src/App.tsx</code> and save to test HMR
            </p>
          </div>
          <p className="read-the-docs">
            Click on the Vite and React logos to learn more
          </p>

      </div>
      <div className="right-side">
          <h1>Right Side</h1>

          {count % 2 === 0 ? <ReactComponent /> : <ViteComponent />}

      </div>
    </div>

      
    </>
  )
}

export default App
