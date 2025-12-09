document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const form = btn.closest('form');
            const card = btn.closest('.article-card');
            //console.log("TEST")

            if (!confirm("Willst du diesen Artikel wirklich löschen?")) return;

            const response = await fetch(form.action, { method: "DELETE" });
            if (response.ok) {
                card.remove(); // Karte aus dem DOM entfernen
                const remaining = document.querySelectorAll('.article-card').length;
                if (remaining === 0) {
                    document.getElementById('empty-fallback').style.display = 'block';
                }
            } else {
              alert("Fehler beim Löschen des Artikels.");
            }
        });
    });
});