---
title: "OpenVidu support and consultancy"
description: "Commercial support and consultancy from the OpenVidu team, plus the community channels where COMMUNITY edition users get help with self-hosting."
hide:
  - feedback
  - path
  - navigation
  - toc
  - footer
  - search-bar
  - version-selector
page_features:
  - leadform
---

<style>
  /* Lead form. Styled here rather than in extra.css because it is used on this
     page only. Light values are the base; the slate (dark) scheme overrides. */
  .lead-form {
    /* Tinted surface with white fields: separates the card from the page in
       light mode, where a white card would only be a border on white */
    --lead-form-surface: #f6f9fa;
    --lead-form-field-bg: #ffffff;
    --lead-form-border: rgba(0, 0, 0, 0.14);
    --lead-form-shadow: rgba(0, 0, 0, 0.12);
    --lead-form-disabled-bg: #dbe3e7;
    --lead-form-disabled-fg: #8b9aa1;
    max-width: 44rem;
    margin: 2em auto 2.5em;
    padding: 2.2em 2.4em 2em;
    background-color: var(--lead-form-surface);
    border: 1px solid var(--lead-form-border);
    border-radius: 7px;
    box-shadow: 0 8px 16px 0 var(--lead-form-shadow);
    /* The accent bar is what makes the block read as the page's call to action */
    border-top: 4px solid var(--primary-color-of-platform);
  }

  [data-md-color-scheme="slate"] .lead-form {
    --lead-form-surface: hsla(var(--md-hue), 15%, 19%, 1);
    --lead-form-field-bg: hsla(var(--md-hue), 15%, 13%, 1);
    --lead-form-border: hsla(var(--md-hue), 15%, 90%, 0.16);
    --lead-form-shadow: rgba(0, 0, 0, 0.3);
    --lead-form-disabled-bg: hsla(var(--md-hue), 12%, 30%, 1);
    --lead-form-disabled-fg: hsla(var(--md-hue), 15%, 90%, 0.4);
  }

  /* Two columns for the short fields, one for the message: keeps the form
     visually compact so its full height is not intimidating */
  .lead-form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.1em 1.4em;
  }

  .lead-form-row--full {
    grid-column: 1 / -1;
  }

  .lead-form label {
    display: block;
    margin-bottom: 0.4em;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    color: var(--md-default-fg-color--light);
  }

  .lead-form input[type="text"],
  .lead-form input[type="email"],
  .lead-form select,
  .lead-form textarea {
    width: 100%;
    padding: 0.6em 0.75em;
    font-family: var(--md-text-font-family);
    font-size: 0.78rem;
    color: var(--md-default-fg-color);
    background-color: var(--lead-form-field-bg);
    border: 1px solid var(--lead-form-border);
    border-radius: 5px;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
  }

  .lead-form input::placeholder,
  .lead-form textarea::placeholder {
    color: var(--md-default-fg-color--lighter);
  }

  .lead-form input:focus,
  .lead-form select:focus,
  .lead-form textarea:focus {
    outline: none;
    border-color: var(--primary-color-of-platform);
    box-shadow: 0 0 0 3px rgba(0, 136, 170, 0.18);
  }

  .lead-form [aria-invalid="true"] {
    border-color: #f44336;
  }

  .lead-form textarea {
    resize: vertical;
  }

  .lead-form-consent {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 0.6em;
    margin: 1.4em 0 1.6em;
  }

  .lead-form-consent label {
    flex: 1 1 16rem;
    margin-bottom: 0;
    font-size: 0.7rem;
    font-weight: 400;
    letter-spacing: normal;
    text-transform: none;
  }

  .lead-form-error {
    margin: 0.35em 0 0;
    font-size: 0.68rem;
    color: #f44336;
  }

  .lead-form-actions {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.6em 1.2em;
  }

  /* The theme's primary is the nav gray, so the submit button takes the
     OpenVidu Platform teal used by the CTAs on the landing page */
  .md-typeset .lead-form .lead-form-submit {
    margin: 0;
    padding: 0.5em 1.8em;
    font-weight: 700;
    color: #ffffff;
    background-color: #0088aa;
    border-color: #0088aa;
  }

  .md-typeset .lead-form .lead-form-submit:hover,
  .md-typeset .lead-form .lead-form-submit:focus {
    color: #ffffff;
    background-color: #007394;
    border-color: #007394;
  }

  /* Disabled until every required field is valid, so the button itself shows
     whether the form is ready to send. The cursor is reset to the plain arrow
     because .md-button sets pointer, which would invite a click that does nothing. */
  .md-typeset .lead-form .lead-form-submit:disabled {
    color: var(--lead-form-disabled-fg);
    background-color: var(--lead-form-disabled-bg);
    border-color: var(--lead-form-disabled-bg);
    cursor: default;
  }

  .md-typeset .lead-form.is-sending .lead-form-submit:disabled {
    cursor: progress;
  }

  .lead-form-reassurance {
    margin: 0;
    font-size: 0.68rem;
    color: var(--md-default-fg-color--light);
  }

  .lead-form-status {
    margin: 1em 0 0;
    font-size: 0.72rem;
  }

  /* Invisible to humans, filled by bots: a non-empty value gets the submission rejected */
  .lead-form-honeypot {
    position: absolute;
    left: -5000px;
  }

  @media screen and (max-width: 44em) {
    .lead-form {
      padding: 1.6em 1.3em 1.4em;
    }

    .lead-form-grid {
      grid-template-columns: 1fr;
    }
  }
