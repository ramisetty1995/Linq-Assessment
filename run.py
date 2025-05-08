from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    print(f"JWT Secret Key: {app.config['JWT_SECRET_KEY']}")
    print(f"Secret Key: {app.config['SECRET_KEY']}")
