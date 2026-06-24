// https://randomnerdtutorials.com/esp32-useful-wi-fi-functions-arduino/
#include <esp_now.h>
#include <WiFi.h>
#include <WebServer.h>
#include "WEBPAGE.h"


// Create AsyncWebServer object on port 80
WebServer server(80);

// [TCP-IP ADDITION] Dedicated TCP server for plain text servo commands.
WiFiServer tcpServer(5000);
WiFiClient tcpClient;
String tcpRxLine = "";
unsigned long tcpLastActivityMs = 0;
const unsigned long TCP_CLIENT_TIMEOUT_MS = 30000;


// select the ID of active servo.
void activeID(int cmdInput){
  activeNumInList += cmdInput;
  if(activeNumInList >= searchNum){
    activeNumInList = 0;
  }
  else if(activeNumInList < 0){
    activeNumInList = searchNum;
  }
}


void activeSpeed(int cmdInput){
  activeServoSpeed += cmdInput;
  if (activeServoSpeed > ServoMaxSpeed){
    activeServoSpeed = ServoMaxSpeed;
  }
  else if(activeServoSpeed < 0){
    activeServoSpeed = 0;
  }
}


int rangeCtrl(int rawInput, int minInput, int maxInput){
  if(rawInput > maxInput){
    return maxInput;
  }
  else if(rawInput < minInput){
    return minInput;
  }
  else{
    return rawInput;
  }
}


void activeCtrl(int cmdInput){
  switch(cmdInput){
    case 1:st.WritePosEx(listID[activeNumInList], ServoDigitalMiddle, activeServoSpeed, ServoInitACC);break;
    case 2:
      if(modeRead[listID[activeNumInList]] == 0) {
        servoStop(listID[activeNumInList]);
      }
      else if(modeRead[listID[activeNumInList]] == 3){
        st.WritePos(listID[activeNumInList], 0, 0, 0);
      }
      break;
    case 3:servoTorque(listID[activeNumInList],0);Torque_List[activeNumInList] = false;break;
    case 4:servoTorque(listID[activeNumInList],1);Torque_List[activeNumInList] = true;break;
    case 5:
      if(modeRead[listID[activeNumInList]] == 0){
        if(SERVO_TYPE_SELECT == 1){
          st.WritePosEx(listID[activeNumInList], ServoDigitalRange - 1, activeServoSpeed, ServoInitACC);
        }
        else if(SERVO_TYPE_SELECT == 2){
          st.WritePosEx(listID[activeNumInList], ServoDigitalRange - MAX_MIN_OFFSET, activeServoSpeed, ServoInitACC);
        }
      }


      else if(modeRead[listID[activeNumInList]] == 3){
        if(SERVO_TYPE_SELECT == 1){
          st.WritePosEx(listID[activeNumInList], 10000, activeServoSpeed, ServoInitACC);
        }
        else if(SERVO_TYPE_SELECT == 2){
          st.WritePos(listID[activeNumInList], 0, rangeCtrl(activeServoSpeed,200,999), 0);
        }
      }
      break;
    case 6:
      if(modeRead[listID[activeNumInList]] == 0){
        if(SERVO_TYPE_SELECT == 1){
          st.WritePosEx(listID[activeNumInList], 0, activeServoSpeed, ServoInitACC);
        }
        else if(SERVO_TYPE_SELECT == 2){
          st.WritePosEx(listID[activeNumInList], MAX_MIN_OFFSET, activeServoSpeed, ServoInitACC);
        }
      }


      else if(modeRead[listID[activeNumInList]] == 3){
        if(SERVO_TYPE_SELECT == 1){
          st.WritePosEx(listID[activeNumInList], -10000, activeServoSpeed, ServoInitACC);
        }
        else if(SERVO_TYPE_SELECT == 2){
          st.WritePos(listID[activeNumInList], 0, rangeCtrl(activeServoSpeed,200,999)+1024, 0);
        }
      }
      break;
    case 7:activeSpeed(100);break;
    case 8:activeSpeed(-100);break;
    case 9:servotoSet += 1;if(servotoSet > 250){servotoSet = 0;}break;
    case 10:servotoSet -= 1;if(servotoSet < 0){servotoSet = 0;}break;
    case 11:setMiddle(listID[activeNumInList]);break;
    case 12:setMode(listID[activeNumInList], 0);break;
    case 13:setMode(listID[activeNumInList], 3);break;
    case 14:SERIAL_FORWARDING = true;break;
    case 15:SERIAL_FORWARDING = false;break;
    case 16:setID(listID[activeNumInList], servotoSet);break;

    case 17:DEV_ROLE = 0;break;
    case 18:DEV_ROLE = 1;break;
    case 19:DEV_ROLE = 2;break;

    case 20:RAINBOW_STATUS = 1;break;
    case 21:RAINBOW_STATUS = 0;break;
  }
}


