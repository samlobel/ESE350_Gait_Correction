#include "mbed.h"
#include "MRF24J40.h"
#include <string>

//in milliseconds
#define TRANSMIT_TIME 4500
#define RECEIVE_TIME 500 



AnalogIn   ain0(A0);
AnalogIn   ain1(A1);
AnalogIn   ain2(A2);
AnalogIn   ain3(A3);
AnalogIn   ain4(A4);


DigitalOut led1(LED1);
DigitalOut led2(LED2);
DigitalOut led3(LED3);
DigitalOut led4(LED4);

DigitalOut pinOne(p7);
DigitalOut pinTwo(p8);
DigitalOut enable(p6);




Serial pc(USBTX, USBRX);
Timer t;


MRF24J40 mrf(p11, p12, p13, p14, p21);
char txBuffer[128];
char rxBuffer[128];
int rxLen;


char state;


int success;

int received_state;



float temp_data;
char ain_data[6];



void makeUpFootDown(char *dataBuffer){
    dataBuffer[0] = 71;
    dataBuffer[1]  = 72;
    dataBuffer[2] = 4;
    dataBuffer[3] = 73;
    dataBuffer[4] = 75;
}

void makeUpFootUp(char *dataBuffer){
    dataBuffer[0] = 4;
    dataBuffer[1]  = 3;
    dataBuffer[2] = 6;
    dataBuffer[3] = 8;
    dataBuffer[4] = 9;
}


void makeUpFootDownTwo(char *dataBuffer){
    dataBuffer[0] = 2;
    dataBuffer[1]  = 80;
    dataBuffer[2] = 4;
    dataBuffer[3] = 81;
    dataBuffer[4] = 79;
}


void makeUpReading(char *dataBuffer, int i){
    if (i % 100 < 20){
        makeUpFootDown(dataBuffer);
    }
    else if(i % 100 < 40){
        makeUpFootDownTwo(dataBuffer);
    }
    else if (i % 100 < 60){
        makeUpFootDown(dataBuffer);
    }
    else if(i % 100 < 80){
        makeUpFootDownTwo(dataBuffer);
    }
    else{
        makeUpFootUp(dataBuffer);
    }
}


void ainToBuffer(char *dataBuffer){
    // if this works, it'll copy 100 times the float value of read into the array (as a char).
    // The plus one is so that it'll never be the zero character (which would end the string).
    dataBuffer[0] = int (ain0.read() * 100) + 1;
    dataBuffer[1]  = int (ain1.read() * 100) + 1;
    dataBuffer[2] = int (ain2.read() * 100) + 1;
    dataBuffer[3] = int (ain3.read() * 100) + 1;
    dataBuffer[4] = int (ain4.read() * 100) + 1;
}


int rf_receive(char *data, uint8_t maxLength)
{
    uint8_t len = mrf.Receive((uint8_t *)data, maxLength);
    uint8_t header[8]= {1, 8, 0, 0xA1, 0xB2, 0xC3, 0xD4, 0x00};

    if(len > 10) {
        //Remove the header and footer of the message
        for(uint8_t i = 0; i < len-2; i++) {
            if(i<8) {
                //Make sure our header is valid first
                if(data[i] != header[i])
                    return 0;
            } else {
                data[i-8] = data[i];
            }
        }

        //pc.printf("Received: %s length:%d\r\n", data, ((int)len)-10);
    }
    return ((int)len)-10;
}


void rf_send(char *data, uint8_t len)
{
    //We need to prepend the message with a valid ZigBee header
    uint8_t header[8]= {1, 8, 0, 0xA1, 0xB2, 0xC3, 0xD4, 0x00};
    uint8_t *send_buf = (uint8_t *) malloc( sizeof(uint8_t) * (len+8) );

    for(uint8_t i = 0; i < len+8; i++) {
        //prepend the 8-byte header
        send_buf[i] = (i<8) ? header[i] : data[i-8];
    }
    //pc.printf("Sent: %s\r\n", send_buf+8);

    mrf.Send(send_buf, len+8);
    free(send_buf);
}







// THIS WAS SUPPOSED TO BE FOR THE COMPUTER
// int printPressureData(){
//     rxLen = rf_receive(rxBuffer, 128);
//     if (rxLen > 0){
//         pc.printf("%s\n", rxBuffer); //prints the line
//         return 1; //symbol of success
//     }
//     else{
//         return 0;
//     }
// }





int transmit(){
    t.reset();
    t.start();
    int i = 0;
    while(t.read_ms() < TRANSMIT_TIME){
        wait(0.005);
        ainToBuffer(ain_data); //puts data into buffer

        // makeUpReading(ain_data, i);
        i++;
        strcpy(txBuffer, ain_data);
        rf_send(txBuffer, strlen(txBuffer) + 1);
        // success = printPressureData();
    }
    return 1;
}


void hBridgeCW(){
    pinOne = 1;
    pinTwo = 0;
    wait(1);

}

void hBridgeCCW(){
    pinOne = 1;
    pinTwo = 0;
    wait(1);

}

void hBridgeStop(){
    pinOne = 0;
    pinTwo = 0;
}


int receive(){
    t.reset();
    t.start();
    led4 = 1;
    while(t.read_ms() < RECEIVE_TIME){
        rxLen = rf_receive(rxBuffer, 128);
        wait(0.3);
        if(rxLen > 0){
            led4 = 0; 
            state = rxBuffer[0];
            if(state == '0'){
                led1 = 1;
                led2 = 0;
                led3 = 0;   
                hBridgeCW(); 
            }
            else if(state == '1'){
                led1 = 0;
                led2 = 1;
                led3 = 0;
                hBridgeCCW();  
            }
            else if(state == '2'){
                hBridgeStop();
                led1 = 0;
                led2 = 0;
                led3 = 1;    
            } else{
                led1 = 1;
                led2 = 1;
                led3 = 1;    
            }
            // pc.printf("%s\n", rxBuffer);
            break;
        }
    }
    led4 = 0;
    hBridgeStop();
    return 1;
}



int main() {
    // setup
    state = '\0';
    ain_data[5] = '\0'; //so it knows its a string. NEVER WRITE OVER THIS.
    hBridgeStop();
    while(1){
        // led4 = 1;
        // wait(0.2);
        // led4 = 0;

        transmit();
        // led4 = 1;
        // wait(0.2);
        // led4 = 0;

        receive();
    }
    
}
