# Real-Time E-commerce Analytics Platform

## Project Overview
A serverless, real-time analytics system that tracks e-commerce events (product views, cart actions, purchases) and provides instant insights through REST APIs.

## Architecture
- **Kinesis Data Streams** - Event ingestion (data highway)
- **AWS Lambda** - Serverless compute (event processing)
- **DynamoDB** - NoSQL database (data storage)
- **ElastiCache Redis** - In-memory cache (fast queries)
- **API Gateway** - REST API (external access)
- **CloudWatch** - Monitoring & logging

## Tech Stack
- Python 3.11
- AWS SDK (boto3)
- AWS Free Tier Services

## Project Status
- [x] AWS CLI configured
- [x] Billing alarm set ($1 threshold)
- [x] Project structure created
- [ ] DynamoDB tables
- [ ] Kinesis stream
- [ ] Lambda functions
- [ ] API Gateway
- [ ] Redis cache

## Author
Jahnavi Kedia - Master's student seeking SWE internship

## Timeline
Start: November 12, 2025
Target completion: December 2, 2025 (3 weeks)
EOF