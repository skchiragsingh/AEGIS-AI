import { Routes, Route, Navigate } from "react-router-dom";
import "./App.css";

import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import Incidents from "./pages/Incidents";
import Events from "./pages/Events";
import Investigation from "./pages/Investigation";
import Recovery from "./pages/Recovery";
import History from "./pages/History";
import AIAssistant from "./pages/AIAssistant";
import Login from "./pages/Login";


function ProtectedLayout({ children }) {
  const token = localStorage.getItem("aegis_token");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="app">
      <Sidebar />

      <main className="main-content">
        {children}
      </main>
    </div>
  );
}


function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route
        path="/"
        element={
          <ProtectedLayout>
            <Dashboard />
          </ProtectedLayout>
        }
      />

      <Route
        path="/incidents"
        element={
          <ProtectedLayout>
            <Incidents />
          </ProtectedLayout>
        }
      />

      <Route
        path="/events"
        element={
          <ProtectedLayout>
            <Events />
          </ProtectedLayout>
        }
      />

      <Route
        path="/investigation"
        element={
          <ProtectedLayout>
            <Investigation />
          </ProtectedLayout>
        }
      />

      <Route
        path="/recovery"
        element={
          <ProtectedLayout>
            <Recovery />
          </ProtectedLayout>
        }
      />

      <Route
        path="/history"
        element={
          <ProtectedLayout>
            <History />
          </ProtectedLayout>
        }
      />

      <Route
        path="/assistant"
        element={
          <ProtectedLayout>
            <AIAssistant />
          </ProtectedLayout>
        }
      />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;