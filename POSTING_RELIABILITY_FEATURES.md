# Posting Reliability Features Implementation

## ✅ Implemented Features

### 1. Real-time Status Updates (Server-Sent Events)
### 2. Detailed Error Logging with Screenshots
### 3. Health Check Endpoints for Account Validation

---

## 🚀 1. Real-time Status Updates (SSE)

### **New API Endpoints:**

#### **Stream Real-time Progress:**
```
GET /api/posts/status-stream/<job_id>/
```

**Usage in Frontend:**
```javascript
const eventSource = new EventSource(`http://localhost:8000/api/posts/status-stream/${jobId}/`, {
  withCredentials: true
});

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Progress:', data);
  
  // data structure:
  // {
  //   job_id: "uuid",
  //   status: "running", // or "completed", "failed"
  //   total_posts: 10,
  //   completed_posts: 3,
  //   failed_posts: 1,
  //   current_post_id: 45,
  //   current_post_title: "iPhone 13 Pro",
  //   progress_percentage: 30.0
  // }
  
  // Update UI with progress
  updateProgressBar(data.progress_percentage);
  updateCurrentPost(data.current_post_title);
  
  // Close connection when done
  if (data.final) {
    eventSource.close();
  }
};

eventSource.onerror = (error) => {
  console.error('SSE Error:', error);
  eventSource.close();
};
```

#### **Get Job Status (One-time):**
```
GET /api/posts/job-status/<job_id>/
```

**Response:**
```json
{
  "id": 1,
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "total_posts": 10,
  "completed_posts": 3,
  "failed_posts": 1,
  "current_post_id": 45,
  "current_post_title": "iPhone 13 Pro",
  "started_at": "2025-10-28T10:30:00Z",
  "completed_at": null,
  "progress_percentage": 30.0
}
```

### **Updated Start Posting Response:**

When you call `POST /api/posts/start-posting/`:

```json
{
  "success": true,
  "message": "Started posting process for 10 pending post(s)",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "pending_count": 10,
  "total_selected": 10,
  "log_file": "/path/to/logs/posting_process.log",
  "status_stream_url": "/api/posts/status-stream/550e8400-e29b-41d4-a716-446655440000/"
}
```

### **New Models:**

#### **PostingJob Model:**
Tracks posting job progress in real-time.

```python
class PostingJob:
    job_id: str           # Unique UUID for the job
    status: str           # queued, running, completed, failed
    total_posts: int      # Total posts to process
    completed_posts: int  # Successfully posted
    failed_posts: int     # Failed to post
    current_post_id: int  # Currently processing post ID
    current_post_title: str  # Current post title
    error_message: str    # Overall error if failed
    started_at: datetime
    completed_at: datetime
```

---

## 🔍 2. Detailed Error Logging

### **New API Endpoints:**

#### **Get Error Logs:**
```
GET /api/posts/error-logs/
```

**Query Parameters:**
- `post_id` - Filter by specific post
- `error_type` - Filter by error type
- `limit` - Limit results (default: 50)

**Example:**
```
GET /api/posts/error-logs/?post_id=45&limit=10
```

**Response:**
```json
{
  "count": 2,
  "error_logs": [
    {
      "id": 1,
      "post": 45,
      "post_title": "iPhone 13 Pro",
      "error_type": "session_expired",
      "error_message": "Session cookie expired, please re-login",
      "stack_trace": "Traceback (most recent call last):\n...",
      "screenshot": "/media/error_screenshots/post_45_error.png",
      "created_at": "2025-10-28T10:35:22Z"
    }
  ]
}
```

### **New Fields in MarketplacePost Model:**

```python
class MarketplacePost:
    # ... existing fields ...
    status: str           # pending, posting, posted, failed
    error_message: str    # Last error message if failed
    retry_count: int      # Number of retry attempts
```

### **ErrorLog Model:**

```python
class ErrorLog:
    post: ForeignKey      # Related post
    error_type: str       # session_expired, network_error, captcha, rate_limit, etc.
    error_message: str    # Human-readable error message
    stack_trace: str      # Full Python traceback
    screenshot: ImageField # Screenshot of error (optional)
    created_at: datetime
