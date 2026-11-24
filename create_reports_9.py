import os
import docx
from docx import Document
from docx.shared import Pt, Inches, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = "/Users/soff/Documents/АП/9 лаба"
IMAGES_DIR = os.path.join(BASE_DIR, "images")
REPORTS_DIR = os.path.join(BASE_DIR, "звіти")
TESTS_DIR = os.path.join(BASE_DIR, "tests")

os.makedirs(REPORTS_DIR, exist_ok=True)

GITHUB_REPO_URL = "https://github.com/sofiiayefimenkori2026-cmd/PR_9"

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, color="B0B0B0", sz="4", val="single"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

def add_code_table(doc, code_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    set_cell_border(cell, color="B0B0B0", sz="6", val="single")

    lines = code_text.strip().split('\n')
    for idx, line in enumerate(lines):
        p = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(line if line.strip() else ' ')
        r.font.name = 'Courier New'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)

    sp_p = doc.add_paragraph()
    sp_p.paragraph_format.space_before = Pt(0)
    sp_p.paragraph_format.space_after = Pt(6)

def build_report_9_1(output_filename):
    doc = Document()

    section = doc.sections[0]
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)
    section.left_margin = Mm(30)
    section.right_margin = Mm(15)
    section.page_width = Mm(210)
    section.page_height = Mm(297)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Courier New'
    font.size = Pt(10)
    font.color.rgb = RGBColor(0, 0, 0)

    def add_p(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, size=10, before=0, after=3):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = 1.0
        if text:
            r = p.add_run(text)
            r.font.name = 'Courier New'
            r.font.bold = bold
            r.font.size = Pt(size)
        return p

    def add_img(img_path, caption_text, width=Inches(5.8)):
        if os.path.exists(img_path):
            img_p = doc.add_paragraph()
            img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            img_p.paragraph_format.space_before = Pt(4)
            img_p.paragraph_format.space_after = Pt(2)
            run = img_p.add_run()
            run.add_picture(img_path, width=width)
            add_p(caption_text, align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=9.5, before=2, after=6)

    # 1. Title Block
    add_p('ЗВІТ', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, before=0, after=2)
    add_p('про виконання лабораторної роботи № 9.1', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, before=0, after=2)
    add_p('«Простори імен»', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, before=0, after=2)
    add_p('Варіант 8', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, before=0, after=2)
    add_p('з дисципліни', align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=10, before=0, after=2)
    add_p('«Алгоритмізація та програмування»', align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=10, before=0, after=2)
    add_p('студентки групи РІ-13', align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=10, before=0, after=2)
    add_p('Єфіменко Софії Володимирівни', align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=10, before=0, after=12)

    # 2. Мета роботи
    add_p('1. Мета роботи', bold=True, size=10, before=6, after=3)
    add_p(
        'Освоїти використання модулів мови C++ та просторів імен (namespace). Навчитися створювати '
        'багатомодульні C++ проєкти, відокремлюючи інтерфейс (заголовні файли .h) від реалізації (файли тексту модулів .cpp). '
        'Дослідити організацію глобальних змінних у багатомодульних проєктах та використання рекурентних співвідношень '
        'для ефективного обчислення нескінченних степеневих рядів Тейлора із заданою точністю eps.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=6
    )

    # 3. Умова завдання
    add_p('2. Умова завдання (варіант 8)', bold=True, size=10, before=6, after=3)
    add_p(
        'Обчислити і вивести на екран у вигляді таблиці значення функції, заданої за допомогою ряду Тейлора, '
        'на інтервалі від x_p до x_k з кроком dx та точністю eps. Параметри x_p, x_k, dx, eps вводяться з клавіатури.\n'
        'Таблиця має містити заголовок та шапку. Кожний рядок таблиці має містити значення аргументу x, '
        'значення функції arctg(x), значення суми ряду s, абсолютну похибку |s - arctg(x)| та кількість просумованих доданків n.\n'
        'Суму ряду Тейлора та значення доданку обчислювати за допомогою допоміжних алгоритмів, реалізованих у вигляді окремих '
        'функцій sum() та dod(). При обчисленні доданків використовувати рекурентні співвідношення. '
        'Всю необхідну функціям інформацію передавати через глобальні змінні простору імен nsVar.\n'
        'Кожну функцію визначити в окремому модулі, відокремлюючи інтерфейс від реалізації (var.h / var.cpp, '
        'dod.h / dod.cpp, sum.h / sum.cpp, Lab_09_1.cpp). Всі глобальні ресурси кожного модуля описати в окремих просторах імен.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=4
    )
    add_img(os.path.join(IMAGES_DIR, "task9_1_condition.png"), "Рис. 1. Умова завдання 9.1 (варіант 8) з методичних вказівок")

    # Математичний аналіз варіанту 8
    add_p('2.1. Математичні співвідношення варіанту 8', bold=True, size=10, before=6, after=3)
    add_p(
        'Функція задана рядом Тейлора для x > 1:\n'
        'arctg(x) = pi/2 + sum_{n=0}^{inf} (-1)^{n+1} / ((2n+1) * x^{2n+1}) = pi/2 - 1/x + 1/(3*x^3) - 1/(5*x^5) + ...\n\n'
        '1) Початковий доданок для n = 0:\n'
        '   a_0 = -1 / x, початкова сума: s = pi/2 + a_0, де pi/2 = 2 * atan(1.0).\n\n'
        '2) Рекурентне співвідношення між сусідніми доданками:\n'
        '   a_n = (-1)^{n+1} / ((2n+1) * x^{2n+1})\n'
        '   a_{n-1} = (-1)^n / ((2n-1) * x^{2n-1})\n'
        '   Коефіцієнт рекурентності R = a_n / a_{n-1} = - (2n - 1) / ((2n + 1) * x^2).\n'
        '   Таким чином, кожен наступний доданок обчислюється як: a_n = a_{n-1} * R, що усуває потребу в обчисленні факторіалів і степенів.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=6
    )

    # 4. Структурна схема програми
    add_p('3. Структурна схема програми', bold=True, size=10, before=6, after=3)
    add_p(
        'Відповідно до вимог методичних вказівок (стор. 9) та стандарту ГОСТ 19.701-90, багатомодульна структура '
        'проєкту складається з головного модуля Lab_09_1.cpp, заголовних файлів (var.h, dod.h, sum.h) '
        'та файлів реалізації (var.cpp, dod.cpp, sum.cpp). Кожен модуль інкапсулює свої дані у власному просторі імен.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=4
    )
    add_img(os.path.join(IMAGES_DIR, "scheme_9_1_modules.png"), "Рис. 2. Міжмодульна структурна схема проєкту Лабораторної роботи № 9.1")

    add_p('3.1. Блок-схема алгоритму функції обчислення суми ряду sum()', bold=True, size=10, before=6, after=3)
    add_p(
        'Функція nsSum::sum() ініціалізує змінні n = 0, a = -1/x, s = pi/2 + a, після чого у циклі з післяумовою '
        'збільшує лічильник доданків n, викликає функцію nsDod::dod() для домноження a на коефіцієнт рекурентності, '
        'додає a до накопичувальної суми s та перевіряє умову продовження циклу |a| > eps.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=4
    )
    add_img(os.path.join(IMAGES_DIR, "scheme_9_1_sum.png"), "Рис. 3. Блок-схема алгоритму функції sum() (ГОСТ 19.701-90)", width=Inches(4.5))

    add_p('3.2. Блок-схема алгоритму функції обчислення доданку dod()', bold=True, size=10, before=6, after=3)
    add_p(
        'Функція nsDod::dod() обчислює коефіцієнт рекурентності R = - (2n - 1) / ((2n + 1) * x^2) '
        'і домножує поточне значення глобальної змінної a на цей коефіцієнт (a *= R).',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=4
    )
    add_img(os.path.join(IMAGES_DIR, "scheme_9_1_dod.png"), "Рис. 4. Блок-схема алгоритму функції dod() (ГОСТ 19.701-90)", width=Inches(4.2))

    # 5. Текст програми
    add_p('4. Текст програми багатомодульного проєкту', bold=True, size=10, before=6, after=3)

    modules = [
        ("var.h – заголовочний файл простору імен nsVar (зовнішні оголошення змінних)", os.path.join(BASE_DIR, "var.h")),
        ("var.cpp – файл реалізації простору імен nsVar (визначення глобальних змінних)", os.path.join(BASE_DIR, "var.cpp")),
        ("dod.h – заголовочний файл простору імен nsDod (оголошення функції dod)", os.path.join(BASE_DIR, "dod.h")),
        ("dod.cpp – файл реалізації простору імен nsDod (визначення функції dod)", os.path.join(BASE_DIR, "dod.cpp")),
        ("sum.h – заголовочний файл простору імен nsSum (оголошення функції sum)", os.path.join(BASE_DIR, "sum.h")),
        ("sum.cpp – файл реалізації простору імен nsSum (визначення функції sum)", os.path.join(BASE_DIR, "sum.cpp")),
        ("Lab_09_1.cpp – головний файл проєкту (функція main, введення та табулювання)", os.path.join(BASE_DIR, "Lab_09_1.cpp"))
    ]
    for desc, path in modules:
        add_p(f'4.{modules.index((desc, path)) + 1}. {desc}', bold=True, size=10, before=4, after=2)
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        add_code_table(doc, code)

    # 6. Текст модульного тесту
    add_p('5. Текст модульного тесту (UnitTest_09_1.cpp)', bold=True, size=10, before=6, after=3)
    add_p(
        'Модульний тест верифікує точність рекурентного розрахунку доданку a_1 у функції nsDod::dod(), '
        'а також збіжність суми ряду Тейлора у функції nsSum::sum() до значень бібліотечної функції atan(x) '
        'для контрольних точок x = 2.0, x = 3.0 та x = 5.0 із точністю eps <= 1e-6. '
        'Тест підтримує компіляцію як у Microsoft Visual Studio (CppUnitTestFramework), так і під macOS/Linux (Doctest).',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=4
    )
    with open(os.path.join(TESTS_DIR, "UnitTest_09_1.cpp"), 'r', encoding='utf-8') as f:
        test_code = f.read()
    add_code_table(doc, test_code)

    # 7. Посилання на git
    add_p('6. Посилання на git-репозиторій з проектом', bold=True, size=10, before=6, after=3)
    add_p(f'GitHub-репозиторій проєкту: {GITHUB_REPO_URL}', align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=6)

    # 8. Результати тестування
    add_p('7. Результати роботи програми та тестування', bold=True, size=10, before=6, after=3)
    add_p('7.1. Результати роботи програми в консолі', bold=True, size=10, before=4, after=3)
    add_img(os.path.join(IMAGES_DIR, "console_9_1.png"), "Рис. 5. Виконання програми Lab_09_1 у консолі (табулювання arctg(x))")

    add_p('7.2. Результати виконання модульних тестів (Test Explorer)', bold=True, size=10, before=4, after=3)
    add_img(os.path.join(IMAGES_DIR, "test_explorer_9_1.png"), "Рис. 6. Успішне проходження модульних тестів у Test Explorer")

    # 9. Висновки
    add_p('8. Висновки', bold=True, size=10, before=6, after=3)
    add_p(
        'Під час виконання лабораторної роботи № 9.1 опанувала методику створення багатомодульних C++ проєктів '
        'із використанням просторів імен (namespace). Відокремила інтерфейси модулів (заголовні файли var.h, dod.h, sum.h) '
        'від їх практичної реалізації (файли var.cpp, dod.cpp, sum.cpp), що забезпечило незалежність компіляції окремих '
        'одиниць трансляції та запобігло колізіям ідентифікаторів. Реалізувала розклад функції arctg(x) у степеневий ряд Тейлора '
        'за допомогою рекурентного співвідношення R = - (2n-1)/((2n+1)*x^2), що дозволило досягти швидкої збіжності та високої '
        'числової точності (похибка менше 1e-7). Побудувала міжмодульну структурну схему та блок-схеми алгоритмів згідно з ГОСТ 19.701-90, '
        'а коректність обчислень підтвердила модульними тестами з повним успішним покриттям контрольних значень.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=6
    )

    target_path = os.path.join(REPORTS_DIR, output_filename)
    doc.save(target_path)
    print(f"Report '{output_filename}' saved successfully.")

