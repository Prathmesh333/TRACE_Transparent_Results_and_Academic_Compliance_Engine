import { useState, useEffect } from 'react'
import './App.css'

// API Configuration
const API_BASE = 'http://localhost:8000/api/v1'

// API Helper
async function fetchAPI(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options
    })
    if (response.ok) return await response.json()
    const error = await response.json()
    throw new Error(error.detail || 'API Error')
  } catch (error) {
    console.error(`API Error: ${endpoint}`, error)
    throw error
  }
}

// SVG Icons
const Icons = {
  Dashboard: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="3" y="3" width="7" height="7" rx="1" />
      <rect x="14" y="3" width="7" height="7" rx="1" />
      <rect x="3" y="14" width="7" height="7" rx="1" />
      <rect x="14" y="14" width="7" height="7" rx="1" />
    </svg>
  ),
  Upload: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
      <polyline points="17,8 12,3 7,8" />
      <line x1="12" y1="3" x2="12" y2="15" />
    </svg>
  ),
  FileText: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
      <polyline points="14,2 14,8 20,8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
    </svg>
  ),
  Users: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 00-3-3.87" />
      <path d="M16 3.13a4 4 0 010 7.75" />
    </svg>
  ),
  AlertTriangle: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
      <line x1="12" y1="9" x2="12" y2="13" />
      <line x1="12" y1="17" x2="12.01" y2="17" />
    </svg>
  ),
  BarChart: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <line x1="12" y1="20" x2="12" y2="10" />
      <line x1="18" y1="20" x2="18" y2="4" />
      <line x1="6" y1="20" x2="6" y2="14" />
    </svg>
  ),
  CheckCircle: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M22 11.08V12a10 10 0 11-5.93-9.14" />
      <polyline points="22,4 12,14.01 9,11.01" />
    </svg>
  ),
  Clock: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="12" r="10" />
      <polyline points="12,6 12,12 16,14" />
    </svg>
  ),
  Settings: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z" />
    </svg>
  ),
  Bell: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" />
      <path d="M13.73 21a2 2 0 01-3.46 0" />
    </svg>
  ),
  Target: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="12" r="10" />
      <circle cx="12" cy="12" r="6" />
      <circle cx="12" cy="12" r="2" />
    </svg>
  ),
  Book: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M4 19.5A2.5 2.5 0 016.5 17H20" />
      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z" />
    </svg>
  ),
  Camera: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z" />
      <circle cx="12" cy="13" r="4" />
    </svg>
  ),
  GraduationCap: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
      <path d="M6 12v5c3 3 9 3 12 0v-5" />
    </svg>
  ),
  LogOut: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4" />
      <polyline points="16 17 21 12 16 7" />
      <line x1="21" y1="12" x2="9" y2="12" />
    </svg>
  ),
  Building: () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="4" y="2" width="16" height="20" rx="2" ry="2" />
      <line x1="9" y1="22" x2="9" y2="2" />
      <line x1="14" y1="2" x2="14" y2="22" />
    </svg>
  ),
}

