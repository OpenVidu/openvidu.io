// Terminal recordings (page feature `terminalrecording`): every <div class="ov-rec"> becomes an
// asciinema player of a recording of the ov end-to-end tests, from assets/recordings/ (written
// by tools/export-recordings.py), with a switch between the edited copy (long waits cut) and
// the full recording in real time.
//
// Which recording: `data-rec="<cell>"` on the element, or `data-rec-suffix="<rest>"` under an
// ancestor carrying `data-rec-prefix` (the install pages name their cloud and type once, around
// a shared snippet): the cell is `<prefix>-<rest>`.
//
// Nothing heavy loads with the page: the player (asciinema-player, vendored beside this file)
// and the edited recording load the first time a recording scrolls into view, the real-time
// one only when it is asked for. A recording pauses when it leaves the screen (a tab switch
// hides it too). The player reads its colours once, when it mounts, so a palette change mounts
// it again at the same moment.
(function () {
  "use strict";

  var nodes = document.querySelectorAll(".ov-rec");
  if (!nodes.length || !document.currentScript) return;

  // Every URL is relative to this script, so each published version reads its own files.
  var here = document.currentScript.src;
  var PLAYER_JS = new URL("asciinema-player.min.js", here).href;
  var PLAYER_CSS = new URL("../stylesheets/asciinema-player.css", here).href;
  var RECORDINGS = new URL("../assets/recordings/", here).href;

  var libPromise = null;
  function loadPlayer() {
    if (libPromise) return libPromise;
    var css = new Promise(function (resolve) {
      var link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = PLAYER_CSS;
      link.onload = link.onerror = resolve;
      document.head.appendChild(link);
    });
    var js = new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      script.src = PLAYER_JS;
      script.async = true;
      script.onload = function () {
        resolve(window.AsciinemaPlayer);
      };
      script.onerror = reject;
      document.head.appendChild(script);
    });
    libPromise = Promise.all([js, css]).then(function (r) {
      return r[0];
    });
    libPromise.catch(function () {
      libPromise = null;
    });
    return libPromise;
  }

  var casts = {};
  function fetchCast(url) {
    if (!casts[url]) {
      casts[url] = fetch(url).then(function (res) {
        if (!res.ok) throw new Error(res.status + " " + url);
        return res.text();
      });
      casts[url].catch(function () {
        delete casts[url];
      });
    }
    return casts[url];
  }

  // What the page needs from a cast: its size and length, where the cut waits are (the export
  // writes them into the edited copy's header) and the frame to show before it plays: the
  // moment ov says the stack is up, or else the deploy.
  function describe(text) {
    var lines = text.split("\n");
    var header = JSON.parse(lines[0]);
    var duration = 0;
    var up = null;
    var deploy = null;
    for (var i = 1; i < lines.length; i++) {
      if (!lines[i]) continue;
      var e = JSON.parse(lines[i]);
      duration = e[0];
      if (up === null && e[1] === "o" && e[2].indexOf(" is up on ") >= 0) up = e[0];
      if (deploy === null && e[1] === "m" && e[2].indexOf("Deploy") === 0) deploy = e[0];
    }
    var extra = header.x_openvidu || {};
    var poster = up !== null ? up + 1.5 : deploy !== null ? deploy + 4 : 0;
    return {
      cols: header.width,
      rows: header.height,
      duration: duration,
      rawDuration: extra.raw_duration,
      gaps: extra.gaps || [],
      poster: Math.min(poster, duration),
    };
  }

  function minutes(seconds) {
    if (!(seconds > 0)) return "";
    return seconds < 90 ? Math.round(seconds) + " s" : Math.round(seconds / 60) + " min";
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  var recordings = [];

  function setUp(node) {
    var cell = node.getAttribute("data-rec");
    if (!cell) {
      var host = node.closest("[data-rec-prefix]");
      var suffix = node.getAttribute("data-rec-suffix");
      if (host && suffix) cell = host.getAttribute("data-rec-prefix") + "-" + suffix;
    }
    if (!cell) return;

    var bar = el("div", "ov-rec-bar");
    var group = el("div", "ov-rec-switch");
    group.setAttribute("role", "group");
    group.setAttribute("aria-label", "Recording");
    var edited = el("button", null, "Edited");
    var raw = el("button", null, "Full real time");
    [edited, raw].forEach(function (b) {
      b.type = "button";
      group.appendChild(b);
    });
    var note = el("span", "ov-rec-note");
    bar.appendChild(group);
    bar.appendChild(note);
    var stage = el("div", "ov-rec-stage");
    var term = el("div", "ov-rec-term");
    var gap = el("div", "ov-rec-gap");
    gap.setAttribute("aria-live", "polite");
    var status = el("div", "ov-rec-status");
    stage.appendChild(term);
    stage.appendChild(gap);
    stage.appendChild(status);
    node.textContent = "";
    node.appendChild(bar);
    node.appendChild(stage);

    var rec = {
      cell: cell,
      node: node,
      term: term,
      gap: gap,
      status: status,
      note: note,
      buttons: { edited: edited, raw: raw },
      which: "edited",
      player: null,
      info: null,
      playing: false,
      timer: null,
      started: false,
    };
    edited.addEventListener("click", function () {
      choose(rec, "edited");
    });
    raw.addEventListener("click", function () {
      choose(rec, "raw");
    });
    pressed(rec);
    recordings.push(rec);
    return rec;
  }

  function pressed(rec) {
    rec.buttons.edited.setAttribute("aria-pressed", String(rec.which === "edited"));
    rec.buttons.raw.setAttribute("aria-pressed", String(rec.which === "raw"));
    rec.note.textContent =
      rec.which === "edited" ? "Long waits cut" : "Every second, as it ran";
  }

  function urlOf(rec, which) {
    return RECORDINGS + rec.cell + (which === "raw" ? ".raw.cast" : ".edited.cast");
  }

  function label(rec) {
    var info = rec.editedInfo;
    if (!info) return;
    rec.buttons.edited.textContent = "Edited · " + minutes(info.duration);
    if (info.rawDuration) rec.buttons.raw.textContent = "Full real time · " + minutes(info.rawDuration);
  }

  // Mounts `which` in the stage, at `opts.at` seconds (or on its poster) and playing if
  // `opts.play`.
  function mount(rec, which, opts) {
    opts = opts || {};
    rec.status.textContent = which === "raw" ? "Loading the real-time recording…" : "Loading…";
    rec.node.classList.add("is-loading");
    return Promise.all([loadPlayer(), fetchCast(urlOf(rec, which))])
      .then(function (r) {
        var AP = r[0];
        var text = r[1];
        var info = describe(text);
        if (which === "edited") rec.editedInfo = info;
        label(rec);
        unmount(rec);
        rec.info = info;
        rec.which = which;
        pressed(rec);
        var options = {
          cols: info.cols,
          rows: info.rows,
          fit: "width",
          theme: "openvidu",
          terminalLineHeight: 1.33,
          preload: true,
          controls: true,
          autoPlay: !!opts.play,
        };
        if (opts.at > 0) options.startAt = opts.at;
        else if (!opts.play && info.poster > 0) options.poster = "npt:" + info.poster;
        rec.player = AP.create({ data: text }, rec.term, options);
        rec.player.addEventListener("play", function () {
          playing(rec, true);
        });
        rec.player.addEventListener("playing", function () {
          playing(rec, true);
        });
        rec.player.addEventListener("pause", function () {
          playing(rec, false);
        });
        rec.player.addEventListener("ended", function () {
          playing(rec, false);
        });
        rec.status.textContent = "";
        rec.node.classList.remove("is-loading");
      })
      .catch(function () {
        rec.node.classList.remove("is-loading");
        rec.status.textContent = "The recording could not be loaded.";
        rec.started = false;
      });
  }

  function unmount(rec) {
    playing(rec, false);
    if (rec.player) {
      rec.player.dispose();
      rec.player = null;
    }
    rec.term.textContent = "";
  }

  function now(rec) {
    return Promise.resolve(rec.player ? rec.player.getCurrentTime() : 0).then(function (t) {
      return typeof t === "number" ? t : 0;
    });
  }

  // While it plays, the edited copy announces each cut wait as it crosses it.
  function playing(rec, on) {
    rec.playing = on;
    if (on && !rec.timer && rec.which === "edited" && rec.info && rec.info.gaps.length) {
      rec.timer = setInterval(function () {
        now(rec).then(function (t) {
          var hit = null;
          rec.info.gaps.forEach(function (g) {
            if (!hit && t >= g.at - 1 && t < g.at + 2) hit = g;
          });
          if (hit) {
            if (rec.gap.getAttribute("data-at") !== String(hit.at)) {
              rec.gap.setAttribute("data-at", String(hit.at));
              rec.gap.textContent = hit.label + " ";
              rec.gap.appendChild(el("small", null, "of waiting cut"));
            }
            rec.gap.classList.add("on");
          } else {
            rec.gap.classList.remove("on");
          }
        });
      }, 250);
    }
    if (!on) {
      clearInterval(rec.timer);
      rec.timer = null;
      rec.gap.classList.remove("on");
    }
  }

  function choose(rec, which) {
    if (which === rec.which && rec.player) return;
    var wasPlaying = rec.playing;
    rec.started = true;
    mount(rec, which, { play: wasPlaying });
  }

  // A palette change: the same recording, at the same moment, in the new colours.
  function repaint() {
    recordings.forEach(function (rec) {
      if (!rec.player) return;
      var wasPlaying = rec.playing;
      now(rec).then(function (t) {
        mount(rec, rec.which, { at: t, play: wasPlaying });
      });
    });
  }

  var list = Array.prototype.map.call(nodes, setUp).filter(Boolean);

  if (!("IntersectionObserver" in window)) {
    list.forEach(function (rec) {
      rec.started = true;
      mount(rec, "edited");
    });
  } else {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          var rec = list.filter(function (r) {
            return r.node === entry.target;
          })[0];
          if (!rec) return;
          if (entry.isIntersecting && !rec.started) {
            rec.started = true;
            mount(rec, "edited");
          } else if (!entry.isIntersecting && rec.playing && rec.player) {
            rec.player.pause();
          }
        });
      },
      { rootMargin: "200px 0px" }
    );
    list.forEach(function (rec) {
      io.observe(rec.node);
    });
  }

  if ("MutationObserver" in window) {
    var scheme = document.body.getAttribute("data-md-color-scheme");
    new MutationObserver(function () {
      var next = document.body.getAttribute("data-md-color-scheme");
      if (next !== scheme) {
        scheme = next;
        repaint();
      }
    }).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
  }
})();
