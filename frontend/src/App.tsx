import './App.css'
import { useState } from 'react'
import type { ComponentType } from 'react'
import { DeviceType } from './components/device-dependancies'
import TemperatureSensor from './components/temperature-sensor'
import PressureSensor from './components/pressure-sensor'
import HumiditySensor from './components/humidity-sensor'

const deviceTypeOptions = [
  { type: DeviceType.TemperatureSensor,
    label: 'Temperature Sensor',
    description: 'Temperature sensor device' },
  { type: DeviceType.PressureSensor,
    label: 'Pressure Sensor',
    description: 'Pressure sensor device' },
    { type: DeviceType.HumiditySensor,
    label: 'Humidity Sensor',
    description: 'Humidity sensor device' },
]

function App() {
  const [selectedDeviceType, setSelectedDeviceType] = useState<DeviceType | null>(null)

  let Panel: ComponentType<any>
  switch (selectedDeviceType) {
    case DeviceType.TemperatureSensor:
      Panel = TemperatureSensor
      break
    case DeviceType.PressureSensor:
      Panel = PressureSensor
      break
    case DeviceType.HumiditySensor:
      Panel = HumiditySensor
      break
    default:
      Panel = () => (
        <div>
          <h2>Select Operation from the Action Type Selector Panel</h2>
        </div>
      )
  }

  return (
    <>
      <div className="container">

        <div className="left-side">
          <h1>Action Type Selector</h1>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'center', borderBottom: '2px solid #e6e6e6', padding: '8px' }}>Operation Type</th>
                <th style={{ textAlign: 'center', borderBottom: '2px solid #e6e6e6', padding: '8px' }}>Operation Description</th>
              </tr>
            </thead>
            <tbody>
              {deviceTypeOptions.map((option) => (
                <tr
                  key={option.type}
                  onClick={() => setSelectedDeviceType(selectedDeviceType === option.type ? null : option.type)}
                  style={{
                    cursor: 'pointer',
                    background: selectedDeviceType === option.type ? '#f5f7ff' : 'transparent',
                    transition: 'background 0.15s'
                  }}
                >
                  <td style={{ borderBottom: '1px solid #f0f0f0', padding: '8px', color: selectedDeviceType === option.type ? '#000' : '#e6e6e6' }}>{option.label}</td>
                  <td style={{ borderBottom: '1px solid #f0f0f0', padding: '8px', color: selectedDeviceType === option.type ? '#000' : '#e6e6e6' }}>{option.description}</td>
                </tr>
              ))}
            </tbody>
          </table>

        </div>
        <div className="right-side">
          <h1>Control Panel</h1>

          <Panel />

        </div>
      </div>


    </>
  )
}

export default App
