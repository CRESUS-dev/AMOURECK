import {Chart} from  "chart.js/auto"

// Fonts par défaut
Chart.defaults.font.family = "'Inter', 'Roboto', sans-serif";
Chart.defaults.font.size = 14;
Chart.defaults.datasets.bar.borderWidth = 0;
Chart.defaults.datasets.bar.borderColor="#000000";

// Legend globale
Chart.defaults.plugins.legend.position = "bottom";
Chart.defaults.plugins.legend.labels.boxWidth = 16;
Chart.defaults.plugins.title.display=true
// Tooltip global
Chart.defaults.plugins.tooltip.backgroundColor = "rgba(0,0,0,0.7)";
Chart.defaults.plugins.tooltip.cornerRadius = 6;

// Layout responsive
Chart.defaults.maintainAspectRatio = false;
Chart.defaults.responsive = true;


