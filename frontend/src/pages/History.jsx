function History() {
  const incidents = [
    {
      id: "INC-024",
      title: "Payment API Timeout",
      service: "payment-service",
      severity: "HIGH",
      status: "RESOLVED",
      recovery: "Restarted service",
      time: "Today, 14:32",
    },
    {
      id: "INC-023",
      title: "Memory Usage Threshold Exceeded",
      service: "analytics-service",
      severity: "MEDIUM",
      status: "RESOLVED",
      recovery: "Memory optimization",
      time: "Today, 11:18",
    },
    {
      id: "INC-022",
      title: "Database Replication Lag",
      service: "database-service",
      severity: "CRITICAL",
      status: "RESOLVED",
      recovery: "Failover initiated",
      time: "Yesterday",
    },
  ];

  return (
    <>
      <header className="header">
        <div>
          <p className="breadcrumb">INCIDENT RECORDS</p>
          <h2>Incident History</h2>
        </div>
      </header>

      <section className="dashboard">
        <div className="welcome">
          <div>
            <h2>Past Incidents</h2>

            <p>
              Review resolved incidents, recovery actions, and historical
              system behavior.
            </p>
          </div>
        </div>

        <div className="events-summary">
          <div className="event-summary-card">
            <p>Total Incidents</p>
            <h3>248</h3>
          </div>

          <div className="event-summary-card">
            <p>Resolved Automatically</p>
            <h3>64%</h3>
          </div>

          <div className="event-summary-card">
            <p>Average Recovery Time</p>
            <h3>8m</h3>
          </div>

          <div className="event-summary-card">
            <p>AI Confidence Avg.</p>
            <h3>84%</h3>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <div>
              <p className="panel-label">HISTORICAL RECORDS</p>
              <h3>Resolved Incidents</h3>
            </div>

            <button className="view-btn">
              Export History
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
                  <th>RECOVERY</th>
                  <th>STATUS</th>
                  <th>TIME</th>
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

                    <td>{incident.recovery}</td>

                    <td>
                      <span className="status-badge resolved">
                        {incident.status}
                      </span>
                    </td>

                    <td>{incident.time}</td>
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

export default History;