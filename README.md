yadr
====

Yet Another Delta Robot



Механика.
---------

Рука сервомашинки (плечо - те деталь которая крепится прямо на вал сервы)
вырезана из поликарбоната толщиной 5мм (по ширине вала) и плотно насаживается
с предварительным нагреванием, например феном.
Люфта в месте крепления нет, но само плечо гнётся при боковых нагрузках.
Возможно, этого можно избежать используя более толстый лист поликарбоната.
Тяга дельты - карбоновая трубка с вклеенными с двух сторон болтами 3мм резбой
наружу.
На болты накручиваются шаровые соединения (ball-joint)
повсеместно используемые в авиа и авто-моделировании. Вроде таких:
http://www.hobbyking.com/hobbyking/store/__13099__m3_alloy_ball_joint_5pcs_bag_.html
Остальные детали печатаются из пластика на 3D принтере.
Модели лежат в каталоге scad/
Для проектирования и экспорта моделей в stl формат (для печати) используется OpenSCAD.
http://www.openscad.org/documentation.html


Управление.
-----------

Контроллер - arduino UNO.
Пока не используются датчики в контроллер никакая логика не выносится вообще.
Рассчёты координат и сглаживание реализуется в управляющей программе на
стороне ПК.
Контроллер хранит состояние и меняет соответствующий сигнал шима после
получение команды.

Протокол.
---------

Протокол текстовый, ASCII кодировка.
Каждая комманда состоит из одного десятиричного числа и следующего за ним
управляющего символа. Остальные символы, кроме десятичных цифр и описанныех управляющих
символов - игнорируются и являются разделителями комманд.
Т.е. внутри команды не может быть игнорируемых символов.
Символы:
'a', 'b', 'c' - угол одной из серв.
'f', 'g', 'h' - заполнение шим одной из серв соответственно, в микросекундах.
Например:
"120a95b  \n 60c\n" - установить угол первой сервы - 120, второй - 95, третьей - 60.
"1350b" - установить заполнение шима второй сервы 1.35 миллисекунды.


Управляющая программа на стороне ПК.
------------------------------------


Использованные ресурсы.
-----------------------

Подробный разбор кинематики дельта-робота с кодом рассчёта углов и координат на Си:
http://forums.trossenrobotics.com/tutorials/introduction-129/delta-robot-kinematics-3276/

Управление сервой.
http://www.avislab.com/blog/serva/