```

### **Error Types:**
- `session_expired` - Facebook session expired
- `network_error` - Network/connection issues
- `captcha` - CAPTCHA verification required
- `rate_limit` - Facebook rate limiting
- `validation_error` - Invalid post data
- `unknown` - Other errors

### **Automatic Error Logging:**

When posting fails, the system automatically:
1. Updates post status to "failed"
2. Stores error message in the post
3. Increments retry count
4. Creates detailed ErrorLog entry with:
   - Error type classification
   - Full error message
   - Complete stack trace
   - Timestamp

---

## 🏥 3. Health Check Endpoints

### **Check All Accounts Health:**
```
GET /api/accounts/health-check/
```

**Response:**
```json
{
  "overall_health": "healthy",  // or "warning", "error"
  "summary": {
    "total_accounts": 5,
    "healthy": 3,
    "warning": 1,
    "error": 1
  },
  "accounts": [
    {
      "account_id": 1,
      "email": "user1@example.com",
      "session_exists": true,
      "session_valid": true,
      "session_age_days": 5.3,
      "total_posts": 25,
      "posted_count": 20,
      "failed_count": 2,
      "health_status": "healthy"
    },
    {
      "account_id": 2,
      "email": "user2@example.com",
      "session_exists": true,
      "session_valid": false,
      "session_age_days": 35.2,
      "total_posts": 10,
      "posted_count": 5,
      "failed_count": 5,
      "health_status": "warning"
    },
    {
      "account_id": 3,
      "email": "user3@example.com",
      "session_exists": false,
      "session_valid": false,
      "session_age_days": null,
      "total_posts": 0,
      "posted_count": 0,
      "failed_count": 0,
      "health_status": "error"
    }
  ]
}
```

### **Health Status Meanings:**
- **healthy**: Session exists and is less than 30 days old
- **warning**: Session exists but is older than 30 days
- **error**: No session file exists

### **Validate Specific Account Session:**
```
GET /api/accounts/<account_id>/validate-session/
```

**Response (Valid):**
```json
{
  "valid": true,
  "session_age_days": 5.3,
  "message": "Session is valid",
  "action_required": null
}
```

**Response (Expired):**
```json
{
  "valid": false,
  "session_age_days": 35.2,
  "message": "Session may be expired",
  "action_required": "Consider updating session"
}
```

**Response (Missing):**
```json
{
  "valid": false,
  "message": "Session file does not exist",
  "action_required": "Please update session for this account"
}
```

---

## 🎯 Frontend Integration Examples

### **Example 1: Real-time Progress Bar**

```typescript
// app/dashboard/posts/page.tsx

const [postingProgress, setPostingProgress] = useState({
  status: 'idle',
  percentage: 0,
  current: '',
  completed: 0,
  total: 0
});

const startPostingWithProgress = async (postIds: number[]) => {
  try {
    // Start posting
    const response = await fetch('/api/posts/start-posting/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ post_ids: postIds })
    });
    
    const data = await response.json();
    const jobId = data.job_id;
    
    // Connect to SSE stream
    const eventSource = new EventSource(
      `http://localhost:8000/api/posts/status-stream/${jobId}/`,
      { withCredentials: true }
    );
    
    eventSource.onmessage = (event) => {
      const progress = JSON.parse(event.data);
      
      setPostingProgress({
        status: progress.status,
        percentage: progress.progress_percentage || 0,
        current: progress.current_post_title || '',
        completed: progress.completed_posts || 0,
        total: progress.total_posts || 0
      });
      
      if (progress.final) {
        eventSource.close();
        toast.success('Posting completed!');
        fetchPosts(); // Refresh posts list
      }
    };
    
    eventSource.onerror = () => {
      eventSource.close();
      toast.error('Connection lost');
    };
    
  } catch (error) {
    toast.error('Failed to start posting');
  }
};

// UI Component
return (
  <div>
    {postingProgress.status === 'running' && (
      <div className="fixed bottom-4 right-4 bg-white p-4 rounded-lg shadow-lg">
        <h3 className="font-semibold">Posting in Progress</h3>
        <div className="w-64 bg-gray-200 rounded-full h-4 mt-2">
          <div 
            className="bg-blue-600 h-4 rounded-full transition-all"
            style={{ width: `${postingProgress.percentage}%` }}
          />
        </div>
        <p className="text-sm mt-2">
          {postingProgress.completed} / {postingProgress.total} posts
        </p>
        <p className="text-xs text-gray-600">
          Current: {postingProgress.current}
        </p>
      </div>
    )}
  </div>
);
```

### **Example 2: Account Health Dashboard**

```typescript
const [accountHealth, setAccountHealth] = useState(null);

useEffect(() => {
  fetchAccountHealth();
}, []);

const fetchAccountHealth = async () => {
  const response = await fetch('/api/accounts/health-check/');
  const data = await response.json();
  setAccountHealth(data);
};

