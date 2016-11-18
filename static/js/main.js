function openTerminal(options) {
    var client = new WSSHClient();
    var term = new Terminal({cols: 80, rows: 24, screenKeys: true, useStyle:true});
    term.on('data', function (data) {
        client.sendClientData(data);
    });
    term.open();
    $('.terminal').detach().appendTo('#term');
    term.write('Connecting...');
    client.connect({
        onError: function (error) {
            term.write('Error: ' + error + '\r\n');
            console.debug('error happened');
        },
        onConnect: function () {
            client.sendInitData(options);
            client.sendClientData('\r');
            console.debug('connection established');
        },
        onClose: function () {
            term.write("\rconnection closed")
            console.debug('connection reset by peer');
        },
        onData: function (data) {
            term.write(data);
            console.debug('get data:' + data);
        }
    })
}
