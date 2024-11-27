Проект command_line
https://github.com/dumkast/conf_dz1/

Задание:
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. Эмулятор должен запускаться из реальной командной строки, а файл с виртуальной файловой системой не нужно распаковывать у пользователя. Эмулятор принимает образ виртуальной файловой системы в виде файла формата tar. Эмулятор должен работать в режиме CLI.
Конфигурационный файл имеет формат xml и содержит:
• Имя пользователя для показа в приглашении к вводу.
• Имя компьютера для показа в приглашении к вводу.
• Путь к архиву виртуальной файловой системы.
• Путь к лог-файлу.
• Путь к стартовому скрипту.

Лог-файл имеет формат csv и содержит все действия во время последнего сеанса работы с эмулятором. Для каждого действия указан пользователь. Стартовый скрипт служит для начального выполнения заданного списка команд из файла.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также следующие команды:
1. uptime.
2. uname.
3. who.
Все функции эмулятора должны быть покрыты тестами, а для каждой из поддерживаемых команд необходимо написать 3 теста.

Файловая структура:

![image (54)](https://github.com/user-attachments/assets/6fdba1f4-c74d-453c-b241-ae368a636e00)


Используемые библиотеки python:

Описание команд: 

Пример конфигурационных файлов:

![image (50)](https://github.com/user-attachments/assets/139ae349-c6ab-4c2e-b0fe-cf2bf9cd4fd9)

![image (51)](https://github.com/user-attachments/assets/00392846-3fae-49c9-8e70-26327af53cdd)

![image (52)](https://github.com/user-attachments/assets/72356b2d-61dd-40a7-9adc-02ee47b4b5de)

Стартовый скрипт:

![image (53)](https://github.com/user-attachments/assets/d2dd1100-d0ad-4289-86e0-d7c99736f92d)

Запуск программы: 

![image (45)](https://github.com/user-attachments/assets/cb0c938f-f53b-40cd-9141-b3044787a0f5)

![image (46)](https://github.com/user-attachments/assets/75c08f2e-fd67-41c0-a5c6-569584a9166b)

![image (47)](https://github.com/user-attachments/assets/56c4ee2a-bc48-4b8e-8c34-a44f5659a758)

Примеры работы различных команд: 

![image (44)](https://github.com/user-attachments/assets/09d8f371-909e-4a4e-bdd4-94f82b9c504e)

![image (48)](https://github.com/user-attachments/assets/d11e7ed5-5d79-4c72-9b9e-2c0c34bf46b8)

![image (49)](https://github.com/user-attachments/assets/20941099-04b3-4fd5-8c63-b4f665d51aa9)

Содержимое лог-файла  log.csv:

![image (56)](https://github.com/user-attachments/assets/0f6525a7-12b9-4518-b8c0-46d29879249d)

Результат прогона тестов в файле test_line.py: 

![image (55)](https://github.com/user-attachments/assets/edb0538e-cc3a-4d95-bbe9-bd0cd253b322)
