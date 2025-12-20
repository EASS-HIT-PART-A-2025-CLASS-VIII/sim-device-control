import './App.css'
import {
  useState,
  type ComponentType,
} from 'react'
import DeviceList from './panels/device-list'
import TemperatureSensor from './panels/temperature-sensor'
import PressureSensor from './panels/pressure-sensor'
import HumiditySensor from './panels/humidity-sensor'
import DcMotor from './panels/dc-motor'
import StepperMotor from './panels/stepper-motor'
import LogViewer from './panels/log-viewer'
import {
  PanelType,
  deviceTypeOptions,
} from './panel-config'

type PanelComponent = ComponentType<Record<string, unknown>>

const DefaultPanel: PanelComponent = () => (
  <div>
    <h2>Select which panel to view from the "View Selector" on the left.</h2>
  </div>
)

function App() {
  const [selectedPanel, setSelectedPanel] = useState<PanelType | null>(null)

  let Panel: PanelComponent
  switch (selectedPanel) {
    case PanelType.DeviceList:
      Panel = DeviceList
      break
    case PanelType.TemperatureSensor:
      Panel = TemperatureSensor
      break
    case PanelType.PressureSensor:
      Panel = PressureSensor
      break
    case PanelType.HumiditySensor:
      Panel = HumiditySensor
      break
    case PanelType.DcMotor:
      Panel = DcMotor
      break
    case PanelType.StepperMotor:
      Panel = StepperMotor
      break
    case PanelType.Logs:
      Panel = LogViewer
      break
    default:
      Panel = DefaultPanel
  }

  return (
    <>
      <div className="container">

        <div className="left-side">

          <h1>View Selector</h1>

          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style=
                {{
                  textAlign: 'center',
                  borderBottom: '3px solid #e6e6e6',
                  padding: '8px',
                  fontSize: '20px',
                  }}>Operation Type</th>
                <th style=
                {{
                  textAlign: 'center',
                  borderBottom: '3px solid #e6e6e6',
                  padding: '8px',
                  fontSize: '20px',
                  }}>Operation Description</th>
              </tr>
            </thead>
            <tbody>
              {deviceTypeOptions.map((option) => (
                <tr
                  key={option.type}
                  onClick={() => setSelectedPanel(selectedPanel === option.type ? null : option.type)}
                  style={{
                    cursor: 'pointer',
                    background: selectedPanel === option.type ? '#f5f7ff' : 'transparent',
                    transition: 'background 0.15s'
                  }}
                >
                  <td style=
                  {{
                    borderBottom: '1px solid #f0f0f0',
                    padding: '8px',
                    color: selectedPanel === option.type ? '#000' : '#e6e6e6'
                    }}>{option.label}</td>
                  <td style=
                  {{
                    borderBottom: '1px solid #f0f0f0',
                    padding: '8px',
                    color: selectedPanel === option.type ? '#000' : '#e6e6e6'
                    }}>{option.description}</td>
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
