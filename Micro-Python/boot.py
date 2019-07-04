from machine import ADC,UART
from time import sleep
uart=UART(0,baudrate=9600)
REF_RESISTANCE = 5600
LUX_CALC_SCALAR = 388316378.8
LUX_CALC_EXPONENT = -1.702715371
def ohm2lux():
    num=10
    avg=0
    for i in range(num):
        rawdata=ADC(0).read()
        resistorVoltage = rawdata / 1023 * 3.3;
        ldrVoltage = 3.3 - resistorVoltage;
        ldrResistance = ldrVoltage / resistorVoltage * REF_RESISTANCE;
        ldrLux = LUX_CALC_SCALAR * pow(ldrResistance, LUX_CALC_EXPONENT);
        avg+=ldrLux
        sleep(0.2)
    return avg/num;
    
def main():
    while(1):
        data=ohm2lux()
        print(data)
        uart.write(','+str(data))

main()
   
