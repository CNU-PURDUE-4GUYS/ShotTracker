/*******************************************************************************
 *
 * Copyright (c) 2018 Dragino
 *
 * http://www.dragino.com
 *
 *******************************************************************************/

#include <string>
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>
#include <sys/time.h>
#include <signal.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/ioctl.h>

#include <wiringPi.h>
#include <wiringPiSPI.h>


// #############################################
// #############################################

#define REG_FIFO                    0x00
#define REG_OPMODE                  0x01
#define REG_FIFO_ADDR_PTR           0x0D
#define REG_FIFO_TX_BASE_AD         0x0E
#define REG_FIFO_RX_BASE_AD         0x0F
#define REG_RX_NB_BYTES             0x13
#define REG_FIFO_RX_CURRENT_ADDR    0x10
#define REG_IRQ_FLAGS               0x12
#define REG_DIO_MAPPING_1           0x40
#define REG_DIO_MAPPING_2           0x41
#define REG_MODEM_CONFIG            0x1D
#define REG_MODEM_CONFIG2           0x1E
#define REG_MODEM_CONFIG3           0x26
#define REG_SYMB_TIMEOUT_LSB  		0x1F
#define REG_PKT_SNR_VALUE			0x19
#define REG_PAYLOAD_LENGTH          0x22
#define REG_IRQ_FLAGS_MASK          0x11
#define REG_MAX_PAYLOAD_LENGTH 		0x23
#define REG_HOP_PERIOD              0x24
#define REG_SYNC_WORD				0x39
#define REG_VERSION	  				0x42

#define PAYLOAD_LENGTH              0x40

// LOW NOISE AMPLIFIER
#define REG_LNA                     0x0C
#define LNA_MAX_GAIN                0x23
#define LNA_OFF_GAIN                0x00
#define LNA_LOW_GAIN		    	0x20

#define RegDioMapping1                             0x40 // common
#define RegDioMapping2                             0x41 // common

#define RegPaConfig                                0x09 // common
#define RegPaRamp                                  0x0A // common
#define RegPaDac                                   0x5A // common

#define SX72_MC2_FSK                0x00
#define SX72_MC2_SF7                0x70
#define SX72_MC2_SF8                0x80
#define SX72_MC2_SF9                0x90
#define SX72_MC2_SF10               0xA0
#define SX72_MC2_SF11               0xB0
#define SX72_MC2_SF12               0xC0

#define SX72_MC1_LOW_DATA_RATE_OPTIMIZE  0x01 // mandated for SF11 and SF12

// sx1276 RegModemConfig1
#define SX1276_MC1_BW_125                0x70
#define SX1276_MC1_BW_250                0x80
#define SX1276_MC1_BW_500                0x90
#define SX1276_MC1_CR_4_5            0x02
#define SX1276_MC1_CR_4_6            0x04
#define SX1276_MC1_CR_4_7            0x06
#define SX1276_MC1_CR_4_8            0x08

#define SX1276_MC1_IMPLICIT_HEADER_MODE_ON    0x01

// sx1276 RegModemConfig2
#define SX1276_MC2_RX_PAYLOAD_CRCON        0x04

// sx1276 RegModemConfig3
#define SX1276_MC3_LOW_DATA_RATE_OPTIMIZE  0x08
#define SX1276_MC3_AGCAUTO                 0x04

// preamble for lora networks (nibbles swapped)
#define LORA_MAC_PREAMBLE                  0x34

#define RXLORA_RXMODE_RSSI_REG_MODEM_CONFIG1 0x0A
#ifdef LMIC_SX1276
#define RXLORA_RXMODE_RSSI_REG_MODEM_CONFIG2 0x70
#elif LMIC_SX1272
#define RXLORA_RXMODE_RSSI_REG_MODEM_CONFIG2 0x74
#endif

// FRF
#define        REG_FRF_MSB              0x06
#define        REG_FRF_MID              0x07
#define        REG_FRF_LSB              0x08

#define        FRF_MSB                  0xD9 // 868.1 Mhz
#define        FRF_MID                  0x06
#define        FRF_LSB                  0x66

