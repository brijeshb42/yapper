import app

if __name__ == '__main__':
    ap = app.create_app('dev')
    ap.run(port=8080, debug=True)