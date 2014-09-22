///////////////////////////////////////////
// Global variables
var active_tab;
var debug_websocket = false;
var debug_js = true;
var debug_all = true;

var ws;
////////////////////////////////////////
// Chart and plot variables
var plot_height = 450;
var chart;
var plot;
/////////////////////////////////////////////////////////////////////
// UTILITY FUNCTIONS
//
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
		$("#debug_console").html( $("#debug_console").text() + message + '\n');					
	    var psconsole = $('#debug_console');
	    psconsole.scrollTop(psconsole[0].scrollHeight - psconsole.height());
	}
}

function console_response_msg(message, show) {
	if(show){
		dbg(message,true);
		chan = message['FROM'];
		console.log(message['MSG'])
		//$("#json_res").html($("#json_res").text() + chan + "> " + "cmd [" + message['MSG'][1] + "]: " + message['MSG'][2].data + '\n');
		$("#json_res").html($("#json_res").text() + chan + "> " + JSON.stringify(message['MSG']) + '\n');
		var psconsole = $('#json_res');
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

///////////////////////////////////////////////////////////////////////
// HIGHCHARTS
//
//
function empty_data() {
	var data = [], time = (new Date()).getTime(), i;
	for( i = -999; i <= 0; i++) {
		data.push([
			time + i * 1000,
			0.0
			]);
	}
	return data;
};

function draw_chart(data) {
	
	render_to = 'chart'

	Highcharts.setOptions({
		global : {
			useUTC : false
		}
	});
	
	// Create the chart
	chart = new Highcharts.StockChart({
		chart : {
			renderTo : render_to,
			height : plot_height,			
		},
		
		rangeSelector: {
			buttons: [{
				count: 1,
				type: 'minute',
				text: '1M'
			}, {
				count: 5,
				type: 'minute',
				text: '5M'
			}, {
				type: 'all',
				text: 'All'
			}],
			inputEnabled: true,
			selected: 0
		},		
		title : {
			text : 'Timeseries Data'
		},
		
		exporting: {
			enabled: false
		},
		
		legend : {
			enabled: true
		},
		
		yAxis : {
			title : {
				text : 'VAL'
			},
			//max : 100,
			//min : 0,
		},
		
		series : [{
			name : 'Data 0',
			color: '#00FF00',
			step: true,
			data : data,
		}]
	});
}

function draw_plot(data) {
	plot = new Highcharts.Chart({
		chart : {
			renderTo : 'chart',
			//defaultSeriesType : 'line',
			zoomType : 'xy'
		},
		title : {
			text : 'Data'
		},
		subtitle : {
			text : ' '
		},
		xAxis : {
			title : {
				enabled : true,
				text : 'Time'
			},
			type: 'datetime',
			startOnTick : true,
			endOnTick : true,
			showLastLabel : true
		},
		yAxis : {
			title : {
				text : 'Value'
			}			
		},
		tooltip : {
			formatter : function() {
				return '' + this.x + ' ' + this.y + ' ';
			}
		},
		plotOptions : {
			scatter : {
				marker : {
					radius : 2,
					states : {
						hover : {
							enabled : true,
							lineColor : 'rgb(100,100,100)'
						}
					}
				},
				states : {
					hover : {
						marker : {
							enabled : false
						}
					}
				}
			}
		},
		series : [{
			name : 'Sensor',
			color : 'rgba(223, 83, 83, .5)',
			data : data

		}]
	});
}

function add_measurement(value){
	
	var t = (new Date()).getTime();
	var num_of_series = chart.series.length;
	
	console.log('adding value to the plot :' + value);	

	for (i=0;i<value.length;i++){
		if (i >= num_of_series-1){
			chart.addSeries({name : 'Data[' + i + ']', data : empty_data()},false,false);
		}
		else{
			series = chart.series[i];		
			dbg('series.name = '+ series.name +', value[' + i +'] = ' + value[i],$('#debug_chart').prop("checked"));
			if(series.name != 'Navigator'){
				series.addPoint([t, value[i]], true, true);	
			}
		}
	}
}

function parse_message(message_text){
	var temp;
}
///////////////////////////////////////////////////////////////////////
// WEBSOCKETS FUNCTIONS
//
//
function open_websocket(hostname, hostport, hosturl) {

	dbg('Attempting to open web socket',true);
	function show_message(message) {
		show_server_msg(message);		
	}

	var websocket_address = "ws://" + hostname + ":" + hostport + "/websocket/" + hosturl;
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

	try {
		JsonData = JSON.parse(data);
	} catch(e) {
		dbg('JSON.parse error: "' + e + '". JsonData = ' + JsonData);
		return;

	}
	//console.log(JsonData)
	console_response_msg(JsonData, true);
	
	var sn_to_plot = $('#sn_to_plot').val();
	if (JsonData.hasOwnProperty('MSG')) {
				
				if (JsonData.MSG.hasOwnProperty('sn')){
					if (JsonData.MSG.sn === sn_to_plot){
						data = JsonData.MSG.data[0];
						console.log('adding value to the plot :' + data)
						add_measurement([data]);
					};
				};
				if (JsonData.MSG.cmd === 'irq_0'){
					//dbg(JsonData.data, $('#debug_irq').prop("checked"))
					//msg = JsonData.data[2].data;					
					//console_response_msg(JsonData.data, $('#debug_irq').prop("checked"));
					data = JsonData.MSG.data[1];
					power_W = Math.round(3600.0/((Math.pow(2,16)*data[1] + data[2])/16e6*1024));
					console.log(power_W);
					add_measurement([power_W]);
				}
	}
}

function connect_to_websocket_host(){
	var hostname = $('#hostname').val();
	var hostport = $('#hostport').val();
	var hosturl  = $('#hosturl').val();
	dbg('Pressed button: button_connect: [host, port] ' + hostname +':' + hostport + '/websocket/'+ hosturl, true);
	open_websocket(hostname, hostport, hosturl);
}
///////////////////////////////////////////////////////////////////////
// MAIN GUI - jQUERY
//
//
$(document).ready(function() {	
	var sn_value = $('#sn_value').val();	
	var data_url = '/sensordata/api/datavalue/sn/'+ sn_value +'/today/.json'
	console.log(data_url)	
	$.getJSON(data_url, function (data) {
		console.log(data);
		draw_chart(data);
	});

});