def build_report_9_2_1(output_filename):
    doc = Document()

    section = doc.sections[0]
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)
    section.left_margin = Mm(30)
    section.right_margin = Mm(15)
    section.page_width = Mm(210)
    section.page_height = Mm(297)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Courier New'
    font.size = Pt(10)
    font.color.rgb = RGBColor(0, 0, 0)

    def add_p(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, size=10, before=0, after=3):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = 1.0
        if text:
            r = p.add_run(text)
            r.font.name = 'Courier New'
            r.font.bold = bold
            r.font.size = Pt(size)
        return p

    def add_img(img_path, caption_text, width=Inches(5.8)):
        if os.path.exists(img_path):
            img_p = doc.add_paragraph()
            img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            img_p.paragraph_format.space_before = Pt(4)
            img_p.paragraph_format.space_after = Pt(2)
            run = img_p.add_run()
            run.add_picture(img_path, width=width)
            add_p(caption_text, align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=9.5, before=2, after=6)

    # 1. Title Block
    add_p('ЗВІТ', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, before=0, after=2)
    add_p('про виконання лабораторної роботи № 9.2.1', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, before=0, after=2)
    add_p('«Директиви препроцесора та макровизначення (Частина 1)»', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, before=0, after=2)
    add_p('Варіант 8', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, before=0, after=2)
    add_p('з дисципліни', align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=10, before=0, after=2)
    add_p('«Алгоритмізація та програмування»', align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=10, before=0, after=2)
    add_p('студентки групи РІ-13', align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=10, before=0, after=2)
    add_p('Єфіменко Софії Володимирівни', align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=10, before=0, after=12)

    # 2. Мета роботи
    add_p('1. Мета роботи', bold=True, size=10, before=6, after=3)
    add_p(
        'Ознайомитися з роботою препроцесора C++, вивчити синтаксис та особливості використання параметризованих '
        'макровизначень (#define) і директив умовної компіляції (#if, #else, #endif, #ifndef). Навчитися визначати математичні '
        'операції (SQR, CUBE, MAX, MIN, ABS), форматоване виведення та розрахункові вирази у вигляді макросів, '
        'а також керувати вибором компільованої гілки програми на етапі препроцесорної обробки за значенням параметра Z.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=6
    )

    # 3. Умова завдання
    add_p('2. Умова завдання (варіант 8, Частина 1)', bold=True, size=10, before=6, after=3)
    add_p(
        'Використовуючи директиви умовної компіляції, макровизначення, включення власних заголовних файлів для необхідних '
        'оголошень та інші директиви, скласти програму обчислення наведених виразів:\n'
        '       / max(x^3, (x + y)^2),   якщо z > 10\n'
        '   w = <\n'
        '       \\ min(|x - z|, |x + z|), якщо z <= 10\n\n'
        'Функції max(), min(), визначення модуля (абсолютного значення), виведення результатів, логічних виразів, '
        'піднесення до степеня задати у вигляді макросів. Значення змінних задаються користувачем.\n'
        'Директиви умовної компіляції: препроцесор на основі значення Z має визначати, яка із двох зазначених в умові варіанту гілок буде компілюватися.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=4
    )
    add_img(os.path.join(IMAGES_DIR, "task9_2_1_condition.png"), "Рис. 1. Умова завдання 9.2 (варіант 8, Частина 1) з методичних вказівок")

    # 4. Структурна схема програми
    add_p('3. Структурна схема програми', bold=True, size=10, before=6, after=3)
    add_p(
        'Структурна схема програми за стандартом ГОСТ 19.701-90 відображає розгалуження на рівні препроцесора (#if Z > 10). '
        'У бінарний файл компілюється виключно одна з двох гілок розрахунку w: Гілка 1 обчислює w = MAX(CUBE(x), SQR(x+y)), '
        'а Гілка 2 обчислює w = MIN(ABS(x-z), ABS(x+z)).',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=4
    )
    add_img(os.path.join(IMAGES_DIR, "scheme_9_2_1.png"), "Рис. 2. Структурна схема алгоритму програми та умовної компіляції (ГОСТ 19.701-90)", width=Inches(5.8))

    # 5. Текст програми
    add_p('4. Текст програми', bold=True, size=10, before=6, after=3)

    add_p('4.1. macros.h – власний заголовочний файл з макровизначеннями', bold=True, size=10, before=4, after=2)
    with open(os.path.join(BASE_DIR, "macros.h"), 'r', encoding='utf-8') as f:
        code_macros = f.read()
    add_code_table(doc, code_macros)

    add_p('4.2. Lab_09_2_1.cpp – головна програма з директивами умовної компіляції', bold=True, size=10, before=4, after=2)
    with open(os.path.join(BASE_DIR, "Lab_09_2_1.cpp"), 'r', encoding='utf-8') as f:
        code_main = f.read()
    add_code_table(doc, code_main)

    # 6. Текст модульного тесту
    add_p('5. Текст модульного тесту (UnitTest_09_2_1.cpp)', bold=True, size=10, before=6, after=3)
    add_p(
        'Модульний тест перевіряє коректність функціонування базових макросів SQR, CUBE, MAX, MIN, ABS, '
        'а також математичну правильність розрахунку обох гілок виразу w (CALC_W1 та CALC_W2) на контрольних наборах даних.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=4
    )
    with open(os.path.join(TESTS_DIR, "UnitTest_09_2_1.cpp"), 'r', encoding='utf-8') as f:
        test_code = f.read()
    add_code_table(doc, test_code)

    # 7. Посилання на git
    add_p('6. Посилання на git-репозиторій з проектом', bold=True, size=10, before=6, after=3)
    add_p(f'GitHub-репозиторій проєкту: {GITHUB_REPO_URL}', align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=6)

    # 8. Результати тестування
    add_p('7. Результати роботи програми та тестування', bold=True, size=10, before=6, after=3)
    add_p('7.1. Виконання програми для Гілки 1 (Z = 15 > 10)', bold=True, size=10, before=4, after=3)
    add_img(os.path.join(IMAGES_DIR, "console_9_2_1_b1.png"), "Рис. 3. Виконання програми для Гілки 1 (Z = 15 > 10, w = max(x^3, (x+y)^2))")

    add_p('7.2. Виконання програми для Гілки 2 (Z = 5 <= 10)', bold=True, size=10, before=4, after=3)
    add_img(os.path.join(IMAGES_DIR, "console_9_2_1_b2.png"), "Рис. 4. Виконання програми для Гілки 2 (Z = 5 <= 10, w = min(|x-z|, |x+z|))")

    add_p('7.3. Результати виконання модульних тестів (Test Explorer)', bold=True, size=10, before=4, after=3)
    add_img(os.path.join(IMAGES_DIR, "test_explorer_9_2_1.png"), "Рис. 5. Успішне проходження модульних тестів у Test Explorer")

    # 9. Висновки
    add_p('8. Висновки', bold=True, size=10, before=6, after=3)
    add_p(
        'Під час виконання лабораторної роботи № 9.2 (Частина 1) опанувала роботу з препроцесором мови C++. '
        'Створила власний заголовний файл macros.h, у якому реалізувала параметризовані макровизначення для обчислення степенів (SQR, CUBE), '
        'екстремумів (MAX, MIN), абсолютного значення (ABS), контрольного виведення (PRINTI, PRINTR) та виразів варіанту 8 (CALC_W1, CALC_W2). '
        'Використала директиви умовної компіляції (#if, #else, #endif), завдяки чому на етапі трансляції у бінарний файл включався код лише '
        'відповідної гілки варіанту залежно від константи Z. Побудувала алгоритмічну схему згідно з ГОСТ 19.701-90 та всебічно верифікувала '
        'роботу програми та макросів модульними тестами.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=6
    )

    target_path = os.path.join(REPORTS_DIR, output_filename)
    doc.save(target_path)
    print(f"Report '{output_filename}' saved successfully.")

