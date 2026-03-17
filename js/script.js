console.log('js/script.js loaded');
document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('productModal');
  const pmImage = document.getElementById('pm-image');
  const closeBtn = modal.querySelector('.pm-close');
  const imageCloseBtn = modal.querySelector('.pm-image-close');
  const whatsappBtn = document.getElementById('pm-whatsapp');
  const shareBtn = document.getElementById('pm-share');
  const addCartBtn = document.getElementById('pm-addcart');

  function openModal(imgSrc) {
    pmImage.src = imgSrc;
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
  }

  function closeModal() {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    pmImage.src = '';
  }

  document.querySelectorAll('.product-img').forEach(img => {
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', function (e) {
      openModal(e.currentTarget.src);
    });
  });

  // Prevent parent anchor from navigating when image is clicked
  document.querySelectorAll('a').forEach(a => {
    if (a.querySelector('.product-img')) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
      });
    }
  });

  closeBtn.addEventListener('click', closeModal);
  if (imageCloseBtn) imageCloseBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', function (e) {
    if (e.target === modal) closeModal();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeModal();
  });

  whatsappBtn.addEventListener('click', function () {
    const url = pmImage.src || window.location.href;
    const wa = 'https://wa.me/?text=' + encodeURIComponent('Check this product: ' + url);
    window.open(wa, '_blank');
  });

  shareBtn.addEventListener('click', async function () {
    const url = pmImage.src || window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({ title: 'Product', text: 'Check this product', url });
      } catch (err) {
        // ignore
      }
    } else {
      // fallback: copy to clipboard
      try {
        await navigator.clipboard.writeText(url);
        alert('Product link copied to clipboard');
      } catch (err) {
        prompt('Copy this link', url);
      }
    }
  });

  addCartBtn.addEventListener('click', function () {
    alert('Added to cart (demo). Implement cart logic as needed.');
  });
});
