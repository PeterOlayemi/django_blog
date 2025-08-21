document.addEventListener("DOMContentLoaded", function() {
  const loadMoreBtn = document.getElementById('loadMoreBtn');
  const postCards = document.querySelectorAll('#postsContainer .post-card-wrapper');
  let visibleCount = 6;

  loadMoreBtn.addEventListener('click', () => {
    let revealed = 0;

    for (let i = visibleCount; i < postCards.length && revealed < 3; i++) {
      postCards[i].classList.remove('d-none');
      revealed++;
    }

    visibleCount += revealed;

    if (visibleCount >= postCards.length) {
      loadMoreBtn.textContent = 'No more posts';
      loadMoreBtn.disabled = true;
    }
  });
});
