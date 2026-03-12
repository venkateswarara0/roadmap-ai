from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.roadmap import Node
from models.progress import QuizResult
from ai_engine.generator import generate_quiz, chat_with_advisor

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quiz/<int:node_id>')
@login_required
def quiz(node_id):
    node = Node.query.get_or_404(node_id)
    roadmap = node.roadmap
    questions = generate_quiz(roadmap.topic, node.title)
    return render_template('quiz.html', node=node, questions=questions, roadmap=roadmap)

@quiz_bp.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    data = request.get_json()
    node_id = data.get('node_id')
    score = data.get('score')
    total = data.get('total')

    result = QuizResult(
        user_id=current_user.id,
        node_id=node_id,
        score=score,
        total_questions=total
    )
    db.session.add(result)
    db.session.commit()

    return jsonify({'success': True, 'score': score, 'total': total})

@quiz_bp.route('/advisor/<int:roadmap_id>', methods=['POST'])
@login_required
def advisor(roadmap_id):
    from models.roadmap import Roadmap
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    data = request.get_json()
    message = data.get('message', '')
    history = data.get('history', [])

    reply = chat_with_advisor(roadmap.topic, message, history)
    return jsonify({'reply': reply})