void handleRoot() {
 server.send(200, "text/html", index_html); //Send web page
}


void handleID() {
  if(!searchedStatus && searchFinished){
    String IDmessage = "ID:";
    for(int i = 0; i< searchNum; i++){
      IDmessage += String(listID[i]) + " ";
    }
    server.send(200, "text/plane", IDmessage);
  }
  else if(searchedStatus){
    String IDmessage = "Searching...";
    server.send(200, "text/plane", IDmessage);
  }
}


void handleSTS() {
  String stsValue = "Active ID:" + String(listID[activeNumInList]);
  if(voltageRead[listID[activeNumInList]] != -1){
    stsValue += "  Position:" + String(posRead[listID[activeNumInList]]);
    if(DEV_ROLE == 0){
      stsValue += "<p>Device Mode: Normal";
    }
    else if(DEV_ROLE == 1){
      stsValue += "<p>Device Mode: Leader";
    }
    else if(DEV_ROLE == 2){
      stsValue += "<p>Device Mode: Follower";
    }
    stsValue += "<p>Voltage:" + String(float(voltageRead[listID[activeNumInList]])/10);
    stsValue += "  Load:" + String(loadRead[listID[activeNumInList]]);
    stsValue += "<p>Speed:" + String(speedRead[listID[activeNumInList]]);

    stsValue += "  Temper:" + String(temperRead[listID[activeNumInList]]);
    stsValue += "<p>Speed Set:" + String(activeServoSpeed);
    stsValue += "<p>ID to Set:" + String(servotoSet);
    stsValue += "<p>Mode:";
    if(modeRead[listID[activeNumInList]] == 0){
      stsValue += "Servo Mode";
    }
    else if(modeRead[listID[activeNumInList]] == 3){
      stsValue += "Motor Mode";
    }

    if(Torque_List[activeNumInList]){
      stsValue += "<p>Torque On";
    }
    else{
      stsValue += "<p>Torque Off";
    }
  }
  else{
    stsValue += " FeedBack err";
  }
  server.send(200, "text/plane", stsValue); //Send ADC value only to client ajax request
}


// [TCP-IP ADDITION] Build a compact status line for TCP clients.
String buildTcpStatusLine() {
  if (!searchNum) {
    return "ERR no servo detected";
  }

  int activeIDNum = listID[activeNumInList];
  String out = "ID=" + String(activeIDNum);
  out += " POS=" + String(posRead[activeIDNum]);
  out += " SPD=" + String(speedRead[activeIDNum]);
  out += " LOAD=" + String(loadRead[activeIDNum]);
  out += " V=" + String(float(voltageRead[activeIDNum]) / 10.0f, 1);
  out += " T=" + String(temperRead[activeIDNum]);
  return out;
}


// [TCP-IP ADDITION] Parse one text command and execute matching servo action.
void tcpHandleCommand(String cmdLine, WiFiClient &client) {
  cmdLine.trim();
  cmdLine.toUpperCase();

  if (cmdLine.length() == 0) {
    client.println("ERR empty command");
    return;
  }

  if (cmdLine == "PING") {
    client.println("PONG");
    return;
  }

  if (cmdLine == "GET STS") {
    client.println(buildTcpStatusLine());
    return;
  }

  if (cmdLine == "SEARCH") {
    searchCmd = true;
    client.println("OK SEARCH");
    return;
  }

  int cmdNum = -1;
  if (sscanf(cmdLine.c_str(), "CMD %d", &cmdNum) == 1) {
    activeCtrl(cmdNum);
    client.println("OK CMD");
    return;
  }

  int servoID = -1;
  int servoPos = -1;
  int servoSpeed = -1;
  if (sscanf(cmdLine.c_str(), "SET POS %d %d %d", &servoID, &servoPos, &servoSpeed) == 3) {
    int clampedID = rangeCtrl(servoID, 0, MAX_ID);
    int clampedPos = rangeCtrl(servoPos, 0, (int)(ServoDigitalRange - 1));
    int clampedSpeed = rangeCtrl(abs(servoSpeed), 0, ServoMaxSpeed);
    st.WritePosEx(clampedID, clampedPos, clampedSpeed, ServoInitACC);
    client.println("OK SET POS");
    return;
  }

  client.println("ERR unknown command");
}


