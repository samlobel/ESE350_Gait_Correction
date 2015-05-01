#include "mbed.h"
#include "MRF24J40.h"
#include <string>

//in milliseconds
#define TRANSMIT_TIME 5000
#define RECEIVE_TIME 30000 



Serial pc(USBTX, USBRX);
Timer t;

DigitalOut led1(LED1);
DigitalOut led2(LED2);
DigitalOut led3(LED3);
DigitalOut led4(LED4);

 


MRF24J40 mrf(p11, p12, p13, p14, p21);
char txBuffer[128];
char rxBuffer[128];
int rxLen;
char mostRecent;
char tester;



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
        led4 = 1;
        wait(0.1);
        led4 = 0;
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


int transmit(){
    // led4 = 1;
    // wait(0.2);
    // led4 = 0;
    if(pc.readable()){
        // led4 = 1;

        //get most recent
        while(pc.readable()){
            tester = pc.getc();
            if(tester != '\0'){
                mostRecent = tester; //so end of line character isn't included
            }
        }
        txBuffer[0] = mostRecent;
        txBuffer[1] = '\0'; //that ends the string, only sends that little bit.
        // pc.putc(mostRecent);
        if(mostRecent == '\0'){
            led1 = 1;
            led2 = 1;
            led3 = 1;    
        }
        else if(mostRecent == '\n'){
            led1 = 1;
            led2 = 0;
            led3 = 1;    
        }
        else if(mostRecent == '0'){
            led1 = 1;
            led2 = 0;
            led3 = 0;    
        }
        else if(mostRecent == '1'){
            led1 = 0;
            led2 = 1;
            led3 = 0;    
        }
        else if(mostRecent == '2'){
            led1 = 0;
            led2 = 0;
            led3 = 1;    
        }
        else{
            led1 = 0;
            led2 = 1;
            led3 = 1;    
        }
        t.reset();
        t.start();
        
        while(t.read_ms() < TRANSMIT_TIME){
            //////////
            led4 = 1;
            wait(0.3);
            led4 = 0;
            rf_send(txBuffer, 2);
        }

    }
    return 0;
}


int receive(){
    t.reset();
    t.start();
    while(t.read_ms() < RECEIVE_TIME){
        printPressureData();
    }
    return 1;
}


int stupid(){
    
    // while(!pc.readable()){
    //     pc.printf("hello\n\r"); 
    // }
    led4 = 1;
    wait(0.2);
    led4 = 0;
    if(pc.readable()){
        led4 = 1;

        //get most recent
        while(pc.readable()){
            tester = pc.getc();
            pc.putc(tester);
            pc.putc('\n');
            if(tester != '\0'){
                mostRecent = tester; //so end of line character isn't included
            }
        }
        txBuffer[0] = mostRecent;
        txBuffer[1] = '\0'; //that ends the string, only sends that little bit.
        // pc.putc(mostRecent);
        if(mostRecent == '\0'){
            led1 = 1;
            led2 = 1;
            led3 = 1;    
        }
        else if(mostRecent == '\n'){
            led1 = 1;
            led2 = 0;
            led3 = 1;    
        }
        else if(mostRecent == '0'){
            led1 = 1;
            led2 = 0;
            led3 = 0;    
        }
        else if(mostRecent == '1'){
            led1 = 0;
            led2 = 1;
            led3 = 0;    
        }
        else if(mostRecent == '2'){
            led1 = 0;
            led2 = 0;
            led3 = 1;    
        }
        else{
            led1 = 1;
            led2 = 1;
            led3 = 1;  
            led4 = 0;  
        }
    // pc.printf("hello\n");
    // while(pc.readable()){
    //     pc.putc(pc.getc());
    //     pc.putc('\n');
    // }
    }
    return 0;
}



int main() {
    // setup
    

    mostRecent = '0';
    led1 = 0;
    led2 = 0;
    led3 = 0;

    // while(1){
    //     stupid();
    //     wait(3);
    // }

    while(1){
    //     led4 = 1;
    //     wait(0.2);
    //     led4 = 0;
        receive();
    //     led4 = 1;
    //     wait(0.2);
    //     led4 = 0;

        transmit();
    }
    
}
