const int analogInPin = A0; // Potenciômetro ligado ao pino A0

void setup() {
Serial.begin(115200); // Comunicação serial a 115200 baud
}

void loop() {
  int valor = analogRead(analogInPin); // Leitura ADC 10 bits (0-1023)
  byte convertido = valor / 10.23;
  Serial.write(convertido);
  //Serial.print(valor);
  //Serial.print(" => ");
  //Serial.println(convertido);
  delay(100); // Envia a cada 100ms (10 vezes por segundo)
}
