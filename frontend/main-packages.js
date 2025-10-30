import { Chart } from "chart.js/auto";

// Sélection du canvas
const canvas = document.getElementById("packagesChart");
let chartInstance = null;

// ---- Charger les données depuis Django ----
async function loadChartData() {
    const from = document.getElementById("date_from").value;
    const to   = document.getElementById("date_to").value;

    // URL API Django pour les packages
    let url = `/package/dashboard/data/`;
    const params = new URLSearchParams();
    if (from) params.append("date_from", from);
    if (to) params.append("date_to", to);
    if (params.toString()) url += "?" + params.toString();

    const response = await fetch(url);
    const data = await response.json();

    // Mise à jour du graphique et du tableau
    renderChart(data.labels, data.values);
    renderAmounts(data.amounts);
}

// ---- Afficher le graphique ----
function renderChart(labels, values) {
    if (chartInstance) chartInstance.destroy();

    chartInstance = new Chart(canvas, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: "Packages vendus",
                data: values,
                // backgroundColor: "rgba(75, 192, 192, 0.5)",
                // borderColor: "rgba(75, 192, 192, 1)",
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: "Packages vendus par agence"
                },
                legend: { display: false }
            },
            scales: {
                x: { grid: { display: false } },
                y: { grid: { display: false }, beginAtZero: true }
            }
        }
    });
}

// ---- Afficher le tableau des montants ----
function renderAmounts(amounts) {
    const tbody = document.querySelector("#amountsSummary tbody");
    tbody.innerHTML = amounts.map(item => `
        <tr>
            <td>${item.agency__name}</td>
            <td>${Number(item.total_amount).toLocaleString()}</td>
            <td><span class="badge bg-secondary">${item.agency_currency}</span></td>
        </tr>
    `).join("");
}

// ---- Événement : filtre par date ----
document.getElementById("filterForm").addEventListener("submit", e => {
    e.preventDefault();
    loadChartData();
});

// ---- Charger les données au démarrage ----
loadChartData();
