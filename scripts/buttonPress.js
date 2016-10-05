function sendEvent(data) {
  // Data Shape: {name, eventName}
  var XHR = new XMLHttpRequest();
  var urlEncodedData = "";
  var urlEncodedDataPairs = [];
  var name;
  var curTime = new Date().getTime() / 1000;
  var dataMessage = {"event": data.eventName, "name": data.name, "time": curTime};

  // We turn the data object into an array of URL encoded key value pairs.
  for(name in dataMessage) {
    urlEncodedDataPairs.push(encodeURIComponent(name) + '=' + encodeURIComponent(dataMessage[name]));
  }

  // We combine the pairs into a single string and replace all encoded spaces to
  // the plus character to match the behaviour of the web browser form submit.
  urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');

  // We define what will happen if the data is successfully sent
  XHR.addEventListener('load', function(event) {
    alert('Event Sent Successfully. :) ');
  });

  // We define what will happen in case of error
  XHR.addEventListener('error', function(event) {
    alert('The Request Did not get sent correctly. :( ');
  });

  // We setup our request
  XHR.open('POST', 'https://5vsoxh69gj.execute-api.us-east-1.amazonaws.com/v1/cat-event');

  // We add the required HTTP header to handle a form data POST request
  XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  //XHR.setRequestHeader('Content-Length', urlEncodedData.length);
  XHR.setRequestHeader('Access-Control-Allow-Origin', '*');
  // And finally, We send our data.
  XHR.send(urlEncodedData);
}



function updatePerformed(eventName, userName, timePer){
  // This function is going to update all the panels that are related and the performed section.


}
