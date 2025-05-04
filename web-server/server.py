from flask import Flask, request, jsonify
from datetime import datetime
import json
import os
import logging
from logging.handlers import RotatingFileHandler
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Ensure data directory exists
os.makedirs(os.path.dirname(app.config['LOG_FILE']), exist_ok=True)

# Set up logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/server.log', maxBytes=1024000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

def append_to_log(data):
    """Append data to log file based on configured format"""
    data['received_at'] = datetime.now().isoformat()
    
    if app.config['LOG_FORMAT'] == 'jsonl':
        # JSON Lines format - one JSON object per line
        with open(app.config['LOG_FILE'], 'a') as f:
            json.dump(data, f)
            f.write('\n')
    else:
        # Array format - maintain valid JSON array
        try:
            if os.path.exists(app.config['LOG_FILE']) and os.path.getsize(app.config['LOG_FILE']) > 0:
                with open(app.config['LOG_FILE'], 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = []
            
            log_data.append(data)
            
            with open(app.config['LOG_FILE'], 'w') as f:
                json.dump(log_data, f, indent=2)
        except Exception as e:
            app.logger.error(f"Error writing to log file: {e}")
            raise

@app.route('/data', methods=['POST'])
def receive_data():
    """Endpoint to receive JSON data from ESP32"""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        
        # Validate data (add your validation logic here)
        if not data:
            return jsonify({"error": "Empty data"}), 400
        
        # Add metadata
        data['client_ip'] = request.remote_addr
        
        append_to_log(data)
        
        app.logger.info(f"Data received from {request.remote_addr}")
        
        return jsonify({
            "status": "success",
            "message": "Data received",
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "log_file": app.config['LOG_FILE'],
        "log_format": app.config['LOG_FORMAT']
    }), 200

@app.route('/logs', methods=['GET'])
def view_logs():
    """View recent log entries"""
    try:
        limit = int(request.args.get('limit', 10))
        
        if app.config['LOG_FORMAT'] == 'jsonl':
            logs = []
            with open(app.config['LOG_FILE'], 'r') as f:
                for line in f:
                    logs.append(json.loads(line))
            return jsonify(logs[-limit:])
        else:
            with open(app.config['LOG_FILE'], 'r') as f:
                logs = json.load(f)
            return jsonify(logs[-limit:])
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"Starting server on {app.config['HOST']}:{app.config['PORT']}")
    print(f"Logging to {app.config['LOG_FILE']}")
    print(f"POST endpoint: http://{app.config['HOST']}:{app.config['PORT']}/data")
    print(f"Health check: http://{app.config['HOST']}:{app.config['PORT']}/health")
    print(f"View logs: http://{app.config['HOST']}:{app.config['PORT']}/logs")
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )