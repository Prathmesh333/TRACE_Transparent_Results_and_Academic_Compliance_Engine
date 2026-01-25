import { useState, useEffect, useRef } from 'react'
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
    // Return mock data for demo if backend is offline/erroring
    return null
  }
}

// SVG Icons
const Icons = {
  Dashboard: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" /><rect x="14" y="14" width="7" height="7" rx="1" /></svg>,
  Upload: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" /><polyline points="17,8 12,3 7,8" /><line x1="12" y1="3" x2="12" y2="15" /></svg>,
  FileText: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" /><polyline points="14,2 14,8 20,8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" /></svg>,
  Users: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M23 21v-2a4 4 0 00-3-3.87" /><path d="M16 3.13a4 4 0 010 7.75" /></svg>,
  AlertTriangle: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" /></svg>,
  BarChart: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="20" x2="12" y2="10" /><line x1="18" y1="20" x2="18" y2="4" /><line x1="6" y1="20" x2="6" y2="14" /></svg>,
  CheckCircle: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14" /><polyline points="22,4 12,14.01 9,11.01" /></svg>,
  Clock: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10" /><polyline points="12,6 12,12 16,14" /></svg>,
  Settings: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z" /></svg>,
  Bell: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" /><path d="M13.73 21a2 2 0 01-3.46 0" /></svg>,
  Target: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="2" /></svg>,
  Book: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 19.5A2.5 2.5 0 016.5 17H20" /><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z" /></svg>,
  Camera: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z" /><circle cx="12" cy="13" r="4" /></svg>,
  GraduationCap: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z" /><path d="M6 12v5c3 3 9 3 12 0v-5" /></svg>,
  LogOut: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4" /><polyline points="16 17 21 12 16 7" /><line x1="21" y1="12" x2="9" y2="12" /></svg>,
  Building: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="4" y="2" width="16" height="20" rx="2" ry="2" /><line x1="9" y1="22" x2="9" y2="2" /><line x1="14" y1="2" x2="14" y2="22" /></svg>,
  Message: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" /></svg>,
  Search: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /></svg>,
  Bot: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="10" rx="2" /><circle cx="12" cy="5" r="2" /><path d="M12 7v4" /><line x1="8" y1="16" x2="8" y2="16" /><line x1="16" y1="16" x2="16" y2="16" /></svg>,
  Sun: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="5" /><line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" /><line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" /><line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" /><line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" /></svg>,
  Moon: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" /></svg>
}

// Mini Sparkline Graph
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

// Stat Card
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

// Loading Component
function LoadingSpinner() {
  return <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading...</div>
}

// Empty State Component
function EmptyState({ title, message, icon }) {
  return (
    <div className="empty-state">
      <div className="empty-icon">{Icons[icon] ? Icons[icon]() : Icons.FileText()}</div>
      <div className="empty-title">{title}</div>
      <div className="empty-text">{message}</div>
    </div>
  )
}

// ============================================
// SHARED VIEWS (Used by multiple roles)
// ============================================
function ResourcesView() {
  const [resources, setResources] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      const data = await fetchAPI('/data/resources')
      setResources(data || [])
      setLoading(false)
    }
    load()
  }, [])

  if (loading) return <LoadingSpinner />

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Learning Resources</h1>
        <p className="page-description">Platform-wide study materials and references</p>
      </div>
      <div className="card fade-in">
        <div className="card-body">
          {resources.length > 0 ? (
            <div className="resources-grid">
              {resources.map((res, i) => (
                <div key={i} className="resource-card">
                  <div className="resource-icon">{res.type === 'video' ? Icons.Camera() : Icons.FileText()}</div>
                  <div className="resource-info">
                    <h4>{res.title}</h4>
                    <p>{res.difficulty} • {res.type}</p>
                  </div>
                  <a href={res.url} target="_blank" className="btn btn-sm btn-ghost">View</a>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No Resources Found" message="Check back later for uploaded materials." icon="Upload" />
          )}
        </div>
      </div>
    </>
  )
}

// ============================================
// ADMIN COMPONENTS
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
        setStats({ total_students: 64, total_submissions: 294, auto_approved_rate: 49.3, avg_confidence: 0.84 })
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
        <p className="page-description">System Overview & Health</p>
      </div>

      <div className="stats-grid fade-in">
        <StatCard label="Total Students" value={stats?.total_students || 0} data={trend} positive={true} icon="Users" />
        <StatCard label="Total Submissions" value={stats?.total_submissions || 0} data={trend} positive={true} icon="FileText" />
        <StatCard label="Auto-Approved" value={`${stats?.auto_approved_rate || 0}%`} data={trend} positive={true} variant="success" icon="CheckCircle" />
        <StatCard label="AI Confidence" value={(stats?.avg_confidence || 0).toFixed(2)} data={trend} positive={true} variant="info" icon="Target" />
      </div>

      <div className="schools-grid fade-in">
        {['SCIS', 'SoP', 'SoC', 'SMS', 'SLS', 'SoE', 'SoH', 'SoSS'].map((code, i) => (
          <div key={i} className="school-card">
            <div className="school-icon">{Icons.Building()}</div>
            <div className="school-code">{code}</div>
            <div className="school-name">{{
              SCIS: 'Computer & Information Sciences', 
              SoP: 'Physics', 
              SoC: 'Chemistry', 
              SMS: 'Maths & Stats', 
              SLS: 'Life Sciences',
              SoE: 'Economics',
              SoH: 'Humanities',
              SoSS: 'Social Sciences'
            }[code]}</div>
          </div>
        ))}
      </div>
    </>
  )
}

function AdminSchoolsView({ onSelectSchool }) {
  const [schools, setSchools] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      const data = await fetchAPI('/data/schools')
      setSchools(data || [])
      setLoading(false)
    }
    load()
  }, [])

  if (loading) return <LoadingSpinner />

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">School Management</h1>
        <p className="page-description">Manage University Schools and Departments</p>
      </div>
      <div className="schools-grid fade-in">
        {schools.map((s, i) => (
          <div key={i} className="school-card" onClick={() => onSelectSchool(s.code)} style={{ cursor: 'pointer' }}>
            <div className="school-icon">{Icons.Building()}</div>
            <div className="school-code">{s.code}</div>
            <div className="school-name">{s.name}</div>
            <div className="school-stats">
              <span>{s.department_count} Departments</span> • <span>{s.course_count} Courses</span>
            </div>
            <div style={{ marginTop: '10px', fontSize: '13px', color: 'var(--text-muted)' }}>{s.description}</div>
          </div>
        ))}
      </div>
    </>
  )
}

