#include <DHT.h>

#define KYPIN A0          // analog pin where KY-037 sensor is connected
#define DHTPIN 2          // digital pin where DHT22 sensor is connected

DHT dht(DHTPIN, DHT22);   // initialize DHT22 object

float h;  // humidity
float t;  // temperature
int s;    // sound

void setup()
{
    Serial.begin(9600);
    dht.begin();
}

void loop()
{
    // sensors need some time to produce valid values
    delay(2000);

    // read values from sensors
    h = dht.readHumidity();
    t = dht.readTemperature();
    s = analogRead(KYPIN);

    // print "<humidity>,<temperature>,<sound>" (CSV-like)
    // all values are numbers
    if (!isnan(h) && !isnan(t) && !isnan(s)) {
        Serial.print(h);
        Serial.print(",");
        Serial.print(t);
        Serial.print(",");
        Serial.println(s);
    }
}
