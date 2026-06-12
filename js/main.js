/* EMIL'S COOK BOOK — reveal on scroll, nav after hero, photo lightbox */
(function () {
  'use strict';

  /* ---------- fade/raise blocks into view ---------- */
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- show the fixed nav once the hero is scrolled past ---------- */
  var nav = document.getElementById('nav');
  var hero = document.querySelector('.hero');
  if (nav && hero && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      nav.classList.toggle('show', !entries[0].isIntersecting);
    }, { rootMargin: '-60px 0px 0px 0px' }).observe(hero);
  } else if (nav) {
    nav.classList.add('show');
  }

  /* ---------- lightbox: click a photo for the high-resolution view ----------
     Pure enhancement: if anything fails, the site works exactly as before. */
  try {
    var photos = Array.prototype.slice.call(
      document.querySelectorAll('.canvas .ph img, .breather img, .strip-grid img')
    );
    if (!photos.length) return;

    // largest available source of an <img> (last srcset entry, else src)
    function fullSrc(img) {
      var ss = img.getAttribute('srcset');
      if (ss) {
        var parts = ss.split(',');
        return parts[parts.length - 1].trim().split(/\s+/)[0];
      }
      return img.getAttribute('src');
    }

    var lb = document.createElement('div');
    lb.className = 'lb';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-label', 'Photo view');
    lb.innerHTML =
      '<img alt="">' +
      '<button class="lb-close" aria-label="Close">\u00d7</button>' +
      '<button class="lb-prev" aria-label="Previous">\u2039</button>' +
      '<button class="lb-next" aria-label="Next">\u203a</button>' +
      '<span class="lb-count"></span>';
    document.body.appendChild(lb);

    var lbImg = lb.querySelector('img');
    var count = lb.querySelector('.lb-count');
    var cur = 0;

    function show(i) {
      cur = (i + photos.length) % photos.length;
      var p = photos[cur];
      lbImg.src = fullSrc(p);
      lbImg.alt = p.alt || '';
      count.textContent = (cur + 1) + ' / ' + photos.length;
      // preload neighbours for instant stepping
      [cur + 1, cur - 1].forEach(function (j) {
        var n = new Image();
        n.src = fullSrc(photos[(j + photos.length) % photos.length]);
      });
    }
    function open(i) {
      show(i);
      lb.classList.add('open');
      document.body.classList.add('lb-lock');
    }
    function close() {
      lb.classList.remove('open');
      document.body.classList.remove('lb-lock');
      lbImg.src = '';
    }

    photos.forEach(function (img, i) {
      img.addEventListener('click', function () { open(i); });
    });
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function (e) { e.stopPropagation(); show(cur - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function (e) { e.stopPropagation(); show(cur + 1); });
    lb.addEventListener('click', function (e) {
      if (e.target === lb) close();          // click on the dark backdrop
    });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft') show(cur - 1);
      else if (e.key === 'ArrowRight') show(cur + 1);
    });

    // swipe on touch devices
    var tx = null;
    lb.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (tx === null) return;
      var dx = e.changedTouches[0].clientX - tx;
      if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1));
      tx = null;
    }, { passive: true });
  } catch (err) {
    /* lightbox is optional — never break the page */
  }
})();
