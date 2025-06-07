from flask import Blueprint, render_template, flash,request, jsonify, send_file, redirect, url_for
from flask_login import login_required, current_user, logout_user, login_user
from forms import LoginForm, RegistrationForm
from models import User, Report, db
from scripts import *
import logging
import os
import pandas as pd
from helpers import seperate_firewall, extract_and_merge_firewall_status

main_bp = Blueprint('main', __name__)

# Create a handler for console output
handler = logging.StreamHandler()

# Define a custom log message format
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

# Assign the formatter to the handler
handler.setFormatter(formatter)

# Get the root logger and add the handler
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)


scripts = {'QuickScan': quick_scan,'IntenseScan': intense_scan,'RegularScan': regular_scan,'SlowComprehensiveScan': slow_comprehensive_scan,
    'PingScan': ping_scan,'QuickScanPlus': quick_scan_plus,'IntenseScanNoPing': intense_scan_no_ping,'IntenseScanPlusUDP': intense_scan_plus_udp,
    'IntenseScanAllTCP': intense_scan_all_tcp,'FireWallStatus': FireWall}

@main_bp.route('/')
def index():
    return render_template('home_test.html')

@main_bp.route('/report/<id>')
@login_required
def report(id):
    report = db.session.query(Report).filter_by(id=id, user_id=current_user.id).first()
    image_data = None
    FireWall_report = None

    # load report csv data 
    report_date = report.scan_date.strftime("%Y-%m-%d-%H-%M-%S")

    report_data = pd.read_csv(f'data/{current_user.username}/{report.name}_{report.scan_type}_{report_date}.csv',index_col=None)
   # report_data.fillna('N/A', inplace=True)

    #check if it is a firewall report seperate the data and firewall status
    if report.scan_type == 'FireWallStatus':
        report_data, FireWall_report = seperate_firewall(report_data) 
        FireWall_report = [FireWall_report.IP, FireWall_report.Version] 

    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    
    #root_logger.info(f'orginal data {report_data}')
    
    if report.option:
        image_data = generate_report(report_data)

    # map the report data to list of records
    report_data = report_data.to_dict(orient='records')

    return render_template('report_test.html',report=report_data,figures=image_data,firewall_report=FireWall_report)

@main_bp.route('/download-report/<id>')
@login_required
def download_report(id):
    report = db.session.query(Report).filter_by(id=id, user_id=current_user.id).first()
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    report_date = report.scan_date.strftime("%Y-%m-%d-%H-%M-%S")
    report_path = f'data/{current_user.username}/{report.name}_{report.scan_type}_{report_date}.csv'
    
    if not os.path.exists(report_path):
        return jsonify({'error': 'Report not found'}), 404
    return send_file(report_path, as_attachment=True)

@main_bp.route('/profile')
@login_required
def profile():
    scans = []
    reports = db.session.query(Report).filter_by(user_id=current_user.id).all()
    root_logger.info(f'reports are {reports}')
    for report in reports:
        report_id = report.id
        report_name = report.name
        report_date = report.scan_date.strftime("%Y-%m-%d")
        report_type = report.scan_type
        scans.append({'id': report_id, 'name': report_name, 'date': report_date, 'type': report_type})
    return render_template('profile_test.html',scans=scans)

