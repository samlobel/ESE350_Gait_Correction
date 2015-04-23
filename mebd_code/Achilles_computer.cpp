#include "mbed.h"
#include "MRF24J40.h"
#include <string>

//in milliseconds
#define TRANSMIT_TIME 10000
#define RECEIVE_TIME 100000 



Serial pc(USBTX, USBRX);
Timer t;


MRF24J40 mrf(p11, p12, p13, p14, p21);
char txBuffer[128];
char rxBuffer[128];
int rxLen;


// int success;

// int received_state;

// float temp_data;
// char *ain_data = char[6];




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







int printPressureData(){
    rxLen = rf_receive(rxBuffer, 128);
    if (rxLen > 0){
        pc.printf("%s\n", rxBuffer); //prints the line
        return 1; //symbol of success
    }
    else{
        return 0;
    }
}





// int transmit(){
//     t.reset();
//     t.start();
//     while(t.read_ms() < TRANSMIT_TIME){
//         ainToBuffer(ain_data); //puts data into buffer
//         strcpy(txBuffer, ain_data);
//         rf_send(txBuffer, strlen(txBuffer) + 1)
//         // success = printPressureData();
//     }
// }


int receive(){
    t.reset();
    t.start();
    while(t.read_ms() < RECEIVE_TIME){
        printPressureData();
    }
}



int main() {
    // setup
    while(1){
        receive();
    }
    
}