// ----------------------------------------
// Constants for radio registers
#define OPMODE_LORA      0x80
#define OPMODE_MASK      0x07
#define OPMODE_SLEEP     0x00
#define OPMODE_STANDBY   0x01
#define OPMODE_FSTX      0x02
#define OPMODE_TX        0x03
#define OPMODE_FSRX      0x04
#define OPMODE_RX        0x05
#define OPMODE_RX_SINGLE 0x06
#define OPMODE_CAD       0x07

// ----------------------------------------
// Bits masking the corresponding IRQs from the radio
#define IRQ_LORA_RXTOUT_MASK 0x80
#define IRQ_LORA_RXDONE_MASK 0x40
#define IRQ_LORA_CRCERR_MASK 0x20
#define IRQ_LORA_HEADER_MASK 0x10
#define IRQ_LORA_TXDONE_MASK 0x08
#define IRQ_LORA_CDDONE_MASK 0x04
#define IRQ_LORA_FHSSCH_MASK 0x02
#define IRQ_LORA_CDDETD_MASK 0x01

// DIO function mappings                D0D1D2D3
#define MAP_DIO0_LORA_RXDONE   0x00  // 00------
#define MAP_DIO0_LORA_TXDONE   0x40  // 01------
#define MAP_DIO1_LORA_RXTOUT   0x00  // --00----
#define MAP_DIO1_LORA_NOP      0x30  // --11----
#define MAP_DIO2_LORA_NOP      0xC0  // ----11--

// #############################################
// #############################################

typedef bool boolean;
typedef unsigned char byte;

static const int CHANNEL = 0;

char message[256];

bool sx1272 = true;

byte receivedbytes;

enum sf_t { SF7=7, SF8, SF9, SF10, SF11, SF12 };

/*******************************************************************************
 *
 * Configure these values!
 *
 *******************************************************************************/

// SX1272 - Raspberry connections
int ssPin = 6;
int dio0  = 7;
int RST   = 0;

// Set spreading factor (SF7 - SF12)
sf_t sf = SF7;

// Set center frequency
uint32_t  freq = 915000000; // in Mhz! (868.1)

byte hello[32] = "HELLO";
byte ACK[4] = "ACK";
char* rbuff;

void die(const char *s)
{
    perror(s);
    exit(1);
}

void selectreceiver()
{
    digitalWrite(ssPin, LOW);
}

void unselectreceiver()
{
    digitalWrite(ssPin, HIGH);
}

byte readReg(byte addr)
{
    unsigned char spibuf[2];

    selectreceiver();
    spibuf[0] = addr & 0x7F;
    spibuf[1] = 0x00;
    wiringPiSPIDataRW(CHANNEL, spibuf, 2);
    unselectreceiver();

    return spibuf[1];
}

void writeReg(byte addr, byte value)
{
    unsigned char spibuf[2];

    spibuf[0] = addr | 0x80;
    spibuf[1] = value;
    selectreceiver();
    wiringPiSPIDataRW(CHANNEL, spibuf, 2);

    unselectreceiver();
}

static void opmode (uint8_t mode) {
    writeReg(REG_OPMODE, (readReg(REG_OPMODE) & ~OPMODE_MASK) | mode);
}

static void opmodeLora() {
    uint8_t u = OPMODE_LORA;
    if (sx1272 == false)
        u |= 0x8;   // TBD: sx1276 high freq
    writeReg(REG_OPMODE, u);
}


