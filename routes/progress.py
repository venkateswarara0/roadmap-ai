from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.database import db
from models.progress import Progress
from datetime import date

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/update_progress', methods=['POST'])
@login_required
def update_progress():
    data = request.get_json()
    node_id = data.get('node_id')
    status = data.get('status')

    if status not in ['pending', 'in_progress', 'done']:
        return jsonify({'error': 'Invalid status'}), 400

    progress = Progress.query.filter_by(
        user_id=current_user.id,
        node_id=node_id
    ).first()

    if progress:
        progress.status = status
    else:
        progress = Progress(user_id=current_user.id, node_id=node_id, status=status)
        db.session.add(progress)

    current_user.last_active = date.today()
    db.session.commit()

    return jsonify({'success': True, 'status': status})