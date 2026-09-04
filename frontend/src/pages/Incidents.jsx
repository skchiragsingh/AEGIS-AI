import { useNavigate } from "react-router-dom";

function Incidents() {
  const navigate = useNavigate();

  const incidents = [
    {
      id: "INC-001",
      title: "Database Connection Pool Exhausted",
      service: "user-service",
      severity: "CRITICAL",
      status: "INVESTIGATING",
      time: "2 minutes ago",
    },
    {
      id: "INC-002",
      title: "API Response Time Above Threshold",
      service: "api-gateway",
      severity: "HIGH",
      status: "OPEN",
      time: "8 minutes ago",
    },
    {
      id: "INC-003",
      title: "Memory Usage Threshold Exceeded",
      service: "analytics-service",
      severity: "MEDIUM",
      status: "RECOVERING",
      time: "15 minutes ago",
    },
  ];

  return (
    <>
      <header className="header">
        <div>
          <p className="breadcrumb">INCIDENT MANAGEMENT</p>
          <h2>Active Incidents</h2>
        </div>

        <div className="header-actions">
          <button className="notification">🔔</button>

          <div className="user-profile">
            <div className="avatar">A</div>

            <div>
              <strong>Administrator</strong>
              <span>AEGIS Control</span>
            </div>
          </div>
        </div>
      </header>

      <section className="dashboard">
        <div className="welcome">
          <div>
            <h2>Incident Command Center</h2>

            <p>
              Track detected incidents and follow their investigation and
              recovery progress.
            </p>
          </div>

          <button
            className="create-btn"
            onClick={() => navigate("/events")}
          >
            + Create Incident
          </button>
        </div>

        <div className="events-summary">
          <div className="event-summary-card">
            <p>Open Incidents</p>
            <h3>8</h3>
          </div>

          <div className="event-summary-card critical-summary">
            <p>Critical</p>
            <h3>2</h3>
          </div>

          <div className="event-summary-card">
            <p>Under Investigation</p>
            <h3>3</h3>
          </div>

          <div className="event-summary-card">
            <p>Recovery In Progress</p>
            <h3>1</h3>
          </div>
        </div>

        <div className="panel incidents-panel">
          <div className="panel-header">
            <div>
              <p className="panel-label">INCIDENT QUEUE</p>
              <h3>Detected Incidents</h3>
            </div>

            <button className="view-btn">
              Filter
            </button>
          </div>

          <div className="incident-table-wrapper">
            <table className="incidents-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>INCIDENT</th>
                  <th>SERVICE</th>
                  <th>SEVERITY</th>
                  <th>STATUS</th>
                  <th>DETECTED</th>
                  <th>ACTION</th>
                </tr>
              </thead>

              <tbody>
                {incidents.map((incident) => (
                  <tr key={incident.id}>
                    <td>
                      <span className="incident-id">
                        {incident.id}
                      </span>
                    </td>

                    <td>
                      <strong>{incident.title}</strong>
                    </td>

                    <td>
                      <span className="service-name">
                        {incident.service}
                      </span>
                    </td>

                    <td>
                      <span
                        className={`severity-badge ${incident.severity.toLowerCase()}`}
                      >
                        {incident.severity}
                      </span>
                    </td>

                    <td>
                      <span
                        className={`status-badge ${incident.status.toLowerCase()}`}
                      >
                        {incident.status}
                      </span>
                    </td>

                    <td>{incident.time}</td>

                    <td>
                      <button
                        className="investigate-btn"
                        onClick={() =>
                          navigate(
                            `/investigation?incident=${incident.id}`
                          )
                        }
                      >
                        Investigate →
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </>
  );
}

export default Incidents;