void SetupLoRa()
{
    
    digitalWrite(RST, HIGH);
    delay(100);
    digitalWrite(RST, LOW);
    delay(100);

    byte version = readReg(REG_VERSION);

    if (version == 0x22) {
        // sx1272
        printf("SX1272 detected, starting.\n");
        sx1272 = true;
    } else {
        // sx1276?
        digitalWrite(RST, LOW);
        delay(100);
        digitalWrite(RST, HIGH);
        delay(100);
        version = readReg(REG_VERSION);
        if (version == 0x12) {
            // sx1276
            printf("SX1276 detected, starting.\n");
            sx1272 = false;
        } else {
            printf("Unrecognized transceiver.\n");
            //printf("Version: 0x%x\n",version);
            exit(1);
        }
    }

    opmode(OPMODE_SLEEP);

    // set frequency
    uint64_t frf = ((uint64_t)freq << 19) / 32000000;
    writeReg(REG_FRF_MSB, (uint8_t)(frf>>16) );
    writeReg(REG_FRF_MID, (uint8_t)(frf>> 8) );
    writeReg(REG_FRF_LSB, (uint8_t)(frf>> 0) );

    writeReg(REG_SYNC_WORD, 0x34); // LoRaWAN public sync word

    if (sx1272) {
        if (sf == SF11 || sf == SF12) {
            writeReg(REG_MODEM_CONFIG,0x0B);
        } else {
            writeReg(REG_MODEM_CONFIG,0x0A);
        }
        writeReg(REG_MODEM_CONFIG2,(sf<<4) | 0x04);
    } else {
        if (sf == SF11 || sf == SF12) {
            writeReg(REG_MODEM_CONFIG3,0x0C);
        } else {
            writeReg(REG_MODEM_CONFIG3,0x04);
        }
        writeReg(REG_MODEM_CONFIG,0x72);
        writeReg(REG_MODEM_CONFIG2,(sf<<4) | 0x04);
    }

    if (sf == SF10 || sf == SF11 || sf == SF12) {
        writeReg(REG_SYMB_TIMEOUT_LSB,0x05);
    } else {
        writeReg(REG_SYMB_TIMEOUT_LSB,0x08);
    }
    writeReg(REG_MAX_PAYLOAD_LENGTH,0x80);
    writeReg(REG_PAYLOAD_LENGTH,PAYLOAD_LENGTH);
    writeReg(REG_HOP_PERIOD,0xFF);
    writeReg(REG_FIFO_ADDR_PTR, readReg(REG_FIFO_RX_BASE_AD));

    writeReg(REG_LNA, LNA_MAX_GAIN);

}

boolean receive(char *payload) {
    // clear rxDone
    writeReg(REG_IRQ_FLAGS, 0x40);

    int irqflags = readReg(REG_IRQ_FLAGS);

    //  payload crc: 0x20
    if((irqflags & 0x20) == 0x20)
    {
        printf("CRC error\n");
        writeReg(REG_IRQ_FLAGS, 0x20);
        return false;
    } else {

        byte currentAddr = readReg(REG_FIFO_RX_CURRENT_ADDR);
        byte receivedCount = readReg(REG_RX_NB_BYTES);
        receivedbytes = receivedCount;

        writeReg(REG_FIFO_ADDR_PTR, currentAddr);

        for(int i = 0; i < receivedCount; i++)
        {
            payload[i] = (char)readReg(REG_FIFO);
        }
    }
    return true;
}

char* receivepacket() {

    long int SNR;
    int rssicorr;

    if(digitalRead(dio0) == 1)
    {
        if(receive(message)) {
            byte value = readReg(REG_PKT_SNR_VALUE);
            if( value & 0x80 ) // The SNR sign bit is 1
            {
                // Invert and divide by 4
                value = ( ( ~value + 1 ) & 0xFF ) >> 2;
                SNR = -value;
            }
            else
            {
                // Divide by 4
                SNR = ( value & 0xFF ) >> 2;
            }
            
            if (sx1272) {
                rssicorr = 139;
            } else {
                rssicorr = 157;
            }

	    return message;
        } // received a message
	return "";
    } // dio0=1
	return "";
}

static void configPower (int8_t pw) {
    if (sx1272 == false) {
        // no boost used for now
        if(pw >= 17) {
            pw = 15;
        } else if(pw < 2) {
            pw = 2;
        }
        // check board type for BOOST pin
        writeReg(RegPaConfig, (uint8_t)(0x80|(pw&0xf)));
        writeReg(RegPaDac, readReg(RegPaDac)|0x4);

    } else {
        // set PA config (2-17 dBm using PA_BOOST)
        if(pw > 17) {
            pw = 17;
        } else if(pw < 2) {
            pw = 2;
        }
        writeReg(RegPaConfig, (uint8_t)(0x80|(pw-2)));
    }
}


