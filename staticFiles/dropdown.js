
const movieSelection = document.getElementById("movieSelection");

let timer;              // Timer identifier
const waitTime = 200;   // Wait time in milliseconds 

const search = (text, callback) => {
    let request = new XMLHttpRequest();
    request.open("GET", "https://imdb-api.com/en/API/Search/k_ck108nll/" + text);
    request.send();
  
    request.onload = () => {
      if (request.status === 200) {
        const response = JSON.parse(request.responseText);
        callback(response);
      } else {
        console.log(`error ${request.status} ${request.statusText}`);
      }
    };
  };
  

// Listen for `keyup` event
const input = document.querySelector('#movie');
input.addEventListener('keyup', (e) => {
    const text = e.currentTarget.value;
    let selection;

    clearTimeout(timer);

    timer = setTimeout(() => {
      search(text, (response) => {
          // Clear existing options
        movieSelection.innerHTML = '';
        selection = response;
        for (let i = 0; i < 5; i++) {
          let option = document.createElement("option");
          option.setAttribute("value", "/recommendations/"+selection.results[i].id);

          let optionText = document.createTextNode(selection.results[i].title);
          option.appendChild(optionText);

          movieSelection.appendChild(option);
        }
      });
    }, waitTime);
  });
      
  movieSelection.addEventListener('change', (e) => {
    location.href = e.currentTarget.value;
  });