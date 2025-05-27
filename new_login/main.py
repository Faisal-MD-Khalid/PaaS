from flask import Flask, request, render_template_string, jsonify
import mysql.connector
import os
from mysql.connector import Error
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration - Using environment variables for Render
DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'port': int(os.environ.get('DB_PORT', 3306)),  # Changed default port to standard MySQL
    'database': os.environ.get('DB_NAME', 'defaultdb'),  # Set default database name
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'ssl_disabled': False,
    'ssl_verify_cert': False,  # Aiven compatibility
    'autocommit': True,
    'use_unicode': True,
    'charset': 'utf8mb4',
    'connect_timeout': 60,  # Added connection timeout
    'sql_mode': 'STRICT_TRANS_TABLES'  # Added for better data integrity
}

def get_db_connection():
    """Create and return a database connection with improved error handling"""
    try:
        # Remove None values from config to avoid connection issues
        config = {k: v for k, v in DB_CONFIG.items() if v is not None}
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            logger.info("Database connection established successfully")
            return connection
        else:
            logger.error("Database connection failed")
            return None
            
    except Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during database connection: {e}")
        return None

def validate_user(username, password, email=None, phone=None):
    """Validate user credentials against existing database with additional info"""
    connection = get_db_connection()
    if not connection:
        logger.error("No database connection available")
        return False
    
    cursor = None
    try:
        cursor = connection.cursor(buffered=True)  # Use buffered cursor
        
        # Log validation attempt (without password for security)
        logger.info(f"Attempting to validate user: '{username}'")
        if email:
            logger.info(f"Email provided: '{email}'")
        if phone:
            logger.info(f"Phone provided: '{phone}'")
        
        # Debug: Check table structure first
        try:
            cursor.execute("DESCRIBE User_info")
            columns = cursor.fetchall()
            logger.info(f"Table structure: {columns}")
        except Error as e:
            logger.error(f"Error checking table structure: {e}")
        
        # Build dynamic query based on provided information
        base_query = "SELECT user_id, user_name, password, email, phone FROM User_info WHERE user_name = %s AND password = %s"
        params = [username, password]
        
        # Add email check if provided and not empty
        if email and email.strip():
            base_query += " AND email = %s"
            params.append(email.strip())
        
        # Add phone check if provided and not empty
        if phone and phone.strip():
            base_query += " AND phone = %s"
            params.append(phone.strip())
        
        logger.info(f"Executing query with {len(params)} parameters")
        
        cursor.execute(base_query, params)
        result = cursor.fetchone()
        
        if result:
            logger.info("User validation successful!")
            return True
        else:
            # Try case-insensitive search for username and email
            logger.info("Trying case-insensitive search")
            case_query = "SELECT user_id, user_name, password, email, phone FROM User_info WHERE LOWER(user_name) = LOWER(%s) AND password = %s"
            case_params = [username, password]
            
            if email and email.strip():
                case_query += " AND LOWER(email) = LOWER(%s)"
                case_params.append(email.strip())
            
            if phone and phone.strip():
                case_query += " AND phone = %s"
                case_params.append(phone.strip())
            
            cursor.execute(case_query, case_params)
            result_case = cursor.fetchone()
            
            if result_case:
                logger.info("User validation successful (case-insensitive)!")
                return True
            else:
                logger.info("No matching user found")
                return False
                
    except Error as e:
        logger.error(f"Database error validating user: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error validating user: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# HTML template for login form - MODIFIED INTERFACE
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Login Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            width: 100%;
            max-width: 450px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .logo h1 {
            color: #2d3748;
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .logo p {
            color: #718096;
            font-size: 14px;
            font-weight: 400;
        }
        
        .form-section {
            margin-bottom: 25px;
        }
        
        .section-title {
            color: #2d3748;
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        
        .section-title::before {
            content: "";
            width: 4px;
            height: 16px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            margin-right: 10px;
            border-radius: 2px;
        }
        
        .input-group {
            margin-bottom: 20px;
            position: relative;
        }
        
        .input-group label {
            display: block;
            color: #4a5568;
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 8px;
        }
        
        .required-star {
            color: #e53e3e;
            margin-left: 4px;
        }
        
        .input-field {
            width: 100%;
            padding: 14px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 16px;
            font-family: inherit;
            transition: all 0.3s ease;
            background: #ffffff;
        }
        
        .input-field:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            transform: translateY(-2px);
        }
        
        .input-field::placeholder {
            color: #a0aec0;
        }
        
        .optional-text {
            color: #718096;
            font-size: 12px;
            margin-top: 5px;
            font-style: italic;
        }
        
        .divider {
            margin: 30px 0;
            position: relative;
            text-align: center;
        }
        
        .divider::before {
            content: "";
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        }
        
        .divider-text {
            background: rgba(255, 255, 255, 0.95);
            color: #718096;
            padding: 0 20px;
            font-size: 14px;
            font-weight: 500;
        }
        
        .login-btn {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 16px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }
        
        .login-btn:active {
            transform: translateY(0);
        }
        
        .message {
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 20px;
            font-weight: 500;
            text-align: center;
        }
        
        .success {
            background: linear-gradient(135deg, #48bb78, #38a169);
            color: white;
            border: none;
        }
        
        .error {
            background: linear-gradient(135deg, #f56565, #e53e3e);
            color: white;
            border: none;
        }
        
        .footer-links {
            text-align: center;
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
        }
        
        .footer-links a {
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.3s ease;
        }
        
        .footer-links a:hover {
            color: #764ba2;
        }
        
        .info-badge {
            background: linear-gradient(135deg, #4299e1, #3182ce);
            color: white;
            padding: 12px 16px;
            border-radius: 12px;
            margin-bottom: 25px;
            font-size: 14px;
            text-align: center;
        }
        
        @media (max-width: 480px) {
            .login-container {
                padding: 30px 25px;
            }
            
            .logo h1 {
                font-size: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <h1>SecureAccess</h1>
            <p>Advanced Authentication System</p>
        </div>
        
        <div class="info-badge">
            🔐 Multi-factor authentication with optional email & phone verification
        </div>
        
        {% if message %}
            <div class="message {{ message_type }}">{{ message }}</div>
        {% endif %}
        
        <form method="POST" action="/login">
            <div class="form-section">
                <div class="section-title">Primary Credentials</div>
                
                <div class="input-group">
                    <label for="username">Username<span class="required-star">*</span></label>
                    <input type="text" id="username" name="username" class="input-field" required 
                           value="{{ request.form.username if request.form.username else '' }}"
                           placeholder="Enter your username">
                </div>
                
                <div class="input-group">
                    <label for="password">Password<span class="required-star">*</span></label>
                    <input type="password" id="password" name="password" class="input-field" required
                           placeholder="Enter your password">
                </div>
            </div>
            
            <div class="divider">
                <span class="divider-text">Enhanced Security</span>
            </div>
            
            <div class="form-section">
                <div class="section-title">Additional Verification</div>
                
                <div class="input-group">
                    <label for="email">Email Address</label>
                    <input type="email" id="email" name="email" class="input-field"
                           placeholder="your.email@example.com"
                           value="{{ request.form.email if request.form.email else '' }}">
                    <div class="optional-text">Optional - Leave blank to skip email verification</div>
                </div>
                
                <div class="input-group">
                    <label for="phone">Phone Number</label>
                    <input type="tel" id="phone" name="phone" class="input-field"
                           placeholder="+1 (555) 123-4567"
                           value="{{ request.form.phone if request.form.phone else '' }}">
                    <div class="optional-text">Optional - Leave blank to skip phone verification</div>
                </div>
            </div>
            
            <button type="submit" class="login-btn">Authenticate</button>
        </form>
        
        <div class="footer-links">
            <a href="/debug">System Diagnostics</a> | 
            <a href="/health">Health Check</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Display login form"""
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    """Handle login form submission with improved error handling"""
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Validate required fields
        if not username or not password:
            return render_template_string(LOGIN_TEMPLATE, 
                                        message="Please enter both username and password", 
                                        message_type="error",
                                        request=request)
        
        # Check database connection first
        connection = get_db_connection()
        if not connection:
            logger.error("Database connection failed during login attempt")
            return render_template_string(LOGIN_TEMPLATE, 
                                        message="Database connection failed. Please check your environment variables and try again.", 
                                        message_type="error",
                                        request=request)
        connection.close()
        
        # Attempt user validation
        if validate_user(username, password, email, phone):
            verification_details = []
            if email:
                verification_details.append(f"email ({email})")
            if phone:
                verification_details.append(f"phone ({phone})")
            
            success_message = f"Login successful! Welcome, {username}!"
            if verification_details:
                success_message += f" Additional verification passed for: {', '.join(verification_details)}"
            
            logger.info(f"Successful login for user: {username}")
            return render_template_string(LOGIN_TEMPLATE, 
                                        message=success_message, 
                                        message_type="success",
                                        request=request)
        else:
            error_message = "Invalid credentials. Please check your username and password."
            if email:
                error_message += " Email verification also failed."
            if phone:
                error_message += " Phone verification also failed."
            
            logger.warning(f"Failed login attempt for user: {username}")
            return render_template_string(LOGIN_TEMPLATE, 
                                        message=error_message, 
                                        message_type="error",
                                        request=request)
            
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        return render_template_string(LOGIN_TEMPLATE, 
                                    message=f"An unexpected error occurred. Please try again.", 
                                    message_type="error",
                                    request=request)

@app.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint for login validation with improved error handling"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No JSON data provided'}), 400
            
        if 'username' not in data or 'password' not in data:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        
        username = data['username'].strip()
        password = data['password'].strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password cannot be empty'}), 400
        
        if validate_user(username, password, email, phone):
            verification_info = []
            if email:
                verification_info.append('email')
            if phone:
                verification_info.append('phone')
            
            message = f'Login successful for {username}'
            if verification_info:
                message += f' with additional verification: {", ".join(verification_info)}'
            
            logger.info(f"API login successful for user: {username}")
            return jsonify({'success': True, 'message': message})
        else:
            logger.warning(f"API login failed for user: {username}")
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        logger.error(f"API login error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

def safe_convert_to_json(value):
    """Safely convert database values to JSON-serializable format"""
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8')
        except UnicodeDecodeError:
            return f"<binary data: {len(value)} bytes>"
    elif isinstance(value, (int, float, str, bool)) or value is None:
        return value
    else:
        return str(value)

@app.route('/debug')
def debug_info():
    """Debug endpoint to check database connection and data"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'No database connection', 'db_config': {
            'host': os.environ.get('DB_HOST', 'Not set'),
            'port': os.environ.get('DB_PORT', 'Not set'),
            'database': os.environ.get('DB_NAME', 'Not set'),
            'user': os.environ.get('DB_USER', 'Not set')
        }}), 500
    
    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        
        # Check if table exists
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        # Get table structure
        cursor.execute("DESCRIBE User_info")
        columns = cursor.fetchall()
        
        # Get sample data (first 5 rows, hiding passwords)
        cursor.execute("SELECT user_id, user_name, 'HIDDEN' as password, email, phone FROM User_info LIMIT 5")
        sample_data = cursor.fetchall()
        
        # Count total users
        cursor.execute("SELECT COUNT(*) FROM User_info")
        user_count = cursor.fetchone()[0]
        
        # Safely convert all data to JSON-serializable format
        safe_tables = [safe_convert_to_json(table[0]) for table in tables]
        safe_columns = [{'Field': safe_convert_to_json(col[0]), 
                        'Type': safe_convert_to_json(col[1]), 
                        'Null': safe_convert_to_json(col[2]), 
                        'Key': safe_convert_to_json(col[3])} for col in columns]
        safe_users = [{'user_id': safe_convert_to_json(row[0]), 
                      'user_name': safe_convert_to_json(row[1]), 
                      'password': safe_convert_to_json(row[2]), 
                      'email': safe_convert_to_json(row[3]), 
                      'phone': safe_convert_to_json(row[4])} for row in sample_data]
        
        return jsonify({
            'database_connected': True,
            'tables': safe_tables,
            'user_info_columns': safe_columns,
            'sample_users': safe_users,
            'total_users': safe_convert_to_json(user_count),
            'db_config': {
                'host': os.environ.get('DB_HOST', 'Not set'),
                'port': os.environ.get('DB_PORT', 'Not set'),
                'database': os.environ.get('DB_NAME', 'Not set'),
                'user': os.environ.get('DB_USER', 'Not set')
            }
        })
        
    except Error as e:
        logger.error(f"Debug endpoint database error: {e}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Debug endpoint unexpected error: {e}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

@app.route('/health')
def health_check():
    """Health check endpoint with improved error handling"""
    connection = get_db_connection()
    if connection:
        cursor = None
        try:
            cursor = connection.cursor(buffered=True)
            cursor.execute("SELECT COUNT(*) FROM User_info")
            count = cursor.fetchone()[0]
            
            return jsonify({
                'status': 'healthy', 
                'database': 'connected',
                'users_count': safe_convert_to_json(count),
                'timestamp': safe_convert_to_json(request.environ.get('REQUEST_TIME', 'unknown'))
            })
        except Error as e:
            logger.error(f"Health check database error: {e}")
            return jsonify({
                'status': 'unhealthy', 
                'database': 'connected but query failed',
                'error': str(e)
            }), 500
        except Exception as e:
            logger.error(f"Health check unexpected error: {e}")
            return jsonify({
                'status': 'unhealthy', 
                'database': 'connected but unexpected error',
                'error': str(e)
            }), 500
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
    else:
        return jsonify({
            'status': 'unhealthy', 
            'database': 'disconnected',
            'message': 'Could not establish database connection'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

# Initialize database connection check on startup
if __name__ == '__main__':
    logger.info("Starting Flask application...")
    
    # Check environment variables
    required_env_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD']
    missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.warning("Application may not function properly without proper database configuration")
    
    # Test database connection
    connection = get_db_connection()
    if connection:
        logger.info("Database connection successful!")
        connection.close()
    else:
        logger.warning("Warning: Could not connect to database")
        logger.warning("Please check your environment variables:")
        logger.warning(f"DB_HOST: {os.environ.get('DB_HOST', 'Not set')}")
        logger.warning(f"DB_PORT: {os.environ.get('DB_PORT', 'Not set')}")
        logger.warning(f"DB_NAME: {os.environ.get('DB_NAME', 'Not set')}")
        logger.warning(f"DB_USER: {os.environ.get('DB_USER', 'Not set')}")
    
    # Start the application
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting server on port {port}")
    app.run(debug=True, host='0.0.0.0', port=port)
