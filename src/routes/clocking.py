from flask import Blueprint, jsonify
from src.clocking_script import mark_point_scheduled

clocking_bp = Blueprint('clocking', __name__)

@clocking_bp.route('/mark_lunch_out', methods=['POST'])
def mark_lunch_out():
    mark_point_scheduled(12, 28, 32)
    return jsonify({"message": "Marcação de saída para almoço agendada."})

@clocking_bp.route('/mark_lunch_in', methods=['POST'])
def mark_lunch_in():
    mark_point_scheduled(13, 28, 32)
    return jsonify({"message": "Marcação de entrada do almoço agendada."})

@clocking_bp.route('/mark_end_of_day', methods=['POST'])
def mark_end_of_day():
    mark_point_scheduled(17, 30, 35)
    return jsonify({"message": "Marcação de fim de expediente agendada."})