static void writeBuf(byte addr, byte *value, byte len) {                                                       
    unsigned char spibuf[256];                                                                          
    spibuf[0] = addr | 0x80;                                                                            
    for (int i = 0; i < len; i++) {                                                                         
        spibuf[i + 1] = value[i];                                                                       
    }                                                                                                   
    selectreceiver();                                                                                   
    wiringPiSPIDataRW(CHANNEL, spibuf, len + 1);                                                        
    unselectreceiver();                                                                                 
}

void txlora(byte *frame, byte datalen) {

    // set the IRQ mapping DIO0=TxDone DIO1=NOP DIO2=NOP
    writeReg(RegDioMapping1, MAP_DIO0_LORA_TXDONE|MAP_DIO1_LORA_NOP|MAP_DIO2_LORA_NOP);
    // clear all radio IRQ flags
    writeReg(REG_IRQ_FLAGS, 0xFF);
    // mask all IRQs but TxDone
    writeReg(REG_IRQ_FLAGS_MASK, ~IRQ_LORA_TXDONE_MASK);

    // initialize the payload size and address pointers
    writeReg(REG_FIFO_TX_BASE_AD, 0x00);
    writeReg(REG_FIFO_ADDR_PTR, 0x00);
    writeReg(REG_PAYLOAD_LENGTH, datalen);

    // download buffer to the radio FIFO
    writeBuf(REG_FIFO, frame, datalen);
    // now we actually start the transmission
    opmode(OPMODE_TX);

    printf("send: %s\n", frame);
}


//  Functions for encoding the image
static char encoding_table[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                                'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
                                'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                                'w', 'x', 'y', 'z', '0', '1', '2', '3',
                                '4', '5', '6', '7', '8', '9', '+', '/'};

static char *decoding_table = NULL;

static int mod_table[] = {0, 2, 1};

void build_decoding_table() {
 
    decoding_table = (char *)malloc(256);
 
    for (int i = 0; i < 64; i++)
        decoding_table[(unsigned char) encoding_table[i]] = i;
} 

void base64_cleanup() {
    free(decoding_table);
}

unsigned char *base64_encode(const unsigned char *data,
                    size_t input_length,
                    size_t *output_length) {
 
    *output_length = 4 * ((input_length + 2) / 3);
 
    unsigned char *encoded_data = (unsigned char *)malloc(*output_length);
    if (encoded_data == NULL) return NULL;
 
    for (int i = 0, j = 0; i < input_length;) {
 
        uint32_t octet_a = i < input_length ? (unsigned char)data[i++] : 0;
        uint32_t octet_b = i < input_length ? (unsigned char)data[i++] : 0;
        uint32_t octet_c = i < input_length ? (unsigned char)data[i++] : 0;
 
        uint32_t triple = (octet_a << 0x10) + (octet_b << 0x08) + octet_c;
 
        encoded_data[j++] = encoding_table[(triple >> 3 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 2 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 1 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 0 * 6) & 0x3F];
    }
 
    for (int i = 0; i < mod_table[input_length % 3]; i++)
        encoded_data[*output_length - 1 - i] = '=';
 
    return encoded_data;
}

