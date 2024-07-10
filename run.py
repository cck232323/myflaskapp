import werkzeug
import werkzeug.utils
import werkzeug.datastructures

werkzeug.secure_filename = werkzeug.utils.secure_filename
werkzeug.FileStorage = werkzeug.datastructures.FileStorage

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


