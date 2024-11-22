document
  .getElementById("movie-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const movieName = document.getElementById("movie").value;
    const recommendationsDiv = document.getElementById("recommendations");
    const spinner = document.getElementById("loading-spinner");

    recommendationsDiv.innerHTML = "";
    spinner.style.display = "block";

    try {
      const response = await fetch("/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `movie=${encodeURIComponent(movieName)}`,
      });

      const data = await response.json();
      spinner.style.display = "none";

      if (data.status === "success") {
        const movies = data.movies;
        recommendationsDiv.innerHTML = `<h2>Recommendations for "${movieName}":</h2><ul>${movies
          .map((movie) => `<li>${movie}</li>`)
          .join("")}</ul>`;
      } else {
        recommendationsDiv.innerHTML = `<p>Error: ${data.message}</p>`;
      }
    } catch (error) {
      spinner.style.display = "none";
      recommendationsDiv.innerHTML =
        "<p>An error occurred. Please try again.</p>";
    }
  });
