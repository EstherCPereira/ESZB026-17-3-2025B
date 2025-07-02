#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>

#include <softPwm.h>



#define LED_PIN 23 // wiringPi pin 23 corresponde à GPIO23

// Função para configurar a serial (USB)
int configurarSerial(const char* porta) {
	int fd = open(porta, O_RDWR | O_NOCTTY | O_NDELAY);
	if (fd == -1) {
		perror("Erro abrir serial");
		return -1;
	}

	struct termios options;
	tcgetattr(fd, &options);
	cfsetispeed(&options, B115200);
	cfsetospeed(&options, B115200);
	options.c_cflag |= (CLOCAL | CREAD);
	options.c_cflag &= ~CSIZE;
	options.c_cflag |= CS8; // 8 bits de dados
	options.c_cflag &= ~PARENB; // Sem paridade
	options.c_cflag &= ~CSTOPB; // 1 stop bit
	options.c_cc[VMIN] = 0;
	options.c_cc[VTIME] = 10; // Timeout 1s

	tcsetattr(fd, TCSANOW, &options);
	return fd;
}

int main() {
	if (wiringPiSetupGpio() == -1) {
		printf("Erro ao inicializar wiringPi\n");
		return 1;
	}

	pinMode(LED_PIN, PWM_OUTPUT);
	int range = 100;
	
	softPwmCreate(LED_PIN, 0, range);

	int serialFd = configurarSerial("/dev/ttyACM0"); 

	while(1) {
		char c;
		int n = read(serialFd, &c, 1);
		if (n > 0) {
			softPwmWrite(LED_PIN, c);
	/*		if (1==0){
				if (c == '\n' || c == '\r') {
					buffer[index] = '\0';
					// Converte string do valor do potenciômetro para inteiro
					valorPot = atoi(buffer);
					if (valorPot < 0) valorPot = 0;
					if (valorPot > 1023) valorPot = 1023;

					// Ajusta escala (0-1023) para PWM range (0-1023)
					pwmWrite(LED_PIN, valorPot);

					printf("Potenciometro: %d -> PWM: %d\n", valorPot, valorPot);

					index = 0; // Reseta o buffer
				} else {
					if (index < (int)sizeof(buffer) - 1) {
						buffer[index++] = c;
					}
				}
			}*/
		}
		delay(10); // Para não usar CPU demais
	}

	close(serialFd);
	return 0;
} 