unsigned char *base64_decode(const char *data,
                             size_t input_length,
                             size_t *output_length) {
 
    if (decoding_table == NULL) build_decoding_table();
 
    if (input_length % 4 != 0) return NULL;
 
    *output_length = input_length / 4 * 3;
    if (data[input_length - 1] == '=') (*output_length)--;
    if (data[input_length - 2] == '=') (*output_length)--;
 
    unsigned char *decoded_data = (unsigned char*)malloc(*output_length);
    if (decoded_data == NULL) return NULL;
 
    for (int i = 0, j = 0; i < input_length;) {
 
        uint32_t sextet_a = data[i] == '=' ? 0 & i++ : decoding_table[data[i++]];
        uint32_t sextet_b = data[i] == '=' ? 0 & i++ : decoding_table[data[i++]];
        uint32_t sextet_c = data[i] == '=' ? 0 & i++ : decoding_table[data[i++]];
        uint32_t sextet_d = data[i] == '=' ? 0 & i++ : decoding_table[data[i++]];
 
        uint32_t triple = (sextet_a << 3 * 6)
        + (sextet_b << 2 * 6)
        + (sextet_c << 1 * 6)
        + (sextet_d << 0 * 6);
 
        if (j < *output_length) decoded_data[j++] = (triple >> 2 * 8) & 0xFF;
        if (j < *output_length) decoded_data[j++] = (triple >> 1 * 8) & 0xFF;
        if (j < *output_length) decoded_data[j++] = (triple >> 0 * 8) & 0xFF;
    }
 
    return decoded_data;
}

