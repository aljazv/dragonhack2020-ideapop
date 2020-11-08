from app import app

@app.route('/coordinates', methods=['POST'])
def add_coordinates():
    print("Coordinates")
    return 'OK'