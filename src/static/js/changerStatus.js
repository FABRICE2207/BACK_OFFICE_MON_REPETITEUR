document.addEventListener('DOMContentLoaded', (Event) => {
    // Déclaration des constantes
    const btnPublie = document.getElementById('Btnsubmit');
    const btnRefuse = document.getElementById('BtnsubmitRefuse');
    const changeStatut = document.getElementById('change_status');
    const Statut = document.querySelectorAll('#change_status');
    // Récupérer l'ID de l'article
    id = $(this).data('id');

    // Action btn publié pour changer le texte
    btnPublie.addEventListener('click', ()=> {
        fetch(`/api/update_status_publie/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({newStatut: 'publié'}), // Obtenir le texte en json
        })
        .then(response => response.json())
        .then(data => {
            // Vérification de l'existance du texte
            if(data.success){
                // Changement du texte
                changeStatut.textContent = data.newStatut;
            } else {
                console.error('Erreur du changement du status');
            }
        })
        .catch(error => {
            console.error('Erreur', error);
        });

        setInterval(function(){
            window.location.reload();
        }, 1000); // 5000 millisecondes = 5 secondes
    });
    

       // Action btn publié pour changer le texte
    btnRefuse.addEventListener('click', ()=> {
        fetch(`/api/update_status_refuse/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({newStatut: 'refusé'}), // Obtenir le texte en json
        })
        .then(response => response.json())
        .then(data => {
            // Vérification de l'existance du texte
            if(data.success){
                // Changement du texte
                changeStatut.textContent = data.newStatut;
            } else {
                console.error('Erreur du changement du status');
            }
        })
        .catch(error => {
            console.error('Erreur', error);
        });
        setInterval(function(){
            window.location.reload();
        }, 1000); // 5000 millisecondes = 5 secondes
    });
});




