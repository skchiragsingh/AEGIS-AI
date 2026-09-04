function Events() {
  const events = [
    {
      id: 1,
      source: "Prometheus",
      eventType: "High CPU Usage",
      severity: "HIGH",
      message: "CPU usage exceeded the configured threshold of 90%.",
      service: "payment-service",
      time: "2 minutes ago",
    },
    {
      id: 2,
      source: "Application Logs",
      eventType: "Database Error",
      severity: "CRITICAL",
      message: "Database connection pool exhausted.",
      service: "user-service",
      time: "5 minutes ago",
    },
    {
      id: 3,
      source: "Manual",
      eventType: "Memory Warning",
      severity: "MEDIUM",
      message: "Memory usage is approaching the configured limit.",
      service: "analytics-service",
      time: "12 minutes ago",
    },
  ];

  return (
    <>
      <header className="header">
        <div>
          <p className="breadcrumb">MONITORING</p>
          <h2>System Events</h2>
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
            <h2>Incoming System Events</h2>
            <p>
              Monitor events collected from applications, logs,
              monitoring tools, and manual reports.
            </p>
          </div>

          <button className="create-btn">
            + Add Test Event
          </button>
        </div>

        <div className="events-summary">
          <div className="event-summary-card">
            <p>Total Events</p>
            <h3>1,248</h3>
          </div>

          <div className="event-summary-card critical-summary">
            <p>Critical Events</p>
            <h3>4</h3>
          </div>

          <div className="event-summary-card">
            <p>High Priority</p>
            <h3>12</h3>
          </div>

          <div className="event-summary-card">
            <p>Sources Connected</p>
            <h3>5</h3>
          </div>
        </div>

        <div className="panel events-panel">
          <div className="panel-header">
            <div>
              <p className="panel-label">LIVE EVENT STREAM</p>
              <h3>Recent Events</h3>
            </div>

            <button className="view-btn">Refresh</button>
          </div>

          <div className="events-table-wrapper">
            <table className="events-table">
              <thead>
                <tr>
                  <th>EVENT</th>
                  <th>SOURCE</th>
                  <th>SERVICE</th>
                  <th>SEVERITY</th>
                  <th>TIME</th>
                </tr>
              </thead>

              <tbody>
                {events.map((event) => (
                  <tr key={event.id}>
                    <td>
                      <strong>{event.eventType}</strong>
                      <span className="event-message">
                        {event.message}
                      </span>
                    </td>

                    <td>{event.source}</td>

                    <td>
                      <span className="service-name">
                        {event.service}
                      </span>
                    </td>

                    <td>
                      <span
                        className={`severity-badge ${event.severity.toLowerCase()}`}
                      >
                        {event.severity}
                      </span>
                    </td>

                    <td>{event.time}</td>
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

export default Events;