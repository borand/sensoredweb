///////////////////////////////////////////
// Global variables

/////////////////////////////////////////////////////////////////////
// UTILITY FUNCTIONS
//
function dbg(message, show) {
	console.log(message);
};

function SendCmd(cmd, val) {
	return $.getJSON('/cmd/', "cmd=" + cmd + "&param=" + val, function(data) {			
		console.log(data);
	});
}

///////////////////////////////////////////////////////////////////////
// MAIN GUI - jQUERY
//
//
$(document).ready(function() {
	dbg('Insteon ready', true);
	$( "#lightbulb" ).on( 'slidestop', function( event ) { 
		var slider_value = $("#lightbulb").val();
		//dbg('Value : ' + slider_value, true);
		SendCmd('20.1f.11',slider_value);
	});
});
