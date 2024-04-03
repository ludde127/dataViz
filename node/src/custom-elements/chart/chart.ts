import {CategoryScale, Chart, ChartData, LinearScale, LineController, LineElement, PointElement} from "chart.js";

Chart.register(LineController, CategoryScale, LinearScale, PointElement, LineElement);

class YapityChart extends HTMLElement {
    canvas: HTMLCanvasElement;
    data: { data: ChartData };

    constructor() {
        super();

        this.data = JSON.parse(this.dataset.data || "{}");

        this.canvas = this.querySelector("#canvas")!;

        new Chart(this.canvas, {
            type: 'line',
            data: this.data.data
        });
    }
}

customElements.define("yapity-chart", YapityChart);