int main (int argc, char *argv[]) {
    // initial setup
    wiringPiSetup () ;
    pinMode(ssPin, OUTPUT);
    pinMode(dio0, INPUT);
    pinMode(RST, OUTPUT);

    wiringPiSPISetup(CHANNEL, 500000);

setTargetNumber:	//	Label for new shot session

    SetupLoRa();

    //  start process
    while(1){
        // radio init
        opmodeLora();
        opmode(OPMODE_STANDBY);
        opmode(OPMODE_RX);
        printf("Listening at SF%i on %.6lf Mhz.\n", sf,(double)freq/1000000);
        printf("------------------\n");
        
        //  listen the target number until received
        while(1) {
              
          rbuff = receivepacket();
          //if(!strcmp(rbuff, "1")){
          //if(isdigit(rbuff)){
          //if(rbuff != NULL)	  
          if(strcmp(rbuff, "")){
            //	parse b1 to 1.

            printf("Target No. %s\n", rbuff);
            delay(1500);    //  give some delay to make some time for the other RPi to change its LoRa mode
            break;  //  break the loop when received
          }
        }
       
       	// Send ACK for the Target Number given
        opmodeLora();
        opmode(OPMODE_STANDBY);

        writeReg(RegPaRamp, (readReg(RegPaRamp) & 0xF0) | 0x08); // set PA ramp-up time 50 uSec

        configPower(23);

        printf("Send packets at SF%i on %.6lf Mhz.\n", sf,(double)freq/1000000);
        printf("------------------\n");

        for(int i=0; i<10; ++i) {
            txlora(ACK, 3);
            delay(50);
        }	
        fflush(stdout);

        //	needed for mode_change ( TX -> RX mode )
        SetupLoRa();	        
        opmodeLora();
        opmode(OPMODE_STANDBY);
        opmode(OPMODE_RX);
        printf("Listening at SF%i on %.6lf Mhz.\n", sf,(double)freq/1000000);
        printf("------------------\n");
        //  (reference) target setting complete


        //  start receiving signals
        while(1) {
              
          rbuff = receivepacket();

          if(strcmp(rbuff, "")){	//	if not an empty string,
              if(!strcmp(rbuff, "sig_capture")){	//	if sig_capture
                printf("Start detection\n");
                fflush(stdout);
                
                //  Read coordinates from file and send it to RPI
                FILE *file;
                size_t fileLen;

                // Wait for file to be created, then Open file  
                while(1){
                    file = fopen("/home/pi/ShotTracker/integrated/images/detected/coordinates.txt", "r");
                    delay(1000);

                    if (file){
                        break;
                    }
                }
                
                //  get the length of the coordinates to be sent
                unsigned char *buffer;
                fseek(file, 0, SEEK_END);
                fileLen=ftell(file);
                fseek(file, 0, SEEK_SET);

                //  allocate memory for the buffer
                buffer = (unsigned char *)malloc(fileLen*10);
                if (!buffer)
                {
                  fprintf(stderr, "Memory error!");
                  fclose(file);
                  return 0;
                }

                //  read the file into buffer
                fread(buffer, fileLen, 1, file);


                //  Prepare LoRa mode change
                //	needed for mode_change ( RX -> TX mode )
                opmodeLora();
                opmode(OPMODE_STANDBY);

                writeReg(RegPaRamp, (readReg(RegPaRamp) & 0xF0) | 0x08); // set PA ramp-up time 50 uSec

                configPower(23);

                printf("Send packets at SF%i on %.6lf Mhz.\n", sf,(double)freq/1000000);
                printf("------------------\n");

                delay(1000);

                //  send coordinates
                txlora(buffer, fileLen);
            
                //  free allocated memory
                free(buffer);
                    
                //  close file
                fclose(file);

                // remove coordinates file
                remove("/home/pi/ShotTracker/integrated/images/detected/coordinates.txt");
                   
                // mode change for another signal input
                SetupLoRa();	//	needed for mode_change ( TX -> RX mode )
                opmodeLora();
                opmode(OPMODE_STANDBY);
                opmode(OPMODE_RX);

                continue;	//	 continue listening signals
              }

            else if(!strcmp(rbuff, "sig_sess_fin")){	//	if sig_sess_fin
              printf("Session finished\n");
              fflush(stdout);
              
              //  Prepare LoRa mode change
              //	needed for mode_change ( RX -> TX mode )
              SetupLoRa();
              opmodeLora();
              opmode(OPMODE_STANDBY);

              writeReg(RegPaRamp, (readReg(RegPaRamp) & 0xF0) | 0x08); // set PA ramp-up time 50 uSec

              configPower(23);

              printf("Send packets at SF%i on %.6lf Mhz.\n", sf,(double)freq/1000000);
              printf("------------------\n");

              delay(500);

              FILE *file;
              size_t fileLen;

              //Open file
              file = fopen("/home/pi/ShotTracker/integrated/images/warped/warped.jpeg", "rb");
              
              if (!file)
              {
                fprintf(stderr, "Unable to open file ");
                return 1;
              }

              unsigned char *buffer;
              fseek(file, 0, SEEK_END);
              fileLen=ftell(file);
              fseek(file, 0, SEEK_SET);

              buffer = (unsigned char *)malloc(fileLen+1);
              if (!buffer)
              {
                fprintf(stderr, "Memory error!");
                fclose(file);
                return 1;
              }

              fread(buffer, fileLen, 1, file);
              printf("File Data is: %s \n", buffer);

              size_t input_size = fileLen;

              //  encodoe file data to Base64 format
              unsigned char *encoded_data = base64_encode(buffer, input_size, &input_size);
              printf("Encoded Data is: %s \n", encoded_data);
              //  End of encoding
          

              //  Start image transmission
              unsigned char sbuff[254];
              long len = strlen((char *)encoded_data);
              long ptr = 0;
              long div = len / 253;
              int mod = len % 253;

              //  fragment the encoded data into packets
              //  Packet payload size : 253 bytes
              for(int i=0; i<=div; ++i){
                  if(i == div){
                      for(int j=0; j<mod; ++j){
                          sbuff[j] = encoded_data[ptr++];
                      }
                      sbuff[mod++] = '!';
                      sbuff[mod++] = '!';
                      sbuff[mod] = '\0';

                      txlora(sbuff, strlen((char*)sbuff));
                  }

                  else{
                      for(int k=0; k<253; ++k){
                          sbuff[k] = encoded_data[ptr++];
                      }
                      txlora(sbuff, strlen((char*)sbuff));
                      delay(400);
                  }
              }

              byte EEOOFF[4] = "!!";

              for(int i=0; i<10; ++i){
                txlora(EEOOFF, strlen((char*)EEOOFF));
              }
              fflush(stdout);

              //  free buffer
              free(buffer);
              //  close file
              fclose(file);

              //  start a new session and set a new target image
              goto setTargetNumber;
            }

            else if(!strcmp(rbuff, "sig_shutdown\n")){	//	if sig_shutdown
              printf("Shutdown\n");
              fflush(stdout);
              return(0);	//	shutdown
            }
            else{	// unexpected behavior
              continue;	//	continue listening signals
            }
        }
      }
    }

    return (0);
}
