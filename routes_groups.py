from flask import Blueprint, request, jsonify, session
from app import db
from models import User, UserGroup, GroupMember, ContentShare, Notification, CustomRecipePage, CoCreationDraft
from sqlalchemy import or_

groups_bp = Blueprint('groups', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@groups_bp.route('/api/users/search', methods=['GET'])
@login_required
def search_users():
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])

    current_user_id = session.get('user_id')
    users = User.query.filter(
        (User.name.ilike(f'%{query}%')) | (User.email.ilike(f'%{query}%')),
        User.id != current_user_id
    ).limit(10).all()

    return jsonify([{
        'id': u.id,
        'name': u.name,
        'email': u.email,
        'department': u.department,
        'position': u.position
    } for u in users])

@groups_bp.route('/api/groups', methods=['GET', 'POST'])
@login_required
def groups():
    user_id = session.get('user_id')

    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        members = data.get('members', []) # List of user IDs

        if not name:
            return jsonify({'success': False, 'error': 'Group name is required'}), 400

        group = UserGroup(name=name, description=description, created_by=user_id)
        db.session.add(group)
        db.session.flush() # Get ID

        # Add creator as owner
        owner_membership = GroupMember(group_id=group.id, user_id=user_id, role='owner')
        db.session.add(owner_membership)

        # Add other members
        for member_id in members:
            if member_id != user_id:
                membership = GroupMember(group_id=group.id, user_id=member_id, role='member')
                db.session.add(membership)

                # Notification
                notif = Notification(
                    recipient_id=member_id,
                    type='group_invite',
                    message=f"You have been added to group '{group.name}'",
                    link=f"/groups/{group.id}" # Handled by frontend to open sidebar
                )
                db.session.add(notif)

        db.session.commit()
        return jsonify({'success': True, 'group': {'id': group.id, 'name': group.name}})

    else: # GET
        # Groups where user is a member
        memberships = GroupMember.query.filter_by(user_id=user_id).all()
        group_ids = [m.group_id for m in memberships]
        groups = UserGroup.query.filter(UserGroup.id.in_(group_ids)).all()

        return jsonify([{
            'id': g.id,
            'name': g.name,
            'description': g.description,
            'role': next((m.role for m in memberships if m.group_id == g.id), 'member'),
            'member_count': len(g.members)
        } for g in groups])

@groups_bp.route('/api/groups/<int:group_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def group_detail(group_id):
    user_id = session.get('user_id')
    group = UserGroup.query.get_or_404(group_id)
    membership = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()

    if not membership:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    if request.method == 'GET':
        members = []
        for m in group.members:
            members.append({
                'user_id': m.user.id,
                'name': m.user.name,
                'email': m.user.email,
                'role': m.role,
                'joined_at': m.joined_at.isoformat()
            })

        return jsonify({
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'my_role': membership.role,
            'members': members
        })

    elif request.method == 'PUT':
        if membership.role not in ['owner', 'admin']:
            return jsonify({'success': False, 'error': 'Permission denied'}), 403

        data = request.get_json()
        group.name = data.get('name', group.name).strip()
        group.description = data.get('description', group.description).strip()
        db.session.commit()
        return jsonify({'success': True})

    elif request.method == 'DELETE':
        if membership.role != 'owner':
            return jsonify({'success': False, 'error': 'Only the owner can delete the group'}), 403

        db.session.delete(group)
        db.session.commit()
        return jsonify({'success': True})

@groups_bp.route('/api/groups/<int:group_id>/members', methods=['POST'])
@login_required
def add_member(group_id):
    user_id = session.get('user_id')
    group = UserGroup.query.get_or_404(group_id)
    membership = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()

    if not membership or membership.role not in ['owner', 'admin']:
        return jsonify({'success': False, 'error': 'Permission denied'}), 403

    data = request.get_json()
    new_member_id = data.get('user_id')

    existing = GroupMember.query.filter_by(group_id=group_id, user_id=new_member_id).first()
    if existing:
        return jsonify({'success': False, 'error': 'User is already a member'}), 400

    new_member = GroupMember(group_id=group_id, user_id=new_member_id, role='member')
    db.session.add(new_member)

    notif = Notification(
        recipient_id=new_member_id,
        type='group_invite',
        message=f"You have been added to group '{group.name}'",
        link=f"/groups/{group.id}"
    )
    db.session.add(notif)

    db.session.commit()
    return jsonify({'success': True})

@groups_bp.route('/api/groups/<int:group_id>/members/<int:member_id>', methods=['PUT', 'DELETE'])
@login_required
def manage_member(group_id, member_id):
    user_id = session.get('user_id')
    group = UserGroup.query.get_or_404(group_id)
    requester_membership = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()
    target_membership = GroupMember.query.filter_by(group_id=group_id, user_id=member_id).first()

    if not requester_membership or not target_membership:
        return jsonify({'success': False, 'error': 'Member not found'}), 404

    if requester_membership.role not in ['owner', 'admin']:
        return jsonify({'success': False, 'error': 'Permission denied'}), 403

    # Prevent modifying owner
    if target_membership.role == 'owner' and user_id != member_id:
         return jsonify({'success': False, 'error': 'Cannot modify owner'}), 403

    if request.method == 'DELETE':
        # Self-leave logic or remove other logic
        if user_id == member_id:
             # Leaving group
             if requester_membership.role == 'owner':
                  return jsonify({'success': False, 'error': 'Owner cannot leave group, delete it instead'}), 400
        else:
             # Removing someone else
             if requester_membership.role == 'admin' and target_membership.role in ['owner', 'admin']:
                  return jsonify({'success': False, 'error': 'Admins cannot remove other admins or owners'}), 403

        db.session.delete(target_membership)

        # Revoke access to group shared content?
        # Actually logic for checking access will handle it (since they are no longer in group)

        db.session.commit()
        return jsonify({'success': True})

    elif request.method == 'PUT':
        if requester_membership.role != 'owner':
            return jsonify({'success': False, 'error': 'Only owner can change roles'}), 403

        data = request.get_json()
        new_role = data.get('role')
        if new_role not in ['admin', 'member']:
            return jsonify({'success': False, 'error': 'Invalid role'}), 400

        target_membership.role = new_role

        notif = Notification(
            recipient_id=member_id,
            type='role_change',
            message=f"Your role in group '{group.name}' has been changed to {new_role}",
            link=f"/groups/{group.id}"
        )
        db.session.add(notif)

        db.session.commit()
        return jsonify({'success': True})
