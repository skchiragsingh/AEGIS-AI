import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const savedUser = localStorage.getItem("aegis_user");

    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (error) {
        console.error("Failed to load user:", error);
      }
    }
  }, []);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/metrics/latest"
        );

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const result = await response.json();

        if (result.status === "success") {
          setMetrics(result.data);
          setLastUpdated(new Date());
        }
      } catch (error) {
        console.error("Failed to fetch system metrics:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();

    const interval = setInterval(fetchMetrics, 10000);

    return () => clearInterval(interval);
  }, []);

  const processes = metrics?.processes || [];

  const topProcesses = [...processes]
    .sort(
      (a, b) =>
        (b.cpu_usage || 0) - (a.cpu_usage || 0)
    )
    .slice(0, 8);

  const processChanges = metrics?.process_changes || {
    started: [],
    stopped: [],
  };

  const userName = user?.name || "Administrator";
  const userEmail = user?.email || "AEGIS Control";
  const userInitial = userName.charAt(0).toUpperCase();

  return (
    <>
      <header className="header">
        <div>
          <p className="breadcrumb">OVERVIEW</p>
          <h2>System Command Center</h2>
        </div>

        <div className="header-actions">
          <button className="notification">
            🔔
          </button>

          <div className="user-profile">
            <div className="avatar">
              {userInitial}
            </div>

            <div>
              <strong>{userName}</strong>
              <span>{userEmail}</span>
            </div>
          </div>
        </div>
      </header>

      <section className="dashboard">

        <div className="welcome">
          <div>
            <h2>System Overview</h2>

            <p>
              Monitor your system, applications, processes,
              incidents, and AEGIS activity from one place.
            </p>

            {lastUpdated && (
              <small>
                Last updated:{" "}
                {lastUpdated.toLocaleTimeString()}
              </small>
            )}
          </div>

          <button
            className="create-btn"
            onClick={() => navigate("/events")}
          >
            + Create Incident
          </button>
        </div>


        <div className="stats-grid">

          <div className="stat-card">
            <div className="stat-icon">⚙</div>

            <div>
              <p>CPU Usage</p>

              <h3>
                {metrics
                  ? `${metrics.cpu_usage}%`
                  : "--"}
              </h3>

              <span className="neutral">
                {metrics
                  ? "Live system usage"
                  : "Loading metrics..."}
              </span>
            </div>
          </div>


          <div className="stat-card">
            <div className="stat-icon">◉</div>

            <div>
              <p>Memory Usage</p>

              <h3>
                {metrics
                  ? `${metrics.memory_usage}%`
                  : "--"}
              </h3>

              <span className="neutral">
                {metrics
                  ? "Live system usage"
                  : "Loading metrics..."}
              </span>
            </div>
          </div>


          <div className="stat-card">
            <div className="stat-icon">▣</div>

            <div>
              <p>Disk Usage</p>

              <h3>
                {metrics
                  ? `${metrics.disk_usage}%`
                  : "--"}
              </h3>

              <span className="neutral">
                {metrics
                  ? "Live system usage"
                  : "Loading metrics..."}
              </span>
            </div>
          </div>


          <div className="stat-card">
            <div className="stat-icon">▤</div>

            <div>
              <p>Running Processes</p>

              <h3>
                {metrics
                  ? processes.length
                  : "--"}
              </h3>

              <span className="success">
                {metrics
                  ? "Processes detected"
                  : "Waiting for agent..."}
              </span>
            </div>
          </div>

        </div>


        <div className="content-grid">

          <div className="panel">

            <div className="panel-header">
              <div>
                <p className="panel-label">
                  PROCESS MONITORING
                </p>

                <h3>
                  Top CPU Processes
                </h3>
              </div>
            </div>


            <div className="incident-list">

              {loading && (
                <div className="incident-row">
                  <div className="incident-info">
                    <strong>
                      Loading process telemetry...
                    </strong>
                  </div>
                </div>
              )}


              {!loading &&
                topProcesses.length === 0 && (
                  <div className="incident-row">
                    <div className="incident-info">
                      <strong>
                        No process data available
                      </strong>

                      <span>
                        Make sure the AEGIS Agent is running.
                      </span>
                    </div>
                  </div>
                )}


              {topProcesses.map((process) => (
                <div
                  className="incident-row"
                  key={`${process.pid}-${process.name}`}
                >
                  <div className="incident-indicator info-line"></div>

                  <div className="incident-info">
                    <strong>
                      {process.name || "Unknown Process"}
                    </strong>

                    <span>
                      PID {process.pid} · {process.status}
                    </span>
                  </div>

                  <span className="badge medium-badge">
                    CPU {process.cpu_usage ?? 0}%
                  </span>
                </div>
              ))}

            </div>

          </div>


          <div className="panel activity-panel">

            <div className="panel-header">
              <div>
                <p className="panel-label">
                  PROCESS EVENTS
                </p>

                <h3>
                  Recent Changes
                </h3>
              </div>
            </div>


            <div className="pipeline">

              {processChanges.started?.length > 0 && (
                <>
                  <div className="pipeline-item completed">

                    <span>+</span>

                    <div>
                      <strong>
                        Processes Started
                      </strong>

                      <p>
                        {processChanges.started.length} new process
                        {processChanges.started.length !== 1
                          ? "es"
                          : ""}
                      </p>
                    </div>

                  </div>

                  <div className="pipeline-line"></div>
                </>
              )}


              {processChanges.stopped?.length > 0 && (
                <>
                  <div className="pipeline-item completed">

                    <span>−</span>

                    <div>
                      <strong>
                        Processes Stopped
                      </strong>

                      <p>
                        {processChanges.stopped.length} process
                        {processChanges.stopped.length !== 1
                          ? "es"
                          : ""}
                      </p>
                    </div>

                  </div>

                  <div className="pipeline-line"></div>
                </>
              )}


              {(!processChanges.started ||
                processChanges.started.length === 0) &&
                (!processChanges.stopped ||
                  processChanges.stopped.length === 0) && (
                  <div className="pipeline-item active-pipeline">

                    <span>✓</span>

                    <div>
                      <strong>
                        System Stable
                      </strong>

                      <p>
                        No process changes detected
                      </p>
                    </div>

                  </div>
                )}

            </div>

          </div>

        </div>


        <div className="panel">

          <div className="panel-header">
            <div>
              <p className="panel-label">
                DEVICE
              </p>

              <h3>
                Monitored System
              </h3>
            </div>
          </div>


          <div className="incident-list">

            <div className="incident-row">

              <div className="incident-indicator info-line"></div>

              <div className="incident-info">

                <strong>
                  {metrics?.hostname || "Unknown Device"}
                </strong>

                <span>
                  {metrics?.os || "Waiting for agent"}

                  {metrics?.os_version
                    ? ` · ${metrics.os_version}`
                    : ""}
                </span>

              </div>

              <span className="badge success-badge">
                {metrics ? "CONNECTED" : "OFFLINE"}
              </span>

            </div>

          </div>

        </div>


        <div className="panel">

          <div className="panel-header">

            <div>
              <p className="panel-label">
                AEGIS ACTIVITY
              </p>

              <h3>
                AI Response Pipeline
              </h3>
            </div>

            <button
              className="view-btn"
              onClick={() => navigate("/ai-assistant")}
            >
              AI Assistant →
            </button>

          </div>


          <div className="pipeline">

            <div className="pipeline-item completed">

              <span>✓</span>

              <div>
                <strong>
                  Telemetry Collection
                </strong>

                <p>
                  System and process data collected
                </p>
              </div>

            </div>


            <div className="pipeline-line"></div>


            <div className="pipeline-item active-pipeline">

              <span>○</span>

              <div>
                <strong>
                  Incident Detection
                </strong>

                <p>
                  Waiting for abnormal behaviour
                </p>
              </div>

            </div>


            <div className="pipeline-line"></div>


            <div className="pipeline-item">

              <span>○</span>

              <div>
                <strong>
                  AI Investigation
                </strong>

                <p>
                  LLM and RAG investigation layer
                </p>
              </div>

            </div>


            <div className="pipeline-line"></div>


            <div className="pipeline-item">

              <span>○</span>

              <div>
                <strong>
                  Recovery Planning
                </strong>

                <p>
                  Human approval for risky actions
                </p>
              </div>

            </div>

          </div>

        </div>

      </section>
    </>
  );
}

export default Dashboard;