@main_bp.route('/scan', methods=['GET', 'POST'])
@login_required
def scan():
    if request.method == 'POST':
        ip_address = request.form.get('ip')
        scan_type = request.form.get('scan_type')
        option = request.form.get('option')
        root_logger.info(f'option is {option}')

        try:
            # Call the appropriate Python script based on scan_type
            script = scripts[scan_type]
            df = script(ip_address)
            root_logger.info(f'here is the scan results: {df}')

            # Sanitize the IP address for use in a file name
            sanitized_ip = ip_address.replace('/', '_')  # Replace '/' with '_'
            root_logger.info(f'Sanitized IP: {sanitized_ip}')

            if df.empty:
                root_logger.error(f'No results found for {ip_address} using {scan_type} scan')
                return jsonify({'status': 'error', 'message': f'No results found for {ip_address} using {scan_type} scan'}), 400

            # Create a report object
            report = Report(name=sanitized_ip, scan_type=scan_type, user_id=current_user.id)

            # Merge datasets if option is true and scan type is not PingScan
            if option == 'true' and scan_type != 'PingScan':
                merged_df = merge_datasets(df)
                report.option = True
            else:
                merged_df = df
                report.option = False

            root_logger.info(f'{merged_df}')

            # Add the report to the database
            db.session.add(report)
            db.session.commit()

            # Handle FireWallStatus scan type
            if scan_type == 'FireWallStatus':
                merged_df = extract_and_merge_firewall_status(df, merged_df)

            root_logger.info(f'report id is {report.id}')
            root_logger.info(f'{current_user.username} is scanning {ip_address} using {scan_type} scan')

           

            # Save the DataFrame to a CSV file
            report_date = report.scan_date.strftime("%Y-%m-%d-%H-%M-%S")
            file_name = f'{sanitized_ip}_{scan_type}_{report_date}.csv'
            file_path = f'data/{current_user.username}/{file_name}'

            merged_df.to_csv(file_path, index=False)

            root_logger.info(f'{current_user.username} scan is completed')

            return jsonify({'status': 'success', 'report_id': report.id}), 200

        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            root_logger.error(f'Error: {str(e)}')
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return render_template('scan_test.html')



@main_bp.route('/clearall',methods=['POST'])
@login_required
def clearall():
    reports = db.session.query(Report).filter_by(user_id=current_user.id).all()
    if not reports:
        return jsonify({'status': 'error', 'message': 'No reports found'}), 404
    for report in reports:
        db.session.delete(report)
        report_date = report.scan_date.strftime("%Y-%m-%d-%H-%M-%S")
        os.remove(f'data/{current_user.username}/{report.name}_{report.scan_type}_{report_date}.csv')
    db.session.commit()
    return jsonify({'status': 'success'}), 200

@main_bp.route('/clear',methods=['POST'])
@login_required
def clear():    
    data = request.get_json()
    if not data or 'ids' not in data:
        return jsonify({'error': 'No IDs provided'}), 400

    ids = data['ids']
    if not isinstance(ids, list):
        return jsonify({'error': 'IDs should be provided as a list'}), 400

    # Iterate over the list of IDs and delete the corresponding reports
    for id in ids:
        report = db.session.query(Report).filter_by(id=id, user_id=current_user.id).first()
        if report:
            db.session.delete(report)
            report_date = report.scan_date.strftime("%Y-%m-%d-%H-%M-%S")
            os.remove(f'data/{current_user.username}/{report.name}_{report.scan_type}_{report_date}.csv')
    db.session.commit()

    return jsonify({'message': 'Reports deleted successfully'}), 200

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        root_logger.info(f'Login attempt for email: {form.email.data}')
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            root_logger.info(f'{user.username} logged in successfully')
            return jsonify({'message': 'User logged in successfully'}), 200

        root_logger.error('Invalid username or password.')
        return jsonify({'message': 'Invalid username or password.'}), 401

    return render_template('login.html', form=form)
@main_bp.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    root_logger.info('logged out')
    #flash('You have been logged out.')
    return redirect(url_for('main.login'))
@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        root_logger.info(f'{current_user.username} is already logged in')
        return redirect(url_for('profile'))

    root_logger.info('signing up')
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if passwords match
        if form.password.data != form.confirm_password.data:
            return jsonify({'message': 'Passwords do not match'}), 400

        user_exists = User.query.filter_by(email=form.email.data).first()
        if user_exists:
            root_logger.info(f'{form.email.data} already exists')
            return jsonify({'message': 'User already exists'}), 409

        try:
            root_logger.info(f'{form.username.data} is trying to register')

            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            try:
                os.makedirs(f"data/{user.username}", exist_ok=True)
            except Exception as e:
                root_logger.error(f"Error creating user directory: {e}")
                db.session.rollback()
                return jsonify({'message': 'Error: User directory creation failed. Please try again.'}), 500

            root_logger.info(f'{user.username} registered successfully')
            return jsonify({'message': 'User registered successfully'}), 200

        except Exception as e:
            db.session.rollback()
            root_logger.error(e)
            return jsonify({'message': 'Error: User registration failed. Please try again.'}), 500

    return render_template('signup.html', form=form)