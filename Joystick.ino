const int xPin = A0; // аналоговый вывод X джойстика
const int yPin = A1; // аналоговый вывод Y джойстика
const int buttonPin = 2; // цифровой вывод кнопки под джойстиком

// Границы чувствительности для направления
#define THRESHOLD_LOW 200
#define THRESHOLD_HIGH 800

// Переменные состояния направлений
bool prevXRight = false;
bool prevXLeft = false;
bool prevYForward = false;
bool prevYBack = false;
bool buttonState = false;

void setup() {
  Serial.begin(9600);   // инициализация последовательного порта
  pinMode(buttonPin, INPUT_PULLUP); // Настройка кнопки с подтяжкой к питанию
}

void loop() {
  int xValue = analogRead(xPin);
  int yValue = analogRead(yPin);
  bool currentButtonState = digitalRead(buttonPin);

  // Проверка горизонтального перемещения джойстика
  if (xValue > THRESHOLD_HIGH && !prevXRight) {          
    Serial.println("d");                                 // Клавиша D (правое направление)
    prevXRight = true;
    prevXLeft = false;
  } else if (xValue < THRESHOLD_LOW && !prevXLeft) {     
    Serial.println("a");                                 // Клавиша A (левое направление)
    prevXLeft = true;
    prevXRight = false;
  } else if ((THRESHOLD_LOW <= xValue && xValue <= THRESHOLD_HIGH)) { 
    if (prevXLeft) {
      Serial.println("noa");                              // Освобождение клавиши A
      prevXLeft = false;
    }
    if (prevXRight) {
      Serial.println("nod");                              // Освобождение клавиши D
      prevXRight = false;
    }
  }

  // Проверка вертикального перемещения джойстика
  if (yValue > THRESHOLD_HIGH && !prevYForward) {       
    Serial.println("w");                                  // Клавиша W (вперёд)
    prevYForward = true;
    prevYBack = false;
  } else if (yValue < THRESHOLD_LOW && !prevYBack) {   
    Serial.println("s");                                  // Клавиша S (назад)
    prevYBack = true;
    prevYForward = false;
  } else if ((THRESHOLD_LOW <= yValue && yValue <= THRESHOLD_HIGH)) { 
    if (prevYForward) {
      Serial.println("now");                               // Освобождение клавиши W
      prevYForward = false;
    }
    if (prevYBack) {
      Serial.println("nos");                               // Освобождение клавиши S
      prevYBack = false;
    }
  }

  // Проверка состояния кнопки
  if (currentButtonState != buttonState) {
    if (currentButtonState == LOW) {
      Serial.println("button_press"); // Сообщение о нажатии кнопки
    } else {
      Serial.println("button_release"); // Сообщение об отпускании кнопки
    }
    buttonState = currentButtonState;
  }

  delay(10);                                           // Уменьшенная пауза для стабильности
}