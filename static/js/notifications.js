document.addEventListener('DOMContentLoaded', function() {
    const notificationDropdown = document.getElementById('notificationDropdown');
    const notificationList = document.getElementById('notification-list');
    const notificationBadge = document.getElementById('notification-badge');
    const markAllReadBtn = document.getElementById('mark-all-read-btn');

    // Load notifications periodically
    loadNotifications();
    setInterval(loadNotifications, 60000); // Every minute

    function loadNotifications() {
        fetch('/api/notifications')
            .then(response => response.json())
            .then(notifs => {
                renderNotifications(notifs);
                updateBadge(notifs);
            })
            .catch(err => console.error('Error loading notifications', err));
    }

    function renderNotifications(notifs) {
        notificationList.innerHTML = '';

        if (notifs.length === 0) {
            notificationList.innerHTML = '<div class="p-3 text-center text-muted"><small>No new notifications</small></div>';
            return;
        }

        notifs.forEach(n => {
            const item = document.createElement('a');
            item.href = '#'; // Default to # to prevent navigation if link is invalid
            if (n.link && n.link.startsWith('/')) {
                item.href = n.link;
            }

            item.className = `list-group-item list-group-item-action ${!n.is_read ? 'bg-light fw-bold' : ''}`;

            let iconClass = 'fa-info-circle';
            if (n.type === 'group_invite') iconClass = 'fa-users';
            if (n.type === 'content_share') iconClass = 'fa-share-alt';
            if (n.type === 'role_change') iconClass = 'fa-user-shield';

            // Safe rendering to prevent XSS
            const dateStr = new Date(n.created_at).toLocaleDateString();
            const badgeHtml = !n.is_read ? '<span class="badge bg-primary rounded-pill">New</span>' : '';

            // Use innerText/textContent for user-controlled message content
            // Structure: <div>header</div><div><icon> <text></div>

            const headerDiv = document.createElement('div');
            headerDiv.className = 'd-flex w-100 justify-content-between';
            headerDiv.innerHTML = `<small class="text-muted">${dateStr}</small>${badgeHtml}`;

            const bodyDiv = document.createElement('div');
            bodyDiv.className = 'd-flex align-items-center mt-1';

            const icon = document.createElement('i');
            icon.className = `fas ${iconClass} me-2 text-primary`;

            const messageP = document.createElement('p');
            messageP.className = 'mb-1 text-wrap';
            messageP.style.fontSize = '0.9rem';
            messageP.textContent = n.message; // Safe text insertion

            bodyDiv.appendChild(icon);
            bodyDiv.appendChild(messageP);

            item.appendChild(headerDiv);
            item.appendChild(bodyDiv);

            item.addEventListener('click', (e) => {
                if (!n.is_read) {
                    markRead(n.id);
                }

                // If it's a group invite link placeholder, maybe open sidebar?
                if (n.link && n.link.startsWith('/groups/')) {
                    e.preventDefault();
                    // Open sidebar logic if possible, or just ignore
                    const sidebarBtn = document.getElementById('sidebar-toggle-btn');
                    if (sidebarBtn) sidebarBtn.click();
                }
            });

            notificationList.appendChild(item);
        });
    }

    function updateBadge(notifs) {
        const unreadCount = notifs.filter(n => !n.is_read).length;
        if (unreadCount > 0) {
            notificationBadge.textContent = unreadCount;
            notificationBadge.classList.remove('d-none');
        } else {
            notificationBadge.classList.add('d-none');
        }
    }

    function markRead(id) {
        fetch('/api/notifications/read', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify({ id: id })
        }).then(() => loadNotifications());
    }

    if (markAllReadBtn) {
        markAllReadBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation(); // Keep dropdown open
            markRead(null); // Mark all
        });
    }
});
