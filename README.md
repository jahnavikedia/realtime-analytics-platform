# Real-Time E-Commerce Analytics Platform

A production-ready serverless analytics system processing real-time e-commerce events with business intelligence calculations.

## 🚀 Live Demo

**API Endpoint:** https://izob8k3keg.execute-api.us-east-1.amazonaws.com/prod/dashboard/summary

### Available Endpoints

1. **Dashboard Summary** - `/dashboard/summary`
   - Today's metrics with conversion rate & cart abandonment

2. **Category Breakdown** - `/dashboard/categories`  
   - Views by product category

3. **Metric Query** - `/metrics/{metric_type}`
   - Historical data for any metric

4. **Specific Date Query** - `/metrics/{metric_type}/{date}`
   - Metric for specific date

## 📊 Current Metrics

- **679 product views**
- **169 cart additions**
- **69 purchases**
- **10.16% conversion rate**
- **59.17% cart abandonment rate**

## 🏗️ Architecture
```
Event Generator → Kinesis Stream → Stream Processor → DynamoDB
                                                          ↓
                                            Query Lambda ← API Gateway → Users
```

### AWS Services Used

- **Lambda** (3 functions) - Serverless compute
- **DynamoDB** (2 tables) - NoSQL database
- **API Gateway** - REST API
- **Kinesis** - Real-time streaming (can be disabled)
- **CloudWatch** - Monitoring & billing alerts
- **IAM** - Security & permissions

## 💡 Key Features

✅ Real-time event processing
✅ Automatic aggregation & analytics
✅ Business intelligence calculations
✅ RESTful API with CORS
✅ Serverless & auto-scaling
✅ Cost-optimized (can run at $0/month)

## 🛠️ Technical Implementation

### Data Flow

1. **Event Generation**: Lambda generates realistic e-commerce events
2. **Streaming**: Events sent to Kinesis Data Stream
3. **Processing**: Stream Processor aggregates data
4. **Storage**: Raw events + analytics in DynamoDB
5. **Query**: API Gateway exposes REST endpoints
6. **Response**: Sub-200ms JSON responses

### Data Models

**Raw Events Table:**
- Partition Key: `event_id`
- Stores: Complete event details

**Analytics Table:**
- Partition Key: `metric_type`
- Sort Key: `time_window` (date)
- Stores: Aggregated counts and metrics

## 💰 Cost Analysis

**Development/Portfolio Use:**
- Lambda: Free tier (1M requests/month)
- DynamoDB: Free tier (25GB, 25 read/write units)
- API Gateway: Free tier (1M calls/month, 12 months)
- **Total: $0/month**

**After Free Tier:**
- Estimated: $0.01-0.05/month for portfolio use

## 🧹 Cleanup

To delete all resources:
```bash
./cleanup.sh
```

This removes all AWS resources and returns monthly cost to $0.

## 📈 Business Metrics Tracked

- **Conversion Rate**: (Purchases ÷ Views) × 100
- **Cart Abandonment**: ((Adds - Purchases) ÷ Adds) × 100
- **Category Performance**: Views by product category
- **Hourly Trends**: Event patterns over time

## 🎯 Interview Talking Points

1. **Distributed Systems**: Event-driven architecture with decoupled services
2. **Real-time Processing**: Kinesis streaming with Lambda triggers
3. **Scalability**: Auto-scaling from 1 to 1000s of requests
4. **Cost Optimization**: Serverless design, free tier optimization
5. **API Design**: RESTful endpoints with proper HTTP methods
6. **Data Modeling**: Composite keys for efficient queries
7. **Error Handling**: Graceful degradation, proper status codes
8. **Security**: IAM least-privilege, CORS configuration

## �� Local Development

1. Clone repository
2. Configure AWS CLI
3. Deploy infrastructure (commands in deployment history)
4. Generate test data
5. Query API endpoints

## 📝 Project Structure
```
realtime-analytics-platform/
├── lambda/
│   ├── event-generator/     # Generates e-commerce events
│   ├── stream-processor/    # Processes & aggregates
│   └── api/                 # Query API
├── cleanup.sh               # Resource cleanup script
├── API_INFO.md             # API documentation
└── README.md               # This file
```

## 🚀 Future Enhancements

- [ ] DynamoDB TTL for auto-cleanup
- [ ] React dashboard with charts
- [ ] WebSocket for real-time updates
- [ ] CloudFront CDN for global distribution
- [ ] API authentication with Cognito
- [ ] Additional metrics (revenue, user cohorts)
- [ ] ElastiCache for hot data caching

## 📚 Learning Outcomes

- Serverless architecture patterns
- Real-time data streaming
- NoSQL database design
- RESTful API development
- AWS cloud services integration
- Cost optimization strategies
- Production deployment practices

---

**Built with:** AWS Lambda, DynamoDB, API Gateway, Kinesis
**Author:** Jahnavi Kedia
**GitHub:** https://github.com/jahnavikedia/realtime-analytics-platform
