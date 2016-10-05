function sendEvent(data) {
  //Data Shape: {name, eventName}
  var curTime = new Date().getTime() / 1000;
  var dataMessage = {"event": data.eventName, "name": data.name, "time": curTime};

  var apigClient = apigClientFactory.newClient();
  var params = {};
  var body = dataMessage;
  var additionalParams = {};
  apigClient.catEventPost(params, body, additionalParams)
      .then(function(result){
          //This is where you would put a success callback
          document.getElementById("successMessage").style.visibility = "visible";
          updatePerformed(data.eventName, data.name, curTime);
      }).catch( function(result){
          //This is where you would put an error callback
          //alert('The Request Did not get sent correctly. :( :' + result);
          document.getElementById("failMessage").style.visibility = "visible";
      });
}


function updatePerformed(eventName, userName, timePer){
  // This function is going to update all the panels that are related and the performed section.
  const BASE_BUTTON_PANEL = "panel margin0";
  const BASE_BUTTON = "btn btn-sm";
  const DROPDOWN_BUTTON = "dropdown-toggle";
  const BASE_PER_PANEL = "panel margin0 performedPanel text-center";
  var buttonPanel = eventName;
  var panelName = eventName + "PerPanel";
  var textName = eventName + "PerText";
  var time = new Date(timePer * 1000);

  // Setting the Button Panel Color
  if(buttonPanel != "MillieNails" && buttonPanel != "KittyXNails"){
    document.getElementById(buttonPanel).className = BASE_BUTTON_PANEL + " panel-success";
  } else {
    var classString = BASE_BUTTON + " btn-success";
    if(buttonPanel == "KittyXNails"){
      classString = classString + " " + DROPDOWN_BUTTON;
    }
    document.getElementById(buttonPanel).className = classString;
  }

  // Setting the Performed Panel Colors
  document.getElementById(panelName).className = BASE_PER_PANEL + " panel-success";

  // Setting the Performed Panel Text
  var dateString = time.getMonth().toString() + "/" + time.getDate().toString() + " " + time.getHours().toString() + ":" + time.getMinutes().toString();
  document.getElementById(textName).innerHTML = dateString + " By " + userName;
}
