class Searcher {
    constructor(search_bar, search_results_element_list, search_results_div_element) {
        this.search_bar = search_bar;
        this.search_results_elements = search_results_element_list;
        this.search_results_div_elements = search_results_div_element;


        this.selected_search_element_index = null;
        this.search_results = [];

        this.search_bar.addEventListener("input", (event) => {
            this.search().then(r => null);
        })

        this.search_bar.addEventListener("keydown", (event) => {
            // Handle key presses, enter will select highest link and go there,
            // Down will mark a lower element and up up.
            if (event.isComposing || event.keyCode === 229) {
                return;
            }
            console.log(this.selected_search_element_index)
            if (event.code === "ArrowDown") {
                this.unsetSelectedResultItem(this.selected_search_element_index);
                this.selected_search_element_index = (this.selected_search_element_index + 1) % this.search_results.length;
            } else if (event.code === "ArrowUp") {
                this.unsetSelectedResultItem(this.selected_search_element_index);
                this.selected_search_element_index = (this.selected_search_element_index - 1) % this.search_results.length;
            } else if (event.code === "Enter") {
                if (this.selected_search_element_index !== null) {
                    let selected = this.search_results[this.selected_search_element_index];
                    console.log("Selected ", selected);
                    window.location.replace(selected.url);

                } else {console.log("No selected elem")}
            }
            if (this.selected_search_element_index ===  -1) {
                this.selected_search_element_index=this.search_results.length-1;
            }
            if (this.selected_search_element_index !== null) {
                this.setSelectedResultItem(this.selected_search_element_index);
            }
        })

        document.addEventListener("keypress", (event) => {
            if (event.isComposing || event.keyCode === 229) {
                return;
            }


            this.search_bar.focus();
        })
    }

    async search() {
        let input = this.search_bar.value;
        const resp = await fetch("/search/?query=" + input).then(function (response) {
            return response.json();
        }).catch(function (err) {

            console.log('Fetch Error :-S', err);
            return false;
        });
        this.updateResults(resp);
    }

    updateResults(results) {
            this.search_results = [];

            if (Object.values(results["results"]).length > 0) {

                if (this.selected_search_element_index === null) {this.selected_search_element_index=0;}


                this.search_results_div_elements.style.display = "inline";
                this.search_results_div_elements.style.visibility = "visible";

                let html = "";
                let index = 0;
                for (const result of Object.values(results["results"])) {
                    html += `<li class="nav-item search-results" id="search-result-item-${index}"><a href=${result["url"]}>${result["title"]}</a>
                                <hr style='margin-top: 3px;margin-bottom: 2px;color: black;'></li>`
                    this.search_results.push({url: result["url"], title: result["title"]});
                    index++;
                }
                this.search_results_elements.innerHTML = html;
            } else {
                this.search_results_div_elements.style.display = "none";
                this.search_results_div_elements.style.visibility = "hidden";
                this.selected_search_element_index = null;

            }


    }

    setSelectedResultItem(index) {
        let elem = document
            .getElementById("search-result-item-"+index);
        elem.style.border = "2px solid black";
    }

    unsetSelectedResultItem(index) {
        let elem = document
            .getElementById("search-result-item-"+index);
        elem.style.border = "none";
    }
}

export default Searcher;