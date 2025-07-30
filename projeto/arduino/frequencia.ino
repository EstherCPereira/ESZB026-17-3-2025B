long x;
long delta;
float fs;




// the setup routine runs once when you press reset :
void setup () {
// initialize serial communication at 9600 bits per second :
Serial.begin (9600) ;
}
// the loop routine runs over and over again forever :
void loop() {


delta = millis() - x; //ms -> delta da taxa de aquisição
x = millis(); //ms -> taxa de aquisição


// read the input on analog pin 0:
float sensorValue = analogRead(A0)*5.0/1023.0;
// print out the value you read :
//Serial.println(sensorValue);
delay(27) ; // delay in between reads for stability (ms)


fs = 1.0/(delta/1000.0); //Hz --> divide por 1000 para ir de ms para segundos. fs = x^-1, ou seja o inverso do período, a frequência
Serial.println(fs); //queremos saber a taxa de aquisição de dados, pois sem ela não conseguimos verificar a frequência --> delta t = 1/fs


}

