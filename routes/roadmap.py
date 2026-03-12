from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models.database import db
from models.roadmap import Roadmap, Node, Resource
from models.progress import Progress
from ai_engine.generator import generate_roadmap

roadmap_bp = Blueprint('roadmap', __name__)

@roadmap_bp.route('/dashboard')
@login_required
def dashboard():
    roadmaps = Roadmap.query.filter_by(user_id=current_user.id).order_by(Roadmap.created_at.desc()).all()
    return render_template('dashboard.html', roadmaps=roadmaps)

@roadmap_bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        topic = request.form.get('topic')
        if not topic:
            flash('Please enter a topic!', 'error')
            return redirect(url_for('roadmap.generate'))
        try:
            data = generate_roadmap(topic)

            roadmap = Roadmap(
                user_id=current_user.id,
                topic=data['topic'],
                difficulty=data.get('difficulty', 'Beginner'),
                estimated_weeks=data.get('estimated_weeks', 8)
            )
            db.session.add(roadmap)
            db.session.flush()

            for node_data in data['nodes']:
                node = Node(
                    roadmap_id=roadmap.id,
                    title=node_data['title'],
                    description=node_data['description'],
                    node_order=node_data['order'],
                    difficulty=node_data.get('difficulty', 'Beginner'),
                    estimated_hours=node_data.get('estimated_hours', 5)
                )
                db.session.add(node)
                db.session.flush()

                for res in node_data.get('resources', []):
                    resource = Resource(
                        node_id=node.id,
                        title=res['title'],
                        url=res['url'],
                        resource_type=res.get('type', 'article')
                    )
                    db.session.add(resource)

            db.session.commit()
            flash('Roadmap generated successfully!', 'success')
            return redirect(url_for('roadmap.view_roadmap', roadmap_id=roadmap.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error generating roadmap: {str(e)}', 'error')
            return redirect(url_for('roadmap.generate'))

    return render_template('generate.html')

@roadmap_bp.route('/roadmap/<int:roadmap_id>')
@login_required
def view_roadmap(roadmap_id):
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    nodes = Node.query.filter_by(roadmap_id=roadmap_id).order_by(Node.node_order).all()

    progress_map = {}
    for node in nodes:
        p = Progress.query.filter_by(user_id=current_user.id, node_id=node.id).first()
        progress_map[node.id] = p.status if p else 'pending'

    completed = sum(1 for s in progress_map.values() if s == 'done')
    percent = int((completed / len(nodes)) * 100) if nodes else 0

    return render_template('roadmap.html',
                           roadmap=roadmap,
                           nodes=nodes,
                           progress_map=progress_map,
                           percent=percent)

@roadmap_bp.route('/roadmap/delete/<int:roadmap_id>', methods=['POST'])
@login_required
def delete_roadmap(roadmap_id):
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    if roadmap.user_id != current_user.id:
        flash('Unauthorized!', 'error')
        return redirect(url_for('roadmap.dashboard'))
    db.session.delete(roadmap)
    db.session.commit()
    flash('Roadmap deleted.', 'success')
    return redirect(url_for('roadmap.dashboard'))