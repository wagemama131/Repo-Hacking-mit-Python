document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".add-note form");
    const list = document.querySelector(".article-list");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(form);

        const response = await fetch("/add/article", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            let response2 = await response.json();
            alert("Artikel konnte nicht gespeichert werden: " + response2.message);
            return;
        }

        const article = await response.json();

        //  HTML für neue Karte erstellen
        const card = document.createElement("div");
        card.classList.add("article-card");

        card.innerHTML = `
            <img src="${article.image_url || '/static/img/no_image.png'}" alt="${article.title}">
            <div class="content">
                <h3>${article.title }</h3>
                <hr>
                <strong>Preis: </strong>${article.price} € 
                <hr>
                <strong>Verhandelbar:</strong> ${article.negotiable ? 'Ja' : 'Nein'}
                <hr>
                <strong>Zustand:</strong> ${article.condition || 'Unbekannt'}
                <hr>
                <strong>Ort:</strong> ${article.location} (${article.postalcode})
                <hr>
                <small>${article.description || ''}</small>
                <hr>
                <small>☎ ${article.phone_number || 'Keine Angabe'} / 📧${article.email || ''}</small><br>
                <small>Erstellt ${article.created_at || ''}</small>
            </div>
        `;

        //  Als erstes Element einfügen
        list.prepend(card);

        //  Formular zurücksetzen
        form.reset();

        // Zettel einklappen
        document.getElementById("addNote").classList.remove("open");
    });

});

