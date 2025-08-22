// For Contact us Page
(function () {
    function onReady(fn) {
      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", fn);
      } else {
        fn();
      }
    }
    onReady(function () {
      const form = document.querySelector("#contactForm") || document.querySelector("form");
      const container = document.querySelector(".contact-container")
      if (!form) {
        console.error('script.js: No form found. Add id="contactForm" to your <form> or make sure a <form> exists.');
        return;
      }
      if (container) {
        container.style.opacity = container.style.opacity || "0";
        container.style.transform = container.style.transform || "translateY(-20px)";
        setTimeout(() => {
          container.style.transition = "opacity 0.8s ease, transform 0.8s ease";
          container.style.opacity = "1";
          container.style.transform = "translateY(0)";
        }, 50);
      } else {
        console.warn("script.js: Container for animation not found — animation skipped.");
      }
  
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        const invalid = Array.from(form.elements).filter(el => el.required && (!el.value || el.value.trim() === ""));
        if (invalid.length) {
          invalid[0].focus();
          alert("Please fill all required fields before submitting.");
          return;
        }
        alert("✅ Your query has been submitted successfully!");
        try { form.reset(); } catch (err) { console.warn("script.js: form.reset() failed", err); }
      });
    });
  })();
  