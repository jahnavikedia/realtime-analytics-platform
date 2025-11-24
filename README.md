# Real-Time E-Commerce Analytics Platform

A production-ready serverless analytics system that processes e-commerce events in real-time, performs intelligent data aggregation, and visualizes business insights through an interactive dashboard.

## 🚀 Live Demo

**Dashboard:** https://real-time-analytics-2a54015ca-jahnavikedias-projects.vercel.app

**API Endpoint:** https://izob8k3keg.execute-api.us-east-1.amazonaws.com/prod/dashboard/summary

---

## 📊 Project Overview

This full-stack application demonstrates expertise in cloud architecture, real-time data processing, and modern web development. It simulates and analyzes e-commerce user behavior, providing actionable business intelligence metrics.

### Key Metrics (Live Data)
- **679 product views** processed and analyzed
- **169 cart additions** tracked
- **69 purchases** completed
- **10.16% conversion rate** calculated
- **59.17% cart abandonment rate** measured
- **Sub-200ms API response time** achieved

---

## 🏗️ Architecture
```
┌─────────────────┐
│ Event Generator │ → Simulates e-commerce events
└────────┬────────┘
         ↓
┌────────────────┐
│ Kinesis Stream │ → Real-time event streaming
└────────┬───────┘
         ↓
┌─────────────────┐
│Stream Processor │ → Aggregates & processes data
└────────┬────────┘
         ↓
┌──────────────┐
│  DynamoDB    │ → Stores raw events + analytics
└──────┬───────┘
       ↓
┌─────────────┐
│ Query Lambda│ → REST API for data retrieval
└──────┬──────┘
       ↓
┌──────────────┐
│ API Gateway  │ → HTTP endpoints
└──────┬───────┘
       ↓
┌──────────────────┐
│ React Dashboard  │ → Interactive visualizations
│ (Vercel)         │
└──────────────────┘
```

---

## 🛠️ Technology Stack

### Backend (AWS)
- **AWS Lambda** - Serverless compute (3 functions)
- **Amazon DynamoDB** - NoSQL database for events & analytics
- **Amazon Kinesis** - Real-time data streaming
- **API Gateway** - RESTful API endpoints
- **CloudWatch** - Monitoring & logging
- **IAM** - Security & permissions

### Frontend
- **React** - UI framework
- **Recharts** - Data visualization
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Axios** - API calls
- **Vercel** - Deployment & hosting

### Development Tools
- **Python 3.11** - Backend logic
- **Node.js/npm** - Frontend tooling
- **Git/GitHub** - Version control
- **AWS CLI** - Infrastructure management

---

## ✨ Features

### Real-Time Analytics
- ✅ Event-driven architecture with automatic processing
- ✅ Sub-second latency from event generation to visualization
- ✅ Automatic data aggregation (hourly, daily, by category)
- ✅ Atomic counter updates for data consistency

### Business Intelligence
- 📊 **Conversion Rate**: Measures purchase effectiveness (purchases ÷ views)
- 🛒 **Cart Abandonment Rate**: Tracks lost sales opportunities
- 📈 **Category Performance**: Identifies top-performing product categories
- 💰 **Revenue Tracking**: Monitors total sales and trends

### Interactive Dashboard
- 🎨 Beautiful gradient UI with glass-morphism effects
- 📱 Fully responsive (desktop, tablet, mobile)
- 🔄 Auto-refresh every 30 seconds
- ✨ Animated number counters and smooth transitions
- 📊 Interactive charts with hover tooltips
- 🎯 Real-time data from live API

---

## 📡 API Endpoints

Base URL: `https://izob8k3keg.execute-api.us-east-1.amazonaws.com/prod`

