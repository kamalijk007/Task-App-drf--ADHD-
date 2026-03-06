function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function loadHabits() {
    const token = getCookie('token');

    const response = await fetch('/tracker/habits/', {
        headers: {
            'Authorization': `Bearer ${token}`,
        }
    });

    if (!response.ok) {
        console.error('Failed to load habits:', response.status);
        return;
    }

    const data = await response.json();
    const habits = Array.isArray(data) ? data : data.results;

    const listElement = document.getElementById('habit-list');
    listElement.innerHTML = '';

    habits.forEach(habit => {
        const li = document.createElement('li');

        li.innerHTML = `
            <div style="display: flex; flex-direction: column; flex-grow: 1;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <strong style="${habit.is_done_today ? 'text-decoration: line-through; color: #94a3b8;' : 'color: white; font-size: 1.1rem;'}">
                        ${habit.name}
                    </strong>
                    ${habit.current_streak > 0 ? 
                        `<span style="color: #ff9f43; font-weight: bold; font-size: 0.85rem; background: rgba(255, 159, 67, 0.1); padding: 2px 8px; border-radius: 10px;">
                            ${habit.current_streak} 🔥
                        </span>` : ''}
                </div>
                <span style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">${habit.description || "No Description"}</span>
                
                <div class="heatmap">
                    ${habit.last_7_days.map(done => `<div class="dot ${done ? 'dot-filled' : ''}"></div>`).join('')}
                </div>
            </div>`;

        const btnGroup = document.createElement('div');
        btnGroup.style.display = 'flex';
        btnGroup.style.alignItems = 'center';
        btnGroup.style.marginLeft = '20px';

        const doneBtn = document.createElement('button');
        if (habit.is_done_today) {
            li.classList.add('habit-card-done');
            doneBtn.textContent = '✅ Completed';
            doneBtn.classList.add('btn-completed');
            doneBtn.disabled = true;
        } else {
            doneBtn.textContent = 'Done';
            doneBtn.onclick = (e) => markHabitDone(habit.id, e.target);
        }

        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = '🗑️';
        deleteBtn.className = 'delete-btn';
        deleteBtn.onclick = () => deleteHabit(habit.id);

        btnGroup.appendChild(doneBtn);
        btnGroup.appendChild(deleteBtn);
        li.appendChild(btnGroup);

        listElement.appendChild(li);
    });

    // Update Progress Bar
    const totalHabits = habits.length;
    const completedHabits = habits.filter(h => h.is_done_today).length;
    const percentage = totalHabits > 0 ? Math.round((completedHabits / totalHabits) * 100) : 0;

    const textCenter = document.getElementById('progress-text-center');
    if (textCenter) {
        textCenter.textContent = `${percentage}%`;
    }

    const circumference = 339.29;
    const offset = circumference - (percentage / 100) * circumference;
    const circle = document.getElementById('progress-circle');
    if (circle) {
        circle.style.strokeDashoffset = offset;
    }

    const progressText = document.getElementById('progress-text');
    if (progressText) {
        progressText.textContent = `Progress: ${percentage}% (${completedHabits}/${totalHabits})`;
    }
}

async function createHabit() {
    const nameInput = document.getElementById('habit-name');
    const descInput = document.getElementById('habit-desc');
    const csrftoken = getCookie('csrftoken');
    const token = getCookie('token');

    const response = await fetch('/tracker/habits/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            name: nameInput.value,
            description: descInput.value
        })
    });

    if (response.ok) {
        nameInput.value = '';
        descInput.value = '';
        await loadHabits();
    } else {
        const errorData = await response.json();
        console.error('Failed to create habit:', response.status, errorData);
        alert(`Error ${response.status}: ${JSON.stringify(errorData)}`);
    }
}

async function markHabitDone(habitId, clickedButton) {
    const csrftoken = getCookie('csrftoken');
    const token = getCookie('token');

    try {
        const response = await fetch('/tracker/records/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({
                record: habitId,
                completed: true
            })
        });

        if (response.ok) {
            clickedButton.textContent = '✅ Completed';
            clickedButton.style.backgroundColor = '#2ecc71';
            clickedButton.disabled = true;

            confetti({
                particleCount: 150,
                spread: 70,
                origin: { y: 0.6 }
            });

            setTimeout(() => loadHabits(), 1500);
        } else {
            alert("Record already exists for today!");
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

async function deleteHabit(habitId) {
    if (!confirm("Are you sure you want to delete this habit? All progress will be lost! 😱")) {
        return;
    }

    const csrftoken = getCookie('csrftoken');
    const token = getCookie('token');

    const response = await fetch(`/tracker/habits/${habitId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken,
            'Authorization': `Bearer ${token}`,
        }
    });

    if (response.ok) {
        loadHabits();
    } else {
        alert("Failed to delete the habit.");
    }
}

window.onload = loadHabits;