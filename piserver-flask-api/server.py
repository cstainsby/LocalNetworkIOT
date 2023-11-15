from flask import Flask, request, jsonify, render_template, g
from datetime import datetime

from db import PiDatabase
from datatypes import MPU6050_Data

DEBUG_MODE = True
PORT = 8080

app = Flask(__name__)
dbo = PiDatabase(debug_mode=DEBUG_MODE)

# device mac_address (identifier) to its ip
active_connections = {}


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/", methods=['GET'])
def home():
    data = {
        "devices": []
    }

    with app.app_context():
        conn = dbo.get_db()
        cursor = conn.cursor()

        checked_out_devices = dbo.get_active_devices_with_user_info(cursor)

        for device in checked_out_devices:
            timestamp_datetime = datetime.strptime(device[3], '%Y-%m-%d %H:%M:%S')
            current_time = datetime.now()

            time_dff = current_time - timestamp_datetime

            # Extract hours, minutes, and seconds from the time difference
            hours, remainder = divmod(time_dff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            data["devices"].append({
                "in_use": True,
                "mac_address": device[0],
                "device_name": device[1],
                "device_desc": device[2],
                "time_since_start": f"{hours} hrs, {minutes} minutes",
                "user_fname": device[4],
                "user_lname": device[5]
            })
        # non_in_use_devices = dbo.get_deactivated_devices(cursor)
        # for device in non_in_use_devices:
        #     data["devices"].append({
        #         "in_use": False,
        #         "mac_address": device[0],
        #         "device_name": device[1],
        #         "device_desc": device[2],
        #         "end_time": device[3]
        #     })
        conn.commit()

    return render_template('home_dashboard.html', data=data)

@app.route('/devices/<mac_address>', methods=['GET'])
def device_view(mac_address: str):
    data = {}

    
    return render_template('device_template.html')

@app.route('/devices/logs', methods=['GET'])
def device_log_view():
    data = {
        ""
    }

    return render_template('device_logs.html')

@app.route('/devices/<mac_address>/logs', methods=['POST'])
def device_log_data():
    '''Some things to possibly measure'''
    #  Device Information:
    #     Device ID: Unique identifier for each IoT device.
    #     Device Type: The type or model of the IoT device.
    #     Firmware Version: The version of the firmware/software running on the device.
    #     Hardware Information: CPU, memory, storage, etc.

    # Connectivity Metrics:
    #     Online/Offline Status: Indicates whether the device is currently connected.
    #     Signal Strength: For wireless devices, the strength of the signal.
    #     Network Latency: Round-trip time for communication with a server.
    #     Bandwidth Usage: Amount of data transmitted and received.

    # Power and Battery Status:
    #     Battery Level: For battery-powered devices.
    #     Power Source: Whether the device is connected to a power source.
    #     Power Consumption: Amount of power the device is consuming.

    # Temperature and Environmental Conditions:
    #     Device Temperature: Internal temperature of the device.
    #     Humidity Level: For devices sensitive to humidity.
    #     Atmospheric Pressure: Relevant for certain environmental conditions.

    # Error and Exception Logs:
    #     Log error messages and exceptions to identify issues.
    #     Stack Traces: Detailed information about where errors occurred.
    #     Timestamps: When errors or exceptions were logged.

    # Usage and Performance Metrics:
    #     CPU Usage: Percentage of CPU being utilized.
    #     Memory Usage: Amount of RAM being used.
    #     Storage Usage: Available storage space on the device.
    #     Processing Time: Time taken to execute specific tasks.

    # Security and Anomaly Detection:
    #     Unauthorized Access Attempts: Failed login attempts or security breaches.
    #     Anomalies in Behavior: Unusual patterns in device behavior.

    # Communication Protocols:
    #     Number of Successful Data Transmissions.
    #     Number of Failed Data Transmissions.

    # Location Information:
    #     GPS Coordinates: If applicable.
    #     Location Updates: Timestamps of when location data is updated.

    # System Uptime:
    #     Amount of time the device has been continuously running without a restart.

    # Firmware/Software Updates:
    #     Timestamps of when firmware or software updates were applied.

    # Custom Metrics:
    #     Any specific metrics relevant to your IoT device and its use case.
    return 

@app.route('/ping', methods=['GET'])
def ping():
    return 'Hello from Python server!\n'

# @app.route('/registered-devices', methods=["GET", "POST"])
# def registered_devices():
#     if request.method == "GET":
#         return jsonify({})
#         return dbo.get_registered_devices()
    
#     elif request.method == "POST":
#         return



@app.route('/dog-tracker/mpu-motion6', methods=['POST'])
def dog_tracker_motion_data():
    try:
        data = request.json  # Assuming the data is sent as JSON
        print(data)

        print(MPU6050_Data(data))

        # motion_data = MPU6050_Data(**data)

        # db.add_dog_motion_data(motion_data)
        
        return jsonify({'status': 'success', 'message': 'Data received successfully'})

    except KeyError as e:
        # Handle missing keys in the request data
        return jsonify({'status': 'error', 'message': f'Missing key: {str(e)}'}), 400

    except Exception as e:
        # Handle other exceptions
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
 
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG_MODE)
