import{C as s}from"./auto-aF82oVy8.js";const l=document.getElementById("packagesChart");let o=null;async function d(){const t=document.getElementById("date_from").value,e=document.getElementById("date_to").value;let a="/package/dashboard/data/";const n=new URLSearchParams;t&&n.append("date_from",t),e&&n.append("date_to",e),n.toString()&&(a+="?"+n.toString());const r=await(await fetch(a)).json();c(r.labels,r.values),u(r.amounts)}function c(t,e){o&&o.destroy(),o=new s(l,{type:"bar",data:{labels:t,datasets:[{label:"Packages vendus",data:e,backgroundColor:"rgba(75, 192, 192, 0.5)",borderColor:"rgba(75, 192, 192, 1)",borderWidth:1}]},options:{plugins:{title:{display:!0,text:"Packages vendus par agence"},legend:{display:!1}},scales:{x:{grid:{display:!1}},y:{grid:{display:!1},beginAtZero:!0}}}})}function u(t){const e=document.querySelector("#amountsSummary tbody");e.innerHTML=t.map(a=>`
        <tr>
            <td>${a.agency__name}</td>
            <td>${Number(a.total_amount).toLocaleString()}</td>
            <td><span class="badge bg-secondary">${a.agency_currency}</span></td>
        </tr>
    `).join("")}document.getElementById("filterForm").addEventListener("submit",t=>{t.preventDefault(),d()});d();
