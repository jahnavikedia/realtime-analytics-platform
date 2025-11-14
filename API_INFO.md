# Live API Endpoints

Base URL: https://izob8k3keg.execute-api.us-east-1.amazonaws.com/prod

## Endpoints

### Dashboard Summary
GET /dashboard/summary

Returns today's analytics with conversion metrics.

### Category Breakdown  
GET /dashboard/categories

Returns views by product category.

### Metric Query
GET /metrics/{metric_type}

Returns all dates for a specific metric.
Example: /metrics/product_view_count

### Metric with Date
GET /metrics/{metric_type}/{date}

Returns specific metric for specific date.
Example: /metrics/purchase_count/2025-11-14

## Response Format
All endpoints return JSON with CORS enabled.