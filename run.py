from app import app, db

if __name__ == '__main__':
    print("Starting application...")
    app.logger.info("Application starting up")
    app.run(debug=True, host='0.0.0.0', port=5000)

