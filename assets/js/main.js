/* ================================================
   SHIVRAM NEKKANTI PORTFOLIO — main.js
   ================================================ */

// ── SCROLL ANIMATIONS ──
const animatedEls = document.querySelectorAll('[data-animate]');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

animatedEls.forEach(el => observer.observe(el));

// ── ACTIVE NAV LINK ──
// Highlights the correct nav link based on current page
const currentPage = window.location.pathname.split('/').pop() || 'index.html';

document.querySelectorAll('.nav-links a').forEach(link => {
  const href = link.getAttribute('href').split('/').pop();
  if (href === currentPage) {
    link.classList.add('active');
  } else {
    link.classList.remove('active');
  }
});

// ── NAV SCROLL SHADOW ──
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  if (window.scrollY > 10) {
    nav.style.borderBottomColor = 'rgba(255,255,255,0.1)';
  } else {
    nav.style.borderBottomColor = 'rgba(255,255,255,0.07)';
  }
});

// ── CONTACT FORM ──
const form = document.getElementById('contact-form');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = form.querySelector('.form-submit');
    btn.textContent = 'Sent ✓';
    btn.style.opacity = '0.7';
    btn.disabled = true;
    setTimeout(() => {
      btn.textContent = 'Send Message';
      btn.style.opacity = '1';
      btn.disabled = false;
      form.reset();
    }, 3000);
  });
}