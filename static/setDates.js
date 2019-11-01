// window.addEventListener("load", function() {
	var now = addDays(new  Date(), 1);
	
	var outStartField = document.getElementById("out_start");
    var outEndField = document.getElementById("out_end");
    var backStartField = document.getElementById("back_start");
    var backEndField = document.getElementById("back_end");

    var outOffsetHour = 3
    var backOffsetHour = 3
    
	outStartField.value = createDate(now);
    outEndField.value = createDate(addHours(now,outOffsetHour));
    
    backStartField.value = createDate(addDays(now,1));
    backEndField.value = createDate(addHours(addDays(now,1),3));
	
function createDate(date) {
    var utcString = date.toISOString().substring(0,19);
	var year = date.getFullYear();
	var month = date.getMonth() + 1;
	var day = date.getDate();
	var hour = date.getHours();
	var minute = date.getMinutes();
	var second = date.getSeconds();
var localDatetime = year + "-" +
    (month < 10 ? "0" + month.toString() : month) + "-" +
    (day < 10 ? "0" + day.toString() : day) + "T" +
    (hour < 10 ? "0" + hour.toString() : hour) + ":" +
    (minute < 10 ? "0" + minute.toString() : minute)
    //(second < 10 ? "0" + second.toString() :second)
    //utcString.substring(16,19);
    return localDatetime;
}

function addDays(date, days) {
  var result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

function addHours(date, h) {
  var result = new Date(date);
  result.setTime(result.getTime() + (h*60*60*1000));
  return result;
}
