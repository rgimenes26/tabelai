from webapp import app
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Dashboard Sistemático")
    parser.add_argument("-d", "--debug", action="store_true", default=False)
    parser.add_argument("-p", "--port", nargs='?', const=80, type=int, help='Filename without extension.')
    args = parser.parse_args()
    PORT = args.port
    
    if args.debug:    
        app.run(debug=True, port=5000)
    else:
        from waitress import serve
        serve(app, _quiet=False, host='0.0.0.0', port=5000, threads=14, url_scheme='https')
