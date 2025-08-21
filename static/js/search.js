document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const suggestionsBox = document.getElementById("searchSuggestions");

    let debounceTimer;
    searchInput.addEventListener("input", () => {
        clearTimeout(debounceTimer);
        const query = searchInput.value.trim();

        if (!query) {
            suggestionsBox.style.display = "none";
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/search-suggestions/?q=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => {
                    suggestionsBox.innerHTML = "";

                    const hasResults = (
                        data.articles.length ||
                        data.writers.length ||
                        data.categories.length
                    );

                    if (!hasResults) {
                        suggestionsBox.innerHTML =
                            `<div class="list-group-item disabled">No results found</div>`;
                    } else {
                        if (data.articles.length) {
                            suggestionsBox.innerHTML += `<div class="list-group-item active">Articles</div>`;
                            data.articles.forEach(a => {
                                suggestionsBox.innerHTML +=
                                    `<a href="${a.url}" class="list-group-item list-group-item-action">${a.title}</a>`;
                            });
                        }
                        if (data.writers.length) {
                            suggestionsBox.innerHTML += `<div class="list-group-item active">Writers</div>`;
                            data.writers.forEach(w => {
                                suggestionsBox.innerHTML +=
                                    `<a href="${w.url}" class="list-group-item list-group-item-action">${w.username}</a>`;
                            });
                        }
                        if (data.categories.length) {
                            suggestionsBox.innerHTML += `<div class="list-group-item active">Categories</div>`;
                            data.categories.forEach(c => {
                                suggestionsBox.innerHTML +=
                                    `<a href="${c.url}" class="list-group-item list-group-item-action">${c.name}</a>`;
                            });
                        }
                    }

                    suggestionsBox.style.display = "block";
                });
        }, 300);
    });

    document.addEventListener("click", (e) => {
        if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
            suggestionsBox.style.display = "none";
        }
    });
});