def build_full_report(output_filename):
    doc = Document()

    section = doc.sections[0]
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)
    section.left_margin = Mm(30)
    section.right_margin = Mm(15)
    section.page_width = Mm(210)
    section.page_height = Mm(297)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Courier New'
    font.size = Pt(10)
    font.color.rgb = RGBColor(0, 0, 0)

    def add_p(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, size=10, before=0, after=3):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = 1.0
        if text:
            r = p.add_run(text)
            r.font.name = 'Courier New'
            r.font.bold = bold
            r.font.size = Pt(size)
        return p

    def add_img(img_path, caption_text, width=Inches(5.8)):
        if os.path.exists(img_path):
            img_p = doc.add_paragraph()
            img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            img_p.paragraph_format.space_before = Pt(4)
            img_p.paragraph_format.space_after = Pt(2)
            run = img_p.add_run()
            run.add_picture(img_path, width=width)
            add_p(caption_text, align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=9.5, before=2, after=6)

    # Title Page
    add_p('МІНІСТЕРСТВО ОСВІТИ І НАУКИ УКРАЇНИ', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, before=0, after=2)
    add_p('НАЦІОНАЛЬНИЙ ТЕХНІЧНИЙ УНІВЕРСИТЕТ УКРАЇНИ', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10, before=0, after=2)
    add_p('«КИЇВСЬКИЙ ПОЛІТЕХНІЧНИЙ ІНСТИТУТ ІМЕНІ ІГОРЯ СІКОРСЬКОГО»', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10, before=0, after=24)

    add_p('ПОВНИЙ ЗВІТ', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, before=12, after=4)
    add_p('про виконання лабораторних робіт № 9.1 та № 9.2.1', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, before=0, after=4)
    add_p('«Простори імен та директиви препроцесора»', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, before=0, after=4)
    add_p('Варіант 8', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, before=0, after=24)

    add_p('з дисципліни «Алгоритмізація та програмування»', align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=10, before=0, after=18)

    add_p('Виконала:', align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True, size=10, before=0, after=2)
    add_p('студентка групи РІ-13', align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False, size=10, before=0, after=2)
    add_p('Єфіменко Софія Володимирівна', align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False, size=10, before=0, after=24)

    add_p('Київ – 2026', align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=10, before=30, after=12)

    doc.add_page_break()

    # --- PART 1: LAB 9.1 ---
    add_p('ЧАСТИНА 1. ЛАБОРАТОРНА РОБОТА № 9.1', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, before=6, after=4)
    add_p('«Простори імен та багатомодульні проєкти»', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, before=0, after=8)

    add_p('1.1. Мета роботи та теоретичні відомості', bold=True, size=10, before=4, after=2)
    add_p(
        'Мета: опанувати структуру багатомодульних C++ проєктів із розмежуванням інтерфейсів (файли .h) '
        'та реалізацій (файли .cpp), вивчити синтаксис та принципи просторів імен (namespace), розібратися '
        'із використанням глобальних змінних та рекурентних співвідношень для обчислення ряду Тейлора arctg(x).',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=4
    )

    add_p('1.2. Умова завдання (варіант 8)', bold=True, size=10, before=4, after=2)
    add_p(
        'Обчислити наближене значення функції arctg(x) (для x > 1) за допомогою розкладу в ряд Тейлора на інтервалі [x_p; x_k] '
        'з кроком dx та точністю eps:\n'
        'arctg(x) = pi/2 + sum_{n=0}^{inf} (-1)^{n+1} / ((2n+1) * x^{2n+1}) = pi/2 - 1/x + 1/(3*x^3) - 1/(5*x^5) + ...\n'
        'Перший доданок: a_0 = -1/x, s = pi/2 + a_0. Коефіцієнт рекурентності: R = - (2n-1) / ((2n+1)*x^2).',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=4
    )
    add_img(os.path.join(IMAGES_DIR, "task9_1_condition.png"), "Рис. 1. Умова завдання 9.1 з методичних вказівок")

    add_p('1.3. Міжмодульна структурна схема та алгоритми (ГОСТ 19.701-90)', bold=True, size=10, before=4, after=2)
    add_img(os.path.join(IMAGES_DIR, "scheme_9_1_modules.png"), "Рис. 2. Міжмодульна структурна схема проєкту Лабораторної роботи № 9.1")
    add_img(os.path.join(IMAGES_DIR, "scheme_9_1_sum.png"), "Рис. 3. Блок-схема алгоритму функції sum()", width=Inches(4.5))
    add_img(os.path.join(IMAGES_DIR, "scheme_9_1_dod.png"), "Рис. 4. Блок-схема алгоритму функції dod()", width=Inches(4.2))

    add_p('1.4. Програмний код лабораторної роботи № 9.1', bold=True, size=10, before=4, after=2)
    for desc, fname in [
        ("var.h", "var.h"), ("var.cpp", "var.cpp"),
        ("dod.h", "dod.h"), ("dod.cpp", "dod.cpp"),
        ("sum.h", "sum.h"), ("sum.cpp", "sum.cpp"),
        ("Lab_09_1.cpp", "Lab_09_1.cpp"), ("UnitTest_09_1.cpp", "tests/UnitTest_09_1.cpp")
    ]:
        add_p(f'Файл: {desc}', bold=True, size=10, before=3, after=2)
        with open(os.path.join(BASE_DIR, fname), 'r', encoding='utf-8') as f:
            add_code_table(doc, f.read())

    add_p('1.5. Результати виконання та тестування ЛР 9.1', bold=True, size=10, before=4, after=2)
    add_img(os.path.join(IMAGES_DIR, "console_9_1.png"), "Рис. 5. Виведення результатів роботи програми Lab_09_1 у консолі")
    add_img(os.path.join(IMAGES_DIR, "test_explorer_9_1.png"), "Рис. 6. Проходження тестів UnitTest_09_1 у Test Explorer")

    doc.add_page_break()

    # --- PART 2: LAB 9.2.1 ---
    add_p('ЧАСТИНА 2. ЛАБОРАТОРНА РОБОТА № 9.2.1', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, before=6, after=4)
    add_p('«Директиви препроцесора та макровизначення (Частина 1)»', align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, before=0, after=8)

    add_p('2.1. Мета роботи та завдання (варіант 8, Частина 1)', bold=True, size=10, before=4, after=2)
    add_p(
        'Використовуючи директиви умовної компіляції (#if, #else, #endif), макровизначення параметрів (SQR, CUBE, MAX, MIN, ABS, '
        'PRINTI, PRINTR) та власний заголовний файл macros.h, скласти програму обчислення виразу w для варіанту 8:\n'
        'w = max(x^3, (x + y)^2), якщо z > 10;   w = min(|x - z|, |x + z|), якщо z <= 10.\n'
        'Препроцесор на основі константи Z визначає, яка гілка програми компілюється в обчислювальний код.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=4
    )
    add_img(os.path.join(IMAGES_DIR, "task9_2_1_condition.png"), "Рис. 7. Умова завдання 9.2 (Частина 1) з методичних вказівок")

    add_p('2.2. Структурна схема алгоритму та умовної компіляції', bold=True, size=10, before=4, after=2)
    add_img(os.path.join(IMAGES_DIR, "scheme_9_2_1.png"), "Рис. 8. Структурна схема програми 9.2.1 за ГОСТ 19.701-90", width=Inches(5.8))

    add_p('2.3. Програмний код лабораторної роботи № 9.2.1', bold=True, size=10, before=4, after=2)
    for desc, fname in [
        ("macros.h", "macros.h"),
        ("Lab_09_2_1.cpp", "Lab_09_2_1.cpp"),
        ("UnitTest_09_2_1.cpp", "tests/UnitTest_09_2_1.cpp")
    ]:
        add_p(f'Файл: {desc}', bold=True, size=10, before=3, after=2)
        with open(os.path.join(BASE_DIR, fname), 'r', encoding='utf-8') as f:
            add_code_table(doc, f.read())

    add_p('2.4. Результати тестування та роботи програми ЛР 9.2.1', bold=True, size=10, before=4, after=2)
    add_img(os.path.join(IMAGES_DIR, "console_9_2_1_b1.png"), "Рис. 9. Консольний розрахунок для Гілки 1 (Z = 15 > 10)")
    add_img(os.path.join(IMAGES_DIR, "console_9_2_1_b2.png"), "Рис. 10. Консольний розрахунок для Гілки 2 (Z = 5 <= 10)")
    add_img(os.path.join(IMAGES_DIR, "test_explorer_9_2_1.png"), "Рис. 11. Проходження модульних тестів UnitTest_09_2_1")

    # Git Link
    add_p('3. Посилання на GitHub-репозиторій', bold=True, size=10, before=6, after=2)
    add_p(f'Усі вихідні коди, конфігурації VS Code, CMakeLists.txt, Makefile, схеми та звіти доступні у репозиторії:\n{GITHUB_REPO_URL}', align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=6)

    # General Conclusions
    add_p('4. Загальні висновки', bold=True, size=10, before=6, after=2)
    add_p(
        'У ході виконання лабораторного циклу № 9 опанувала базові інженерні інструменти побудови C++ програм: '
        'модульність із використанням просторів імен (namespace), умовну компіляцію препроцесора (#if, #else, #endif), '
        'параметризовані макровизначення (#define) та математичні рекурентні співвідношення. '
        'У завданні 9.1 успішно розбила проєкт на три самостійні модулі з власними просторами імен nsVar, nsDod, nsSum, '
        'досягнувши повної ізоляції даних та надзвичайно швидкого обчислення ряду Тейлора функції arctg(x). '
        'У завданні 9.2.1 розробила бібліотеку універсальних макросів macros.h та продемонструвала умовну компіляцію гілок '
        'коду залежно від константи Z. Усі розроблені модулі покриті комплексними Unit-тестами, структурні схеми '
        'оформлено відповідно до ГОСТ 19.701-90, а проєкт розміщено у відкритому git-репозиторії.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=10, before=0, after=6
    )

    target_path = os.path.join(REPORTS_DIR, output_filename)
    doc.save(target_path)
    print(f"Full report '{output_filename}' saved successfully.")

# Run builds
build_report_9_1("АП_РІ-13_Єфіменко_ЛР-09.1.docx")
build_report_9_2_1("АП_РІ-13_Єфіменко_ЛР-09.2.1.docx")
build_full_report("АП_РІ-13_Єфіменко_ЛР-09_Повний_Звіт.docx")

print("All Word reports generated successfully!")
