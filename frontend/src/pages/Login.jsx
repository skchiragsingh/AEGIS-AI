import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const [isLogin, setIsLogin] = useState(true);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMessage("");
    setLoading(true);

    try {
      const endpoint = isLogin
        ? "http://127.0.0.1:8000/auth/login"
        : "http://127.0.0.1:8000/auth/register";

      const body = isLogin
        ? {
            email,
            password,
          }
        : {
            name,
            email,
            password,
          };

      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Something went wrong");
        return;
      }

      if (isLogin) {
        localStorage.setItem(
          "aegis_token",
          data.access_token || "authenticated"
        );

        localStorage.setItem(
          "aegis_user",
          JSON.stringify(data.user)
        );

        navigate("/");
      } else {
        setMessage("Registration successful. Please login.");
        setIsLogin(true);
        setPassword("");
      }
    } catch {
      setMessage("Unable to connect to AEGIS backend.");
    } finally {
      setLoading(false);
    }
  };

  const switchAuthMode = () => {
    setIsLogin(!isLogin);
    setMessage("");
    setPassword("");
  };

  return (
    <div className="auth-page">
      <div className="auth-left">
        <div className="auth-brand">
          <div className="auth-logo">A</div>

          <div>
            <h1>AEGIS</h1>
            <p>AI INCIDENT RESPONSE PLATFORM</p>
          </div>
        </div>

        <div className="auth-content">
          <span className="auth-tag">
            AUTONOMOUS AI OPERATIONS
          </span>

          <h2>
            Intelligent incident response
            <br />
            for modern systems.
          </h2>

          <p>
            Monitor infrastructure, detect incidents, investigate root causes,
            and generate intelligent recovery plans using AI agents.
          </p>

          <div className="auth-features">
            <div className="feature-card">
              <span className="feature-icon">◉</span>

              <h3>Real-time Monitoring</h3>

              <p>
                Continuously monitor your infrastructure and detect anomalies.
              </p>
            </div>

            <div className="feature-card">
              <span className="feature-icon">✦</span>

              <h3>AI Investigation</h3>

              <p>
                AI agents analyze incidents and identify possible root causes.
              </p>
            </div>

            <div className="feature-card">
              <span className="feature-icon">✓</span>

              <h3>Smart Recovery</h3>

              <p>
                Generate recovery plans with validation and human approval.
              </p>
            </div>
          </div>
        </div>

        <div className="auth-footer">
          AEGIS AI • Autonomous Incident Response
        </div>
      </div>

      <div className="auth-right">
        <div className="auth-form-container">
          <div className="auth-form-header">
            <span className="form-label">
              {isLogin ? "WELCOME BACK" : "CREATE ACCOUNT"}
            </span>

            <h2>
              {isLogin
                ? "Access your AEGIS console"
                : "Create your AEGIS account"}
            </h2>

            <p>
              {isLogin
                ? "Enter your credentials to continue."
                : "Register to access the AEGIS platform."}
            </p>
          </div>

          <form onSubmit={handleSubmit}>
            {!isLogin && (
              <div className="form-group">
                <label>Full Name</label>

                <input
                  type="text"
                  placeholder="Enter your name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
            )}

            <div className="form-group">
              <label>Email Address</label>

              <input
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label>Password</label>

              <input
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            {message && (
              <div
                className={`auth-message ${
                  message.includes("successful")
                    ? "success-message"
                    : ""
                }`}
              >
                {message}
              </div>
            )}

            <button
              type="submit"
              className={`auth-submit-btn ${
                loading ? "loading" : ""
              }`}
              disabled={loading}
            >
              {loading && (
                <span className="button-loader"></span>
              )}

              <span>
                {loading
                  ? isLogin
                    ? "Signing In..."
                    : "Creating Account..."
                  : isLogin
                  ? "Sign In to AEGIS"
                  : "Create Account"}
              </span>
            </button>
          </form>

          <div className="auth-switch">
            {isLogin ? (
              <>
                <span>New to AEGIS?</span>

                <button
                  type="button"
                  onClick={switchAuthMode}
                >
                  Create an account
                </button>
              </>
            ) : (
              <>
                <span>Already have an account?</span>

                <button
                  type="button"
                  onClick={switchAuthMode}
                >
                  Sign in
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;