// Mini Sparkline Graph Component
function Sparkline({ data, positive = true, height = 32 }) {
  if (!data || data.length < 2) return null

  const max = Math.max(...data)
  const min = Math.min(...data)
  const range = max - min || 1

  const points = data.map((val, i) => {
    const x = (i / (data.length - 1)) * 100
    const y = 100 - ((val - min) / range) * 100
    return `${x},${y}`
  }).join(' ')

  const strokeColor = positive ? 'var(--success)' : 'var(--danger)'

  return (
    <svg viewBox="0 0 100 100" preserveAspectRatio="none" style={{ width: '80px', height: `${height}px` }}>
      <defs>
        <linearGradient id={`gradient-${positive}`} x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor={strokeColor} stopOpacity="0.3" />
          <stop offset="100%" stopColor={strokeColor} stopOpacity="0" />
        </linearGradient>
      </defs>
      <polygon points={`0,100 ${points} 100,100`} fill={`url(#gradient-${positive})`} />
      <polyline points={points} fill="none" stroke={strokeColor} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

// Stat Card with Mini Graph
function StatCard({ label, value, data, variant = '', icon, positive = true }) {
  return (
    <div className={`stat-card ${variant}`}>
      <div className="stat-header">
        <span className="stat-label">{label}</span>
        <div className="stat-icon">{Icons[icon] && Icons[icon]()}</div>
      </div>
      <div className="stat-value">{value}</div>
      <div className="stat-graph">
        <Sparkline data={data} positive={positive} />
      </div>
    </div>
  )
}

// Loading Spinner
function LoadingSpinner() {
  return <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading...</div>
}

// ============================================
// LOGIN PAGE
// ============================================
function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [selectedRole, setSelectedRole] = useState('student')

  const demoCredentials = {
    admin: { email: 'admin@uohyd.ac.in', hint: 'Full system access' },
    teacher: { email: 'anjali.verma.80bc491c@uohyd.ac.in', hint: 'Department view' },
    student: { email: '2023101116@uohyd.ac.in', hint: 'Personal dashboard' }
  }

  const handleDemoLogin = async (role) => {
    setEmail(demoCredentials[role].email)
    setPassword('demo123')
    setSelectedRole(role)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetchAPI('/auth/demo-login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      })

      if (response.success) {
        localStorage.setItem('uoh_user', JSON.stringify(response.user))
        onLogin(response.user)
      }
    } catch (err) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <div className="login-logo">
            <div className="logo-mark">UoH</div>
            <div>
              <div className="login-title">University of Hyderabad</div>
              <div className="login-subtitle">Academic Intelligence Platform</div>
            </div>
          </div>
        </div>

        <div className="login-roles">
          <button
            className={`role-btn ${selectedRole === 'admin' ? 'active' : ''}`}
            onClick={() => handleDemoLogin('admin')}
          >
            {Icons.Settings()}
            <span>Admin</span>
          </button>
          <button
            className={`role-btn ${selectedRole === 'teacher' ? 'active' : ''}`}
            onClick={() => handleDemoLogin('teacher')}
          >
            {Icons.GraduationCap()}
            <span>Faculty</span>
          </button>
          <button
            className={`role-btn ${selectedRole === 'student' ? 'active' : ''}`}
            onClick={() => handleDemoLogin('student')}
          >
            {Icons.Users()}
            <span>Student</span>
          </button>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Email / User ID</label>
            <input
              type="email"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="yourname@uohyd.ac.in"
              required
            />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>

          {error && <div className="login-error">{error}</div>}

          <button type="submit" className="btn btn-primary btn-login" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

          <div className="login-hint">
            <strong>Demo Mode:</strong> Click a role above, then sign in with password: <code>demo123</code>
          </div>
        </form>
      </div>
    </div>
  )
}

// ============================================
// SIDEBAR COMPONENT
// ============================================
function Sidebar({ activeNav, setActiveNav, user, onLogout }) {
  const getNavItems = () => {
    if (user.role === 'admin') {
      return [
        {
          group: 'Admin', items: [
            { id: 'dashboard', label: 'Dashboard', icon: 'Dashboard' },
            { id: 'schools', label: 'Schools', icon: 'Building' },
            { id: 'teachers', label: 'Faculty', icon: 'GraduationCap' },
            { id: 'students', label: 'Students', icon: 'Users' },
          ]
        },
        {
          group: 'Analytics', items: [
            { id: 'analytics', label: 'Analytics', icon: 'BarChart' },
            { id: 'risk', label: 'Risk Monitor', icon: 'AlertTriangle' },
          ]
        },
      ]
    } else if (user.role === 'teacher') {
      return [
        {
          group: 'Teaching', items: [
            { id: 'dashboard', label: 'Dashboard', icon: 'Dashboard' },
            { id: 'courses', label: 'My Courses', icon: 'Book' },
            { id: 'attendance', label: 'Attendance', icon: 'Clock' },
            { id: 'face-attendance', label: 'AI Attendance', icon: 'Camera' },
          ]
        },
        {
          group: 'Students', items: [
            { id: 'my-students', label: 'My Students', icon: 'Users' },
            { id: 'grading', label: 'Grading', icon: 'CheckCircle' },
            { id: 'alerts', label: 'Student Alerts', icon: 'AlertTriangle' },
          ]
        },
        {
          group: 'Communication', items: [
            { id: 'notifications', label: 'Send Notification', icon: 'Bell' },
            { id: 'resources', label: 'Resources', icon: 'Upload' },
          ]
        },
      ]
    } else {
      return [
        {
          group: 'Learning', items: [
            { id: 'dashboard', label: 'Dashboard', icon: 'Dashboard' },
            { id: 'my-courses', label: 'My Courses', icon: 'Book' },
            { id: 'grades', label: 'My Grades', icon: 'CheckCircle' },
            { id: 'attendance', label: 'My Attendance', icon: 'Clock' },
          ]
        },
        {
          group: 'Resources', items: [
            { id: 'resources', label: 'Study Materials', icon: 'FileText' },
            { id: 'ai-assistant', label: 'AI Assistant', icon: 'Target' },
          ]
        },
        {
          group: 'Updates', items: [
            { id: 'notifications', label: 'Notifications', icon: 'Bell' },
          ]
        },
      ]
    }
  }

  const navGroups = getNavItems()

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <div className="logo-mark">UoH</div>
          <span className="logo-text">UoH Academic</span>
          <span className="logo-version">v2.0</span>
        </div>
      </div>

      <nav className="nav-container">
        {navGroups.map((group, gi) => (
          <div key={gi} className="nav-group">
            <div className="nav-group-title">{group.group}</div>
            {group.items.map(item => (
              <div key={item.id} className={`nav-item ${activeNav === item.id ? 'active' : ''}`} onClick={() => setActiveNav(item.id)}>
                {Icons[item.icon] && Icons[item.icon]()}
                <span>{item.label}</span>
              </div>
            ))}
          </div>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="user-card">
          <div className="user-avatar">{user.full_name?.split(' ').map(n => n[0]).join('').slice(0, 2)}</div>
          <div className="user-info">
            <div className="user-name">{user.full_name}</div>
            <div className="user-role">{user.role.charAt(0).toUpperCase() + user.role.slice(1)}</div>
          </div>
        </div>
        <button className="btn btn-ghost btn-sm" onClick={onLogout} style={{ width: '100%', marginTop: '8px' }}>
          {Icons.LogOut()} Sign Out
        </button>
      </div>
    </aside>
  )
}

// TopBar Component
function TopBar({ title, user }) {
  return (
    <header className="topbar">
      <div className="topbar-left">
        <div className="breadcrumb">
          <span>UoH Academic</span>
          <span style={{ margin: '0 8px', color: 'var(--text-dim)' }}>/</span>
          <span className="breadcrumb-current">{title}</span>
        </div>
      </div>
      <div className="topbar-right">
        <span className={`role-badge role-${user.role}`}>{user.role}</span>
        <button className="icon-btn">{Icons.Bell()}</button>
        <button className="icon-btn">{Icons.Settings()}</button>
      </div>
    </header>
  )
}

// ============================================
// STUDENT VIEWS
// ============================================
function StudentDashboard({ user }) {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const trend = [1, 2, 3, 4, 5, 6, 7]

  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchAPI('/data/attendance/stats')
        setStats(data)
      } catch (e) {
        setStats({ total_records: 0, present_count: 0, absent_count: 0, attendance_rate: 0 })
      }
      setLoading(false)
    }
    loadData()
  }, [])

  if (loading) return <LoadingSpinner />

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Welcome, {user.full_name?.split(' ')[0]}!</h1>
        <p className="page-description">Your personal academic dashboard • {user.department} • Semester {user.semester || 'N/A'}</p>
      </div>

      <div className="stats-grid fade-in">
        <StatCard label="Attendance Rate" value={`${stats?.attendance_rate || 0}%`} data={trend} positive={stats?.attendance_rate > 75} variant={stats?.attendance_rate > 75 ? 'success' : 'warning'} icon="Clock" />
        <StatCard label="Classes Attended" value={stats?.present_count || 0} data={trend} positive={true} variant="success" icon="CheckCircle" />
        <StatCard label="Classes Missed" value={stats?.absent_count || 0} data={trend} positive={false} variant="danger" icon="AlertTriangle" />
        <StatCard label="Current Semester" value={user.semester || 'N/A'} data={trend} positive={true} icon="GraduationCap" />
      </div>

      <div className="privacy-notice fade-in">
        <div className="privacy-icon">{Icons.CheckCircle()}</div>
        <div>
          <strong>Grade Privacy</strong>
          <p>Your grades are private and only visible to you and your instructors.</p>
        </div>
      </div>

      <div className="card fade-in">
        <div className="card-header">
          <h3 className="card-title">Your Information</h3>
        </div>
        <div className="card-body">
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">Registration Number</span>
              <span className="info-value">{user.registration_number || 'N/A'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Program</span>
              <span className="info-value">{user.program || 'N/A'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Department</span>
              <span className="info-value">{user.department || 'N/A'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Email</span>
              <span className="info-value">{user.email}</span>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

function StudentGrades({ user }) {
  return (
    <>
      <div className="page-header">
        <h1 className="page-title">My Grades</h1>
        <p className="page-description">Your personal academic performance (Private)</p>
      </div>

      <div className="privacy-notice fade-in">
        <div className="privacy-icon">{Icons.CheckCircle()}</div>
        <div>
          <strong>Private View</strong>
          <p>Only you and your instructors can see your grades. Other students cannot access this information.</p>
        </div>
      </div>

      <div className="card fade-in">
        <div className="card-header">
          <h3 className="card-title">Grade Summary</h3>
        </div>
        <div className="card-body">
          <p style={{ color: 'var(--text-muted)' }}>Grade details will appear here once available from your enrolled courses.</p>
        </div>
      </div>
    </>
  )
}

// ============================================
// TEACHER VIEWS
// ============================================
function TeacherDashboard({ user }) {
  const [stats, setStats] = useState(null)
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const trend = [1, 2, 3, 4, 5, 6, 7]

  useEffect(() => {
    async function loadData() {
      try {
        const [statsData, coursesData] = await Promise.all([
          fetchAPI('/data/stats'),
          fetchAPI('/data/courses')
        ])
        setStats(statsData)
        setCourses(coursesData || [])
      } catch (e) {
        setStats({ total_students: 0, total_submissions: 0, auto_approved_rate: 0, avg_confidence: 0 })
      }
      setLoading(false)
    }
    loadData()
  }, [])

  if (loading) return <LoadingSpinner />

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Faculty Dashboard</h1>
        <p className="page-description">{user.designation} • {user.department}</p>
      </div>

      <div className="stats-grid fade-in">
        <StatCard label="Total Students" value={stats?.total_students || 0} data={trend} positive={true} icon="Users" />
        <StatCard label="Submissions" value={stats?.total_submissions || 0} data={trend} positive={true} icon="FileText" />
        <StatCard label="Auto-Approved" value={`${stats?.auto_approved_rate || 0}%`} data={trend} positive={true} variant="success" icon="CheckCircle" />
        <StatCard label="My Courses" value={courses.length} data={trend} positive={true} variant="info" icon="Book" />
      </div>

      <div className="card fade-in">
        <div className="card-header">
          <h3 className="card-title">Quick Actions</h3>
        </div>
        <div className="card-body">
          <div className="quick-actions">
            <button className="action-card">
              <div className="action-icon">{Icons.Camera()}</div>
              <span>AI Attendance</span>
            </button>
            <button className="action-card">
              <div className="action-icon">{Icons.Bell()}</div>
              <span>Send Notice</span>
            </button>
            <button className="action-card">
              <div className="action-icon">{Icons.Upload()}</div>
              <span>Upload Resources</span>
            </button>
            <button className="action-card">
              <div className="action-icon">{Icons.AlertTriangle()}</div>
              <span>View Alerts</span>
            </button>
          </div>
        </div>
      </div>

      <div className="card fade-in" style={{ marginTop: 20 }}>
        <div className="card-header">
          <h3 className="card-title">My Courses ({courses.length})</h3>
        </div>
        <div className="card-body" style={{ padding: 0 }}>
          <table className="data-table">
            <thead>
              <tr><th>Code</th><th>Name</th><th>Credits</th><th>Semester</th></tr>
            </thead>
            <tbody>
              {courses.slice(0, 5).map((course, i) => (
                <tr key={i}>
                  <td style={{ fontFamily: 'monospace', fontWeight: 500 }}>{course.code}</td>
                  <td style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{course.name}</td>
                  <td><span className="badge badge-info">{course.credits}</span></td>
                  <td>Sem {course.semester}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}

function FaceAttendance({ user }) {
  const [image, setImage] = useState(null)
  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState(null)

  const handleUpload = async () => {
    if (!image) return
    setProcessing(true)

    // Simulate AI processing
    await new Promise(r => setTimeout(r, 3000))

    setResult({
      faces_detected: 28,
      students_recognized: 24,
      unknown_faces: 4,
      students: [
        { name: 'Aarav Sharma', reg: '2023101101', confidence: 98 },
        { name: 'Priya Kumar', reg: '2023101102', confidence: 95 },
        { name: 'Rohan Patel', reg: '2023101103', confidence: 97 },
        { name: 'Sneha Gupta', reg: '2023101104', confidence: 92 },
        { name: 'Vikram Singh', reg: '2023101105', confidence: 99 },
      ]
    })
    setProcessing(false)
  }

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">AI Attendance (Face Recognition)</h1>
        <p className="page-description">Upload classroom photo for automated attendance marking</p>
      </div>

      <div className="content-grid content-grid-equal fade-in">
        <div className="card">
          <div className="card-header"><h3 className="card-title">Upload Classroom Photo</h3></div>
          <div className="card-body">
            <div className="upload-zone" onClick={() => document.getElementById('faceInput')?.click()}>
              <input type="file" id="faceInput" hidden accept="image/*" onChange={(e) => {
                const file = e.target.files?.[0]
                if (file) setImage(URL.createObjectURL(file))
              }} />
              {image ? (
                <img src={image} alt="Classroom" style={{ maxWidth: '100%', maxHeight: '200px', borderRadius: '8px' }} />
              ) : (
                <>
                  <div className="upload-icon">{Icons.Camera()}</div>
                  <div className="upload-title">Click to upload classroom photo</div>
                  <div className="upload-hint">Supports JPG, PNG up to 10MB</div>
                </>
              )}
            </div>

            <button
              className="btn btn-primary"
              style={{ width: '100%', marginTop: '16px' }}
              onClick={handleUpload}
              disabled={!image || processing}
            >
              {processing ? 'Processing with AI...' : 'Mark Attendance with AI'}
            </button>
          </div>
        </div>

        <div className="card">
          <div className="card-header"><h3 className="card-title">Recognition Results</h3></div>
          <div className="card-body">
            {result ? (
              <>
                <div className="stats-mini">
                  <div className="stat-mini">
                    <span className="stat-mini-value">{result.faces_detected}</span>
                    <span className="stat-mini-label">Faces Detected</span>
                  </div>
                  <div className="stat-mini">
                    <span className="stat-mini-value" style={{ color: 'var(--success)' }}>{result.students_recognized}</span>
                    <span className="stat-mini-label">Recognized</span>
                  </div>
                  <div className="stat-mini">
                    <span className="stat-mini-value" style={{ color: 'var(--warning)' }}>{result.unknown_faces}</span>
                    <span className="stat-mini-label">Unknown</span>
                  </div>
                </div>
                <div style={{ color: 'var(--text-muted)', fontSize: '12px', marginTop: '16px', marginBottom: '12px' }}>Recognized Students:</div>
                {result.students.map((s, i) => (
                  <div key={i} className="recognized-student">
                    <div className="student-info">
                      <span className="student-name">{s.name}</span>
                      <span className="student-reg">{s.reg}</span>
                    </div>
                    <span className="badge badge-success">{s.confidence}%</span>
                  </div>
                ))}
                <button className="btn btn-primary btn-sm" style={{ width: '100%', marginTop: '16px' }}>
                  Confirm & Save Attendance
                </button>
              </>
            ) : (
              <div className="empty-state">
                <div className="empty-icon">{Icons.Camera()}</div>
                <div className="empty-title">No Results Yet</div>
                <div className="empty-text">Upload a photo to start face recognition</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}

function TeacherNotifications({ user }) {
  const [type, setType] = useState('announcement')
  const [title, setTitle] = useState('')
  const [message, setMessage] = useState('')
  const [sent, setSent] = useState(false)

  const handleSend = () => {
    if (title && message) {
      setSent(true)
      setTimeout(() => setSent(false), 3000)
      setTitle('')
      setMessage('')
    }
  }

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Send Notification</h1>
        <p className="page-description">Notify students about class schedule changes, announcements, etc.</p>
      </div>

      <div className="card fade-in">
        <div className="card-header"><h3 className="card-title">Compose Notification</h3></div>
        <div className="card-body">
          <div className="form-group">
            <label className="form-label">Notification Type</label>
            <select className="form-select" value={type} onChange={(e) => setType(e.target.value)}>
              <option value="announcement">General Announcement</option>
              <option value="leave">Class Cancelled (Leave)</option>
              <option value="class_postponed">Class Rescheduled</option>
              <option value="extra_class">Extra Class</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Title</label>
            <input type="text" className="form-input" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g., CS501: Class Cancelled Tomorrow" />
          </div>
          <div className="form-group">
            <label className="form-label">Message</label>
            <textarea className="form-textarea" value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Enter your message to students..." rows={4} />
          </div>

          {sent && <div className="success-banner">✓ Notification sent successfully to all enrolled students!</div>}

          <button className="btn btn-primary" onClick={handleSend}>
            {Icons.Bell()} Send Notification
          </button>
        </div>
      </div>
    </>
  )
}

// ============================================
// ADMIN VIEWS
// ============================================
function AdminDashboard({ user }) {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const trend = [1, 2, 3, 4, 5, 6, 7]

  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchAPI('/data/stats')
        setStats(data)
      } catch (e) {
        setStats({ total_students: 0, total_submissions: 0, auto_approved_rate: 0, avg_confidence: 0 })
      }
      setLoading(false)
    }
    loadData()
  }, [])

  if (loading) return <LoadingSpinner />

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Admin Dashboard</h1>
        <p className="page-description">University of Hyderabad - System Overview</p>
      </div>

      <div className="stats-grid fade-in">
        <StatCard label="Total Students" value={stats?.total_students || 0} data={trend} positive={true} icon="Users" />
        <StatCard label="Total Submissions" value={stats?.total_submissions || 0} data={trend} positive={true} icon="FileText" />
        <StatCard label="Auto-Approved Rate" value={`${stats?.auto_approved_rate || 0}%`} data={trend} positive={true} variant="success" icon="CheckCircle" />
        <StatCard label="Avg. AI Confidence" value={(stats?.avg_confidence || 0).toFixed(2)} data={trend} positive={true} variant="info" icon="Target" />
      </div>

      <div className="schools-grid fade-in">
        {['SCIS', 'SoP', 'SoC', 'SMS', 'SLS'].map((code, i) => (
          <div key={i} className="school-card">
            <div className="school-icon">{Icons.Building()}</div>
            <div className="school-code">{code}</div>
            <div className="school-name">{
              { SCIS: 'Computer & Information Sciences', SoP: 'Physics', SoC: 'Chemistry', SMS: 'Mathematics & Statistics', SLS: 'Life Sciences' }[code]
            }</div>
          </div>
        ))}
      </div>
    </>
  )
}

// ============================================
// PLACEHOLDER PAGE
// ============================================
function PlaceholderPage({ title }) {
  return (
    <>
      <div className="page-header">
        <h1 className="page-title">{title}</h1>
        <p className="page-description">This section is under development</p>
      </div>
      <div className="card">
        <div className="card-body">
          <div className="empty-state">
            <div className="empty-icon">{Icons.Settings()}</div>
            <div className="empty-title">Coming Soon</div>
            <div className="empty-text">This feature is currently being developed.</div>
          </div>
        </div>
      </div>
    </>
  )
}

// ============================================
// MAIN APP
// ============================================
function App() {
  const [user, setUser] = useState(null)
  const [activeNav, setActiveNav] = useState('dashboard')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const savedUser = localStorage.getItem('uoh_user')
    if (savedUser) {
      setUser(JSON.parse(savedUser))
    }
    setLoading(false)
  }, [])

  const handleLogin = (userData) => {
    setUser(userData)
    setActiveNav('dashboard')
  }

  const handleLogout = () => {
    localStorage.removeItem('uoh_user')
    setUser(null)
  }

  if (loading) return <div className="loading-screen">Loading...</div>

  if (!user) {
    return <LoginPage onLogin={handleLogin} />
  }

  const getPageTitle = () => {
    const titles = {
      dashboard: 'Dashboard',
      schools: 'Schools',
      teachers: 'Faculty',
      students: 'Students',
      analytics: 'Analytics',
      risk: 'Risk Monitor',
      courses: 'My Courses',
      attendance: 'Attendance',
      'face-attendance': 'AI Attendance',
      'my-students': 'My Students',
      grading: 'Grading',
      alerts: 'Student Alerts',
      notifications: 'Notifications',
      resources: 'Resources',
      'my-courses': 'My Courses',
      grades: 'My Grades',
      'ai-assistant': 'AI Assistant',
    }
    return titles[activeNav] || 'Page'
  }

  const renderPage = () => {
    // Role-based page rendering
    if (user.role === 'student') {
      switch (activeNav) {
        case 'dashboard': return <StudentDashboard user={user} />
        case 'grades': return <StudentGrades user={user} />
        default: return <PlaceholderPage title={getPageTitle()} />
      }
    } else if (user.role === 'teacher') {
      switch (activeNav) {
        case 'dashboard': return <TeacherDashboard user={user} />
        case 'face-attendance': return <FaceAttendance user={user} />
        case 'notifications': return <TeacherNotifications user={user} />
        default: return <PlaceholderPage title={getPageTitle()} />
      }
    } else {
      switch (activeNav) {
        case 'dashboard': return <AdminDashboard user={user} />
        default: return <PlaceholderPage title={getPageTitle()} />
      }
    }
  }

  return (
    <div className="app">
      <Sidebar activeNav={activeNav} setActiveNav={setActiveNav} user={user} onLogout={handleLogout} />
      <main className="main-content">
        <TopBar title={getPageTitle()} user={user} />
        <div className="page-container">{renderPage()}</div>
      </main>
      <div className="role-indicator">{user.role.charAt(0).toUpperCase() + user.role.slice(1)} View • Live Data</div>
    </div>
  )
}

export default App
