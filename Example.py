from Visualiser import *

drw = get_interface_input('numb(макс. ответ, 01, 10); numb(мин. ответ, 02, 0); list(тип примера, 03, не выбрано, равенство, неравенство); radi(подвох, 04, Добавлять, Не добавлять, Случайно);' +
             'chek(посчитать ответ, 05); text(неизвестная, 06, X)',
             description='Это абсолютно бесполезное и ненужное описание, созданное только для того, чтобы заполнить это бесконечное и ненужное пространство. Впрочем, и моё время тоже. ' +
             'К сожалению, у меня не достаточно фантазии для написания романов, необходимых для показа дополнительного функционала этих окон при работе с большими текстами. ' +
             'Я просто скажу вам здесь же, что у этого типа окон есть вертикальный слайдер, с помощью которого можно прокручивать окно и размещать в нём ещё больше текста.' +
             '\nСъешь ещё этих мягких французских булок да выпей чаю...' * 0)
            
print(drw)
