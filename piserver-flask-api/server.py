"""
    A lot of my views will make calls to both my own endpoints for very common workflows,
    and also have custom db calls for specific use cases
"""


from flask import Flask, request, jsonify, render_template, g
from datetime import datetime
import requests
import json
import sys

from db import PiDatabase
import server_helpers
# from datatypes import MPU6050_Data
from datatypes.project import Project
from datatypes.device import Device
from datatypes.device_checkout import DeviceCheckout
# from datatypes.user import User
# from datatypes.device import Device
# from datatypes.project import Project
# from datatypes.device_checkout import DeviceCheckout


DEBUG_MODE = True
PORT = 8080
HOST = '0.0.0.0'

app = Flask(__name__)
dbo = PiDatabase(debug_mode=DEBUG_MODE)

# this data structure will be filled with devices when they are initially turned on 
# it will hold information which will be important to have on hand while connected 
# devices are generating time sensitive information by reducing lookup overhead
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

    # devices_list_request = build_request_to_self("/api/devices")
    # devices_json_data = requests.get(devices_list_request).json()
    # checked_out_devices = dbo.get_active_devices_with_user_info(cursor)

    # print(devices_json_data)

    # for raw_device in devices_json_data["data"]:



    # # devices = [Device()]

    # for device in checked_out_devices:
    #     timestamp_datetime = datetime.strptime(device[3], '%Y-%m-%d %H:%M:%S')
    #     current_time = datetime.now()

    #     time_dff = current_time - timestamp_datetime
    #     # print("time difference " + str(time_dff.days))

    #     # Extract hours, minutes, and seconds from the time difference
    #     days = time_dff.days
    #     hours, remainder = divmod(time_dff.seconds, 3600)
    #     minutes, seconds = divmod(remainder, 60)

    #     devices.append({
    #         "in_use": True,
    #         "mac_address": device[0],
    #         "device_name": device[1],
    #         "device_desc": device[2],
    #         "time_since_start": (f"{days} days, " if days > 0 else "") + f"{hours} hrs, {minutes} minutes",
    #         "user_fname": device[4],
    #         "user_lname": device[5]
    #     })

    # find all active devices
    


    projects_list_request = build_request_to_self("/api/projects")
    projects_json_data = requests.get(projects_list_request).json()
    
    for raw_project in projects_json_data["data"]:
        formated_project = Project({
            "title": raw_project[0],
            "desc": raw_project[1],
            "created_on": raw_project[2],
            "github_link": raw_project[3]
        })

        projects.append(formated_project.to_template_data_format())
    

    return render_template('home_dashboard.html', devices=devices, projects=projects)

@app.route('/projects', methods=["GET"]) 
def all_projects_view():
    projects = []

    projects_list_request = build_request_to_self("/api/projects")
    projects_json_data = requests.get(projects_list_request).json()

    if projects_json_data["status"] == "success": 
        for raw_project in projects_json_data["data"]:

            formated_project = Project()
            formated_project.inflate_from_sqlLite_dict({
                "title": raw_project[0],
                "desc": raw_project[1],
                "created_on": raw_project[2],
                "github_link": raw_project[3]
            })

            projects.append(formated_project.to_template_data_format())

    return render_template('projects_page.html', projects=projects)

@app.route('/projects/<project_name>', methods=["GET"])
def project_info_view(project_name: str):
    project = {}
    assocc_devices = []
    contributors = []

    # projects
    projects_list_request = build_request_to_self(f"/api/projects/{project_name}")
    projects_json_data = requests.get(projects_list_request).json()
    raw_project = projects_json_data["data"]

    formated_project = Project()
    formated_project.inflate_from_sqlLite_dict({
        "title": raw_project[0],
        "desc": raw_project[1],
        "created_on": raw_project[2],
        "github_link": raw_project[3]
    })


    # devices
    assocc_devices_list_request = build_request_to_self(f"/api/projects/{project_name}/devices")
    assocc_devices_json_data = requests.get(assocc_devices_list_request).json()

    for raw_assocc_device in assocc_devices_json_data["data"]:
        formated_device = Device()
        formated_device.inflate_from_sqlLite_dict({
            "mac_address": raw_assocc_device[0],
            "name": raw_assocc_device[1],
            "type": raw_assocc_device[2],
            "desc": raw_assocc_device[3],
        })

        assocc_devices.append(formated_device.to_template_data_format())


    return render_template("project_info_page.html", project=formated_project.to_template_data_format(), devices=assocc_devices)


