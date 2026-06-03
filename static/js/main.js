// ── Sell page: live price preview ──────────────────────────────────────────
const productSelect = document.getElementById('product-select');
const qtyInput = document.getElementById('qty-input');
const sellPreview = document.getElementById('sell-preview');
const prevPrice = document.getElementById('prev-price');
const prevQty = document.getElementById('prev-qty');
const prevTotal = document.getElementById('prev-total');

function updatePreview() {
  if (!productSelect) return;
  const opt = productSelect.options[productSelect.selectedIndex];
  if (!opt || !opt.dataset.price) { if (sellPreview) sellPreview.style.display = 'none'; return; }

  const price = parseFloat(opt.dataset.price);
  const qty = parseInt(qtyInput.value) || 1;
  const total = price * qty;

  if (sellPreview) {
    sellPreview.style.display = 'block';
    prevPrice.textContent = `₹${price.toFixed(2)}`;
    prevQty.textContent = qty;
    prevTotal.textContent = `₹${total.toFixed(2)}`;
  }
}

if (productSelect) {
  productSelect.addEventListener('change', updatePreview);
  qtyInput.addEventListener('input', updatePreview);
}

// ── Flash auto-dismiss ──────────────────────────────────────────────────────
document.querySelectorAll('.flash').forEach(el => {
  setTimeout(() => {
    el.style.transition = 'opacity 0.5s ease';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 500);
  }, 4000);
});

// ── Product card hover ripple ───────────────────────────────────────────────
document.querySelectorAll('.product-card').forEach(card => {
  card.addEventListener('mouseenter', () => {
    card.style.transition = 'transform 0.2s ease, box-shadow 0.2s ease';
  });
});