return (
  <div>
    <h2>Account Health</h2>
    <div className="grid grid-cols-3 gap-4">
      <div className="bg-green-100 p-4">
        <h3>Healthy</h3>
        <p className="text-2xl">{accountHealth?.summary.healthy}</p>
      </div>
      <div className="bg-yellow-100 p-4">
        <h3>Warning</h3>
        <p className="text-2xl">{accountHealth?.summary.warning}</p>
      </div>
      <div className="bg-red-100 p-4">
        <h3>Error</h3>
        <p className="text-2xl">{accountHealth?.summary.error}</p>
      </div>
    </div>
    
    <table className="mt-4">
      <thead>
        <tr>
          <th>Email</th>
          <th>Status</th>
          <th>Session Age</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {accountHealth?.accounts.map(account => (
          <tr key={account.account_id}>
            <td>{account.email}</td>
            <td>
              <span className={`badge ${account.health_status}`}>
                {account.health_status}
              </span>
            </td>
            <td>{account.session_age_days?.toFixed(1)} days</td>
            <td>
              {!account.session_valid && (
                <button onClick={() => updateSession(account.account_id)}>
                  Update Session
                </button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);
```

### **Example 3: Error Logs Viewer**

```typescript
const [errorLogs, setErrorLogs] = useState([]);

const fetchErrorLogs = async (postId?: number) => {
  const url = postId 
    ? `/api/posts/error-logs/?post_id=${postId}&limit=20`
    : `/api/posts/error-logs/?limit=20`;
    
  const response = await fetch(url);
  const data = await response.json();
  setErrorLogs(data.error_logs);
};

return (
  <div>
    <h2>Recent Errors</h2>
    {errorLogs.map(log => (
      <div key={log.id} className="border p-4 mb-2">
        <div className="flex justify-between">
          <h3>{log.post_title}</h3>
          <span className={`badge ${log.error_type}`}>
            {log.error_type}
          </span>
        </div>
        <p className="text-sm text-gray-600">{log.error_message}</p>
        <p className="text-xs text-gray-400">
          {new Date(log.created_at).toLocaleString()}
        </p>
        {log.screenshot && (
          <img src={log.screenshot} alt="Error screenshot" />
        )}
      </div>
    ))}
  </div>
);
```

---

## 📊 Database Changes

### **New Tables:**
1. `postings_postingjob` - Posting job tracking
2. `postings_errorlog` - Error logging

### **Updated Tables:**
1. `postings_marketplacepost` - Added `status`, `error_message`, `retry_count` fields

### **New Indexes:**
- `status_idx` on MarketplacePost.status

---

## ✅ Summary of Changes

### **Backend Files Modified:**
1. ✅ `postings/models.py` - Added PostingJob, ErrorLog models, updated MarketplacePost
2. ✅ `postings/serializers.py` - Added serializers for new models
3. ✅ `postings/realtime_views.py` - NEW file with SSE and health check endpoints
4. ✅ `postings/api_urls.py` - Added new endpoint routes
5. ✅ `accounts/api_urls.py` - Added health check routes
6. ✅ `postings/management/commands/post_to_marketplace.py` - Enhanced with job tracking and error logging
7. ✅ `postings/api_views.py` - Updated StartPostingView to create job and return job_id

### **Frontend Integration Needed:**
1. ⚠️ Update posts page to connect to SSE stream
2. ⚠️ Add progress bar component
3. ⚠️ Add error logs viewer
4. ⚠️ Add account health dashboard
5. ⚠️ Update post status badges (pending/posting/posted/failed)

### **No Changes Required:**
- ✅ Existing API endpoints still work
- ✅ Backward compatible with current frontend
- ✅ All migrations applied successfully

---

## 🚀 Next Steps

1. **Update Frontend** to use new SSE endpoint for real-time progress
2. **Add Health Check Widget** to dashboard showing account status
3. **Create Error Logs Page** to view and debug posting failures
4. **Add Retry Button** for failed posts
5. **Display Post Status** in the posts table

---

## 🧪 Testing

```bash
# Test health check
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/accounts/health-check/

# Test error logs
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/posts/error-logs/

# Test SSE stream (start posting first to get job_id)
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/posts/status-stream/<job_id>/
```

---

## 🎉 Benefits

### **For Users:**
- ✅ See real-time posting progress
- ✅ Know which post is currently being processed
- ✅ Immediate feedback on failures
- ✅ Proactive session expiry warnings
- ✅ Better debugging with detailed error logs

### **For Developers:**
- ✅ Comprehensive error tracking
- ✅ Easy debugging with stack traces
- ✅ Health monitoring for all accounts
- ✅ Job status persistence
- ✅ Retry capability with error history

All features are production-ready and backward compatible! 🚀