@app.route('/devices', methods=["GET"])
def device_view():
    devices = []

    devices_list_request = build_request_to_self(f"/api/devices")
    devices_json_data = requests.get(devices_list_request).json()

    for raw_device in devices_json_data["data"]:
        formated_device = Device()
        formated_device.inflate_from_sqlLite_dict({
            "mac_address": raw_device[0],
            "name": raw_device[1],
            "type": raw_device[2],
            "desc": raw_device[3],
        })

        devices.append(formated_device.to_template_data_format())

    return render_template('devices_page.html', devices=devices)



@app.route('/devices/<mac_address>', methods=['GET'])
def specific_device_view(mac_address: str):
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
    devices_request_endpoint = build_request_to_self("/api/devices")
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


# @app.route('/api/info', methods=["GET"])
# def api_info_view():
#     return render_template("")


@app.route('/ping', methods=['GET'])
def ping():
    return 'Hello from Python server!\n'


@app.route('/api/devices', methods=["GET", "POST"])
def devices_api():
    if request.method == "GET":
        # get query parameters
        only_active_devices = request.args.get("only_active", default=False)

        devices = []

        with app.app_context():
            conn = dbo.get_db()
            cursor = conn.cursor()

            devices = dbo.get_all_devices(cursor, only_active_devices)
            
            conn.commit()

        return jsonify({'status': 'success', 'data': devices})
    
    elif request.method == "POST":
        return
    else:
        return jsonify({"status": "error", "msg": "invalid request method used"})



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
        try:
            data = request.get_json()

            # Extracting values from the JSON data
            creation_time = data.get('creation_time')
            status_code = data.get('status_code')
            log_data = data.get('log_data')

            # Extracting mac_address from the log_data
            mac_address = log_data.get('mac_address')

            # Assuming 'time_since_start' is a key in log_data
            time_since_start = log_data.get('time_since_start')

            time_delta = datetime.timedelta(seconds=time_since_start)
        

            # Now you can use creation_time, status_code, mac_address, log_data, and time_delta as needed

            # ... (perform database insertion or other operations)

            return jsonify({"status": "success", "msg": "Log successfully added"})

        except Exception as e:
            return jsonify({"status": "error", "msg": f"Failed to process the request: {str(e)}"})

        
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

@app.route('/api/projects/<project_name>', methods=["GET"])
def project_by_name(project_name):
    if request.method == "GET":
        project = {}

        with app.app_context():
            conn = dbo.get_db()
            cursor = conn.cursor()

            project = dbo.get_project_by_name(cursor, project_name)
            
            conn.commit()

        return jsonify({'status': 'success', 'data': project})
    else:
        return jsonify({"status": "error", "msg": "invalid request method used"})

@app.route('/api/projects/<project_name>/devices', methods=["GET"])
def devices_associated_to_project(project_name):
    if request.method == "GET":
        devices = []

        with app.app_context():
            conn = dbo.get_db()
            cursor = conn.cursor()

            devices = dbo.get_devices_by_project_name(cursor, project_name)
            
            conn.commit()

        return jsonify({'status': 'success', 'data': devices})
    else:
        return jsonify({"status": "error", "msg": "invalid request method used"})


@app.route('/api/device/<mac_address>/initialize', methods=["POST"])
def device_initialization(mac_address):

    # find the type of the device, we can format the data based off of that

    # if mac_address in active_connections:
    #     # end currently running recording

    

    # # begin new recording
    # # the new recording will be assumed to be under the same person who checked out 
    # active_connections[mac_address] = 
    pass

@app.route('/api/device/<mac_address>/mpu-motion6', methods=['POST'])
def device_data_api(mac_address):
    '''
    api endpoint for all device data production
    '''

    # from the mac address, we can determine everything we need to about how to store the data in the db

    try:
        data = request.json  # Assuming the data is sent as JSON

        # find the type of the device, we can format the data based off of that

        
        with app.app_context():
            conn = dbo.get_db()
            cursor = conn.cursor()

            dbo.get_de

        
        
        return jsonify({'status': 'success', 'message': 'Data received successfully'})

    except KeyError as e:
        # Handle missing keys in the request data
        return jsonify({'status': 'error', 'message': f'Missing key: {str(e)}'}), 400

    except Exception as e:
        # Handle other exceptions
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     DEBUG_MODE = bool(sys.argv[2])
    app.run(host=HOST, port=PORT, debug=DEBUG_MODE)
