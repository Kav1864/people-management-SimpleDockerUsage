from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import IntegrityError
import os

app = Flask(__name__)

CORS(app)

# Database configuration
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "people_db")
}


# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)


# Add a person
@app.route('/people', methods=['POST'])
def add_person():

    conn = None
    cursor = None

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        name = data.get('name')
        age = data.get('age')
        email = data.get('email')
        city = data.get('city')

        if not all([name, age, email, city]):
            return jsonify({
                "error": "All fields are required"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO people (name, age, email, city)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (name, age, email, city))

        conn.commit()

        return jsonify({
            "message": "Person added successfully!"
        }), 201

    except IntegrityError:
        if conn:
            conn.rollback()

        return jsonify({
            "error": "This email address already exists!"
        }), 409

    except mysql.connector.Error as e:
        if conn:
            conn.rollback()

        app.logger.exception("Database operation failed")

        return jsonify({
            "error": "Database operation failed"
        }), 500

    except Exception:
        app.logger.exception("Unexpected error")

        return jsonify({
            "error": "Something went wrong"
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# Retrieve all people
@app.route('/people', methods=['GET'])
def get_people():

    conn = None
    cursor = None

    try:
        conn = get_db_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM people ORDER BY id DESC")

        people = cursor.fetchall()

        return jsonify(people), 200

    except mysql.connector.Error:
        app.logger.exception("Unable to retrieve people")

        return jsonify({
            "error": "Unable to retrieve records"
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# Health check
@app.route('/health', methods=['GET'])
def health():

    return jsonify({
        "status": "Backend is running"
    }), 200


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000
    )
