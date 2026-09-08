document.addEventListener('DOMContentLoaded', () => {
  const passwordToggle = document.querySelector('.toggle-password');
  if (passwordToggle) {
    passwordToggle.addEventListener('click', () => {
      const input = passwordToggle.parentElement.querySelector('input');
      const visible = input.type === 'text';
      input.type = visible ? 'password' : 'text';
      passwordToggle.textContent = visible ? '◉' : '◌';
      passwordToggle.setAttribute('aria-label', visible ? 'Show password' : 'Hide password');
    });
  }

  const welcome = document.querySelector('[data-welcome-loader]');
  if (welcome && window.SHADOWNET_WELCOME_REDIRECT) {
    const countdown = document.getElementById('countdown');
    let remaining = Number(window.SHADOWNET_WELCOME_SECONDS || 5);
    const timer = setInterval(() => {
      remaining -= 1;
      if (countdown) countdown.textContent = Math.max(remaining, 0);
      if (remaining <= 0) {
        clearInterval(timer);
        window.location.href = window.SHADOWNET_WELCOME_REDIRECT;
      }
    }, 1000);
  }

  const assistantModal = document.getElementById('assistantModal');
  const openButtons = document.querySelectorAll('[data-open-assistant]');
  const closeButtons = document.querySelectorAll('[data-close-assistant]');
  const form = document.getElementById('assistantForm');
  const input = document.getElementById('assistantInput');
  const messages = document.getElementById('assistantMessages');

  const openAssistant = () => {
    if (!assistantModal) return;
    assistantModal.classList.add('open');
    assistantModal.setAttribute('aria-hidden', 'false');
    if (input) input.focus();
  };
  const closeAssistant = () => {
    if (!assistantModal) return;
    assistantModal.classList.remove('open');
    assistantModal.setAttribute('aria-hidden', 'true');
  };
  openButtons.forEach(button => button.addEventListener('click', openAssistant));
  closeButtons.forEach(button => button.addEventListener('click', closeAssistant));
  if (assistantModal) assistantModal.addEventListener('click', e => { if (e.target === assistantModal) closeAssistant(); });

  const addMessage = (text, type) => {
    if (!messages) return;
    const bubble = document.createElement('div');
    bubble.className = type === 'user' ? 'user-message' : 'bot-message';
    bubble.textContent = text;
    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
    return bubble;
  };

  if (form && input && messages) {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const text = input.value.trim();
      if (!text) return;
      addMessage(text, 'user');
      input.value = '';
      const pending = addMessage('ShadowBot is thinking…', 'bot');
      const button = form.querySelector('button[type="submit"]');
      if (button) button.disabled = true;
      try {
        const response = await fetch('/api/assistant', {
          method: 'POST',
          headers: {'Content-Type':'application/json', 'X-Requested-With':'XMLHttpRequest'},
          body: JSON.stringify({message: text})
        });
        let data = {};
        try { data = await response.json(); } catch (_) {}
        if (pending) pending.remove();
        if (!response.ok) {
          addMessage(data.reply || `ShadowBot request failed (${response.status}).`, 'bot');
        } else {
          addMessage(data.reply || 'ShadowBot returned an empty response.', 'bot');
        }
      } catch (_error) {
        if (pending) pending.remove();
        addMessage('Connection to ShadowBot failed. Check that the Render service is running and try again.', 'bot');
      } finally {
        if (button) button.disabled = false;
        input.focus();
      }
    });
  }

  // Topic notes modal. Every unlocked topic is backed by a real note object from Flask.
  const notesModal = document.getElementById('notesModal');
  const noteTitle = document.getElementById('noteTitle');
  const noteLevel = document.getElementById('noteLevel');
  const noteSummary = document.getElementById('noteSummary');
  const notePoints = document.getElementById('notePoints');
  const noteExample = document.getElementById('noteExample');
  const notePractice = document.getElementById('notePractice');
  let activeNote = null;

  const closeNotes = () => {
    if (!notesModal) return;
    notesModal.classList.remove('open');
    notesModal.setAttribute('aria-hidden', 'true');
  };

  document.querySelectorAll('[data-close-notes]').forEach(button => button.addEventListener('click', closeNotes));
  if (notesModal) notesModal.addEventListener('click', e => { if (e.target === notesModal) closeNotes(); });

  document.querySelectorAll('.topic-button').forEach(button => {
    button.addEventListener('click', () => {
      const level = button.dataset.level;
      const index = Number(button.dataset.topicIndex);
      const note = window.SHADOWNET_NOTES?.[level]?.[index];
      if (!note || !notesModal) return;
      activeNote = note;
      noteLevel.textContent = `${window.SHADOWNET_LANGUAGE || 'Study'} · ${level}`;
      noteTitle.textContent = note.title;
      noteSummary.textContent = note.summary;
      notePoints.innerHTML = '';
      (note.key_points || []).forEach(point => {
        const li = document.createElement('li');
        li.textContent = point;
        notePoints.appendChild(li);
      });
      noteExample.textContent = note.example || '';
      notePractice.textContent = note.practice || '';
      notesModal.classList.add('open');
      notesModal.setAttribute('aria-hidden', 'false');
    });
  });

  const askFromNote = document.querySelector('[data-note-ask]');
  if (askFromNote) askFromNote.addEventListener('click', () => {
    const title = activeNote?.title || 'this topic';
    closeNotes();
    openAssistant();
    if (input) {
      input.value = `Explain ${title} in ${window.SHADOWNET_LANGUAGE || 'this language'} with a practical example.`;
      input.focus();
    }
  });
});
