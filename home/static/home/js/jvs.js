function add_button(product_id, product_name) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            document.getElementById("count-items").innerHTML = ' ' + xmlHttp.responseText;
            alert("Đã thêm " + product_name + " vào giỏ hàng.");
        }
    }
    xmlHttp.open("GET", "/add/?product_id=" + product_id, true);
    xmlHttp.send(null);
}

function order() {
    var e = document.getElementById("table");
    var table = e.options[e.selectedIndex].value;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            alert(xmlHttp.responseText);
            window.location.href = "/";
        }
    }
    xmlHttp.open("GET", "/success/?table=" + table, true);
    xmlHttp.send(null);
}

function remove_product(product_id) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            window.location.href = "/cart/";
        }
    }
    xmlHttp.open("GET", "/remove/?product_id=" + product_id, true);
    xmlHttp.send(null);
}