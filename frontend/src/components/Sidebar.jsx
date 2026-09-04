import { NavLink } from "react-router-dom";

function Sidebar() {
  const menuItems = [
    { name: "Dashboard", path: "/", icon: "▦" },
    { name: "Incidents", path: "/incidents", icon: "⚠" },
    { name: "Events", path: "/events", icon: "◉" },
    { name: "AI Investigation", path: "/investigation", icon: "⌕" },
    { name: "Recovery Center", path: "/recovery", icon: "↻" },
    { name: "Incident History", path: "/history", icon: "◷" },
    { name: "AI Assistant", path: "/assistant", icon: "✦" },
  ];

  return (
    <aside className="sidebar">
      <div className="logo">
        <div className="logo-icon">A</div>
        <div>
          <h1>AEGIS</h1>
          <span>AI INCIDENT RESPONSE</span>
        </div>
      </div>

      <nav className="nav-menu">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <span>{item.icon}</span>
            {item.name}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <div className="system-status">
          <span className="status-dot"></span>
          <div>
            <p>System Status</p>
            <strong>Operational</strong>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;