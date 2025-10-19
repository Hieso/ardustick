import serial
import keyboard
from pynput.keyboard import Key, Controller 
from serial.tools import list_ports  # Импортируем именно tools.list_ports
from time import sleep

# Соответствие ключей
keys = {
    'w': 'w',
    'a': 'a',
    's': 's',
    'd': 'd'
}

# Функция для выбора функции кнопки
def choose_button_function():
    print("Выберите функцию для кнопки под джойстиком:")
    print("1. Пробел (Space)")
    print("2. Shift")
    print("3. Ctrl")
    choice = input("Введите номер выбора: ")
    if choice == '1':
        return 'space'
    elif choice == '2':
        return 'shift'
    elif choice == '3':
        return 'ctrl'
    else:
        print("Неправильный выбор. По умолчанию выбрана функция 'Пробел'.")
        return 'space'

button_function = choose_button_function()

def find_arduino_port():
    """Ищет доступный порт с подключённой Ардуинкой."""
    ports = list(list_ports.comports())  # Используем правильно импортированную функцию
    for port in ports:
        try:
            ser = serial.Serial(port.device, 9600, timeout=2)
            message = ser.readline().decode('utf-8').strip()
            if message == "button_release":  # Проверяем отклик от устройства
                print(f"Ардуино найдена на порте {port.device}.")
                return port.device
        except Exception as e:
            pass
    return None

def connect_to_arduino():
    """Подключение к найденному порту и ожидание команд."""
    global ser
    global messagessended
    while True:
        arduino_port = find_arduino_port()
        
        if arduino_port is not None:
            try:
                ser = serial.Serial(arduino_port, 9600, timeout=1)
                print(f"Успешно подключён к порту {arduino_port}.")
                
                while True:
                    try:
                        message = ser.readline().decode('utf-8').strip()
                        if message != '':
                            if messagessended >= 49:
                                dmitallx.clear()
                                messagessended = 1
                            else:
                                messagessended += 1
                            print(f"Получено: {message}")
                            if message in keys:
                                keyboard.press(keys[message])
                            elif message.startswith("no"):
                                key_name = message[-1]
                                keyboard.release(key_name)
                            elif message == "button_press":
                                if button_function == 'space':
                                    keytwo.press(Key.space)
                                elif button_function == 'shift':
                                    keytwo.press(Key.shift)
                                elif button_function == 'ctrl':
                                    keytwo.press(Key.ctrl)
                            elif message == "button_release":
                                if button_function == 'space':
                                    keytwo.release(Key.space)
                                elif button_function == 'shift':
                                    keytwo.release(Key.shift)
                                elif button_function == 'ctrl':
                                    keytwo.release(Key.ctrl)
                    
                    except serial.SerialException as e:
                        print(f"Ошибка соединения с портом: {e}")
                        ser.close()
                        break
            
            except serial.SerialException as e:
                print(f"Ошибка подключения к порту: {e}")
                continue
    
        else:
            print("Порт не обнаружен. Повторяю попытку...")
            sleep(0.5)

if __name__ == "__main__":
    keytwo = Controller() 
    messagessended = 0
    connect_to_arduino()
