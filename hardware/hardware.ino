//Includes
//Include WiFi
#include <WiFi.h>
#include <WiFiClient.h>
//Include LCD_I2C
#include <LiquidCrystal_I2C.h>
//Include RFID reader
#include <MFRC522.h>
//Include MQTT
#include <PubSubClient.h>

//Global Variables
//Config RfID ports
#define SS_PIN 17
#define RST_PIN 5

//Config Button and Locker ports
#define locker 2

//WiFi
const char* ssid     = "TDLR";
const char* password = "Thiago2001";

//MQTT
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
const char* MQTT_BROKER_IP_ADDRESS = "192.168.3.46";
const char* MQTTUSERNAME = "door_test";
const char* MQTTPWD = "n9tt-9g0a-b7fq-ranc";

//RFID
MFRC522 rfid(SS_PIN, RST_PIN); 
MFRC522::MIFARE_Key key;

//LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);


//Setup Functions
void mqttStartup(){
    // Configura o servidor MQTT e o cliente MQTT
    mqttClient.setServer(MQTT_BROKER_IP_ADDRESS, 1883);
    mqttClient.setCallback(mqttCallback);
    reconnect();
}

void wifiStartup(){
	Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
	}
}

void openDoor(String name){
	delay(1000);
	digitalWrite(locker,HIGH);
	delay(100);
	digitalWrite(locker,LOW);
}

void notOpenDoor(){

}

//MQTT
//Reconects to MQTT Server
void reconnect() {
	while (!mqttClient.connected()) {
		Serial.println("Tentando reconectar ao broker MQTT...");
		if (mqttClient.connect("ESP32Client", MQTTUSERNAME, MQTTPWD)) {		
			Serial.println("Reconectado ao broker MQTT!");
			mqttClient.subscribe("door/open");
		} else {
			Serial.print("Falha ao se reconectar ao broker MQTT com erro: ");
			Serial.println(mqttClient.state());
		}
	}
}

//MQTT Callback Function
void mqttCallback(char* topic, byte* payload, unsigned int length) {
	payload[length] = '\0';
	String message = (char*)payload;

	if(strcmp(topic, "door/open") == 0){
		if (length == 0)
		{
			notOpenDoor();
		}
		else{
			openDoor(message);
		}
	}
	

	Serial.print("Mensagem MQTT recebida no topico [");
	Serial.print(topic);
	Serial.print("]: ");
	Serial.println(message);
	Serial.println(length);
	Serial.println(message.length());
}

void setup(){
  	Serial.begin(115200);
	delay(10);

	pinMode(locker, OUTPUT);

	wifiStartup();
	mqttStartup();
	SPI.begin(); // Init SPI bus
    rfid.PCD_Init(); // Init MFRC522

}

void loop(){
	// Verifica se a conexão com o broker MQTT está ativa e reconecta-se, se necessário
	if (!mqttClient.connected()) {
	reconnect();
	}
	// Processa as mensagens MQTT recebidas
	mqttClient.loop();

	if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()){
        String cardUID;
        for (size_t i = 0; i < rfid.uid.size; i++)
        {
            cardUID.concat(String(rfid.uid.uidByte[i] < 0x10 ? "0" : ""));
            cardUID.concat(String(rfid.uid.uidByte[i], HEX));
        }
		Serial.println(cardUID);
		mqttClient.publish("server/auth", cardUID.c_str());
        rfid.PICC_HaltA();
    }
}
