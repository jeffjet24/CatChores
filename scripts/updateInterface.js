var millieNailsStatus = false;
var kittyXNailsStatus = false;

function updateComboKitty(){
  var status = "";
  if (millieNailsStatus && kittyXNailsStatus){
    status = "green";
  }else if(!millieNailsStatus && kittyXNailsStatus){
    status = "yellow";
  }else if(millieNailsStatus && !kittyXNailsStatus){
    status = "yellow";
  }else {
    status = "red";
  }
  const BASE_BUTTON_PANEL = "panel margin0";
  var statusCode = ""
  switch (status) {
    case "green":
      statusCode = "success";
      break;
    case "yellow":
      statusCode = "warning";
      break;
    case "red":
      statusCode = "danger";
      break;
    default:
      statusCode = "danger";
  }
  document.getElementById("ClipNails").className = BASE_BUTTON_PANEL + " panel-" + statusCode;
}


function updateFields(data){
  data.forEach(function(item){
    var status = item.status;
    var eventName = item.item.task;
    var userName = item.item.personName;
    var time = parseInt(item.item.time);
    switch (eventName) {
      case "MillieNails":
        millieNailsStatus = status == "green";
        console.log(millieNailsStatus);
        console.log(status == "green");
        break;
      case "KittyXNails":
        kittyXNailsStatus = status == "green";
        console.log(kittyXNailsStatus);
        console.log(status == "green");
        break;
    }
    updatePerformed(eventName, userName, time, status);
  });
}

function getUpdate(){
  var apigClient = apigClientFactory.newClient();
  var params = {};
  var body = {};
  var additionalParams = {};
  apigClient.statusUpdateGet(params, body, additionalParams)
      .then(function(result){
        var jsonResultString = result.data.body;
        var jsonResult = JSON.parse(jsonResultString);
        jsonResult = JSON.parse(jsonResult.Message);
        updateFields(jsonResult);
      }).catch( function(result){
        console.log(result);
      });
  updateComboKitty();
}

function runtimeFunc(){
  getUpdate();
  setInterval(getUpdate, 60000);
  // I should put more stuff here, just don't know what yet.
}
