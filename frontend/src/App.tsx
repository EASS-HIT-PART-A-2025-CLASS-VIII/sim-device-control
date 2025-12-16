import './App.css'
import { useState } from 'react'
import type { ComponentType } from 'react'
import TemperatureSensor from './components/temperature-sensor'

function App() {
  const [count, setCount] = useState(0)

  let Panel: ComponentType<any>
  switch (count % 2) {
    case 0:
      Panel = TemperatureSensor
      break
    default:
      Panel = TemperatureSensor
  }

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

          <Panel />

        </div>
      </div>


    </>
  )
}

export default App