function SchoolDetailsView({ code, onBack }) {
  const [details, setDetails] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      const data = await fetchAPI(`/data/schools/${code}`)
      setDetails(data)
      setLoading(false)
    }
    load()
  }, [code])

  if (loading) return <LoadingSpinner />
  if (!details) return <EmptyState title="School Not Found" />

  return (
    <>
      <div className="page-header">
        <button className="btn btn-sm btn-ghost" onClick={onBack} style={{ marginBottom: '10px' }}>← Back to Schools</button>
        <h1 className="page-title">{details.name}</h1>
        <p className="page-description">Director: {details.director}</p>
      </div>

      <div className="content-grid fade-in">
        {Object.entries(details.students_by_semester).map(([sem, students]) => (
          <div key={sem} className="card">
            <div className="card-header"><h3 className="card-title">{sem} Students</h3></div>
            <div className="card-body" style={{ padding: 0 }}>
              <table className="data-table">
                <thead><tr><th>Reg No.</th><th>Name</th><th>Course</th></tr></thead>
                <tbody>
                  {students.map((s, i) => (
                    <tr key={i}>
                      <td style={{ fontFamily: 'monospace' }}>{s.reg}</td>
                      <td>{s.name}</td>
                      <td>{s.course}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </div>
    </>
  )
}

function AdminAnalyticsView() {
  const [data, setData] = useState(null)
  const [deptAnalytics, setDeptAnalytics] = useState(null)
  const [attendanceStats, setAttendanceStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const [adminData, deptData, attData] = await Promise.all([
          fetchAPI('/data/admin/analytics'),
          fetchAPI('/data/department/analytics'),
          fetchAPI('/data/attendance/stats')
        ])
        setData(adminData)
        setDeptAnalytics(deptData)
        setAttendanceStats(attData)
      } catch (e) {
        console.error('Failed to load analytics:', e)
      }
      setLoading(false)
    }
    load()
  }, [])

  if (loading) return <LoadingSpinner />
  if (!data) return <EmptyState title="No Data Available" icon="BarChart" />

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">System Analytics</h1>
        <p className="page-description">Platform Usage & Distribution Metrics</p>
      </div>

      <div className="stats-grid fade-in">
        <StatCard label="Active Users" value={data.active_users_now} data={data.enrollment_trend} positive={true} icon="Users" />
        <StatCard label="System Health" value={data.system_health} data={[1, 1, 1, 1, 1]} positive={true} variant="success" icon="CheckCircle" />
        {attendanceStats && (
          <>
            <StatCard label="Avg Attendance" value={`${attendanceStats.average_attendance}%`} data={[1, 2, 3, 4, 5]} positive={attendanceStats.average_attendance > 75} variant={attendanceStats.average_attendance > 75 ? 'success' : 'warning'} icon="Clock" />
            <StatCard label="Total Students" value={attendanceStats.total_students} data={[1, 2, 3, 4, 5]} positive={true} icon="Users" />
          </>
        )}
      </div>

      <div className="content-grid content-grid-equal fade-in">
        <div className="card">
          <div className="card-header"><h3 className="card-title">Enrollment Trend</h3></div>
          <div className="card-body">
            <div style={{ height: '200px', display: 'flex', alignItems: 'end', gap: '5px' }}>
              {data.enrollment_trend.map((v, i) => (
                <div key={i} style={{
                  flex: 1,
                  background: 'var(--primary)',
                  height: `${(v / Math.max(...data.enrollment_trend)) * 100}%`,
                  borderRadius: '4px 4px 0 0',
                  opacity: 0.8
                }} title={v}></div>
              ))}
            </div>
            <div style={{ textAlign: 'center', marginTop: '10px', color: 'var(--text-muted)' }}>Last 7 Batches</div>
          </div>
        </div>

        <div className="card">
          <div className="card-header"><h3 className="card-title">School Distribution</h3></div>
          <div className="card-body">
            {Object.entries(data.department_distribution).filter(([_, count]) => count > 0).map(([school, count], i) => {
              const schoolNames = {
                'SCIS': 'Computer & Information Sciences',
                'SoP': 'Physics',
                'SoC': 'Chemistry',
                'SMS': 'Mathematics & Statistics',
                'SLS': 'Life Sciences',
                'SoE': 'Economics',
                'SoH': 'Humanities',
                'SoSS': 'Social Sciences'
              }
              const maxCount = Math.max(...Object.values(data.department_distribution))
              return (
                <div key={i} style={{ marginBottom: '10px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <span><b>{school}</b> - {schoolNames[school] || school}</span>
                    <span>{count} students</span>
                  </div>
                  <div className="progress-bar"><div className="progress-fill" style={{ width: `${(count / maxCount) * 100}%` }}></div></div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {deptAnalytics && (
        <div className="card fade-in" style={{ marginTop: '20px' }}>
          <div className="card-header"><h3 className="card-title">Department Risk Analysis</h3></div>
          <div className="card-body" style={{ padding: 0 }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Department</th>
                  <th>Total Students</th>
                  <th>At Risk</th>
                  <th>Critical</th>
                  <th>Avg Attendance</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(deptAnalytics).map(([dept, stats], i) => (
                  <tr key={i}>
                    <td><b>{dept}</b></td>
                    <td>{stats.total_students}</td>
                    <td>
                      <span className={`badge ${stats.at_risk > 0 ? 'badge-warning' : 'badge-success'}`}>
                        {stats.at_risk}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${stats.critical_risk > 0 ? 'badge-danger' : 'badge-success'}`}>
                        {stats.critical_risk}
                      </span>
                    </td>
                    <td>
                      <span className={stats.avg_attendance >= 75 ? 'text-success' : 'text-warning'}>
                        {stats.avg_attendance}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {attendanceStats && attendanceStats.by_school && (
        <div className="card fade-in" style={{ marginTop: '20px' }}>
          <div className="card-header"><h3 className="card-title">School-wise Attendance</h3></div>
          <div className="card-body">
            <div className="stats-grid">
              {Object.entries(attendanceStats.by_school).map(([school, data], i) => (
                <div key={i} className="stat-card">
                  <div className="stat-label">{school}</div>
                  <div className="stat-value">{data.avg_rate}%</div>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{data.count} students</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </>
  )
}

function AdminStudentsView() {
  const [students, setStudents] = useState([])
  const [loading, setLoading] = useState(true)
  const [editingStudent, setEditingStudent] = useState(null)
  const [refresh, setRefresh] = useState(0)

  useEffect(() => {
    async function load() {
      const data = await fetchAPI('/data/students?limit=100')
      setStudents(data || [])
      setLoading(false)
    }
    load()
  }, [refresh])

  const handleSave = async (e) => {
    e.preventDefault()
    const formData = new FormData(e.target)
    const updates = Object.fromEntries(formData.entries())

    await fetchAPI(`/data/students/${editingStudent.id}`, {
      method: 'PUT',
      body: JSON.stringify(updates)
    })
    setEditingStudent(null)
    setRefresh(r => r + 1)
  }

  // Group by semester
  const groupedStudents = students.reduce((acc, s) => {
    const key = `Semester ${s.current_semester}`
    if (!acc[key]) acc[key] = []
    acc[key].push(s)
    return acc
  }, {})

  if (loading) return <LoadingSpinner />

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Student Directory</h1>
        <p className="page-description">Registered students organized by Semester</p>
      </div>

      {Object.entries(groupedStudents).sort().map(([sem, list]) => (
        <div key={sem} className="card fade-in" style={{ marginBottom: '20px' }}>
          <div className="card-header"><h3 className="card-title">{sem}</h3></div>
          <div className="card-body" style={{ padding: 0 }}>
            <table className="data-table">
              <thead>
                <tr><th>Reg. Number</th><th>Name</th><th>Department</th><th>Action</th></tr>
              </thead>
              <tbody>
                {list.map((s, i) => (
                  <tr key={i}>
                    <td><span className="badge">{s.registration_number}</span></td>
                    <td><b>{s.name}</b><br /><span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{s.email}</span></td>
                    <td>{s.department}</td>
                    <td>
                      <button className="btn btn-sm btn-ghost" onClick={() => setEditingStudent(s)}>Edit</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}

      {students.length === 0 && <EmptyState title="No Students" icon="Users" />}

      {editingStudent && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h3>Edit Student</h3>
            <form onSubmit={handleSave}>
              <div className="form-group">
                <label>Name</label>
                <input className="form-input" name="name" defaultValue={editingStudent.name} />
              </div>
              <div className="form-group">
                <label>Department</label>
                <input className="form-input" name="department" defaultValue={editingStudent.department} />
              </div>
              <div className="form-group">
                <label>Semester</label>
                <input className="form-input" name="current_semester" type="number" defaultValue={editingStudent.current_semester} />
              </div>
              <div style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
                <button type="button" className="btn btn-ghost" onClick={() => setEditingStudent(null)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}

function RiskMonitorView() {
  const [riskStudents, setRiskStudents] = useState([])
  const [counts, setCounts] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const [rs, rc] = await Promise.all([
          fetchAPI('/data/risk-students'),
          fetchAPI('/data/risk-counts')
        ])
        setRiskStudents(rs || [])
        setCounts(rc)
      } catch (e) { }
      setLoading(false)
    }
    load()
  }, [])

  if (loading) return <LoadingSpinner />

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Risk Monitor</h1>
        <p className="page-description">AI-driven at-risk student identification</p>
      </div>

      {counts && (
        <div className="stats-grid fade-in" style={{ marginBottom: '20px' }}>
          <div className="stat-card danger">
            <div className="stat-value">{counts.critical}</div>
            <div className="stat-label">Critical Risk</div>
          </div>
          <div className="stat-card warning">
            <div className="stat-value">{counts.high}</div>
            <div className="stat-label">High Risk</div>
          </div>
          <div className="stat-card info">
            <div className="stat-value">{counts.medium}</div>
            <div className="stat-label">Medium Risk</div>
          </div>
          <div className="stat-card success">
            <div className="stat-value">{counts.low}</div>
            <div className="stat-label">Low Risk</div>
          </div>
        </div>
      )}

      <div className="card fade-in">
        <div className="card-header"><h3 className="card-title">At-Risk Students</h3></div>
        <div className="card-body" style={{ padding: 0 }}>
          <table className="data-table">
            <thead><tr><th>Student</th><th>Risk Level</th><th>Probability</th><th>Factors</th></tr></thead>
            <tbody>
              {riskStudents.map((s, i) => (
                <tr key={i}>
                  <td>{s.student_name}<br /><small>{s.student_reg}</small></td>
                  <td><span className={`badge badge-${s.risk_level === 'critical' ? 'danger' : 'warning'}`}>{s.risk_level.toUpperCase()}</span></td>
                  <td>{(s.probability * 100).toFixed(1)}%</td>
                  <td>{s.factors.slice(0, 2).map((f, fi) => <span key={fi} className="tag">{f}</span>)}</td>
                </tr>
              ))}
              {riskStudents.length === 0 && <tr><td colSpan="4"><EmptyState title="No Risks Detected" icon="CheckCircle" message="All students are currently performing well." /></td></tr>}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}

// ============================================
// TEACHER COMPONENTS
// ============================================

function TeacherDashboard({ user }) {
  const [stats, setStats] = useState(null)
  const [gradingStats, setGradingStats] = useState(null)
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const trend = [1, 2, 3, 4, 5, 6, 7]

  useEffect(() => {
    async function loadData() {
      try {
        const [statsData, coursesData, gradingData] = await Promise.all([
          fetchAPI(`/data/teacher/stats?teacher_email=${user.email}`),
          fetchAPI(`/data/teacher/courses?teacher_email=${user.email}`),
          fetchAPI(`/data/teacher/grading-stats?teacher_email=${user.email}`)
        ])
        setStats(statsData)
        setCourses(coursesData || [])
        setGradingStats(gradingData)
      } catch (e) {
        console.error('Error loading teacher data:', e)
        setStats({ total_students: 0, total_courses: 0, avg_attendance: 0, at_risk_students: 0 })
        setGradingStats({ total_submissions: 0, pending_review: 0, approved: 0, ai_accuracy: 0 })
      }
      setLoading(false)
    }
    loadData()
  }, [user.email])

  if (loading) return <LoadingSpinner />

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Faculty Dashboard</h1>
        <p className="page-description">{user.designation || 'Professor'} • {user.department || 'SCIS'}</p>
      </div>

      <div className="stats-grid fade-in">
        <StatCard label="My Courses" value={stats?.total_courses || 0} data={trend} positive={true} icon="Book" variant="info" />
        <StatCard label="Total Students" value={stats?.total_students || 0} data={trend} positive={true} icon="Users" />
        <StatCard label="Avg Attendance" value={`${stats?.avg_attendance || 0}%`} data={trend} positive={stats?.avg_attendance > 75} variant={stats?.avg_attendance > 75 ? 'success' : 'warning'} icon="Clock" />
        <StatCard label="At-Risk Students" value={stats?.at_risk_students || 0} data={trend} positive={false} variant="danger" icon="AlertTriangle" />
      </div>

      {gradingStats && (
        <div className="stats-grid fade-in" style={{ marginTop: '20px' }}>
          <div className="stat-card">
            <div className="stat-value">{gradingStats.total_submissions}</div>
            <div className="stat-label">Total Submissions</div>
          </div>
          <div className="stat-card warning">
            <div className="stat-value">{gradingStats.pending_review}</div>
            <div className="stat-label">Pending Review</div>
          </div>
          <div className="stat-card success">
            <div className="stat-value">{gradingStats.approved}</div>
            <div className="stat-label">Approved</div>
          </div>
          <div className="stat-card info">
            <div className="stat-value">{gradingStats.ai_accuracy}%</div>
            <div className="stat-label">AI Accuracy</div>
          </div>
        </div>
      )}

      <div className="card fade-in" style={{ marginTop: 20 }}>
        <div className="card-header"><h3 className="card-title">My Teaching Courses</h3></div>
        <div className="card-body" style={{ padding: 0 }}>
          <table className="data-table">
            <thead>
              <tr><th>Code</th><th>Name</th><th>Semester</th><th>Students</th><th>Credits</th></tr>
            </thead>
            <tbody>
              {courses.map((course, i) => (
                <tr key={i}>
                  <td style={{ fontFamily: 'monospace', fontWeight: 500 }}>{course.course_code}</td>
                  <td style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{course.course_name}</td>
                  <td>Sem {course.semester}</td>
                  <td><span className="badge badge-info">{course.total_students}</span></td>
                  <td>{course.credits}</td>
                </tr>
              ))}
              {courses.length === 0 && <tr><td colSpan="5"><EmptyState title="No Courses Assigned" icon="Book" message="You aren't teaching any courses this semester." /></td></tr>}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}

function TeacherCoursesView({ user }) {
  const [courses, setCourses] = useState([])
  const [selectedCourse, setSelectedCourse] = useState(null)
  const [attendance, setAttendance] = useState([])
  const [loading, setLoading] = useState(true)
  const [editingAttendance, setEditingAttendance] = useState(null)

  useEffect(() => {
    async function load() {
      const data = await fetchAPI(`/data/teacher/courses?teacher_email=${user.email}`)
      setCourses(data || [])
      setLoading(false)
    }
    load()
  }, [user.email])

  const loadAttendance = async (courseCode) => {
    const data = await fetchAPI(`/data/course/${courseCode}/attendance`)
    setAttendance(data || [])
  }

  const handleCourseSelect = (course) => {
    setSelectedCourse(course)
    loadAttendance(course.course_code)
  }

  const handleUpdateAttendance = async (attendanceId, newAttended) => {
    try {
      await fetchAPI(`/data/attendance/${attendanceId}?attended=${newAttended}`, { method: 'PUT' })
      // Reload attendance
      loadAttendance(selectedCourse.course_code)
      setEditingAttendance(null)
    } catch (e) {
      console.error('Error updating attendance:', e)
    }
  }

  if (loading) return <LoadingSpinner />

  if (selectedCourse) {
    return (
      <>
        <div className="page-header">
          <button className="btn btn-sm btn-ghost" onClick={() => setSelectedCourse(null)} style={{ marginBottom: '10px' }}>← Back to Courses</button>
          <h1 className="page-title">{selectedCourse.course_name}</h1>
          <p className="page-description">{selectedCourse.course_code} • Semester {selectedCourse.semester} • {selectedCourse.total_students} Students</p>
        </div>

        <div className="card fade-in">
          <div className="card-header">
            <h3 className="card-title">Student Attendance</h3>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>Click on attendance numbers to edit</p>
          </div>
          <div className="card-body" style={{ padding: 0 }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Reg. No.</th>
                  <th>Student Name</th>
                  <th>Total Classes</th>
                  <th>Attended</th>
                  <th>Attendance %</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {attendance.map((record, i) => (
                  <tr key={i}>
                    <td style={{ fontFamily: 'monospace' }}>{record.student_reg}</td>
                    <td><b>{record.student_name}</b></td>
                    <td>{record.total_classes}</td>
                    <td>
                      {editingAttendance === record.id ? (
                        <input 
                          type="number" 
                          defaultValue={record.attended}
                          min="0"
                          max={record.total_classes}
                          style={{ width: '60px', padding: '4px', border: '1px solid var(--border)', borderRadius: '4px' }}
                          onBlur={(e) => handleUpdateAttendance(record.id, parseInt(e.target.value))}
                          onKeyPress={(e) => e.key === 'Enter' && handleUpdateAttendance(record.id, parseInt(e.target.value))}
                          autoFocus
                        />
                      ) : (
                        <span 
                          onClick={() => setEditingAttendance(record.id)}
                          style={{ cursor: 'pointer', textDecoration: 'underline', color: 'var(--primary)' }}
                        >
                          {record.attended}
                        </span>
                      )}
                    </td>
                    <td>
                      <span className={record.attendance_rate >= 0.75 ? 'text-success' : 'text-danger'}>
                        {(record.attendance_rate * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td>
                      {record.attendance_rate >= 0.90 ? (
                        <span className="badge badge-success">Excellent</span>
                      ) : record.attendance_rate >= 0.75 ? (
                        <span className="badge badge-info">Good</span>
                      ) : record.attendance_rate >= 0.60 ? (
                        <span className="badge badge-warning">Warning</span>
                      ) : (
                        <span className="badge badge-danger">Critical</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </>
    )
  }

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">My Teaching Courses</h1>
        <p className="page-description">Manage your courses and student attendance</p>
      </div>
      <div className="schools-grid fade-in">
        {courses.map((c, i) => (
          <div key={i} className="card" onClick={() => handleCourseSelect(c)} style={{ cursor: 'pointer' }}>
            <div className="card-body">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div>
                  <h3 style={{ margin: 0, fontSize: '18px' }}>{c.course_name}</h3>
                  <div style={{ color: 'var(--text-dim)', fontSize: '14px', fontFamily: 'monospace', margin: '4px 0' }}>{c.course_code}</div>
                </div>
                <span className="badge badge-info">{c.credits} Credits</span>
              </div>
              <div style={{ marginTop: '12px', display: 'flex', gap: '12px', fontSize: '13px', color: 'var(--text-muted)' }}>
                <span>📚 Semester {c.semester}</span>
                <span>👥 {c.total_students} Students</span>
              </div>
              <div style={{ marginTop: '16px' }}>
                <button className="btn btn-sm btn-primary" onClick={(e) => { e.stopPropagation(); handleCourseSelect(c); }}>
                  Manage Attendance
                </button>
              </div>
            </div>
          </div>
        ))}
        {courses.length === 0 && <EmptyState title="No Courses" icon="Book" message="You don't have any courses assigned." />}
      </div>
    </>
  )
}

function AIGradingView({ user }) {
  const [courses, setCourses] = useState([])
  const [selectedCourse, setSelectedCourse] = useState(null)
  const [assignments, setAssignments] = useState([])
  const [selectedAssignment, setSelectedAssignment] = useState(null)
  const [submissions, setSubmissions] = useState([])
  const [selectedSubmission, setSelectedSubmission] = useState(null)
  const [loading, setLoading] = useState(true)
  const [verifying, setVerifying] = useState(false)
  const [teacherScore, setTeacherScore] = useState(0)
  const [teacherFeedback, setTeacherFeedback] = useState('')

  useEffect(() => {
    async function load() {
      const data = await fetchAPI(`/data/teacher/courses?teacher_email=${user.email}`)
      setCourses(data || [])
      setLoading(false)
    }
    load()
  }, [user.email])

  const loadAssignments = async (courseCode) => {
    const data = await fetchAPI(`/data/course/${courseCode}/assignments`)
    setAssignments(data || [])
  }

  const loadSubmissions = async (assignmentId) => {
    const data = await fetchAPI(`/data/assignment/${assignmentId}/submissions`)
    setSubmissions(data || [])
  }

  const handleCourseSelect = (course) => {
    setSelectedCourse(course)
    setSelectedAssignment(null)
    setSelectedSubmission(null)
    loadAssignments(course.course_code)
  }

  const handleAssignmentSelect = (assignment) => {
    setSelectedAssignment(assignment)
    setSelectedSubmission(null)
    loadSubmissions(assignment.id)
  }

  const handleSubmissionSelect = (submission) => {
    setSelectedSubmission(submission)
    setTeacherScore(submission.teacher_score || submission.ai_score)
    setTeacherFeedback(submission.teacher_feedback || '')
  }

  const handleVerify = async (approved) => {
    if (!selectedSubmission) return
    setVerifying(true)
    try {
      await fetchAPI(`/data/submission/${selectedSubmission.id}/verify`, {
        method: 'PUT',
        body: JSON.stringify({
          teacher_score: teacherScore,
          teacher_feedback: teacherFeedback,
          approved: approved
        })
      })
      // Reload submissions
      await loadSubmissions(selectedAssignment.id)
      setSelectedSubmission(null)
      setTeacherScore(0)
      setTeacherFeedback('')
    } catch (e) {
      console.error('Error verifying submission:', e)
    }
    setVerifying(false)
  }

  if (loading) return <LoadingSpinner />

  // Submission Detail View
  if (selectedSubmission) {
    const scoreDiff = Math.abs(teacherScore - selectedSubmission.ai_score)
    const isClose = scoreDiff <= 5

    return (
      <>
        <div className="page-header">
          <button className="btn btn-sm btn-ghost" onClick={() => setSelectedSubmission(null)} style={{ marginBottom: '10px' }}>← Back to Submissions</button>
          <h1 className="page-title">Review Submission</h1>
          <p className="page-description">{selectedSubmission.student_name} ({selectedSubmission.student_reg})</p>
        </div>

        <div className="content-grid content-grid-equal fade-in">
          <div className="card">
            <div className="card-header"><h3 className="card-title">Student Submission</h3></div>
            <div className="card-body">
              <div style={{ marginBottom: '12px' }}>
                <strong>File:</strong> {selectedSubmission.file_name}
              </div>
              <div style={{ marginBottom: '12px' }}>
                <strong>Submitted:</strong> {selectedSubmission.submitted_at}
              </div>
              <div style={{ padding: '12px', background: 'var(--surface)', borderRadius: '8px', fontSize: '14px', lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>
                {selectedSubmission.submission_text}
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <h3 className="card-title">AI Grading Analysis</h3>
              <span className={`badge ${isClose ? 'badge-success' : 'badge-warning'}`} style={{ marginLeft: '8px' }}>
                AI Score: {selectedSubmission.ai_score}/100
              </span>
            </div>
            <div className="card-body">
              <div style={{ marginBottom: '16px' }}>
                <strong style={{ display: 'block', marginBottom: '8px' }}>AI Feedback:</strong>
                <div style={{ padding: '12px', background: 'var(--surface)', borderRadius: '8px', fontSize: '14px' }}>
                  {selectedSubmission.ai_feedback}
                </div>
              </div>
              <div>
                <strong style={{ display: 'block', marginBottom: '8px' }}>AI Reasoning:</strong>
                <div style={{ padding: '12px', background: 'var(--surface)', borderRadius: '8px', fontSize: '14px', lineHeight: '1.6' }}>
                  {selectedSubmission.ai_reasoning}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="card fade-in" style={{ marginTop: '20px' }}>
          <div className="card-header"><h3 className="card-title">Teacher Verification</h3></div>
          <div className="card-body">
            <div className="form-group">
              <label className="form-label">Final Score (0-100)</label>
              <input 
                type="number" 
                className="form-input" 
                value={teacherScore}
                onChange={(e) => setTeacherScore(parseInt(e.target.value) || 0)}
                min="0"
                max="100"
                style={{ maxWidth: '200px' }}
              />
              {scoreDiff > 0 && (
                <div style={{ marginTop: '8px', fontSize: '13px', color: isClose ? 'var(--success)' : 'var(--warning)' }}>
                  {isClose ? '✓' : '⚠'} Difference from AI: {scoreDiff > 0 ? '+' : ''}{teacherScore - selectedSubmission.ai_score} points
                </div>
              )}
            </div>
            <div className="form-group">
              <label className="form-label">Teacher Feedback</label>
              <textarea 
                className="form-textarea" 
                rows="4"
                value={teacherFeedback}
                onChange={(e) => setTeacherFeedback(e.target.value)}
                placeholder="Add your feedback for the student..."
              />
            </div>
            <div style={{ display: 'flex', gap: '12px', marginTop: '16px' }}>
              <button 
                className="btn btn-primary" 
                onClick={() => handleVerify(true)}
                disabled={verifying}
              >
                {verifying ? 'Approving...' : 'Approve & Publish'}
              </button>
              <button 
                className="btn btn-ghost" 
                onClick={() => handleVerify(false)}
                disabled={verifying}
              >
                Request Revision
              </button>
              <button 
                className="btn btn-ghost" 
                onClick={() => setSelectedSubmission(null)}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </>
    )
  }

  // Submissions List View
  if (selectedAssignment) {
    const pendingSubmissions = submissions.filter(s => s.status === 'pending_review')
    const approvedSubmissions = submissions.filter(s => s.status === 'approved')

    return (
      <>
        <div className="page-header">
          <button className="btn btn-sm btn-ghost" onClick={() => setSelectedAssignment(null)} style={{ marginBottom: '10px' }}>← Back to Assignments</button>
          <h1 className="page-title">{selectedAssignment.assignment_title}</h1>
          <p className="page-description">{selectedAssignment.description}</p>
        </div>

        <div className="stats-grid fade-in" style={{ marginBottom: '20px' }}>
          <div className="stat-card">
            <div className="stat-value">{submissions.length}</div>
            <div className="stat-label">Total Submissions</div>
          </div>
          <div className="stat-card warning">
            <div className="stat-value">{pendingSubmissions.length}</div>
            <div className="stat-label">Pending Review</div>
          </div>
          <div className="stat-card success">
            <div className="stat-value">{approvedSubmissions.length}</div>
            <div className="stat-label">Approved</div>
          </div>
          <div className="stat-card info">
            <div className="stat-value">{selectedAssignment.max_score}</div>
            <div className="stat-label">Max Score</div>
          </div>
        </div>

        {pendingSubmissions.length > 0 && (
          <div className="card fade-in" style={{ marginBottom: '20px' }}>
            <div className="card-header"><h3 className="card-title">Pending Review ({pendingSubmissions.length})</h3></div>
            <div className="card-body" style={{ padding: 0 }}>
              <table className="data-table">
                <thead>
                  <tr><th>Student</th><th>Submitted</th><th>AI Score</th><th>AI Feedback</th><th>Action</th></tr>
                </thead>
                <tbody>
                  {pendingSubmissions.map((sub, i) => (
                    <tr key={i}>
                      <td><b>{sub.student_name}</b><br /><small>{sub.student_reg}</small></td>
                      <td>{sub.submitted_at}</td>
                      <td><span className="badge badge-info">{sub.ai_score}/100</span></td>
                      <td style={{ maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{sub.ai_feedback}</td>
                      <td>
                        <button className="btn btn-sm btn-primary" onClick={() => handleSubmissionSelect(sub)}>
                          Review
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {approvedSubmissions.length > 0 && (
          <div className="card fade-in">
            <div className="card-header"><h3 className="card-title">Approved ({approvedSubmissions.length})</h3></div>
            <div className="card-body" style={{ padding: 0 }}>
              <table className="data-table">
                <thead>
                  <tr><th>Student</th><th>AI Score</th><th>Final Score</th><th>Teacher Feedback</th></tr>
                </thead>
                <tbody>
                  {approvedSubmissions.map((sub, i) => (
                    <tr key={i}>
                      <td><b>{sub.student_name}</b><br /><small>{sub.student_reg}</small></td>
                      <td>{sub.ai_score}/100</td>
                      <td><span className="badge badge-success">{sub.teacher_score}/100</span></td>
                      <td style={{ maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{sub.teacher_feedback || 'No additional feedback'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {submissions.length === 0 && <EmptyState title="No Submissions Yet" icon="FileText" message="Students haven't submitted any assignments yet." />}
      </>
    )
  }

  // Assignments List View
  if (selectedCourse) {
    return (
      <>
        <div className="page-header">
          <button className="btn btn-sm btn-ghost" onClick={() => setSelectedCourse(null)} style={{ marginBottom: '10px' }}>← Back to Courses</button>
          <h1 className="page-title">{selectedCourse.course_name}</h1>
          <p className="page-description">Assignments & AI Grading</p>
        </div>

        <div className="schools-grid fade-in">
          {assignments.map((assignment, i) => (
            <div key={i} className="card" onClick={() => handleAssignmentSelect(assignment)} style={{ cursor: 'pointer' }}>
              <div className="card-body">
                <h3 style={{ margin: 0, fontSize: '18px', marginBottom: '8px' }}>{assignment.assignment_title}</h3>
                <p style={{ fontSize: '14px', color: 'var(--text-muted)', marginBottom: '12px' }}>{assignment.description}</p>
                <div style={{ display: 'flex', gap: '12px', fontSize: '13px', marginBottom: '12px' }}>
                  <span>📅 Due: {assignment.due_date}</span>
                  <span>📊 Max: {assignment.max_score} pts</span>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <span className="badge badge-info">{assignment.submission_count} Submissions</span>
                  {assignment.pending_review > 0 && (
                    <span className="badge badge-warning">{assignment.pending_review} Pending</span>
                  )}
                </div>
              </div>
            </div>
          ))}
          {assignments.length === 0 && <EmptyState title="No Assignments" icon="FileText" message="No assignments created for this course yet." />}
        </div>
      </>
    )
  }

  // Courses List View
  return (
    <>
      <div className="page-header">
        <h1 className="page-title">AI Grading Dashboard</h1>
        <p className="page-description">Review AI-graded assignments and verify scores</p>
      </div>
      <div className="schools-grid fade-in">
        {courses.map((c, i) => (
          <div key={i} className="card" onClick={() => handleCourseSelect(c)} style={{ cursor: 'pointer' }}>
            <div className="card-body">
              <h3 style={{ margin: 0, fontSize: '18px' }}>{c.course_name}</h3>
              <div style={{ color: 'var(--text-dim)', fontSize: '14px', fontFamily: 'monospace', margin: '4px 0' }}>{c.course_code}</div>
              <div style={{ marginTop: '12px', fontSize: '13px', color: 'var(--text-muted)' }}>
                <span>📚 Semester {c.semester}</span> • <span>👥 {c.total_students} Students</span>
              </div>
            </div>
          </div>
        ))}
        {courses.length === 0 && <EmptyState title="No Courses" icon="Book" message="You don't have any courses assigned." />}
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
    await new Promise(r => setTimeout(r, 2000))
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
        <h1 className="page-title">AI Attendance</h1>
        <p className="page-description">Automated Face Recognition Attendance System</p>
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
                  <div className="upload-title">Click to upload photo</div>
                  <div className="upload-hint">JPG/PNG supported</div>
                </>
              )}
            </div>

            <button className="btn btn-primary" style={{ width: '100%', marginTop: '16px' }} onClick={handleUpload} disabled={!image || processing}>
              {processing ? 'Processing...' : 'Mark Attendance'}
            </button>
          </div>
        </div>

        <div className="card">
          <div className="card-header"><h3 className="card-title">Results</h3></div>
          <div className="card-body">
            {result ? (
              <>
                <div className="stats-mini">
                  <div className="stat-mini"><span className="stat-mini-value">{result.faces_detected}</span><span>Detected</span></div>
                  <div className="stat-mini"><span className="stat-mini-value" style={{ color: 'var(--success)' }}>{result.students_recognized}</span><span>Recognized</span></div>
                  <div className="stat-mini"><span className="stat-mini-value" style={{ color: 'var(--warning)' }}>{result.unknown_faces}</span><span>Unknown</span></div>
                </div>
                <div style={{ marginTop: '16px' }}>
                  {result.students.map((s, i) => (
                    <div key={i} className="recognized-student">
                      <span>{s.name}</span>
                      <span className="badge badge-success">{s.confidence}%</span>
                    </div>
                  ))}
                </div>
              </>
            ) : <EmptyState title="No Results" icon="Target" message="Upload a photo to see results." />}
          </div>
        </div>
      </div>
    </>
  )
}

function TeacherNotifications() {
  const [sent, setSent] = useState(false)

  const handleSend = () => {
    setSent(true)
    setTimeout(() => setSent(false), 3000)
  }

  return (
    <>
      <div className="page-header"><h1 className="page-title">Send Notifications</h1></div>
      <div className="card fade-in">
        <div className="card-body">
          <div className="form-group">
            <label className="form-label">Type</label>
            <select className="form-select"><option>Announcement</option><option>Class Canceled</option></select>
          </div>
          <div className="form-group">
            <label className="form-label">Message</label>
            <textarea className="form-textarea" rows="4" placeholder="Enter message..."></textarea>
          </div>
          {sent && <div className="success-banner">Notification sent!</div>}
          <button className="btn btn-primary" onClick={handleSend}>Send Notification</button>
        </div>
      </div>
    </>
  )
}

// ============================================
// STUDENT COMPONENTS
// ============================================

function StudentDashboard({ user }) {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const trend = [1, 2, 3, 4, 5, 6, 7]

  useEffect(() => {
    async function loadData() {
      try {
        // Use student_id from user object
        const studentId = user.student_id || 's-SCIS-1-0' // Fallback for demo
        const data = await fetchAPI(`/data/student/dashboard?student_id=${studentId}`)
        setStats(data)
      } catch (e) {
        console.error('Error loading student data:', e)
        setStats({ attendance_rate: 0, total_classes: 0, attended: 0, absent_days: 0, avg_grade: 0, total_courses: 0, total_submissions: 0, pending_submissions: 0 })
      }
      setLoading(false)
    }
    loadData()
  }, [user])

  if (loading) return <LoadingSpinner />

  const attendanceStatus = stats.attendance_rate >= 75 ? 'success' : 'warning'

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Student Dashboard</h1>
        <p className="page-description">Welcome back, {user.full_name}</p>
      </div>

      <div className="stats-grid fade-in">
        <StatCard 
          label="Attendance" 
          value={`${stats.attendance_rate.toFixed(1)}%`} 
          data={trend} 
          positive={stats.attendance_rate >= 75} 
          variant={attendanceStatus} 
          icon="Clock" 
        />
        <StatCard 
          label="Average Grade" 
          value={stats.avg_grade.toFixed(1)} 
          data={trend} 
          positive={stats.avg_grade >= 70} 
          variant={stats.avg_grade >= 70 ? 'success' : 'warning'} 
          icon="CheckCircle" 
        />
        <StatCard 
          label="Total Courses" 
          value={stats.total_courses} 
          data={trend} 
          positive={true} 
          icon="Book" 
        />
        <StatCard 
          label="Assignments" 
          value={stats.total_submissions} 
          data={trend} 
          positive={true} 
          variant="info" 
          icon="FileText" 
        />
      </div>

      <div className="content-grid content-grid-equal fade-in" style={{ marginTop: '20px' }}>
        <div className="card">
          <div className="card-header"><h3 className="card-title">Attendance Summary</h3></div>
          <div className="card-body">
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Total Classes</span>
                <span className="info-value">{stats.total_classes}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Attended</span>
                <span className="info-value" style={{ color: 'var(--success)' }}>{stats.attended}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Absent</span>
                <span className="info-value" style={{ color: 'var(--danger)' }}>{stats.absent_days}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Attendance Rate</span>
                <span className="info-value" style={{ color: stats.attendance_rate >= 75 ? 'var(--success)' : 'var(--warning)' }}>
                  {stats.attendance_rate.toFixed(1)}%
                </span>
              </div>
            </div>
            {stats.attendance_rate < 75 && (
              <div style={{ marginTop: '16px', padding: '12px', background: 'var(--warning-bg)', borderRadius: '8px', fontSize: '14px' }}>
                ⚠️ Your attendance is below 75%. Please attend classes regularly to avoid academic issues.
              </div>
            )}
          </div>
        </div>

        <div className="card">
          <div className="card-header"><h3 className="card-title">My Profile</h3></div>
          <div className="card-body">
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Reg. No</span>
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
      </div>

      {stats.pending_submissions > 0 && (
        <div className="card fade-in" style={{ marginTop: '20px' }}>
          <div className="card-body" style={{ padding: '16px', background: 'var(--info-bg)', borderLeft: '4px solid var(--info)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ fontSize: '24px' }}>📝</div>
              <div>
                <strong>You have {stats.pending_submissions} assignment{stats.pending_submissions > 1 ? 's' : ''} pending review</strong>
                <div style={{ fontSize: '14px', color: 'var(--text-muted)', marginTop: '4px' }}>
                  Your submissions are being graded by AI and reviewed by your teachers.
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

function StudentGrades({ user }) {
  const [gradesBySemester, setGradesBySemester] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const studentId = user.student_id || 's-SCIS-1-0' // Fallback for demo
        const data = await fetchAPI(`/data/student/${studentId}/grades`)
        
        // Group grades by semester
        const grouped = (data || []).reduce((acc, grade) => {
          const sem = grade.semester || 1
          if (!acc[sem]) acc[sem] = []
          acc[sem].push(grade)
          return acc
        }, {})
        
        setGradesBySemester(grouped)
      } catch (e) {
        console.error('Error loading grades:', e)
      }
      setLoading(false)
    }
    load()
  }, [user])

  if (loading) return <LoadingSpinner />

  const allGrades = Object.values(gradesBySemester).flat()

  // Calculate overall statistics
  const avgGrade = allGrades.length > 0 
    ? (allGrades.reduce((sum, g) => sum + g.current_grade, 0) / allGrades.length).toFixed(1)
    : 0

  const getGradeColor = (status) => {
    switch (status) {
      case 'Excellent': return 'var(--success)'
      case 'Good': return 'var(--info)'
      case 'At Risk': return 'var(--warning)'
      case 'Critical': return 'var(--danger)'
      default: return 'var(--text-primary)'
    }
  }

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">My Grades</h1>
        <p className="page-description">View your academic performance across all courses</p>
      </div>

      {allGrades.length > 0 && (
        <div className="stats-grid fade-in" style={{ marginBottom: '20px' }}>
          <div className="stat-card">
            <div className="stat-value">{avgGrade}</div>
            <div className="stat-label">Overall Average</div>
          </div>
          <div className="stat-card success">
            <div className="stat-value">{allGrades.filter(g => g.status === 'Excellent' || g.status === 'Good').length}</div>
            <div className="stat-label">Performing Well</div>
          </div>
          <div className="stat-card warning">
            <div className="stat-value">{allGrades.filter(g => g.status === 'At Risk' || g.status === 'Critical').length}</div>
            <div className="stat-label">Need Improvement</div>
          </div>
          <div className="stat-card info">
            <div className="stat-value">{allGrades.length}</div>
            <div className="stat-label">Total Courses</div>
          </div>
        </div>
      )}

      {Object.keys(gradesBySemester).length > 0 ? (
        Object.entries(gradesBySemester).sort(([a], [b]) => parseInt(a) - parseInt(b)).map(([semester, grades]) => (
          <div key={semester} className="card fade-in" style={{ marginBottom: '20px' }}>
            <div className="card-header">
              <h3 className="card-title">Semester {semester}</h3>
              <span className="badge">{grades.length} Courses</span>
            </div>
            <div className="card-body" style={{ padding: 0 }}>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Course</th>
                    <th>Midterm</th>
                    <th>Assignments</th>
                    <th>Quizzes</th>
                    <th>Current Grade</th>
                    <th>Letter</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {grades.map((grade, i) => (
                    <tr key={i}>
                      <td>
                        <b>{grade.course_code}</b>
                        <br />
                        <small style={{ color: 'var(--text-muted)' }}>{grade.course_name}</small>
                      </td>
                      <td>{grade.midterm_score.toFixed(1)}</td>
                      <td>{grade.assignment_avg.toFixed(1)}</td>
                      <td>{grade.quiz_avg.toFixed(1)}</td>
                      <td><b style={{ color: getGradeColor(grade.status) }}>{grade.current_grade.toFixed(1)}</b></td>
                      <td><span className={`badge badge-${grade.status === 'Excellent' || grade.status === 'Good' ? 'success' : 'warning'}`}>{grade.grade_letter}</span></td>
                      <td>
                        <span style={{ color: getGradeColor(grade.status), fontSize: '13px' }}>
                          {grade.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))
      ) : (
        <EmptyState title="No Grades Available" icon="Book" message="Your grades haven't been published yet." />
      )}

      {allGrades.some(g => g.status === 'At Risk' || g.status === 'Critical') && (
        <div className="card fade-in" style={{ marginTop: '20px' }}>
          <div className="card-body" style={{ padding: '16px', background: 'var(--warning-bg)', borderLeft: '4px solid var(--warning)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ fontSize: '24px' }}>⚠️</div>
              <div>
                <strong>Academic Alert</strong>
                <div style={{ fontSize: '14px', color: 'var(--text-muted)', marginTop: '4px' }}>
                  You have courses that need attention. Please consult with your teachers or use the AI Assistant for study recommendations.
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

function StudentCourses({ user }) {
  const [coursesBySemester, setCoursesBySemester] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const studentId = user.student_id || 's-SCIS-1-0' // Fallback for demo
        const data = await fetchAPI(`/data/student/${studentId}/courses`)
        setCoursesBySemester(data || {})
      } catch (e) {
        console.error('Error loading courses:', e)
      }
      setLoading(false)
    }
    load()
  }, [user])

  if (loading) return <LoadingSpinner />

  const allCourses = Object.values(coursesBySemester).flat()
  const avgGrade = allCourses.length > 0 
    ? (allCourses.reduce((sum, c) => sum + c.current_grade, 0) / allCourses.length).toFixed(1)
    : 0
  const avgAttendance = allCourses.length > 0
    ? (allCourses.reduce((sum, c) => sum + c.attendance_rate, 0) / allCourses.length).toFixed(1)
    : 0

  const getStatusColor = (status) => {
    switch (status) {
      case 'Excellent': return 'success'
      case 'Good': return 'info'
      case 'Needs Support': return 'warning'
      case 'At Risk': return 'warning'
      case 'Critical': return 'danger'
      default: return 'info'
    }
  }

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">My Courses</h1>
        <p className="page-description">View all your enrolled courses by semester</p>
      </div>

      {allCourses.length > 0 && (
        <div className="stats-grid fade-in" style={{ marginBottom: '20px' }}>
          <div className="stat-card info">
            <div className="stat-value">{allCourses.length}</div>
            <div className="stat-label">Total Courses</div>
          </div>
          <div className="stat-card success">
            <div className="stat-value">{avgGrade}</div>
            <div className="stat-label">Average Grade</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{avgAttendance}%</div>
            <div className="stat-label">Average Attendance</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{Object.keys(coursesBySemester).length}</div>
            <div className="stat-label">Semesters</div>
          </div>
        </div>
      )}

      {Object.keys(coursesBySemester).length > 0 ? (
        Object.entries(coursesBySemester).sort(([a], [b]) => parseInt(a) - parseInt(b)).map(([semester, courses]) => (
          <div key={semester} className="card fade-in" style={{ marginBottom: '20px' }}>
            <div className="card-header">
              <h3 className="card-title">Semester {semester}</h3>
              <span className="badge">{courses.length} Courses</span>
            </div>
            <div className="card-body" style={{ padding: 0 }}>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Course Code</th>
                    <th>Course Name</th>
                    <th>Current Grade</th>
                    <th>Letter Grade</th>
                    <th>Attendance</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {courses.map((course, i) => (
                    <tr key={i}>
                      <td><span className="badge">{course.course_code}</span></td>
                      <td><b>{course.course_name}</b></td>
                      <td><b>{course.current_grade.toFixed(1)}</b></td>
                      <td><span className={`badge badge-${getStatusColor(course.status)}`}>{course.grade_letter}</span></td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <div className="progress-bar" style={{ flex: 1, maxWidth: '100px' }}>
                            <div className="progress-fill" style={{ 
                              width: `${course.attendance_rate}%`,
                              background: course.attendance_rate >= 75 ? 'var(--success)' : 'var(--warning)'
                            }}></div>
                          </div>
                          <span style={{ fontSize: '13px', color: course.attendance_rate >= 75 ? 'var(--success)' : 'var(--warning)' }}>
                            {course.attendance_rate.toFixed(0)}%
                          </span>
                        </div>
                        <small style={{ color: 'var(--text-muted)', fontSize: '12px' }}>
                          {course.attended}/{course.total_classes} classes
                        </small>
                      </td>
                      <td>
                        <span className={`badge badge-${getStatusColor(course.status)}`}>
                          {course.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))
      ) : (
        <EmptyState title="No Courses Found" icon="Book" message="You are not enrolled in any courses yet." />
      )}
    </>
  )
}

function StudentAssignments({ user }) {
  const [assignments, setAssignments] = useState([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [uploadSuccess, setUploadSuccess] = useState(null)
  const [selectedAssignment, setSelectedAssignment] = useState(null)
  const fileInputRef = useRef(null)

  useEffect(() => {
    async function load() {
      try {
        const studentId = user.student_id || 's-SCIS-1-0' // Fallback for demo
        const data = await fetchAPI(`/data/student/${studentId}/assignments`)
        setAssignments(data || [])
      } catch (e) {
        console.error('Error loading assignments:', e)
      }
      setLoading(false)
    }
    load()
  }, [user])

  const handleFileUpload = async (event, assignment) => {
    const file = event.target.files[0]
    if (!file) return

    // Validate file type
    if (!file.name.endsWith('.txt')) {
      alert('Please upload a .txt file only')
      return
    }

    setUploading(true)
    setUploadSuccess(null)

    try {
      // Read file content
      const text = await file.text()
      
      // Submit to backend for AI grading
      const response = await fetch(`${API_BASE}/grading/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_id: user.student_id || 's-SCIS-1-0',
          student_name: user.name,
          assignment_id: assignment.assignment_id,
          assignment_title: assignment.assignment_title,
          course_code: assignment.course_code,
          submission_text: text,
          max_score: assignment.max_score
        })
      })

      if (response.ok) {
        const result = await response.json()
        setUploadSuccess({
          assignment: assignment.assignment_title,
          ai_score: result.ai_score,
          ai_feedback: result.ai_feedback
        })
        
        // Reload assignments to show updated status
        const studentId = user.student_id || 's-SCIS-1-0'
        const data = await fetchAPI(`/data/student/${studentId}/assignments`)
        setAssignments(data || [])
      } else {
        alert('Failed to submit assignment. Please try again.')
      }
    } catch (error) {
      console.error('Upload error:', error)
      alert('Error uploading file. Please try again.')
    } finally {
      setUploading(false)
      if (fileInputRef.current) fileInputRef.current.value = ''
    }
  }

  if (loading) return <LoadingSpinner />

  const pendingAssignments = assignments.filter(a => !a.submitted)
  const submittedAssignments = assignments.filter(a => a.submitted)
  const gradedAssignments = submittedAssignments.filter(a => a.teacher_verified)

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">My Assignments</h1>
        <p className="page-description">Track your assignments and view AI-graded feedback</p>
      </div>

      {uploadSuccess && (
        <div className="card fade-in" style={{ marginBottom: '20px', background: 'rgba(34, 197, 94, 0.1)', borderColor: 'var(--success)' }}>
          <div className="card-body">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ color: 'var(--success)' }}>{Icons.CheckCircle()}</div>
              <div>
                <h4 style={{ color: 'var(--success)', marginBottom: '4px' }}>Submission Successful!</h4>
                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0 }}>
                  <b>{uploadSuccess.assignment}</b> has been submitted and graded by AI. 
                  Score: <b>{uploadSuccess.ai_score}</b> • Awaiting teacher review.
                </p>
              </div>
              <button className="btn btn-sm btn-ghost" onClick={() => setUploadSuccess(null)} style={{ marginLeft: 'auto' }}>×</button>
            </div>
          </div>
        </div>
      )}

      <div className="stats-grid fade-in" style={{ marginBottom: '20px' }}>
        <div className="stat-card warning">
          <div className="stat-value">{pendingAssignments.length}</div>
          <div className="stat-label">Not Submitted</div>
        </div>
        <div className="stat-card info">
          <div className="stat-value">{submittedAssignments.length - gradedAssignments.length}</div>
          <div className="stat-label">Under Review</div>
        </div>
        <div className="stat-card success">
          <div className="stat-value">{gradedAssignments.length}</div>
          <div className="stat-label">Graded</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{assignments.length}</div>
          <div className="stat-label">Total Assignments</div>
        </div>
      </div>

      {pendingAssignments.length > 0 && (
        <div className="card fade-in" style={{ marginBottom: '20px' }}>
          <div className="card-header">
            <h3 className="card-title">Pending Submissions ({pendingAssignments.length})</h3>
          </div>
          <div className="card-body" style={{ padding: 0 }}>
            <table className="data-table">
              <thead>
                <tr><th>Course</th><th>Assignment</th><th>Due Date</th><th>Max Score</th><th>Action</th></tr>
              </thead>
              <tbody>
                {pendingAssignments.map((assignment, i) => (
                  <tr key={i}>
                    <td><b>{assignment.course_code}</b></td>
                    <td>{assignment.assignment_title}</td>
                    <td>{assignment.due_date}</td>
                    <td>{assignment.max_score}</td>
                    <td>
                      <input
                        ref={fileInputRef}
                        type="file"
                        accept=".txt"
                        style={{ display: 'none' }}
                        onChange={(e) => handleFileUpload(e, assignment)}
                        id={`file-upload-${i}`}
                      />
                      <label htmlFor={`file-upload-${i}`} className="btn btn-sm btn-primary" style={{ cursor: 'pointer', margin: 0 }}>
                        {uploading ? 'Uploading...' : 'Upload .txt'}
                      </label>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {gradedAssignments.length > 0 && (
        <div className="card fade-in" style={{ marginBottom: '20px' }}>
          <div className="card-header">
            <h3 className="card-title">Graded Assignments ({gradedAssignments.length})</h3>
          </div>
          <div className="card-body" style={{ padding: 0 }}>
            <table className="data-table">
              <thead>
                <tr><th>Course</th><th>Assignment</th><th>AI Score</th><th>Final Score</th><th>Feedback</th></tr>
              </thead>
              <tbody>
                {gradedAssignments.map((assignment, i) => (
                  <tr key={i}>
                    <td><b>{assignment.course_code}</b></td>
                    <td>{assignment.assignment_title}</td>
                    <td><span className="badge badge-info">{assignment.ai_score}/{assignment.max_score}</span></td>
                    <td><span className="badge badge-success">{assignment.teacher_score}/{assignment.max_score}</span></td>
                    <td style={{ maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {assignment.teacher_feedback || assignment.ai_feedback}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {submittedAssignments.length > gradedAssignments.length && (
        <div className="card fade-in">
          <div className="card-header">
            <h3 className="card-title">Under Review ({submittedAssignments.length - gradedAssignments.length})</h3>
          </div>
          <div className="card-body" style={{ padding: 0 }}>
            <table className="data-table">
              <thead>
                <tr><th>Course</th><th>Assignment</th><th>AI Score</th><th>AI Feedback</th><th>Status</th></tr>
              </thead>
              <tbody>
                {submittedAssignments.filter(a => !a.teacher_verified).map((assignment, i) => (
                  <tr key={i}>
                    <td><b>{assignment.course_code}</b></td>
                    <td>{assignment.assignment_title}</td>
                    <td><span className="badge badge-info">{assignment.ai_score}/{assignment.max_score}</span></td>
                    <td style={{ maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {assignment.ai_feedback}
                    </td>
                    <td><span className="badge badge-warning">Teacher Review</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {assignments.length === 0 && (
        <EmptyState title="No Assignments" icon="FileText" message="You don't have any assignments yet." />
      )}
    </>
  )
}

function StudentAttendance({ user }) {
  const [attendance, setAttendance] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const studentId = user.student_id || 's-SCIS-1-0' // Fallback for demo
        const data = await fetchAPI(`/data/student/dashboard?student_id=${studentId}`)
        setAttendance(data)
      } catch (e) {
        console.error('Error loading attendance:', e)
      }
      setLoading(false)
    }
    load()
  }, [user])

  if (loading) return <LoadingSpinner />

  const attendanceRate = attendance?.attendance_rate || 0
  const totalClasses = attendance?.total_classes || 0
  const attended = attendance?.attended || 0
  const absentDays = attendance?.absent_days || 0
  const lateDays = 0 // Not in current data structure

  const getAttendanceStatus = () => {
    if (attendanceRate >= 90) return { label: 'Excellent', color: 'success' }
    if (attendanceRate >= 75) return { label: 'Good', color: 'info' }
    if (attendanceRate >= 60) return { label: 'Warning', color: 'warning' }
    return { label: 'Critical', color: 'danger' }
  }

  const status = getAttendanceStatus()

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">My Attendance</h1>
        <p className="page-description">Track your class attendance and maintain good academic standing</p>
      </div>

      <div className="stats-grid fade-in" style={{ marginBottom: '20px' }}>
        <div className={`stat-card ${status.color}`}>
          <div className="stat-value">{attendanceRate.toFixed(1)}%</div>
          <div className="stat-label">Attendance Rate</div>
        </div>
        <div className="stat-card success">
          <div className="stat-value">{attended}</div>
          <div className="stat-label">Classes Attended</div>
        </div>
        <div className="stat-card danger">
          <div className="stat-value">{absentDays}</div>
          <div className="stat-label">Absent Days</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{totalClasses}</div>
          <div className="stat-label">Total Classes</div>
        </div>
      </div>

      <div className="content-grid content-grid-equal fade-in">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Attendance Summary</h3>
            <span className={`badge badge-${status.color}`} style={{ marginLeft: '8px' }}>{status.label}</span>
          </div>
          <div className="card-body">
            <div style={{ marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span>Attendance Progress</span>
                <span><b>{attendanceRate.toFixed(1)}%</b></span>
              </div>
              <div className="progress-bar" style={{ height: '12px' }}>
                <div 
                  className="progress-fill" 
                  style={{ 
                    width: `${attendanceRate}%`,
                    background: attendanceRate >= 75 ? 'var(--success)' : 'var(--warning)'
                  }}
                ></div>
              </div>
            </div>

            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Total Classes</span>
                <span className="info-value">{totalClasses}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Attended</span>
                <span className="info-value" style={{ color: 'var(--success)' }}>{attended}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Absent</span>
                <span className="info-value" style={{ color: 'var(--danger)' }}>{absentDays}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Remaining</span>
                <span className="info-value">{totalClasses - attended - absentDays}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header"><h3 className="card-title">Attendance Guidelines</h3></div>
          <div className="card-body">
            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <span className="badge badge-success">Excellent</span>
                <span style={{ fontSize: '14px' }}>≥ 90%</span>
              </div>
              <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginLeft: '24px' }}>
                Outstanding attendance. Keep up the great work!
              </p>
            </div>

            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <span className="badge badge-info">Good</span>
                <span style={{ fontSize: '14px' }}>75% - 89%</span>
              </div>
              <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginLeft: '24px' }}>
                Meeting minimum requirements. Try to improve further.
              </p>
            </div>

            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <span className="badge badge-warning">Warning</span>
                <span style={{ fontSize: '14px' }}>60% - 74%</span>
              </div>
              <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginLeft: '24px' }}>
                Below requirements. Immediate improvement needed.
              </p>
            </div>

            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <span className="badge badge-danger">Critical</span>
                <span style={{ fontSize: '14px' }}>&lt; 60%</span>
              </div>
              <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginLeft: '24px' }}>
                Critical level. May affect academic eligibility.
              </p>
            </div>
          </div>
        </div>
      </div>

      {attendanceRate < 75 && (
        <div className="card fade-in" style={{ marginTop: '20px' }}>
          <div className="card-body" style={{ padding: '16px', background: 'var(--warning-bg)', borderLeft: '4px solid var(--warning)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ fontSize: '24px' }}>⚠️</div>
              <div>
                <strong>Attendance Alert</strong>
                <div style={{ fontSize: '14px', color: 'var(--text-muted)', marginTop: '4px' }}>
                  Your attendance is below the required 75%. Please attend classes regularly to avoid academic consequences. 
                  Contact your teachers if you have any concerns.
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {attendanceRate >= 90 && (
        <div className="card fade-in" style={{ marginTop: '20px' }}>
          <div className="card-body" style={{ padding: '16px', background: 'var(--success-bg)', borderLeft: '4px solid var(--success)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ fontSize: '24px' }}>🎉</div>
              <div>
                <strong>Excellent Attendance!</strong>
                <div style={{ fontSize: '14px', color: 'var(--text-muted)', marginTop: '4px' }}>
                  You're maintaining excellent attendance. Keep up the great work!
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

function AIAssistant() {
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Hi! I am your academic AI assistant. Ask me about your courses, schedule, or resources.' }
  ])
  const [input, setInput] = useState('')

  const send = () => {
    if (!input.trim()) return
    setMessages([...messages, { role: 'user', text: input }])
    setInput('')
    setTimeout(() => {
      setMessages(prev => [...prev, { role: 'bot', text: 'I can help with that! However, I am in demo mode right now.' }])
    }, 1000)
  }

  return (
    <>
      <div className="page-header"><h1 className="page-title">AI Assistant</h1></div>
      <div className="card fade-in" style={{ height: '500px', display: 'flex', flexDirection: 'column' }}>
        <div style={{ flex: 1, overflowY: 'auto', padding: '20px' }}>
          {messages.map((m, i) => (
            <div key={i} style={{
              marginBottom: '10px',
              textAlign: m.role === 'user' ? 'right' : 'left'
            }}>
              <span style={{
                display: 'inline-block',
                padding: '8px 16px',
                borderRadius: '16px',
                background: m.role === 'user' ? 'var(--primary)' : 'var(--surface-active)',
                color: 'var(--text-primary)'
              }}>{m.text}</span>
            </div>
          ))}
        </div>
        <div style={{ padding: '16px', borderTop: '1px solid var(--border)', display: 'flex', gap: '10px' }}>
          <input className="form-input" value={input} onChange={e => setInput(e.target.value)} onKeyPress={e => e.key === 'Enter' && send()} placeholder="Type a message..." />
          <button className="btn btn-primary" onClick={send}>{Icons.Message()}</button>
        </div>
      </div>
    </>
  )
}


// ============================================
// LOGIN & APP SHELL
// ============================================

function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [selectedRole, setSelectedRole] = useState('student')

  const demoCredentials = {
    admin: { email: 'admin@uohyd.ac.in', hint: 'Full system access' },
    teacher: { email: 'teacher@uohyd.ac.in', hint: 'Department view' },
    student: { email: 'student@uohyd.ac.in', hint: 'Personal dashboard' }
  }

  const handleDemoLogin = (role) => {
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
        method: 'POST', body: JSON.stringify({ email, password })
      })
      if (response.success) {
        localStorage.setItem('uoh_user', JSON.stringify(response.user))
        onLogin(response.user)
      } else {
        throw new Error(response.detail || 'Login failed')
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
          <div className="login-logo"><div className="logo-mark">TRACE</div><div><div className="login-title">TRACE</div><div className="login-subtitle">Transparent Results & Attendance Compliance Engine</div></div></div>
        </div>
        <div className="login-roles">
          {Object.keys(demoCredentials).map(role => (
            <button key={role} className={`role-btn ${selectedRole === role ? 'active' : ''}`} onClick={() => handleDemoLogin(role)}>
              {role === 'admin' ? Icons.Settings() : role === 'teacher' ? Icons.GraduationCap() : Icons.Users()}
              <span>{role.charAt(0).toUpperCase() + role.slice(1)}</span>
            </button>
          ))}
        </div>
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input className="form-input" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input className="form-input" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          </div>
          {error && <div className="login-error">{error}</div>}
          <button type="submit" className="btn btn-primary btn-login" disabled={loading}>{loading ? 'Signing In...' : 'Sign In'}</button>
          <div className="login-hint"><strong>Demo Mode:</strong> Password is <code>demo123</code></div>
        </form>
      </div>
    </div>
  )
}

function Sidebar({ activeNav, setActiveNav, user, onLogout }) {
  const getNavItems = () => {
    if (user.role === 'admin') {
      return [
        { group: 'Admin', items: [{ id: 'dashboard', label: 'Dashboard', icon: 'Dashboard' }, { id: 'schools', label: 'Schools', icon: 'Building' }, { id: 'students', label: 'Students', icon: 'Users' }] },
        { group: 'Analytics', items: [{ id: 'analytics', label: 'Analytics', icon: 'BarChart' }, { id: 'risk', label: 'Risk Monitor', icon: 'AlertTriangle' }] }
      ]
    } else if (user.role === 'teacher') {
      return [
        { group: 'Teaching', items: [{ id: 'dashboard', label: 'Dashboard', icon: 'Dashboard' }, { id: 'courses', label: 'My Courses', icon: 'Book' }, { id: 'ai-grading', label: 'AI Grading', icon: 'CheckCircle' }, { id: 'face-attendance', label: 'AI Attendance', icon: 'Camera' }] },
        { group: 'Students', items: [{ id: 'my-students', label: 'Student Directory', icon: 'Users' }, { id: 'alerts', label: 'Risk Alerts', icon: 'AlertTriangle' }] },
        { group: 'Tools', items: [{ id: 'notifications', label: 'Notifications', icon: 'Bell' }, { id: 'resources', label: 'Resources', icon: 'Upload' }] }
      ]
    } else {
      return [
        { group: 'Learning', items: [{ id: 'dashboard', label: 'Dashboard', icon: 'Dashboard' }, { id: 'courses', label: 'My Courses', icon: 'Book' }, { id: 'grades', label: 'My Grades', icon: 'CheckCircle' }, { id: 'assignments', label: 'Assignments', icon: 'FileText' }, { id: 'attendance', label: 'Attendance', icon: 'Clock' }] },
        { group: 'Resources', items: [{ id: 'resources', label: 'Study Materials', icon: 'FileText' }, { id: 'ai-assistant', label: 'AI Assistant', icon: 'Bot' }] }
      ]
    }
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-header"><div className="logo"><div className="logo-mark">TRACE</div><span className="logo-text">TRACE</span></div></div>
      <nav className="nav-container">
        {getNavItems().map((group, i) => (
          <div key={i} className="nav-group">
            <div className="nav-group-title">{group.group}</div>
            {group.items.map(item => (
              <div key={item.id} className={`nav-item ${activeNav === item.id ? 'active' : ''}`} onClick={() => setActiveNav(item.id)}>
                {Icons[item.icon] ? Icons[item.icon]() : Icons.FileText()}
                <span>{item.label}</span>
              </div>
            ))}
          </div>
        ))}
      </nav>
      <div className="sidebar-footer">
        <div className="user-card">
          <div className="user-avatar">{user.full_name?.substring(0, 2)}</div>
          <div className="user-info"><div className="user-name">{user.full_name}</div><div className="user-role">{user.role}</div></div>
        </div>
        <button className="btn btn-ghost btn-sm" onClick={onLogout} style={{ width: '100%', marginTop: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px', fontSize: '13px', padding: '6px 12px' }}>
          <span style={{ width: '16px', height: '16px' }}>{Icons.LogOut()}</span>
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  )
}

function TopBar({ title, user, theme, toggleTheme }) {
  return (
    <header className="topbar">
      <div className="topbar-left"><div className="breadcrumb"><span>UoH Academic</span><span style={{ margin: '0 8px' }}>/</span><span className="breadcrumb-current">{title}</span></div></div>
      <div className="topbar-right">
        <button className="icon-btn" onClick={toggleTheme} title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}>
          {theme === 'dark' ? Icons.Sun() : Icons.Moon()}
        </button>
        <span className={`role-badge role-${user.role}`}>{user.role}</span>
      </div>
    </header>
  )
}

function App() {
  const [user, setUser] = useState(null)
  const [activeNav, setActiveNav] = useState('dashboard')
  const [selectedSchool, setSelectedSchool] = useState(null)
  const [loading, setLoading] = useState(true)
  const [theme, setTheme] = useState(() => {
    // Load theme from localStorage or default to 'dark'
    return localStorage.getItem('uoh_theme') || 'dark'
  })

  // Apply theme to document root
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('uoh_theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'dark' ? 'light' : 'dark')
  }

  useEffect(() => {
    const savedUser = localStorage.getItem('uoh_user')
    if (savedUser) setUser(JSON.parse(savedUser))
    setLoading(false)
  }, [])

  const handleLogin = (u) => { setUser(u); setActiveNav('dashboard') }
  const handleLogout = () => { 
    localStorage.removeItem('uoh_user')
    setUser(null)
    setActiveNav('dashboard')
    // Force a clean state reset
    window.location.reload()
  }

  if (loading) return <div className="loading-screen">Loading...</div>
  if (!user) return <LoginPage onLogin={handleLogin} />

  const renderPage = () => {
    const commonProps = { user }
    // Role based routing
    if (user.role === 'admin') {
      switch (activeNav) {
        case 'dashboard': return <AdminDashboard {...commonProps} />
        case 'schools': return <AdminSchoolsView onSelectSchool={(code) => { setSelectedSchool(code); setActiveNav('school-details') }} />
        case 'school-details': return <SchoolDetailsView code={selectedSchool} onBack={() => setActiveNav('schools')} />
        case 'students': return <AdminStudentsView {...commonProps} />
        case 'analytics': return <AdminAnalyticsView />
        case 'risk': return <RiskMonitorView {...commonProps} />
        default: return <EmptyState title="Coming Soon" icon="Settings" message="This admin module is under development." />
      }
    } else if (user.role === 'teacher') {
      switch (activeNav) {
        case 'dashboard': return <TeacherDashboard {...commonProps} />
        case 'courses': return <TeacherCoursesView {...commonProps} />
        case 'ai-grading': return <AIGradingView {...commonProps} />
        case 'face-attendance': return <FaceAttendance {...commonProps} />
        case 'my-students': return <AdminStudentsView {...commonProps} /> // Reuse
        case 'alerts': return <RiskMonitorView {...commonProps} /> // Reuse
        case 'notifications': return <TeacherNotifications {...commonProps} />
        case 'resources': return <ResourcesView {...commonProps} />
        default: return <EmptyState title="Coming Soon" icon="Settings" message="This module is under development." />
      }
    } else {
      switch (activeNav) {
        case 'dashboard': return <StudentDashboard {...commonProps} />
        case 'courses': return <StudentCourses {...commonProps} />
        case 'grades': return <StudentGrades {...commonProps} />
        case 'assignments': return <StudentAssignments {...commonProps} />
        case 'attendance': return <StudentAttendance {...commonProps} />
        case 'resources': return <ResourcesView {...commonProps} />
        case 'ai-assistant': return <AIAssistant {...commonProps} />
        default: return <EmptyState title="Coming Soon" icon="Settings" message="This module is under development." />
      }
    }
  }

  const titles = { dashboard: 'Dashboard', students: 'Students', risk: 'Risk Monitor', courses: 'Courses', 'ai-grading': 'AI Grading', 'face-attendance': 'AI Attendance', 'my-students': 'My Students', alerts: 'Alerts', notifications: 'Notifications', resources: 'Resources', grades: 'Grades', assignments: 'Assignments', attendance: 'Attendance', 'ai-assistant': 'AI Assistant', schools: 'Schools', 'school-details': 'School Details', analytics: 'Analytics' }

  return (
    <div className="app">
      <Sidebar activeNav={activeNav} setActiveNav={setActiveNav} user={user} onLogout={handleLogout} />
      <main className="main-content">
        <TopBar title={titles[activeNav] || 'Dashboard'} user={user} theme={theme} toggleTheme={toggleTheme} />
        <div className="page-container">{renderPage()}</div>
      </main>
    </div>
  )
}

export default App
