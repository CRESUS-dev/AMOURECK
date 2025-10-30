import "./chart-default.js";
import { Chart } from "chart.js/auto";


const canvas = document.getElementById("ticketsChart");
let chartInstance = null;

async function loadChartData() {
    const from = document.getElementById("date_from").value;
    const to   = document.getElementById("date_to").value;

    let url = `/ticket/dashboard/data`;
    const params = new URLSearchParams();

    if (from) params.append("date_from", from);
    if (to)   params.append("date_to", to);

    if (params.toString()) {
        url += "?" + params.toString();
    }

    const response = await fetch(url);
    const data = await response.json();

    function renderAmounts(amounts) {
    const tbody = document.querySelector("#amountsSummary tbody");
    tbody.innerHTML = amounts.map(item => `
        <tr>
            <td>${item.agency__name}</td>
            <td>${Number(item.total_amount).toLocaleString()}</td>
            <td>${item.agency_currency}</td>
        </tr>
    `).join("");
}



    renderChart(data.labels, data.values);
    renderAmounts(data.amounts);
}




function renderChart(labels, values) {
    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(canvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Tickets vendus ",
                data: values,
                backgroundColor: "rgba(0,67,100,1)",

            }]
        },
        options: {
            plugins: {
                legend: { display: false, position:'top' },
                title: {
                    display:true,
                    text:"Nombre de tickets vendus par agence",
                    fontSize:30
                }


            },
             scales: {
                  y: {
                      beginAtZero: true,
                      grid: {display:false}
                  },
                  x: {
                      grid:{display:false}
                  }


      }
        }
    });
}

// --- Charger au démarrage
loadChartData();

// --- Lancer fetchData quand on submit le formulaire
document.getElementById("filterForm").addEventListener("submit", function (e) {
    e.preventDefault();
    loadChartData();
});
