document.addEventListener('DOMContentLoaded', function() {
    const worksContainer = document.getElementById('works-container');
    const authorsContainer = document.getElementById('authors-container');
  
    function createWorkHTML(w) {
      return `
        <div class="col-md-4 card-container">
          <div class="card shadow-sm hover-card">
            <div class="card-body">
              <h5 class="card-title"><a href="/work/${w.id}" class="stretched-link text-decoration-none">${w.title}</a></h5>
              <p class="card-text text-muted"><small>Published: ${w.first_publish_date}</small></p>
              <p class="card-text">${w.description ? w.description.substring(0,80) : ''}</p>
            </div>
          </div>
        </div>
      `;
    }
  
    function createAuthorHTML(a) {
      const deathDate = a.death_date ? `, Died: ${a.death_date}` : '';
      return `
        <div class="col-md-4 card-container">
          <div class="card shadow-sm hover-card">
            <div class="card-body">
              <h5 class="card-title"><a href="/author/${a.id}" class="stretched-link text-decoration-none">${a.name}</a></h5>
              <p class="card-text text-muted"><small>Born: ${a.birth_date}${deathDate}</small></p>
              <p class="card-text">${a.bio ? a.bio.substring(0,80) : ''}</p>
            </div>
          </div>
        </div>
      `;
    }
  
    function updateContent(data) {
      // data contains {authors: [...], works: [...]}
      const works = data.works;
      const authors = data.authors;
  
      // Construct HTML for works
      const worksHTML = `
        <div class="row g-4 mb-4">
          ${works.slice(0,3).map(createWorkHTML).join('')}
        </div>
        <div class="row g-4 mb-5">
          ${works.slice(3,6).map(createWorkHTML).join('')}
        </div>
      `;
  
      // Construct HTML for authors
      const authorsHTML = `
        <div class="row g-4 mb-4">
          ${authors.slice(0,3).map(createAuthorHTML).join('')}
        </div>
        <div class="row g-4 mb-5">
          ${authors.slice(3,6).map(createAuthorHTML).join('')}
        </div>
      `;
  
      // Add slide-out class
      worksContainer.classList.add('slide-out');
      authorsContainer.classList.add('slide-out');
  
      setTimeout(() => {
        // Replace content after animation ends
        worksContainer.innerHTML = worksHTML;
        authorsContainer.innerHTML = authorsHTML;
  
        // Remove slide-out and add slide-in
        worksContainer.classList.remove('slide-out');
        authorsContainer.classList.remove('slide-out');
        worksContainer.classList.add('slide-in');
        authorsContainer.classList.add('slide-in');
  
        // Remove slide-in after animation done
        setTimeout(() => {
          worksContainer.classList.remove('slide-in');
          authorsContainer.classList.remove('slide-in');
        }, 500);
      }, 500);
    }
  
    function fetchNewData() {
      fetch('/random_data')
        .then(response => response.json())
        .then(data => {
          updateContent(data);
        })
        .catch(err => console.error('Error fetching data:', err));
    }
  
    setInterval(fetchNewData, 4000);
  });
  