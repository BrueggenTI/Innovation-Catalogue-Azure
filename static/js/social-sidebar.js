document.addEventListener('DOMContentLoaded', function() {
    const sidebar = new bootstrap.Offcanvas(document.getElementById('socialSidebar'));
    const sidebarToggleBtn = document.getElementById('sidebar-toggle-btn');
    const usersListContainer = document.getElementById('users-list-container');
    const groupsListContainer = document.getElementById('groups-list-container');
    const userSearchInput = document.getElementById('user-search-input');
    const groupSearchInput = document.getElementById('group-search-input');
    const createGroupBtn = document.getElementById('create-group-btn');
    const saveNewGroupBtn = document.getElementById('save-new-group-btn');

    // Group Settings Elements
    const groupSettingsModal = new bootstrap.Modal(document.getElementById('groupSettingsModal'));
    const settingsGroupId = document.getElementById('settings-group-id');
    const settingsGroupName = document.getElementById('settings-group-name');
    const settingsGroupDesc = document.getElementById('settings-group-desc');
    const updateGroupInfoBtn = document.getElementById('update-group-info-btn');
    const deleteGroupBtn = document.getElementById('delete-group-btn');
    const groupMembersTbody = document.getElementById('group-members-tbody');

    // Add User to Group Elements
    const addToGroupModal = new bootstrap.Modal(document.getElementById('addToGroupModal'));
    const addUserTargetName = document.getElementById('add-user-target-name');
    const selectGroupGrid = document.getElementById('select-group-grid');
    const addUserGroupSearch = document.getElementById('add-user-group-search');
    let userToAddId = null;
    let myAdminGroupsCache = []; // Cache for filtering in modal

    // Toggle Sidebar
    sidebarToggleBtn.addEventListener('click', function() {
        sidebar.show();
        loadUsers(); // Calls with defaults (empty query, page 1)
        loadGroups();
    });

    // --- Users Tab Logic ---
    let usersCache = [];
    let currentUserPage = 1;
    let currentUserQuery = '';
    let hasMoreUsers = false;

    function loadUsers(query = '', page = 1, append = false) {
        // Encode query
        const url = `/api/users/search?q=${encodeURIComponent(query)}&page=${page}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const users = data.users;
                hasMoreUsers = data.has_next;
                currentUserPage = page;
                currentUserQuery = query;

                if (append) {
                    usersCache = [...usersCache, ...users];
                } else {
                    usersCache = users;
                }

                renderUsers(users, append);
            })
            .catch(err => console.error('Error loading users:', err));
    }

    function renderUsers(users, append = false) {
        if (!append) {
            usersListContainer.innerHTML = '';
        }

        // Remove existing "Load More" button if it exists
        const existingBtn = document.getElementById('load-more-users-btn');
        if (existingBtn) {
            existingBtn.remove();
        }

        if (usersCache.length === 0) {
            usersListContainer.innerHTML = `
                <div class="social-empty">
                    <i class="fas fa-user-slash"></i>
                    <p>No users found</p>
                </div>`;
            return;
        }

        users.forEach(user => {
            const item = document.createElement('div');
            item.className = 'social-card';

            // Get initials for avatar
            const initials = user.name ? user.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() : '??';

            item.innerHTML = `
                <div class="social-avatar">
                    <span>${initials}</span>
                </div>
                <div class="social-info">
                    <div class="social-name">${user.name}</div>
                    <div class="social-meta">
                        <i class="fas fa-briefcase"></i> ${user.position || user.department || 'User'}
                    </div>
                </div>
                <button class="social-action-btn add-user-to-group-btn" data-id="${user.id}" data-name="${user.name}" title="Add to Group">
                    <i class="fas fa-user-plus"></i>
                </button>
            `;
            usersListContainer.appendChild(item);
        });

        // Add "Load More" button if there are more users
        if (hasMoreUsers) {
            const loadMoreBtn = document.createElement('button');
            loadMoreBtn.id = 'load-more-users-btn';
            loadMoreBtn.className = 'btn btn-link w-100 text-center text-muted my-2';
            loadMoreBtn.innerHTML = 'Mehr anzeigen <i class="fas fa-chevron-down ms-1"></i>';
            loadMoreBtn.onclick = function() {
                loadUsers(currentUserQuery, currentUserPage + 1, true);
            };
            usersListContainer.appendChild(loadMoreBtn);
        }

        // Bind events
        bindUserEvents();
    }

    function bindUserEvents() {
        document.querySelectorAll('.add-user-to-group-btn').forEach(btn => {
            // Remove old listener to avoid duplicates if re-rendering (simple way)
            const newBtn = btn.cloneNode(true);
            btn.parentNode.replaceChild(newBtn, btn);

            newBtn.addEventListener('click', function() {
                userToAddId = this.dataset.id;
                addUserTargetName.textContent = this.dataset.name;
                loadMyAdminGroupsForSelect(); // Load groups where I am admin
                addToGroupModal.show();
            });
        });
    }

    userSearchInput.addEventListener('input', function(e) {
        const query = e.target.value.trim();
        loadUsers(query, 1, false);
    });

    // --- Groups Tab Logic ---
    let groupsCache = [];

    function loadGroups() {
        fetch('/api/groups')
            .then(response => response.json())
            .then(groups => {
                groupsCache = groups;
                renderGroups(groups);
            })
            .catch(err => console.error('Error loading groups:', err));
    }

    function renderGroups(groups) {
        groupsListContainer.innerHTML = '';
        if (groups.length === 0) {
            groupsListContainer.innerHTML = `
                <div class="social-empty">
                    <i class="fas fa-users-slash"></i>
                    <p>No groups found</p>
                </div>`;
            return;
        }

        groups.forEach(group => {
            const item = document.createElement('div');
            item.className = 'social-card';

            // Get initials for avatar
            const initials = group.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();

            item.innerHTML = `
                <div class="social-avatar" style="background: linear-gradient(135deg, #661c31 0%, #ff4143 100%); color: white; border: none;">
                    <span>${initials}</span>
                </div>
                <div class="social-info">
                    <div class="social-name">${group.name}</div>
                    <div class="social-meta">
                        <i class="fas fa-users"></i> ${group.member_count} members • <span class="badge bg-light text-dark border ms-1">${group.role}</span>
                    </div>
                </div>
                <button class="social-action-btn group-settings-btn" data-id="${group.id}" title="Settings">
                    <i class="fas fa-cog"></i>
                </button>
            `;
            groupsListContainer.appendChild(item);
        });

        // Bind events
        document.querySelectorAll('.group-settings-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                loadGroupDetails(this.dataset.id);
            });
        });
    }

    groupSearchInput.addEventListener('input', function(e) {
        const query = e.target.value.trim().toLowerCase();
        const filtered = groupsCache.filter(g => g.name.toLowerCase().includes(query));
        renderGroups(filtered);
    });

    // --- Create Group ---
    createGroupBtn.addEventListener('click', function() {
        const modal = new bootstrap.Modal(document.getElementById('createGroupModal'));
        modal.show();
    });

    saveNewGroupBtn.addEventListener('click', function() {
        const name = document.getElementById('new-group-name').value;
        const desc = document.getElementById('new-group-desc').value;
        const initialMember = this.dataset.initialMember; // Get ID if set

        if (!name) return;

        const payload = { name: name, description: desc };
        if (initialMember) {
            payload.members = [parseInt(initialMember)];
        }

        fetch('/api/groups', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                bootstrap.Modal.getInstance(document.getElementById('createGroupModal')).hide();
                document.getElementById('new-group-name').value = '';
                document.getElementById('new-group-desc').value = '';
                // Clear initial member
                delete saveNewGroupBtn.dataset.initialMember;

                loadGroups();
                // Switch to groups tab
                document.getElementById('groups-tab').click();

                if (initialMember) {
                    alert('Group created and user added!');
                }
            } else {
                alert(data.error);
            }
        })
        .catch(err => console.error('Error creating group:', err));
    });

    // --- Group Settings ---
    function loadGroupDetails(groupId) {
        fetch(`/api/groups/${groupId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                settingsGroupId.value = data.id;
                settingsGroupName.value = data.name;
                settingsGroupDesc.value = data.description || '';

                // Disable fields if not admin/owner
                const isAdmin = ['owner', 'admin'].includes(data.my_role);
                const isOwner = data.my_role === 'owner';

                settingsGroupName.disabled = !isAdmin;
                settingsGroupDesc.disabled = !isAdmin;
                updateGroupInfoBtn.disabled = !isAdmin;

                // Hide Danger Tab if not Owner
                const dangerTab = document.getElementById('danger-tab');
                if (dangerTab) {
                    dangerTab.style.display = isOwner ? 'block' : 'none';
                }

                renderGroupMembers(data.members, data.my_role, data.id);

                // Reset to first tab
                const firstTab = document.getElementById('general-tab');
                if (firstTab) {
                    const tabTrigger = new bootstrap.Tab(firstTab);
                    tabTrigger.show();
                }

                groupSettingsModal.show();
            })
            .catch(err => console.error('Error loading details:', err));
    }

    function renderGroupMembers(members, myRole, groupId) {
        groupMembersTbody.innerHTML = '';
        const isOwner = myRole === 'owner';

        members.forEach(member => {
            const tr = document.createElement('tr');

            let actionsHtml = '';
            // Can manage if I am owner, or if I am admin and target is member
            const canManage = isOwner || (myRole === 'admin' && member.role === 'member');

            if (canManage && member.role !== 'owner') { // Cannot manage owner
                actionsHtml = `
                    <div class="dropdown">
                        <button class="btn btn-sm btn-link text-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                            <i class="fas fa-ellipsis-v"></i>
                        </button>
                        <ul class="dropdown-menu">
                            ${isOwner ? `
                            <li><a class="dropdown-item change-role-btn" href="#" data-id="${member.user_id}" data-role="admin">Make Admin</a></li>
                            <li><a class="dropdown-item change-role-btn" href="#" data-id="${member.user_id}" data-role="member">Make Member</a></li>
                            <li><hr class="dropdown-divider"></li>
                            ` : ''}
                            <li><a class="dropdown-item text-danger remove-member-btn" href="#" data-id="${member.user_id}">Remove</a></li>
                        </ul>
                    </div>
                `;
            }

            tr.innerHTML = `
                <td>
                    <div class="fw-bold">${member.name}</div>
                    <small class="text-muted">${member.email}</small>
                </td>
                <td><span class="badge bg-${member.role === 'owner' ? 'warning' : (member.role === 'admin' ? 'info' : 'secondary')}">${member.role}</span></td>
                <td>${actionsHtml}</td>
            `;
            groupMembersTbody.appendChild(tr);
        });

        // Bind member actions
        document.querySelectorAll('.remove-member-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                removeMember(groupId, this.dataset.id);
            });
        });

        document.querySelectorAll('.change-role-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                changeMemberRole(groupId, this.dataset.id, this.dataset.role);
            });
        });
    }

    updateGroupInfoBtn.addEventListener('click', function() {
        const id = settingsGroupId.value;
        const name = settingsGroupName.value;
        const desc = settingsGroupDesc.value;

        fetch(`/api/groups/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify({ name: name, description: desc })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Group updated');
                loadGroups(); // Refresh list
            } else {
                alert(data.error);
            }
        });
    });

    deleteGroupBtn.addEventListener('click', function() {
        if (!confirm('Are you sure you want to delete this group? This cannot be undone.')) return;

        const id = settingsGroupId.value;
        fetch(`/api/groups/${id}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                groupSettingsModal.hide();
                loadGroups();
            } else {
                alert(data.error);
            }
        });
    });

    function removeMember(groupId, userId) {
        if (!confirm('Remove this user from the group?')) return;

        fetch(`/api/groups/${groupId}/members/${userId}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadGroupDetails(groupId); // Refresh members
            } else {
                alert(data.error);
            }
        });
    }

    function changeMemberRole(groupId, userId, newRole) {
        fetch(`/api/groups/${groupId}/members/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify({ role: newRole })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadGroupDetails(groupId); // Refresh members
            } else {
                alert(data.error);
            }
        });
    }

    // --- Add User to Group Logic ---
    function loadMyAdminGroupsForSelect() {
        fetch('/api/groups')
            .then(response => response.json())
            .then(groups => {
                // Filter only groups where I am admin or owner
                myAdminGroupsCache = groups.filter(g => ['owner', 'admin'].includes(g.role));
                renderGroupSelectionGrid(myAdminGroupsCache);
            });
    }

    function renderGroupSelectionGrid(groups) {
        selectGroupGrid.innerHTML = '';

        // 1. Always Add "Create New Group" Card
        const createCard = document.createElement('div');
        createCard.className = 'group-grid-card create-new';
        createCard.innerHTML = `
            <div class="group-grid-icon">
                <i class="fas fa-plus"></i>
            </div>
            <div class="group-grid-name">New Group</div>
        `;
        createCard.onclick = () => {
            addToGroupModal.hide();
            // Reset fields
            document.getElementById('new-group-name').value = '';
            document.getElementById('new-group-desc').value = '';
            // Set context for save button
            saveNewGroupBtn.dataset.initialMember = userToAddId;
            const createModal = new bootstrap.Modal(document.getElementById('createGroupModal'));
            createModal.show();
        };
        selectGroupGrid.appendChild(createCard);

        if (groups.length === 0) {
            // No other groups to show? Maybe show a hint, but the create card is always there.
            return;
        }

        groups.forEach(group => {
            const card = document.createElement('div');
            card.className = 'group-grid-card';

            // Initials
            const initials = group.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();

            card.innerHTML = `
                <div class="group-grid-icon">
                    ${initials}
                </div>
                <div class="group-grid-name" title="${group.name}">${group.name}</div>
            `;
            card.onclick = () => addUserToGroup(group.id);
            selectGroupGrid.appendChild(card);
        });
    }

    // Filter Groups in "Add User" Modal
    if (addUserGroupSearch) {
        addUserGroupSearch.addEventListener('input', function(e) {
            const query = e.target.value.trim().toLowerCase();
            const filtered = myAdminGroupsCache.filter(g => g.name.toLowerCase().includes(query));
            renderGroupSelectionGrid(filtered);
        });
    }

    function addUserToGroup(groupId) {
        if (!userToAddId) return;

        fetch(`/api/groups/${groupId}/members`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify({ user_id: userToAddId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                addToGroupModal.hide();
                alert('User added to group!');
                // Optionally switch to groups tab and show that group
            } else {
                alert(data.error);
            }
        });
    }
});