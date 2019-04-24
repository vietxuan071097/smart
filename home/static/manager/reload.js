var chatSocket = new WebSocket('ws://' + window.location.host + '/ws/manager/');

chatSocket.onopen = function (event) {
        console.log('hello');
        chatSocket.send(JSON.stringify({
            'command': "fetch_messages",
        }));
    };

chatSocket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    var content = "";
    for (r in message) {
        content += "<tr>\n";
        content += "<td>"+message[r].id+"</td>\n";
        content += "<td>"+message[r].creation_date+"</td>\n";
        content += "<td><a href='../bill-detail/"+message[r].id+"'>Xem chi tiết</a></td>\n";
        content += "</tr>\n";
    }


    document.getElementById("table-content").innerHTML = content;

};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};