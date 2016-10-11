function formatAMPM(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var strTime = hours + ':' + minutes + ' ' + ampm;
  return strTime;
}


function createAlert(success){
  var newBoxCon = document.createElement("div");
  if(success){
    newBoxCon.className = "alert alert-success alert-dismissible versionLabel";
  } else {
    newBoxCon.className = "alert alert-danger alert-dismissible versionLabel";
  }
  newBoxCon.setAttribute("role", "alert");
  newBoxCon.style.zIndex = 5;
  var newBoxBut = document.createElement("button");
  newBoxBut.setAttribute("type", "button");
  newBoxBut.className = "close";
  newBoxBut.setAttribute("data-dismiss", "alert");
  newBoxBut.setAttribute("aria-label", "Close");
  var newBoxSpan = document.createElement("span");
  newBoxSpan.setAttribute("aria-hidden", "true");
  newBoxSpan.innerHTML = "&times;";
  newBoxBut.appendChild(newBoxSpan);
  newBoxCon.appendChild(newBoxBut);
  if(success){
    newBoxCon.appendChild(document.createTextNode("Your Operation was Successfully Processed!"));
  } else {
    newBoxCon.appendChild(document.createTextNode("Your Operation has Failed"));
  }
  return newBoxCon;
}


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
          var newBox = createAlert(true);
          document.getElementById("alertBoxes").appendChild(newBox);
          updatePerformed(data.eventName, data.name, curTime, "green");
      }).catch( function(result){
          var newBox = createAlert(false);
          document.getElementById("alertBoxes").appendChild(newBox);
          updatePerformed(data.eventName, data.name, curTime, "green");
      });
}


function updatePerformed(eventName, userName, timePer, statusColor){
  // This function is going to update all the panels that are related and the performed section.
  const BASE_BUTTON_PANEL = "panel margin0";
  const BASE_BUTTON = "btn btn-sm";
  const DROPDOWN_BUTTON = "dropdown-toggle";
  const BASE_PER_PANEL = "panel margin0 performedPanel text-center";
  var statusCode = ""
  switch (statusColor) {
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


  var buttonPanel = eventName;
  var panelName = eventName + "PerPanel";
  var textName = eventName + "PerText";
  var time = new Date(timePer * 1000);

  // Setting the Button Panel Color
  if(buttonPanel != "MillieNails" && buttonPanel != "KittyXNails"){
    document.getElementById(buttonPanel).className = BASE_BUTTON_PANEL + " panel-" + statusCode;
  } else {
    var classString = BASE_BUTTON + " btn-" + statusCode;
    if(buttonPanel == "KittyXNails"){
      classString = classString + " " + DROPDOWN_BUTTON;
    }
    document.getElementById(buttonPanel).className = classString;
  }

  // Setting the Performed Panel Colors
  document.getElementById(panelName).className = BASE_PER_PANEL + " panel-" + statusCode;

  // Setting the Performed Panel Text
  var dateString = (time.getMonth() + 1).toString() + "/" + time.getDate().toString() + " " + formatAMPM(time);
  document.getElementById(textName).innerHTML = dateString + " By " + userName;
}
