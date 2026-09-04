import { useNavigate } from "react-router-dom";

function Investigation() {
  const navigate = useNavigate();

  return (
    <>
      <header className="header">
        <div>
          <p className="breadcrumb">AI INVESTIGATION</p>
          <h2>Incident Investigation</h2>
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
            <h2>AI Investigation Engine</h2>

            <p>
              Analyze incidents using automated triage, evidence collection,
              root-cause analysis, and operational knowledge.
            </p>
          </div>

          <button
            className="create-btn"
            onClick={() => navigate("/recovery")}
          >
            Generate Recovery Plan →
          </button>
        </div>

        <div className="investigation-layout">

          <div className="panel investigation-main">
            <div className="panel-header">
              <div>
                <p className="panel-label">ACTIVE INVESTIGATION</p>
                <h3>Database Connection Pool Exhausted</h3>
              </div>

              <span className="status-badge investigating">
                INVESTIGATING
              </span>
            </div>

            <div className="incident-details">
              <div>
                <span>Incident ID</span>
                <strong>INC-001</strong>
              </div>

              <div>
                <span>Service</span>
                <strong>user-service</strong>
              </div>

              <div>
                <span>Severity</span>
                <strong className="critical-text">CRITICAL</strong>
              </div>
            </div>
          </div>

          <div className="panel">
            <div className="panel-header">
              <div>
                <p className="panel-label">AI PIPELINE</p>
                <h3>Investigation Progress</h3>
              </div>
            </div>

            <div className="ai-pipeline">

              <div className="ai-step completed-step">
                <div className="step-icon">✓</div>

                <div>
                  <strong>Event Triage</strong>
                  <p>Incident classified as critical.</p>
                </div>
              </div>

              <div className="ai-step completed-step">
                <div className="step-icon">✓</div>

                <div>
                  <strong>Evidence Collection</strong>
                  <p>Logs and system metrics collected.</p>
                </div>
              </div>

              <div className="ai-step active-step">
                <div className="step-icon">✦</div>

                <div>
                  <strong>Root Cause Analysis</strong>
                  <p>AI agent analyzing possible causes.</p>
                </div>
              </div>

              <div className="ai-step">
                <div className="step-icon">○</div>

                <div>
                  <strong>Knowledge Retrieval</strong>
                  <p>Searching runbooks and previous incidents.</p>
                </div>
              </div>

              <div className="ai-step">
                <div className="step-icon">○</div>

                <div>
                  <strong>Recovery Planning</strong>
                  <p>Waiting for investigation results.</p>
                </div>
              </div>

            </div>
          </div>

          <div className="panel evidence-panel">
            <div className="panel-header">
              <div>
                <p className="panel-label">COLLECTED EVIDENCE</p>
                <h3>System Evidence</h3>
              </div>
            </div>

            <div className="evidence-list">

              <div className="evidence-item">
                <span className="evidence-type log">LOG</span>

                <div>
                  <strong>Connection pool limit reached</strong>
                  <p>
                    Maximum database connections exceeded.
                  </p>
                </div>
              </div>

              <div className="evidence-item">
                <span className="evidence-type metric">METRIC</span>

                <div>
                  <strong>Active connections increased</strong>
                  <p>
                    Connection count increased from 42 to 100.
                  </p>
                </div>
              </div>

              <div className="evidence-item">
                <span className="evidence-type alert">ALERT</span>

                <div>
                  <strong>Prometheus threshold triggered</strong>
                  <p>
                    Database connection usage exceeded 95%.
                  </p>
                </div>
              </div>

            </div>
          </div>

          <div className="panel root-cause-panel">
            <div className="panel-header">
              <div>
                <p className="panel-label">AI ANALYSIS</p>
                <h3>Probable Root Cause</h3>
              </div>

              <span className="confidence-badge">
                87% Confidence
              </span>
            </div>

            <div className="root-cause-content">
              <h4>Database connection leak</h4>

              <p>
                The AI investigation detected a continuous increase in active
                database connections without corresponding connection releases.
                This pattern suggests a possible connection leak inside the
                user-service.
              </p>

              <div className="possible-causes">
                <span>Possible contributing factors:</span>

                <ul>
                  <li>Connections not properly closed</li>
                  <li>Unexpected traffic spike</li>
                  <li>Connection pool configuration limit</li>
                </ul>
              </div>
            </div>
          </div>

        </div>
      </section>
    </>
  );
}

export default Investigation;