/**
 * Enterprise lead form ("Talk to an expert").
 *
 * Submits the form on /support/ to the leads endpoint and redirects to
 * /support/thanks/ on success. The endpoint answers 400 with per-field errors,
 * 429 when rate limited, and an empty 403 for a rejected origin or a filled
 * honeypot — all of which fall back to the mailto address shown on the page.
 *
 * The submit button starts enabled in the markup and is disabled here on load,
 * so the form still works if this script never runs.
 */

const LEADS_ENDPOINT = "https://crm-api.openvidu.io/leads";
const THANKS_URL = "/support/thanks/";

/** Material's own gtag helper is function-local, so define one for custom events. */
function leadFormGtag() {
  window.dataLayer = window.dataLayer || [];
  // gtag.js reads the arguments object; a plain object push is GTM syntax and gets ignored
  window.dataLayer.push(arguments);
}

function setupLeadForm() {
  const form = document.querySelector("#lead-form");
  if (!form) return;

  const status = form.querySelector(".lead-form-status");
  const submitButton = form.querySelector(".lead-form-submit");

  const syncSubmitState = function () {
    if (form.classList.contains("is-sending")) return;
    submitButton.disabled = !form.checkValidity();
  };

  form.addEventListener("input", syncSubmitState);
  form.addEventListener("change", syncSubmitState);
  syncSubmitState();

  // Explains a greyed-out button while it is still greyed out. Only fields the
  // visitor actually filled in are flagged, so tabbing through stays quiet.
  form.addEventListener("focusout", function (event) {
    const field = event.target;
    if (!field.name || field.name === "website") return;
    if (field.validity.valid) {
      setFieldError(form, field.name, "");
    } else if (field.value) {
      setFieldError(form, field.name, field.validationMessage);
    }
  });

  let startReported = false;
  form.addEventListener("focusin", function () {
    if (startReported) return;
    startReported = true;
    leadFormGtag("event", "form_start", { form_id: "lead-form" });
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!form.reportValidity()) return;

    clearErrors(form);
    setStatus(status, "");
    form.classList.add("is-sending");
    submitButton.disabled = true;

    const data = new FormData(form);
    const payload = {
      name: data.get("name"),
      email: data.get("email"),
      company: data.get("company"),
      message: data.get("message"),
      scale: data.get("scale"),
      consent: data.get("consent") === "on",
      page: window.location.href,
      website: data.get("website") || ""
    };

    const recover = function () {
      form.classList.remove("is-sending");
      syncSubmitState();
    };

    fetch(LEADS_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (response) {
        if (response.status === 201) {
          window.location.href = THANKS_URL;
          return;
        }
        recover();
        if (response.status === 400) {
          return response.json().then(function (body) {
            showFieldErrors(form, body.errors || {});
            setStatus(status, "Please review the highlighted fields and try again.");
          });
        }
        if (response.status === 429) {
          setStatus(status, "Too many attempts from your network. Please try again later, or write to us directly.");
          return;
        }
        setStatus(status, genericFailure());
      })
      .catch(function () {
        recover();
        setStatus(status, genericFailure());
      });
  });
}

function genericFailure() {
  return "We could not send your message. Please try again, or write to us directly.";
}

function setStatus(status, message) {
  if (!status) return;
  status.textContent = message;
  status.hidden = !message;
}

function setFieldError(form, field, message) {
  const element = form.querySelector('.lead-form-error[data-field="' + field + '"]');
  if (element) {
    element.textContent = message;
    element.hidden = !message;
  }
  const input = form.querySelector('[name="' + field + '"]');
  if (input) {
    if (message) {
      input.setAttribute("aria-invalid", "true");
    } else {
      input.removeAttribute("aria-invalid");
    }
  }
}

function clearErrors(form) {
  form.querySelectorAll(".lead-form-error").forEach(function (element) {
    element.textContent = "";
    element.hidden = true;
  });
  form.querySelectorAll("[aria-invalid]").forEach(function (element) {
    element.removeAttribute("aria-invalid");
  });
}

function showFieldErrors(form, errors) {
  Object.keys(errors).forEach(function (field) {
    setFieldError(form, field, errors[field]);
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", setupLeadForm);
} else {
  setupLeadForm();
}
