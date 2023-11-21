from flask import Flask, request, jsonify, render_template, g
from datetime import datetime
import requests
import json

from db import PiDatabase
import server_helpers
from datatypes import MPU6050_Data

DEBUG_MODE = True
PORT = 8080
HOST = '0.0.0.0'

app = Flask(__name__)
dbo = PiDatabase(debug_mode=DEBUG_MODE)

# device mac_address (identifier) to its ip
active_connections = {}


def build_request_to_self(endpoint: str):
    if endpoint: 
        return "http://" + HOST + ":" + str(PORT) + endpoint
    else: 
        return ""

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def to_pretty_json(json_val):
    temp_json_dict = json.loads(json_val)
    return json.dumps(temp_json_dict, sort_keys=True, indent=4, separators=(',', ': '))
app.jinja_env.filters["tojson_pretty"] = to_pretty_json

@app.route("/", methods=['GET'])
def home():
    devices = []
    projects = []

    with app.app_context():
        conn = dbo.get_db()
        cursor = conn.cursor()

        checked_out_devices = dbo.get_active_devices_with_user_info(cursor)

        for device in checked_out_devices:
            timestamp_datetime = datetime.strptime(device[3], '%Y-%m-%d %H:%M:%S')
            current_time = datetime.now()

            time_dff = current_time - timestamp_datetime
            # print("time difference " + str(time_dff.days))

            # Extract hours, minutes, and seconds from the time difference
            days = time_dff.days
            hours, remainder = divmod(time_dff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            devices.append({
                "in_use": True,
                "mac_address": device[0],
                "device_name": device[1],
                "device_desc": device[2],
                "time_since_start": (f"{days} days, " if days > 0 else "") + f"{hours} hrs, {minutes} minutes",
                "user_fname": device[4],
                "user_lname": device[5]
            })

        raw_projects = dbo.get_all_projects(cursor)
        
        for raw_project in raw_projects:
            projects.append({
                "project_id": raw_project[0],
                "project_title": raw_project[1],
                "project_desc": raw_project[2],
                "creation_date": raw_project[3],
                "github_link": raw_project[4] 
            })
        
        conn.commit()

    return render_template('home_dashboard.html', devices=devices, projects=projects)

@app.route('/projects', methods=["GET"]) 
def all_projects_view():
    projects = []

    projects_list_request = build_request_to_self("/api/projects")
    projects_json_data = requests.get(projects_list_request).json()

    if projects_json_data["status"] == "success": 
        for project in projects_json_data["data"]:

            projects.append({
                "project_id": project[0],
                "title": project[1],
                "desc": project[2],
                "created_on": project[3],
                "github_link": project[4]
            })

    return render_template('projects_page.html', projects=projects)

@app.route('/projects/<project_id>', methods=["GET"])
def project_info_view(project_id):
    project = {}
    assocc_devices = []
    contributors = []

    projects_list_request = build_request_to_self(f"/api/projects/{project_id}")
    projects_json_data = requests.get(projects_list_request).json()

    project = {
        "project_id": projects_json_data["data"][0],
        "title": projects_json_data["data"][1],
        "desc": projects_json_data["data"][2],
        "created_on": projects_json_data["data"][3],
        "github_link": projects_json_data["data"][4]
    }

    assocc_devices_list_request = build_request_to_self(f"/api/projects/{project_id}/devices")
    assocc_devices_json_data = requests.get(assocc_devices_list_request).json()
    
    print(assocc_devices_json_data)
    # for assocc_device in assocc_devices_json_data["data"]:
    #     currently_in_use = True if assocc_devices[5] else False 

    #     assocc_devices.append({
    #         "in_use": currently_in_use,
    #         "mac_address": assocc_device[1],
    #         "device_name": assocc_device[2],
    #         "device_desc": assocc_device[3],
    #         "time_since_start": (f"{days} days, " if days > 0 else "") + f"{hours} hrs, {minutes} minutes",
    #         "user_fname": assocc_device[4],
    #         "user_lname": assocc_device[5]
    #     })

    return render_template("project_info_page.html", project=project, devices=assocc_devices)


@app.route('/devices/<mac_address>', methods=['GET'])
def device_view(mac_address: str):
    data = {}

    
    return render_template('device_template.html')

@app.route('/devices/logs', methods=['GET'])
def device_log_view():
    params = []
    logs = []
    devices = []
    
    # get query parameters
    device_addr = request.args.get("device_addr", default=None)
    start_time = request.args.get("datetime_from", default=None)
    end_time = request.args.get("datetime_to", default=None)
    status_code = request.args.get("status_code", default=None)
    curr_checkout_only = request.args.get("curr_checkout_only", default=None)

    # get most recent checkout id
    # checkout_id = 

    # append formated parameters for api call
    if device_addr: params.append(("device_addr", device_addr))
    if start_time: params.append(("datetime_from", start_time))
    if end_time: params.append(("datetime_to", end_time))
    # if checkout_id: params.append(("checkout_id", checkout_id))
    if status_code: params.append(("status_code", status_code))
    # if status_code: params.append(("curr_checkout_only", curr_checkout_only))
    # params.append(("filter_topics", request.args.get("filter_topics", default="").split(',')))
    # params.append(("order_by_topics", request.args.get("order_by_topics", default="").split(',')))
    # params.append(("order_by_asc_or_desc", request.args.get("order_by_asc_or_desc", default="ASC")))


    logs_request_endpoint = build_request_to_self("/api/devices/logs")
    logs_request_endpoint_with_params = server_helpers.add_request_parameters(logs_request_endpoint, params)
    log_json_data = requests.get(logs_request_endpoint_with_params).json()

    for log in log_json_data["data"]:
        log_data = log[5]
        
        # extract log descriptor
        log_descriptor = json.loads(log_data).log_title if "log_title" in json.loads(log_data) else "No Descriptor Added."
        
        logs.append({
            "mac_address": log[0],
            "device_name": log[1],
            "device_type": log[2],
            "creation_time": log[3],
            "status_code": str(log[4]),
            "log_data": log[5],
            "checkout_id": log[6],
            "user_fname": log[7],
            "user_lname": log[8],

            "log_descriptor": log_descriptor
        })
    
    # get all devices 
    devices_request_endpoint = build_request_to_self("/api/registered-devices")
    device_json_data = requests.get(devices_request_endpoint).json()

    for device in device_json_data["data"]:
        devices.append({
            "mac_address": device[0],
            "device_name": device[1]
        })
    
    

    return render_template('log_page.html', devices=devices, logs=logs)


@app.route('/devices/checkout/<checkout_id>')
def checkout_view(checkout_id):
    return render_template("checkout_page.html")



@app.route('/ping', methods=['GET'])
def ping():
    return 'Hello from Python server!\n'


@app.route('/api/devices/logs', methods=["GET", "POST"])
def device_log_api():
    if request.method == "GET":
        # get query parameters
        device_addr = request.args.get("device_addr", default=None)
        date_from = request.args.get("datetime_from", default=None)
        date_to = request.args.get("datetime_to", default=None)
        checkout_id = request.args.get("checkout_id", default=None)
        status_code = request.args.get("status_code", default=None)
        # filter_topics = request.args.get("filter_topics", default="").split(',')
        # order_by_topics = request.args.get("order_by_topics", default="").split(',')
        # order_by_asc_or_desc = request.args.get("order_by_asc_or_desc", default="ASC")

        
        with app.app_context():
            conn = dbo.get_db()
            cursor = conn.cursor()

            logs = dbo.get_device_logs_by_parameters(
                cursor, device_addr, date_from, date_to,
                checkout_id, status_code) 
                # filter_topics, order_by_topics, order_by_asc_or_desc)
            
            conn.commit()
        return jsonify({'status': 'success', 'data': logs})
        
    elif request.method == "POST":
        pass
    else:
        return jsonify({"status": "error", "msg": "invalid request method used"})

# @app.route('/devices/<mac_address>/logs', methods=['POST'])
# def device_log_data():
#     '''Some things to possibly measure'''
    
#     return 

@app.route('/api/projects', methods=["GET", "POST"])
def projects():
    if request.method == "GET":
        projects = []
        with app.app_context():
            conn = dbo.get_db()
            cursor = conn.cursor()

            projects = dbo.get_all_projects(cursor)

            conn.commit()
        
        return jsonify({'status': 'success', 'data': projects})
    else:
        return jsonify({"status": "error", "msg": "invalid request method used"})

@app.route('/api/projects/<project_id>', methods=["GET"])
def project_by_id(project_id):
    if request.method == "GET":
        project = {}

        with app.app_context():
            conn = dbo.get_db()
            cursor = conn.cursor()

            project = dbo.get_project_by_id(cursor, project_id)
            
            conn.commit()

        return jsonify({'status': 'success', 'data': project})
    else:
        return jsonify({"status": "error", "msg": "invalid request method used"})

@app.route('/api/projects/<project_id>/devices', methods=["GET"])
def devices_associated_to_project(project_id):
    if request.method == "GET":
        devices = []

        with app.app_context():
            conn = dbo.get_db()
            cursor = conn.cursor()

            devices = dbo.get_devices_by_project_id(cursor, project_id)
            print(devices)
            
            conn.commit()

        return jsonify({'status': 'success', 'data': devices})
    else:
        return jsonify({"status": "error", "msg": "invalid request method used"})



@app.route('/api/registered-devices', methods=["GET", "POST"])
def registered_devices():
    if request.method == "GET":
        devices = []

        with app.app_context():
            conn = dbo.get_db()
            cursor = conn.cursor()

            devices = dbo.get_all_devices(cursor)
            
            conn.commit()

        return jsonify({'status': 'success', 'data': devices})
    
    elif request.method == "POST":
        return
    else:
        return jsonify({"status": "error", "msg": "invalid request method used"})



@app.route('/api/device/<device_id>/project/<project_id>/mpu-motion6', methods=['POST'])
def dog_tracker_motion_data():
    '''
    api endpoint for tracking 
    '''
    try:
        data = request.json  # Assuming the data is sent as JSON
        print(data)

        # print(MPU6050_Data(data))

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
    app.run(host=HOST, port=PORT, debug=DEBUG_MODE)
