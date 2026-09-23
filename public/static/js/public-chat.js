(function () {
  var root = document.getElementById('db-pub-chat');
  if (!root) return;
  var api = root.getAttribute('data-api') || '';
  var panel = root.querySelector('.db-chat__panel');
  var thread = root.querySelector('.db-chat__thread');
  var form = root.querySelector('.db-chat__form');
  var input = root.querySelector('.db-chat__input');
  var follow = root.querySelector('.db-chat__follow');
  var toggle = root.querySelector('.db-chat__toggle');
  var tokenKey = 'db-pub-chat-token';
  var token = '';
  try { token = localStorage.getItem(tokenKey) || ''; } catch (e) { token = ''; }

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }
  function formatText(s) {
    return escapeHtml(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');
  }
  function add(role, content) {
    var el = document.createElement('div');
    el.className = 'db-chat__bubble db-chat__bubble--' + (role || 'assistant');
    var who = role === 'user' ? 'You' : 'DivineBilling';
    el.innerHTML = '<span class="db-chat__who">' + who + '</span>' + formatText(content);
    thread.appendChild(el);
    thread.scrollTop = thread.scrollHeight;
  }
  function setOpen(open) {
    root.classList.toggle('is-open', open);
    if (toggle) toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open && input) input.focus();
  }
  if (toggle) {
    toggle.addEventListener('click', function () {
      setOpen(!root.classList.contains('is-open'));
    });
  }
  var closeBtn = root.querySelector('.db-chat__close');
  if (closeBtn) closeBtn.addEventListener('click', function () { setOpen(false); });
  var followBtn = root.querySelector('.db-chat__follow-btn');
  if (followBtn && follow) {
    followBtn.addEventListener('click', function () {
      follow.hidden = !follow.hidden;
    });
  }

  add('assistant', 'Assistant V2.0 — ask what any module does, compare plans, or book a demo. Leave an email if you want the team to follow up.');

  root.querySelectorAll('[data-ask]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-ask') || '';
      if (!text) return;
      add('user', text);
      send({ message: text });
    });
  });
  root.querySelectorAll('[data-lead]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (follow) {
        follow.hidden = false;
        var note = follow.querySelector('[name="note"]');
        if (note && !note.value) note.value = btn.getAttribute('data-lead') || '';
        var interest = follow.querySelector('[name="interest"]');
        if (interest) interest.focus();
      }
    });
  });

  function send(payload) {
    var wait = document.createElement('div');
    wait.className = 'db-chat__typing';
    wait.innerHTML = '<span></span><span></span><span></span>';
    thread.appendChild(wait);
    thread.scrollTop = thread.scrollHeight;
    payload.token = token;
    payload.page = location.pathname || '/';
    payload.website = '';
    return fetch(api, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().then(function (data) {
        data = data || {};
        data._status = r.status;
        return data;
      });
    }).then(function (data) {
      wait.remove();
      if (data.token) {
        token = data.token;
        try { localStorage.setItem(tokenKey, token); } catch (e) {}
      }
      if (!data.ok) {
        add('assistant', data.reply || data.error || 'Something went wrong. Try again in a moment.');
        return;
      }
      if (data.reply) add('assistant', data.reply);
      if (data.offer_lead && follow) follow.hidden = false;
    }).catch(function () {
      wait.remove();
      add('assistant', 'I could not reach the desk just now. You can still start a trial from Get started, or email us from the contact section.');
    });
  }

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var text = (input.value || '').trim();
      if (!text) return;
      input.value = '';
      add('user', text);
      send({ message: text });
    });
  }
  if (follow) {
    follow.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = (follow.querySelector('[name="name"]').value || '').trim();
      var email = (follow.querySelector('[name="email"]').value || '').trim();
      var phone = (follow.querySelector('[name="phone"]').value || '').trim();
      var company = (follow.querySelector('[name="company"]').value || '').trim();
      var interestEl = follow.querySelector('[name="interest"]');
      var interest = interestEl ? (interestEl.value || '').trim() : '';
      if (!email) {
        add('assistant', 'Add an email so the team can reply.');
        return;
      }
      var note = (follow.querySelector('[name="note"]').value || '').trim();
      var text = note || 'Please follow up with me.';
      add('user', text + (company ? ' (' + company + ')' : ''));
      follow.hidden = true;
      send({
        message: text,
        name: name,
        email: email,
        phone: phone,
        company: company,
        interest: interest
      });
    });
  }
})();
