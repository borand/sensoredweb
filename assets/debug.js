///////////////////////////////////////////
// Global variables
var active_tab;
var debug_websocket = true;
var debug_js = true;
var debug_all = true;

var ws;
/////////////////////////////////////////////////////////////////////
// UTILITY FUNCTIONS
//
function dbg(message, show) {	
	show_server_msg(message, show);	
}

function SendCmd(cmd, val) {
	return $.getJSON('/cmd/', "cmd=" + cmd + "&param=" + val, function(data) {			
		$("#cmd_status").text(data.cmd);
	});
}

function show_server_msg(message, show) {	
	if (show)
	{	
		console.log(message);
		//$("#console").html( $("#console").text() + message + '\n');					
	    //var psconsole = $('#console');
	    //psconsole.scrollTop(psconsole[0].scrollHeight - psconsole.height());
	}
}

function console_response_msg(message, show) {
	if(show){
		dbg(message,true);
		selected_chan = $("#select-chan").val();
		chan = message['FROM'];
		console.log(message['MSG'])
		//$("#console").html($("#console").text() + chan + "> " + "cmd [" + message['MSG'][1] + "]: " + message['MSG'][2].data + '\n');
		if (selected_chan === chan || selected_chan == 'All')
		{
			$("#console").html($("#console").text() + chan + "> " + JSON.stringify(message['MSG']['data']) + '\n');
			var psconsole = $('#console');
			psconsole.scrollTop(psconsole[0].scrollHeight - psconsole.height());
		}
	}
}

function console_response_text(message, show) {
	if(show){
		dbg(message,true);		
		console.log(message);
		$("#console").html($("#console").text() + "> " + message + '\n');
		var psconsole = $('#console');
		psconsole.scrollTop(psconsole[0].scrollHeight - psconsole.height());		
	}
}

function set_object_value(id, val){
	var datarole = $("#"+id).attr('data-role');
	dbg('id:' + id + " data-role: " + datarole + "  val: " + val, true);
	switch(datarole){
		case 'slider':
			dbg('case: slider', true);
			$('#' + id).val(val).slider("refresh");
			break;
		case 'flipswitch':			
			dbg('about to flip the switch value to:' + val + ' currently set to: ' + $('#' + id).val(), true);
			$('#' + id).val(val).flipswitch("refresh");
			break;
		case 'text':
			$('#' + id).text(val);
			break
		default:
			dbg('case: default', true);
			$('#' + id).val(val)[datarole]("refresh");
	}
}

function parse_message(message_text){
	var temp;
}
///////////////////////////////////////////////////////////////////////
// WEBSOCKETS FUNCTIONS
//MessageHandler
//
function open_websocket(hostname, hostport, hosturl) {

	dbg('Attempting to open web socket',true);
	function show_message(message) {
		show_server_msg(message);		
	}

	var websocket_address = "ws://" + hostname + ":" + hostport + "/" + hosturl;
	ws = new WebSocket(websocket_address);
	
	ws.onopen = function() {
		debug_websocket = $('#debug_websocket').prop("checked");
		dbg('web socket open', debug_websocket);
		$('#live').text('CONNECTED');
		$("#live").css("background-color",'#B2BB1E');
	};

	ws.onmessage = function(event) {
		debug_websocket = $('#debug_websocket').prop("checked");
		dbg('incomming message', debug_websocket);
		server_message_handler(event.data);
	};
	ws.onclose = function() {
		debug_websocket = $('#debug_websocket').prop("checked");
		dbg('closing websockets', debug_websocket);
		$('#live').text('OFFLINE');
		$("#live").css("background-color",'#FF0000');
	};
}

function server_message_handler(data){
	var JsonData;	
	if( $("#hosturl").val() == 'sub')
	{
		console_response_text(data, true);
	}
	else{

	try {
		JsonData = JSON.parse(data);
	} catch(e) {
		dbg('JSON.parse error: "' + e + '". JsonData = ' + JsonData);
		return;

	}
	//console.log(JsonData)
	console_response_msg(JsonData, true);
	
	if (JsonData.hasOwnProperty('id')) {		
		switch(JsonData.id)
		{
			case 'console':
			{	
				;
			}
			default:
			{	
				set_object_value(JsonData.id, JsonData.val);
			}
		}

	}
}
}

function connect_to_websocket_host(){
	var hostname = $('#hostname').val();
	var hostport = $('#hostport').val();
	var hosturl  = $('#hosturl').val();
	dbg('Pressed button: button_connect: [host, port] ' + hostname +':' + hostport + "/websocket/" + hosturl, true);
	open_websocket(hostname, hostport, "websocket/" + hosturl);
}
///////////////////////////////////////////////////////////////////////
// MAIN GUI - jQUERY
//
//
$(document).ready(function() {
	console.log("ready");
	dbg('Document ready', true);

	// debug_websocket = $('#debug_websocket').prop("checked");
	// debug_js        = $('#debug_js').prop("checked");
	// debug_all       = $('#debug_all').prop("checked");
	
	$( "#radio-websocket-online" ).prop( "checked", false ).checkboxradio( "refresh" );
	
	$('#console').attr('style', 'background-color:White; font-size:14px; height: 20em;');
	$('#console').textinput("option", "autogrow", false);

	$('#console').attr('style', 'background-color:White; font-size:14px; height: 20em;');
	$('#console').textinput("option", "autogrow", false);	
		
	$('#server_msg').textinput("option", "autogrow", false);
	$("#live").css("background-color",'#C71C2C');
	
	connect_to_websocket_host();
	
	///////////////////////////////////////////////////////////////////////

	///////////////////////////////////////////////////////////////////////
	//
	// BUTTONS
	//

	$("#button_connect").click(function() {	
		connect_to_websocket_host();
	});


	$("#button_disconnect").click(function() {	
		ws.close();
	});

	$("#button_clear_debug_console").click(function() {
		$("#debug_console").text("");
	});

	$("#options_ping").click(function() {		
		SendCmd('ping', 0);
		$("#cmd_status").text("Pressed options_ping button");
	});

});