// [TCP-IP ADDITION] Accept clients and process line-based commands over TCP.
void tcpServerLoop() {
  if (!tcpClient || !tcpClient.connected()) {
    WiFiClient incoming = tcpServer.available();
    if (incoming) {
      tcpClient = incoming;
      tcpRxLine = "";
      tcpLastActivityMs = millis();
      tcpClient.println("OK TCP SERVO SERVER READY");
      Serial.println("TCP client connected.");
    }
    return;
  }

  while (tcpClient.available()) {
    char c = (char)tcpClient.read();
    tcpLastActivityMs = millis();

    if (c == '\r') {
      continue;
    }

    if (c == '\n') {
      if (tcpRxLine.length() > 0) {
        tcpHandleCommand(tcpRxLine, tcpClient);
        tcpRxLine = "";
      }
      continue;
    }

    if (tcpRxLine.length() < 120) {
      tcpRxLine += c;
    } else {
      tcpRxLine = "";
      tcpClient.println("ERR line too long");
    }
  }

  if ((millis() - tcpLastActivityMs) > TCP_CLIENT_TIMEOUT_MS) {
    tcpClient.println("ERR timeout");
    tcpClient.stop();
    tcpRxLine = "";
    Serial.println("TCP client timeout.");
  }
}


// [TCP-IP ADDITION] Start TCP server once network stack is initialized.
void tcpServerSetup() {
  tcpServer.begin();
  tcpServer.setNoDelay(true);
  Serial.println("TCP server started on port 5000.");
}


void webCtrlServer(){
    server.on("/", handleRoot);
    server.on("/readID", handleID);
    server.on("/readSTS", handleSTS);

    server.on("/cmd", [](){
    int cmdT = server.arg(0).toInt();
    int cmdI = server.arg(1).toInt();
    int cmdA = server.arg(2).toInt();
    int cmdB = server.arg(3).toInt();

    switch(cmdT){
      case 0:activeID(cmdI);break;
      case 1:activeCtrl(cmdI);break;
      case 9:searchCmd = true;break;
    }
  });

  // Start server
  server.begin();
  Serial.println("Server Starts.");
}


void webServerSetup(){
  webCtrlServer();
  // [TCP-IP ADDITION] Keep HTTP and TCP interfaces active in parallel.
  tcpServerSetup();
}


void getMAC(){
  WiFi.mode(WIFI_AP_STA);
  MAC_ADDRESS = WiFi.macAddress();
  Serial.print("MAC:");
  Serial.println(WiFi.macAddress());
}


void getIP(){
  IP_ADDRESS = WiFi.localIP();
}


void setAP(){
  WiFi.softAP(AP_SSID, AP_PWD);
  IPAddress myIP = WiFi.softAPIP();
  IP_ADDRESS = myIP;
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  WIFI_MODE = 1;
}


void setSTA(){
  WIFI_MODE = 3;
  WiFi.begin(STA_SSID, STA_PWD);
}


void getWifiStatus(){
  if(WiFi.status() == WL_CONNECTED){
    WIFI_MODE = 2;
    getIP();
    WIFI_RSSI = WiFi.RSSI();
  }
  else if(WiFi.status() == WL_CONNECTION_LOST && DEFAULT_WIFI_MODE == 2){
    WIFI_MODE = 3;
    // WiFi.disconnect();
    WiFi.reconnect();
  }
}


void wifiInit(){
  DEV_ROLE  = DEFAULT_ROLE;
  WIFI_MODE = DEFAULT_WIFI_MODE;
  if(WIFI_MODE == 1){setAP();}
  else if(WIFI_MODE == 2){setSTA();}
}


void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}


void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  if(DEV_ROLE == 2){
    memcpy(&myData, incomingData, sizeof(myData));
    myData.Spd_send = abs(myData.Spd_send);
    if(myData.Spd_send < 50){
      myData.Spd_send = 200;
    }
    st.WritePosEx(myData.ID_send, myData.POS_send, abs(myData.Spd_send), 0);

    Serial.print("Bytes received: ");
    Serial.println(len);
    Serial.print("POS: ");
    Serial.println(myData.POS_send);
    Serial.print("SPEED: ");
    Serial.println(abs(myData.Spd_send));
  }
}


void espNowInit(){
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Once ESPNow is successfully Init, we will register for Send CB to
  // get the status of Trasnmitted packet
  esp_now_register_send_cb(OnDataSent);
  esp_now_register_recv_cb(OnDataRecv);

  // Register peer
  esp_now_peer_info_t peerInfo={};
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Add peer        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }

  MAC_ADDRESS = WiFi.macAddress();
  Serial.print("MAC:");
  Serial.println(WiFi.macAddress());
}