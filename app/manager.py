from application import manager, db
from www import *
import threading
from flask_script import Server, Command
# web server
import application as app
manager.add_command("runserver", Server(host="0.0.0.0", use_debugger=True, use_reloader=True,threaded=True))


# create_table

@Command
def create_all():
    db.create_all()


manager.add_command("create_all", create_all)


def main():
    manager.run()



if __name__ == '__main__':
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()
