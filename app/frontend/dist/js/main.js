let baseURL = 'https://www.bloodybrands.com';
let checkNameURL = baseURL + '/check/';
let checkImageURL = baseURL + '/check/image';

$('.search-button').on('click', function () {
    clearStatus();
    let searchValue = $(".search-input").val();
    let encodeSearch = utf8_to_b64(searchValue);
    fetch(checkNameURL + encodeSearch).then(respose => {
        return respose.json();
    }).then(resp => {
        checkStatus(resp.status);
    })
});

document.getElementById("img").onchange = function () {
    clearStatus();
    let form = document.getElementById('ImageCheckForm');
    let formData = new FormData(form);

    fetch(checkImageURL, {method: 'POST', body: formData})
        .then(response => response.json()).then(data => {
        let count = Object.keys(data).length;
        if (count === 1) {
            checkStatus(Object.values(data)[0]);
        } else if (count > 1) {
            let tbodyRef = document.getElementById('table-status').getElementsByTagName('tbody')[0];
            for (let i = 0; i < count; i++) {
                let newRow = tbodyRef.insertRow();

                let brand = Object.keys(data)[i];
                let status = Object.values(data)[i];

                if (status === "bloody") {
                    newRow.className = "table-danger";
                }

                let newCell = newRow.insertCell();
                let newText = document.createTextNode(brand);
                newCell.appendChild(newText);

                let newCell2 = newRow.insertCell();
                let newText2 = document.createTextNode(status);
                newCell2.appendChild(newText2);
            }
            $(".statusTable").show();
        } else {
            checkStatus("not found");
        }
    }).catch(error => {
        console.log(error);
    })
};

function checkStatus(checkStatus) {
    if (checkStatus === "clear") {
        $(".alert-success").show();
    } else if (checkStatus === "pressure") {
        $(".alert-warning").show();
    } else if (checkStatus === "bloody") {
        $(".alert-danger").show();
    } else if (checkStatus === "not found") {
        $(".alert-primary").show();
    }
}

function clearStatus() {
    $(".alert-warning").hide();
    $(".alert-danger").hide();
    $(".alert-success").hide();
    $(".alert-primary").hide();
    $(".statusTable").hide();
}

function utf8_to_b64(str) {
    return window.btoa(unescape(encodeURIComponent(str)));
}