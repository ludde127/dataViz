class Searcher {

    constructor(search_element, search_results_element_list, search_results_div_element) {
        this.search_element = search_element;
        this.search_results_elements = search_results_element_list;
        this.search_results_div_elements = search_results_div_element;

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
        this.updateResults(resp);
    }

    updateResults(results) {
            if (Object.values(results["results"]).length > 0) {

                this.search_results_div_elements.style.display = "inline";
                this.search_results_div_elements.style.visibility = "visible";

                let html = "";
                console.log(results);
                for (const result of Object.values(results["results"])) {
                    html += `<li class="nav-item search-results "><a href=${result["url"]}>${result["title"]}</a><hr style='margin-top: 3px;margin-bottom: 2px;color: black;'></li>`
                }
                this.search_results_elements.innerHTML = html;
            } else {
                this.search_results_div_elements.style.display = "none";
                this.search_results_div_elements.style.visibility = "hidden";


            }


    }

}

export default Searcher;