import app

if __name__ == '__main__':
    ap = app.create_app('default')
    ap.run(port=8080, debug=True)