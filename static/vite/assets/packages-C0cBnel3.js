import{C as r}from"./auto-aF82oVy8.js";const l=document.getElementById("packagesChart");let d=null;async function o(){const t=document.getElementById("date_from").value,e=document.getElementById("date_to").value;let a="/package/dashboard/data/";const n=new URLSearchParams;t&&n.append("date_from",t),e&&n.append("date_to",e),n.toString()&&(a+="?"+n.toString());const s=await(await fetch(a)).json();c(s.labels,s.values),i(s.amounts)}function c(t,e){d&&d.destroy(),d=new r(l,{type:"pie",data:{labels:t,datasets:[{label:"Packages vendus",data:e,borderWidth:1}]},options:{plugins:{title:{display:!0,text:"Packages vendus par agence"},legend:{display:!1}},scales:{x:{grid:{display:!1}},y:{grid:{display:!1},beginAtZero:!0}}}})}function i(t){const e=document.querySelector("#amountsSummary tbody");e.innerHTML=t.map(a=>`
        <tr>
            <td>${a.agency__name}</td>
            <td>${Number(a.total_amount).toLocaleString()}</td>
            <td><span class="badge bg-secondary">${a.agency_currency}</span></td>
        </tr>
    `).join("")}document.getElementById("filterForm").addEventListener("submit",t=>{t.preventDefault(),o()});o();
