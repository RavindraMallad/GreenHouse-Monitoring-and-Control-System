import machine
import dht
import utime

# DHT11 sensor setup
dht_pin = machine.Pin(6, machine.Pin.IN)
dht_sensor = dht.DHT11(dht_pin)

# Soil moisture sensor setup
moisture_pin = machine.Pin(27, machine.Pin.IN)

# LCD display setup
rs = machine.Pin(0, machine.Pin.OUT)
e = machine.Pin(1, machine.Pin.OUT)
d4 = machine.Pin(2, machine.Pin.OUT)
d5 = machine.Pin(3, machine.Pin.OUT)
d6 = machine.Pin(4, machine.Pin.OUT)
d7 = machine.Pin(5, machine.Pin.OUT)

def pulseE():
    e.value(1)
    utime.sleep_us(40)
    e.value(0)
    utime.sleep_us(40)

def send2LCD4(BinNum):
    d4.value((BinNum & 0b00000001) >> 0)
    d5.value((BinNum & 0b00000010) >> 1)
    d6.value((BinNum & 0b00000100) >> 2)
    d7.value((BinNum & 0b00001000) >> 3)
    pulseE()

def send2LCD8(BinNum):
    d4.value((BinNum & 0b00010000) >> 4)
    d5.value((BinNum & 0b00100000) >> 5)
    d6.value((BinNum & 0b01000000) >> 6)
    d7.value((BinNum & 0b10000000) >> 7)
    pulseE()
    d4.value((BinNum & 0b00000001) >> 0)
    d5.value((BinNum & 0b00000010) >> 1)
    d6.value((BinNum & 0b00000100) >> 2)
    d7.value((BinNum & 0b00001000) >> 3)
    pulseE()

def setUpLCD():
    rs.value(0)
    send2LCD4(0b0011)
    send2LCD4(0b0011)
    send2LCD4(0b0011)
    send2LCD4(0b0010)
    send2LCD8(0b00101000)
    send2LCD8(0b00001100)
    send2LCD8(0b00000110)
    send2LCD8(0b00000001)
    
    utime.sleep_ms(2)

def read_dht_sensor():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temperature, humidity
    except Exception as e:
        print("Failed to read DHT sensor:", e)
        return None, None

def read_moisture_sensor():
    try:
        moisture = moisture_pin.value()
        return moisture
    except Exception as e:
        print("Failed to read moisture sensor:", e)
        return None

def display_lcd(message):
    rs.value(1)
    for char in message:
        send2LCD8(ord(char))

def main():
    setUpLCD()
    fan_pin = machine.Pin(23, machine.Pin.OUT)  # Pin for the DC fan
    pump_pin = machine.Pin(24, machine.Pin.OUT)  # Pin for the water pump
    while True:
        temperature, humidity = read_dht_sensor()
        moisture = read_moisture_sensor()

        if temperature is not None and humidity is not None and moisture is not None:
            rs.value(0)
            send2LCD8(0b10000000)
            display_lcd("Temp: {}C".format(temperature))
            print("Temp: {}C".format(temperature))
            utime.sleep(2)
            rs.value(0)
            send2LCD8(0b11000000)
            display_lcd("Hum: {}%".format(humidity))
            print("Humidity: {}%".format(humidity))
            utime.sleep(2)
            
            rs.value(0)
            send2LCD8(0b11001010)
            display_lcd("Moi: {}".format(moisture))
            print("Moisture: {}".format(moisture))
            utime.sleep(2)
            
            if temperature >= 30:
                fan_pin.on()  # Turn on the fan
            else:
                fan_pin.off()  # Turn off the fan

            # Control the water pump based on moisture level
            if moisture == 1:
                pump_pin.on()  # Turn on the water pump
            else:
                pump_pin.off()  # Turn off the water pump
            

if __name__ == "__main__":
    main()
 

