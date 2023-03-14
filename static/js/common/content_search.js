function updateResults(results) {
            if (Object.values(results["results"]).length > 0) {
                let element = document.querySelector("#search-results");

                document.querySelector("#search-results-div").style.display = "inline";
                document.querySelector("#search-results-div").style.visibility = "visible";

                let html = "";
                console.log(results);
                for (const result of Object.values(results["results"])) {
                    html += `<li class="nav-item search-results "><a href=${result["url"]}>${result["title"]}</a><hr style='margin-top: 3px;margin-bottom: 2px;color: black;'></li>`
                }
                element.innerHTML = html;
            } else {
                document.querySelector("#search-results-div").style.display = "none";
                document.querySelector("#search-results-div").style.visibility = "hidden";


            }


        }

class Searcher {

    constructor(search_element) {
        this.search_element = search_element;

        this.search_element.addEventListener("input", (event) => {
            this.search().then(r => null);
        })
    }

    async search() {
        let input = this.search_element.value;
        const resp = await fetch("/search/?query=" + input).then(function (response) {
            return response.json();
        }).catch(function (err) {

            console.log('Fetch Error :-S', err);
            return false;
        });
        updateResults(resp);
    }


}

export default Searcher;