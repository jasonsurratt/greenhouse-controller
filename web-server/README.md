# ESP32 Data Logger Server

A simple Flask server that receives JSON data from ESP32 devices and logs it to a file.

## Features

- RESTful API endpoint for receiving JSON data
- Configurable logging formats (JSON Lines or JSON Array)
- Health check endpoint
- Log viewing endpoint
- Rotating log files to prevent disk space issues
- Client IP tracking
- Error handling and logging

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   make
   ```

## Sample requests:

```bash
# log sensor data:
cat data/received_data.json 
{"sensor": "temperature", "value": 25.5, "unit": "celsius", "client_ip": "127.0.0.1", "received_at": "2025-05-04T13:26:19.743766"}
# request 5 most recent logs
curl http://localhost:5000/logs?limit=5
```
