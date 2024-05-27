var backend = this;

backend.dev = false;

if(!backend.dev){
	backend.usuando = "216.238.66.208";
	//backend.usuando = "localhost"45.32.161.183";
}else{
	backend.usuando = "localhost";
	//backend.usuando = "localhost"45.32.160.1";
}

backend.conexionEnvio = function (datos,callback){
	if ("WebSocket" in window){

        if (!backend.dev) {
            var ws = new WebSocket("ws://" + backend.usuando + ":3000");
        } else {
            var ws = new WebSocket("ws://" + backend.usuando + ":3000");
        }

		ws.onopen = function(){
			$("#conectado_server")[0].innerText ="true";
			ws.send(datos);
		};
		ws.onmessage = function (evt) {
			ws.close();
			return callback(evt.data);
		};
		ws.onerror = function (evt) {
			 toastr.error('Error en la conexion de internet','System notification!');
			$("#conectado_server")[0].innerText ="false";
		};
		window.onbeforeunload = function(event) {
			ws.close();

		};
	}else{
	   return callback(JSON.stringify({"e":true,"m":"WebSocket NOT supported by your Browser"}));
	}
};