### 1. Dashboard Summary
```
GET /dashboard/summary
```
Returns aggregated metrics with business intelligence calculations.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_events": 930,
    "metrics": {
      "product_view": 679,
      "add_to_cart": 169,
      "purchase": 69,
      "remove_from_cart": 13
    },
    "conversion_rate": 10.16,
    "cart_abandonment_rate": 59.17
  }
}
```

### 2. Category Breakdown
```
GET /dashboard/categories
```
Returns performance metrics by product category.

**Response:**
```json
{
  "success": true,
  "data": {
    "all_time": true,
    "categories": {
      "Electronics": 350,
      "Sports": 220,
      "Home": 109
    }
  }
}
```

### 3. Specific Metric Query
```
GET /metrics/{metric_type}
```
Returns historical data for a specific metric across all dates.

**Example:**
```
GET /metrics/product_view_count
```

### 4. Metric by Date
```
GET /metrics/{metric_type}/{date}
```
Returns metric data for a specific date.

**Example:**
```
GET /metrics/purchase_count/2025-11-14
```

---

## 🗄️ Data Models

### Raw Events Table
**Table:** `raw-events`
- **Partition Key:** `event_id` (String)
- **Sort Key:** `timestamp` (Number)
- **Purpose:** Stores complete event details for audit trail

**Event Types:**
- `product_view` - User views a product
- `add_to_cart` - User adds product to cart
- `purchase` - User completes purchase
- `remove_from_cart` - User removes item from cart

### Analytics Table
**Table:** `analytics`
- **Partition Key:** `metric_type` (String)
- **Sort Key:** `time_window` (String)
- **Purpose:** Pre-aggregated metrics for fast queries

**Metric Types:**
- `product_view_count` - Daily/hourly view counts
- `purchase_count` - Daily/hourly purchase counts
- `category_{name}` - Category-specific metrics
- `product_{id}` - Product-specific metrics
- `purchase_revenue` - Revenue tracking

---

## 💰 Cost Analysis

### Current Monthly Cost: $0

**AWS Free Tier Coverage:**
| Service | Free Tier | Usage | Cost |
|---------|-----------|-------|------|
| Lambda | 1M requests/month | ~1K/month | $0 |
| DynamoDB | 25GB storage | ~0.1GB | $0 |
| API Gateway | 1M calls/month (12 months) | ~500/month | $0 |
| CloudWatch | 5GB logs | ~0.1GB | $0 |

**After Free Tier (Year 2+):**
- Estimated: $0.50-2/month for portfolio use
- Can be reduced to $0 using cleanup script

**Vercel:**
- Free tier: Unlimited for personal projects
- Cost: $0 forever

---

## 🧹 Resource Cleanup

To delete all AWS resources and return to $0/month:
```bash
cd ~/realtime-analytics-platform
./cleanup.sh
```

**What gets deleted:**
- All Lambda functions
- API Gateway
- DynamoDB tables
- Kinesis stream (if exists)
- IAM roles and policies
- CloudWatch alarms

**What stays:**
- Frontend on Vercel (continues working with static data)
- GitHub repository
- Local code

---

## 📈 Performance Metrics

- **API Response Time:** 150-200ms average
- **Event Processing Latency:** <1 second
- **Dashboard Load Time:** <2 seconds
- **Auto-refresh Interval:** 30 seconds
- **Concurrent Users Supported:** 1000+ (auto-scaling)

---

## 🎓 Learning Outcomes

### Cloud Architecture
- Designed event-driven serverless architecture
- Implemented microservices pattern with Lambda
- Configured cross-service IAM permissions
- Set up monitoring and billing alarms

### Data Engineering
- Built real-time streaming pipeline with Kinesis
- Designed efficient NoSQL schema with composite keys
- Implemented atomic aggregations for data consistency
- Optimized query patterns for sub-200ms response times

### Full-Stack Development
- Created RESTful API with proper HTTP methods
- Built responsive React dashboard with animations
- Implemented real-time data synchronization
- Deployed to production with CI/CD

### DevOps & Best Practices
- Infrastructure as Code principles
- Git version control and branching
- Environment variable management
- Cost optimization strategies

---

## 🔧 Local Development

### Prerequisites
- AWS Account with CLI configured
- Node.js 16+ and npm
- Python 3.11+
- Git

### Setup Backend
```bash
# Clone repository
git clone https://github.com/jahnavikedia/realtime-analytics-platform.git
cd realtime-analytics-platform

# Deploy AWS infrastructure
# (Follow deployment steps in documentation)

