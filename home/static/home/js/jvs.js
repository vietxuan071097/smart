function add_product(product_id, product_name) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            document.getElementById("count-items").innerHTML = ' ' + xmlHttp.responseText;
            alert("Đã thêm " + product_name + " vào giỏ hàng.");
        }
    }
    xmlHttp.open("GET", "/add-product/?product_id=" + product_id, true);
    xmlHttp.send(null);
}


function checked_change() {
    var data = document.querySelector('input[name="method"]:checked').value;
    if (data == 'table') {
        document.getElementById('chose-table').style.display = "block";
        document.getElementById('chose-address').style.display = "none";
    } else {
        document.getElementById('chose-table').style.display = "none";
        document.getElementById('chose-address').style.display = "block";
    }
    ;
};

function pay_checked() {
    var data = document.querySelector('input[name="pay"]:checked').value;
    if (data == 'money') {
        document.getElementById('chose-card').style.display = "none";
    } else {
        document.getElementById('chose-card').style.display = "block";
    }
    ;
};