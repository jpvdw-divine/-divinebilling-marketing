(function () {
  var COPY = {
    "/become-a-reseller": {
      title: "Thank you",
      text: "We received your reseller application and will reply within 24 hours.",
      next: "https://divinebilling.online/"
    },
    "/contact": {
      title: "Thank you",
      text: "Your message was sent. We typically reply within one business day."
    },
    "/get-started/signup": {
      title: "Thank you",
      text: "Your sign-up was received. We typically reply within one business day.",
      next: "https://divinebilling.online/"
    }
  };

  function pathOf(action) {
    try {
      return new URL(action, location.origin).pathname.replace(/\/+$/, "") || "/";
    } catch (e) {
      return "";
    }
  }

  function show(form, copy) {
    if (form.dataset.thanksShown === "1") return;
    form.dataset.thanksShown = "1";
    var box = document.createElement("div");
    box.className = "form-thanks";
    box.setAttribute("role", "status");
    var title = document.createElement("h2");
    title.textContent = copy.title;
    var text = document.createElement("p");
    text.textContent = copy.text;
    box.appendChild(title);
    box.appendChild(text);
    form.hidden = true;
    form.parentNode.insertBefore(box, form);
    if (box.scrollIntoView) box.scrollIntoView({ behavior: "smooth", block: "center" });
    if (copy.next) {
      setTimeout(function () { window.location.href = copy.next; }, 6000);
    }
  }

  document.querySelectorAll("form[method='POST'], form[method='post']").forEach(function (form) {
    var copy = COPY[pathOf(form.getAttribute("action") || "")];
    if (!copy) return;
    if (new URLSearchParams(location.search).get("sent") === "1") {
      show(form, copy);
      return;
    }
    form.addEventListener("submit", function (e) {
      if (typeof form.checkValidity === "function" && !form.checkValidity()) return;
      e.preventDefault();
      var btn = form.querySelector("[type=submit]");
      if (btn) btn.disabled = true;
      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        redirect: "manual",
        credentials: "same-origin"
      }).then(function (resp) {
        if (resp.type === "opaqueredirect" || (resp.status >= 200 && resp.status < 400)) {
          show(form, copy);
          return;
        }
        if (btn) btn.disabled = false;
      }).catch(function () {
        HTMLFormElement.prototype.submit.call(form);
      });
    });
  });
})();