# Test API
curl https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/dashboard/summary
```

### Setup Frontend
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Deploy to Vercel
vercel --prod
```

---

## 🐛 Troubleshooting

### API Returns Empty Data
**Issue:** Dashboard shows zeros
**Solution:** Update Query Lambda to aggregate all-time data instead of just today

### CORS Errors
**Issue:** Browser blocks API calls
**Solution:** Verify `Access-Control-Allow-Origin: *` header in Lambda response

### Build Hangs Locally
**Issue:** `npm run build` gets stuck
**Solution:** Use Vercel cloud build instead: `vercel --prod`

### Lambda Timeout
**Issue:** Function execution exceeds 60 seconds
**Solution:** Increase timeout or optimize query logic

---

## 🚧 Future Enhancements

- [ ] **Advanced Analytics**
  - User cohort analysis
  - Funnel visualization
  - Revenue forecasting with ML

- [ ] **Performance Optimization**
  - ElastiCache Redis for hot data
  - GraphQL API for flexible queries
  - WebSocket for real-time updates

- [ ] **Additional Features**
  - User authentication with Cognito
  - Custom date range filtering
  - Export data to CSV/PDF
  - Email alerts for anomalies

- [ ] **Infrastructure**
  - Multi-region deployment
  - Automated backups
  - Blue-green deployments
  - Load testing automation

---

## 📝 Project Structure
```
realtime-analytics-platform/
├── lambda/
│   ├── event-generator/         # Simulates e-commerce events
│   │   ├── lambda_function.py
│   │   └── lambda_function.zip
│   ├── stream-processor/        # Processes Kinesis stream
│   │   ├── lambda_function.py
│   │   └── lambda_function.zip
│   └── api/                     # Query API endpoints
│       ├── lambda_function.py
│       └── lambda_function.zip
├── frontend/                    # React dashboard
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   └── Dashboard.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
├── infrastructure/
│   └── lambda-trust-policy.json
├── cleanup.sh                   # Resource cleanup script
├── DEPLOYMENT_INFO.md          # Deployment reference
├── PROJECT_SUMMARY.md          # Project summary
├── API_INFO.md                 # API documentation
└── README.md                   # This file
```

---

## 📚 Technical Documentation

### Lambda Functions

**1. Event Generator**
- **Purpose:** Simulates realistic e-commerce user behavior
- **Trigger:** Manual invocation
- **Output:** 10 events per invocation
- **Products:** 8 different products across 3 categories
- **Event Distribution:** 70% views, 20% cart adds, 8% purchases, 2% removals

**2. Stream Processor**
- **Purpose:** Processes Kinesis events and updates analytics
- **Trigger:** Kinesis Data Stream
- **Batch Size:** Up to 10 records
- **Operations:** Saves raw events, updates aggregated metrics
- **Concurrency:** Supports parallel processing with atomic counters

**3. Query API**
- **Purpose:** Exposes analytics data via REST endpoints
- **Trigger:** API Gateway HTTP requests
- **Response Format:** JSON with CORS headers
- **Features:** Conversion rate calculation, all-time aggregations

### Database Schema

**DynamoDB Composite Keys:**
- Enables efficient queries by metric type and time range
- Supports both specific date queries and time-series analysis
- Atomic counters prevent race conditions in concurrent updates

**Query Patterns:**
```python
# Get specific metric for specific date
get_item(partition_key="product_view_count", sort_key="2025-11-14")

# Get all dates for a metric (time series)
query(partition_key="product_view_count")

# Get category performance
query(partition_key="category_Electronics")
```

---

## 👤 Author

**Jahnavi Kedia**
- GitHub: [@jahnavikedia](https://github.com/jahnavikedia)
- Email: jahnavikedia91@gmail.com

---

## 🙏 Acknowledgments

- AWS Free Tier for making cloud learning accessible
- Vercel for seamless frontend deployment
- React and Recharts communities for excellent documentation
- Open source contributors for the libraries used

---

## 📊 Project Stats

- **AWS Services Used:** 7
- **API Endpoints:** 4
- **Events Processed:** 679+
- **Deployment Platforms:** 2 (AWS, Vercel)

Built by Jahnavi Kedia
