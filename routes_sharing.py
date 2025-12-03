from flask import Blueprint, request, jsonify, session
from app import db
from models import User, UserGroup, GroupMember, ContentShare, Notification, CustomRecipePage, CoCreationDraft

sharing_bp = Blueprint('sharing', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@sharing_bp.route('/api/share', methods=['POST'])
@login_required
def share_content():
    user_id = session.get('user_id')
    data = request.get_json()

    content_type = data.get('content_type') # 'custom_page' or 'cocreation_draft'
    content_id = data.get('content_id')
    target_user_id = data.get('user_id')
    target_group_id = data.get('group_id')

    if not content_type or not content_id:
        return jsonify({'success': False, 'error': 'Missing content info'}), 400

    if not target_user_id and not target_group_id:
         return jsonify({'success': False, 'error': 'No recipient specified'}), 400

    # Verify ownership
    if content_type == 'custom_page':
        item = CustomRecipePage.query.get(content_id)
        name = item.name
    elif content_type == 'cocreation_draft':
        item = CoCreationDraft.query.get(content_id)
        name = item.draft_name
    else:
        return jsonify({'success': False, 'error': 'Invalid content type'}), 400

    if not item or item.user_id != user_id:
        return jsonify({'success': False, 'error': 'Content not found or permission denied'}), 403

    # Create share record
    share = ContentShare(
        content_type=content_type,
        content_id=content_id,
        shared_by=user_id,
        shared_with_user_id=target_user_id,
        shared_with_group_id=target_group_id
    )
    db.session.add(share)

    # Notification
    sharer_name = session.get('user_name', 'Someone')

    # Determine link based on content type
    link = ""
    if content_type == 'custom_page':
        link = f"/custom-pages/view/{content_id}"
    elif content_type == 'cocreation_draft':
        # Drafts don't have a direct view page, they load into the editor
        # We can link to the drafts list for now
        link = "/cocreation/drafts?view=shared"

    if target_user_id:
        notif = Notification(
            recipient_id=target_user_id,
            type='content_share',
            message=f"{sharer_name} shared '{name}' with you.",
            link=link
        )
        db.session.add(notif)
    elif target_group_id:
        group = UserGroup.query.get(target_group_id)
        for member in group.members:
            if member.user_id != user_id:
                notif = Notification(
                    recipient_id=member.user_id,
                    type='content_share',
                    message=f"{sharer_name} shared '{name}' with group '{group.name}'.",
                    link=link
                )
                db.session.add(notif)

    db.session.commit()
    return jsonify({'success': True})

@sharing_bp.route('/api/notifications', methods=['GET'])
@login_required
def get_notifications():
    user_id = session.get('user_id')
    notifs = Notification.query.filter_by(recipient_id=user_id).order_by(Notification.created_at.desc()).limit(20).all()

    return jsonify([{
        'id': n.id,
        'message': n.message,
        'type': n.type,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat(),
        'link': n.link
    } for n in notifs])

@sharing_bp.route('/api/notifications/read', methods=['POST'])
@login_required
def mark_read():
    user_id = session.get('user_id')
    data = request.get_json()
    notif_id = data.get('id')

    if notif_id:
        notif = Notification.query.filter_by(id=notif_id, recipient_id=user_id).first()
        if notif:
            notif.is_read = True
    else:
        # Mark all read
        Notification.query.filter_by(recipient_id=user_id, is_read=False).update({'is_read': True})

    db.session.commit()
    return jsonify({'success': True})