</style>

# Support

<div style="font-size: 20px" markdown>

Self-hosting your own solutions can be challenging. We have built OpenVidu to make this task as easy as possible. But of course you may encounter difficulties in the process, or your particular use case may require customized assistance. The OpenVidu team specializes in customer support. Together we will make your project a success!

</div>

## Talk to an expert

We provide consultancy, prioritized bug fixes and new features, custom app development, and help sizing and operating your deployment. Tell us what you are building and we will get back to you as soon as possible.

<form id="lead-form" class="lead-form" novalidate>
  <div class="lead-form-grid">
    <div class="lead-form-row">
      <label for="lead-name">Name</label>
      <input type="text" id="lead-name" name="name" maxlength="200" autocomplete="name" placeholder="Jane Roe" required>
      <p class="lead-form-error" data-field="name" hidden></p>
    </div>
    <div class="lead-form-row">
      <label for="lead-email">Work email</label>
      <input type="email" id="lead-email" name="email" maxlength="254" autocomplete="email" placeholder="jane@acme.com" required>
      <p class="lead-form-error" data-field="email" hidden></p>
    </div>
    <div class="lead-form-row">
      <label for="lead-company">Company</label>
      <input type="text" id="lead-company" name="company" maxlength="200" autocomplete="organization" placeholder="Acme Corp" required>
      <p class="lead-form-error" data-field="company" hidden></p>
    </div>
    <div class="lead-form-row">
      <label for="lead-scale">Expected scale</label>
      <select id="lead-scale" name="scale" required>
        <option value="" disabled selected>Select an option</option>
        <option value="exploring">Just exploring</option>
        <option value="lt100">Up to 100 concurrent users</option>
        <option value="hundreds">Hundreds of concurrent users</option>
        <option value="thousands">Thousands of concurrent users</option>
      </select>
      <p class="lead-form-error" data-field="scale" hidden></p>
    </div>
    <div class="lead-form-row lead-form-row--full">
      <label for="lead-message">What are you building?</label>
      <textarea id="lead-message" name="message" rows="4" minlength="10" maxlength="2000" placeholder="A telehealth app that needs recording and EU data residency. We are aiming to go live next quarter." required></textarea>
      <p class="lead-form-error" data-field="message" hidden></p>
    </div>
  </div>
  <div class="lead-form-consent">
    <input type="checkbox" id="lead-consent" name="consent" required>
    <label for="lead-consent">I accept the <a href="/conditions/privacy-policy/">privacy policy</a> and agree to be contacted about my request.</label>
    <p class="lead-form-error" data-field="consent" hidden></p>
  </div>
  <div class="lead-form-honeypot" aria-hidden="true">
    <input type="text" name="website" tabindex="-1" autocomplete="off">
  </div>
  <div class="lead-form-actions md-typeset">
    <button type="submit" class="md-button md-button--primary lead-form-submit">Send message</button>
    <p class="lead-form-reassurance">We reply as soon as possible.</p>
  </div>
  <p class="lead-form-status" role="status" hidden></p>
</form>

Prefer email? Write to us directly at [commercial@openvidu.io](mailto:commercial@openvidu.io){:target="_blank"}.

Let's work together and build something great!

!!! info

    Do you need help [**updating from OpenVidu 2 to OpenVidu 3** :fontawesome-solid-external-link:{.external-link-icon}](https://docs.openvidu.io/en/stable/openvidu3/){:target="_blank"}? Write us to [pro.support.v2apps@openvidu.io](mailto:pro.support.v2apps@openvidu.io){:target="_blank"} and we will be happy to guide you through the process.

## Community support

The [public forum :simple-discourse:](https://openvidu.discourse.group/){:target="_blank"} is the right place to ask any questions that do not involve private information, so that the whole community can benefit from the exchange of ideas.