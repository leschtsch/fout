import os
import subprocess
import time


def count_True(a):
    res = 0
    for i in a:
        if i.poll() == None:
            res += 1
    return res


latex_list = ['$y=x$', '$y=x^2$', '$y=x^3$', '$y=x^4$', '$y=x^5$',
              'amogus', 'aboba', 'Big Russian Floppa', 'sus',
              '''dfvhsdgfshfdshfsdhfgjhgfjwaakjf
              hjsgfregehdjvhjsgfajksbfjhadsgfjasehfjadsgfdafhdsfhsdfjhs''',
              'dfvhs $y=x$ dgfshfdshfsdh $y=x^2$ fgjh $y=x^3$ gfjwaakjfhjsgfreg $y=x^4$ ehdjvhjsgfaj',
              r'''$f(x) = \frac{A_0}{2} + \sum \limits_{n=1}^{\infty} A_n \cos \left( \frac{2 n \pi x}{\nu} - \alpha_n \right)$''',
              r'''$\lim_{n \to \infty} \sum_{k=1}^n \frac{1}{k^2} = \frac{\pi^2}{6}$'''] * 5
length = len(latex_list)
for i in range(1, length + 1):
    latex_list = ['$y=x$', '$y=x^2$', '$y=x^3$', '$y=x^4$', '$y=x^5$',
                  'amogus', 'aboba', 'Big Russian Floppa', 'sus',
                  '''dfvhsdgfshfdshfsdhfgjhgfjwaakjf
                  hjsgfregehdjvhjsgfajksbfjhadsgfjasehfjadsgfdafhdsfhsdfjhs''',
                  'dfvhs $y=x$ dgfshfdshfsdh $y=x^2$ fgjh $y=x^3$ gfjwaakjfhjsgfreg $y=x^4$ ehdjvhjsgfaj',
                  r'''$f(x) = \frac{A_0}{2} + \sum \limits_{n=1}^{\infty} A_n \cos \left( \frac{2 n \pi x}{\nu} - \alpha_n \right)$''',
                  r'''$\lim_{n \to \infty} \sum_{k=1}^n \frac{1}{k^2} = \frac{\pi^2}{6}$'''] * 5

    name = 1
    processes = []
    start = time.time()
    try:
        while len(latex_list):
            if count_True(processes) < i:
                processes.append(subprocess.Popen([r'C:\Users\ПК\Desktop\проги\проект9.2\fout\venv\Scripts\python.exe',
                                                   r'C:/Users/ПК/Desktop/проги/проект9.2/fout/latex_render.py',
                                                   r'--name=' + str(name),
                                                   r'--ls=' + latex_list.pop(0)]))
                print(str(i) + ':' + str(name) + '/' + str(length))
                name += 1
        for z in processes:
            z.wait()
        time_running = time.time() - start
        f = open('speed.txt', 'r')
        f_d = f.read()
        f.close()
        f = open('speed.txt', 'w')
        print(f_d, file=f)
        print(str(i) + ':' + str(time_running), file=f)
        f.close()
    except Exception:
        f = open('speed.txt', 'r')
        f_d = f.read()
        f.close()
        f = open('speed.txt', 'w')
        print(f_d, file=f)
        print(str(i) + ':-1', file=f)
        f.close()

# a=[subprocess.Popen('notepad.exe')]
# print(count_True(a))
# a[0].wait()
# print(count_True(a))
