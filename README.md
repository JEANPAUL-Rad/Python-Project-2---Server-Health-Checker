# Server Health Checker

A Python-based monitoring tool that checks the health of multiple servers and services concurrently.

The application verifies:

* HTTP status codes
* Response times
* JSON health indicators
* Service availability
* Slow response detection

Failed services are collected into a report for further investigation.

## Features

### Health Checks

* Verify HTTP response status
* Detect unavailable services
* Detect timeout conditions

### Performance Monitoring

* Measure response time in milliseconds
* Flag services responding slower than 500ms

### JSON Validation

* Validate JSON responses
* Detect health payloads containing:

```json
{
  "status": "ok"
}
```

### Parallel Execution

* Check multiple servers concurrently using ThreadPoolExecutor
* Prevent slow endpoints from blocking other checks

### Retry Logic

* Automatically retry failed requests
* Reduce false positives caused by temporary network issues

### Flexible Configuration

Supports:

1. Environment variable
2. JSON configuration file

### Email Alerts

Optional SMTP alert support for failed services.

---
