from backend import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        from backend import db
        db.create_all()
    app.run(debug=False, use_reloader=False, port=5001)