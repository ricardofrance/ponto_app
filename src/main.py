import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from src.clocking_script import mark_point_scheduled
from src.models.user import db
from src.routes.user import user_bp
from src.routes.clocking import clocking_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(clocking_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


from apscheduler.schedulers.background import BackgroundScheduler
from src.clocking_script import mark_point_scheduled

# Configuração do APScheduler
scheduler = BackgroundScheduler()

def schedule_all_clockings():
    # Saída do almoço (12:28-12:32)
    scheduler.add_job(mark_point_scheduled, 'cron', day_of_week='mon-fri', hour=12, minute='28-32', args=[12, 28, 32], id='lunch_out', replace_existing=True)
    # Entrada do almoço (13:28-13:32)
    scheduler.add_job(mark_point_scheduled, 'cron', day_of_week='mon-fri', hour=13, minute='28-32', args=[13, 28, 32], id='lunch_in', replace_existing=True)
    # Final do expediente (17:30-17:35)
    scheduler.add_job(mark_point_scheduled, 'cron', day_of_week='mon-fri', hour=17, minute='30-35', args=[17, 30, 35], id='end_of_day', replace_existing=True)
    print("Tarefas de marcação de ponto agendadas.")

if __name__ == '__main__':
    schedule_all_clockings()
    scheduler.start()
    app.run(host='0.0.0.0', port=5000, debug=True)

