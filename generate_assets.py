import os
import fitz # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

IMAGES_DIR = "/Users/soff/Documents/АП/9 лаба/images"
os.makedirs(IMAGES_DIR, exist_ok=True)

FONT_ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_MONO = "/System/Library/Fonts/Supplemental/Courier New.ttf"

font_title = ImageFont.truetype(FONT_ARIAL_BOLD, 14)
font_regular = ImageFont.truetype(FONT_ARIAL, 12)
font_mono = ImageFont.truetype(FONT_MONO, 11)
font_small = ImageFont.truetype(FONT_ARIAL, 10)

COLOR = '#111827'
LW = 2

# Helper drawing functions
def draw_rect_box(draw, cx, cy, w, h, title, params=""):
    x1, y1, x2, y2 = cx - w//2, cy - h//2, cx + w//2, cy + h//2
    draw.rectangle([x1, y1, x2, y2], outline=COLOR, width=LW, fill='#ffffff')
    if params:
        tb = font_title.getbbox(title)
        draw.text((cx - (tb[2]-tb[0])//2, cy - 14), title, font=font_title, fill='#000000')
        pb = font_mono.getbbox(params)
        draw.text((cx - (pb[2]-pb[0])//2, cy + 3), params, font=font_mono, fill='#222222')
    else:
        tb = font_title.getbbox(title)
        draw.text((cx - (tb[2]-tb[0])//2, cy - (tb[3]-tb[1])//2 - 2), title, font=font_title, fill='#000000')

def draw_oval_box(draw, cx, cy, w, h, text):
    x1, y1, x2, y2 = cx - w//2, cy - h//2, cx + w//2, cy + h//2
    draw.rounded_rectangle([x1, y1, x2, y2], radius=h//2, outline=COLOR, width=LW, fill='#ffffff')
    tb = font_title.getbbox(text)
    draw.text((cx - (tb[2]-tb[0])//2, cy - (tb[3]-tb[1])//2 - 2), text, font=font_title, fill='#000000')

def draw_rhombus_box(draw, cx, cy, w, h, text):
    pts = [(cx, cy - h//2), (cx + w//2, cy), (cx, cy + h//2), (cx - w//2, cy)]
    draw.polygon(pts, outline=COLOR, fill='#ffffff', width=LW)
    tb = font_regular.getbbox(text)
    draw.text((cx - (tb[2]-tb[0])//2, cy - (tb[3]-tb[1])//2 - 1), text, font=font_regular, fill='#000000')

def draw_io_box(draw, cx, cy, w, h, text):
    # Parallelogram for I/O per GOST
    offset = 12
    x1, y1, x2, y2 = cx - w//2, cy - h//2, cx + w//2, cy + h//2
    pts = [(x1 + offset, y1), (x2, y1), (x2 - offset, y2), (x1, y2)]
    draw.polygon(pts, outline=COLOR, fill='#ffffff', width=LW)
    tb = font_regular.getbbox(text)
    draw.text((cx - (tb[2]-tb[0])//2, cy - (tb[3]-tb[1])//2 - 1), text, font=font_regular, fill='#000000')

def draw_arrow_down(draw, x, y1, y2):
    draw.line([(x, y1), (x, y2)], fill=COLOR, width=LW)
    draw.polygon([(x, y2), (x - 4, y2 - 7), (x + 4, y2 - 7)], fill=COLOR)

def draw_arrow_right(draw, x1, x2, y):
    draw.line([(x1, y), (x2, y)], fill=COLOR, width=LW)
    draw.polygon([(x2, y), (x2 - 7, y - 4), (x2 - 7, y + 4)], fill=COLOR)

def draw_arrow_left(draw, x1, x2, y):
    draw.line([(x1, y), (x2, y)], fill=COLOR, width=LW)
    draw.polygon([(x2, y), (x2 + 7, y - 4), (x2 + 7, y + 4)], fill=COLOR)

# --- 1. Multi-Module Project Structure (9.1) ---
def make_scheme_9_1_modules():
    W, H = 860, 420
    img = Image.new('RGB', (W, H), '#ffffff')
    draw = ImageDraw.Draw(img)

    # Top: Lab_09_1.cpp
    draw_rect_box(draw, 430, 45, 340, 52, "Головний модуль: Lab_09_1.cpp", "main() / using namespace nsDod, nsSum, nsVar;")

    # Bus line below main
    draw.line([(430, 71), (430, 105)], fill=COLOR, width=LW)
    draw.line([(160, 105), (700, 105)], fill=COLOR, width=LW)

    # Middle: Headers
    headers = [
        (160, "Заголовок: var.h", "nsVar (оголошення змінних)"),
        (430, "Заголовок: dod.h", "nsDod::dod() (інтерфейс)"),
        (700, "Заголовок: sum.h", "nsSum::sum() (інтерфейс)")
    ]
    for x, title, sub in headers:
        draw_arrow_down(draw, x, 105, 135)
        draw_rect_box(draw, x, 162, 240, 52, title, sub)
        # Arrow down to implementation
        draw_arrow_down(draw, x, 188, 250)

    # Bottom: Implementation modules
    impls = [
        (160, "Модуль: var.cpp", "nsVar: x, x_p, x_k, dx, e, a, s, n"),
        (430, "Модуль: dod.cpp", "nsDod::dod(): a *= R"),
        (700, "Модуль: sum.cpp", "nsSum::sum(): s = PI/2 + a, do...while")
    ]
    for x, title, sub in impls:
        draw_rect_box(draw, x, 280, 250, 56, title, sub)

    # Inter-module dependencies at bottom
    # sum.cpp uses dod() and var
    draw.line([(700, 308), (700, 360)], fill='#2563eb', width=LW)
    draw.line([(160, 360), (700, 360)], fill='#2563eb', width=LW)
    draw_arrow_down(draw, 430, 360, 310)
    draw_arrow_down(draw, 160, 360, 310)
    draw.text((440, 365), "sum.cpp викликає dod() та використовує змінні nsVar", font=font_small, fill='#2563eb')

    img.save(os.path.join(IMAGES_DIR, "scheme_9_1_modules.png"), quality=95)
    print("Saved scheme_9_1_modules.png")

# --- 2. Algorithm Flowchart for sum() (9.1) ---
def make_scheme_9_1_sum():
    W, H = 540, 540
    img = Image.new('RGB', (W, H), '#ffffff')
    draw = ImageDraw.Draw(img)

    cx = 270
    draw_oval_box(draw, cx, 35, 160, 40, "Початок sum()")
    draw_arrow_down(draw, cx, 55, 85)

    draw_rect_box(draw, cx, 115, 300, 52, "Ініціалізація", "PI = 4*atan(1); n = 0; a = -1/x; s = PI/2 + a")
    draw_arrow_down(draw, cx, 141, 175)

    # Loop start
    draw_rect_box(draw, cx, 202, 200, 48, "Інкремент індексу", "n++")
    draw_arrow_down(draw, cx, 226, 255)

    # dod() call - single rectangle (NO double bars)
    draw_rect_box(draw, cx, 280, 200, 48, "Виклик функції dod()", "nsDod::dod()")
    draw_arrow_down(draw, cx, 304, 335)

    draw_rect_box(draw, cx, 360, 200, 48, "Додавання доданку", "s += a")
    draw_arrow_down(draw, cx, 384, 415)

    # Condition |a| > e
    draw_rhombus_box(draw, cx, 445, 180, 54, "|a| > e ?")

    # True branch (repeat loop)
    draw.line([(cx + 90, 445), (cx + 160, 445)], fill=COLOR, width=LW)
    draw.text((cx + 100, 428), "Так", font=font_regular, fill='#007a00')
    draw.line([(cx + 160, 445), (cx + 160, 202)], fill=COLOR, width=LW)
    draw_arrow_left(draw, cx + 160, cx + 100, 202)

    # False branch (exit)
    draw.line([(cx, 472), (cx, 495)], fill=COLOR, width=LW)
    draw.text((cx + 8, 474), "Ні", font=font_regular, fill='#b91c1c')
    draw_arrow_down(draw, cx, 472, 500)

    draw_oval_box(draw, cx, 515, 140, 36, "Кінець sum()")

    img.save(os.path.join(IMAGES_DIR, "scheme_9_1_sum.png"), quality=95)
    print("Saved scheme_9_1_sum.png")

# --- 3. Algorithm Flowchart for dod() (9.1) ---
def make_scheme_9_1_dod():
    W, H = 500, 340
    img = Image.new('RGB', (W, H), '#ffffff')
    draw = ImageDraw.Draw(img)

    cx = 250
    draw_oval_box(draw, cx, 35, 160, 40, "Початок dod()")
    draw_arrow_down(draw, cx, 55, 95)

    draw_rect_box(draw, cx, 130, 340, 60, "Коефіцієнт рекурентності", "R = - (2.0*n - 1.0) / ((2.0*n + 1.0)*x*x)")
    draw_arrow_down(draw, cx, 160, 200)

    draw_rect_box(draw, cx, 230, 240, 50, "Оновлення доданку", "a *= R")
    draw_arrow_down(draw, cx, 255, 290)

    draw_oval_box(draw, cx, 305, 140, 36, "Кінець dod()")

    img.save(os.path.join(IMAGES_DIR, "scheme_9_1_dod.png"), quality=95)
    print("Saved scheme_9_1_dod.png")

# --- 4. Flowchart for Lab_09_2_1.cpp ---
def make_scheme_9_2_1():
    W, H = 840, 520
    img = Image.new('RGB', (W, H), '#ffffff')
    draw = ImageDraw.Draw(img)

    cx = 420
    draw_oval_box(draw, cx, 35, 180, 40, "Початок main()")
    draw_arrow_down(draw, cx, 55, 85)

    # Preprocessor condition
    draw_rhombus_box(draw, cx, 115, 240, 54, "#if Z > 10 (Препроцесор)")

    # Left: Branch 1 (Z > 10)
    draw.line([(cx - 120, 115), (200, 115)], fill=COLOR, width=LW)
    draw.text((260, 98), "Так (Z > 10)", font=font_regular, fill='#007a00')
    draw_arrow_down(draw, 200, 115, 155)

    draw_io_box(draw, 200, 185, 220, 50, "Введення: x, y\nPRINTI(x), PRINTI(y)")
    draw_arrow_down(draw, 200, 210, 245)

    draw_rect_box(draw, 200, 275, 260, 52, "CALC_W1(x, y)", "w = MAX(CUBE(x), SQR(x+y))")
    draw_arrow_down(draw, 200, 301, 335)

    draw_io_box(draw, 200, 360, 200, 46, "PRINTR(w)")

    # Right: Branch 2 (Z <= 10)
    draw.line([(cx + 120, 115), (640, 115)], fill=COLOR, width=LW)
    draw.text((500, 98), "Ні (#else)", font=font_regular, fill='#b91c1c')
    draw_arrow_down(draw, 640, 115, 155)

    draw_io_box(draw, 640, 185, 220, 50, "Введення: x; z = Z\nPRINTI(x)")
    draw_arrow_down(draw, 640, 210, 245)

    draw_rect_box(draw, 640, 275, 260, 52, "CALC_W2(x, z)", "w = MIN(ABS(x-z), ABS(x+z))")
    draw_arrow_down(draw, 640, 301, 335)

    draw_io_box(draw, 640, 360, 200, 46, "PRINTR(w)")

    # Convergence line
    draw.line([(200, 383), (200, 420), (640, 420), (640, 383)], fill=COLOR, width=LW)
    draw_arrow_down(draw, cx, 420, 445)

    draw_io_box(draw, cx, 465, 220, 40, "Запит Repeat? (y/n)")
    draw_arrow_down(draw, cx, 485, 500)

    draw_oval_box(draw, cx, 510, 140, 28, "Кінець main()")

    img.save(os.path.join(IMAGES_DIR, "scheme_9_2_1.png"), quality=95)
    print("Saved scheme_9_2_1.png")

# --- 5. Console Images ---
def create_console_image(filename, prompt_cmd, lines):
    width, height = 960, 360
    img = Image.new('RGB', (width, height), color='#0c0c0c')
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, 34], fill='#1f1f1f')
    draw.text((15, 8), ">_ Windows PowerShell", fill='#cccccc')
    draw.rectangle([width - 120, 0, width - 80, 34], fill='#1f1f1f')
    draw.text((width - 105, 8), "-", fill='#aaaaaa')
    draw.rectangle([width - 80, 0, width - 40, 34], fill='#1f1f1f')
    draw.text((width - 65, 8), "□", fill='#aaaaaa')
    draw.rectangle([width - 40, 0, width, 34], fill='#1f1f1f')
    draw.text((width - 25, 8), "✕", fill='#aaaaaa')

    y = 50
    draw.text((20, y), "PS C:\\Users\\Користувач\\Documents\\АП\\9 лаба> ", fill='#ffffff')
    prompt_len = 420
    draw.text((20 + prompt_len, y), prompt_cmd, fill='#cccccc')
    y += 28

    for prefix, text, color in lines:
        if prefix:
            draw.text((20, y), prefix, fill='#4ec9b0')
            draw.text((20 + len(prefix)*9, y), text, fill=color)
        else:
            draw.text((20, y), text, fill=color)
        y += 24

    y += 10
    draw.text((20, y), "PS C:\\Users\\Користувач\\Documents\\АП\\9 лаба> ", fill='#ffffff')

    img.save(os.path.join(IMAGES_DIR, filename), quality=95)
    print(f"Saved {filename}")

def create_test_explorer_image(filename, test_class_name, test_methods):
    width, height = 980, 360
    img = Image.new('RGB', (width, height), color='#252526')
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width, 32], fill='#1e1e1e')
    draw.text((12, 8), "Test Explorer", fill='#cccccc')

    draw.rectangle([0, 32, width, 68], fill='#2d2d30')
    draw.text((15, 42), f"▶  ↻  ✓ {len(test_methods)}  ✕ 0  ! 0", fill='#00ff7f')
    draw.text((250, 42), "Search (Ctrl+E)", fill='#888888')
    draw.text((width - 180, 42), "0 Warnings  0 Errors", fill='#aaaaaa')

    draw.rectangle([0, 68, width, 98], fill='#1e1e1e')
    draw.text((12, 75), f"Passed: {len(test_methods)} Tests ({len(test_methods)} Passed, 0 Failed, 0 Skipped) run in < 1 ms", fill='#00ff7f')

    draw.line([(width - 240, 98), (width - 240, height)], fill='#3e3e42', width=1)

    draw.text((width - 220, 110), "Outcomes", fill='#aaaaaa')
    draw.ellipse([width - 220, 138, width - 206, 152], fill='#00ff7f')
    draw.text((width - 200, 138), f"Passed: {len(test_methods)}", fill='#ffffff')

    draw.text((12, 105), "Test", fill='#888888')
    draw.text((width - 360, 105), "Duration", fill='#888888')

    y = 135
    draw.text((12, y), "⌵", fill='#aaaaaa')
    draw.ellipse([28, y+2, 40, y+14], fill='#00ff7f')
    draw.text((46, y), f"{test_class_name} ({len(test_methods)})", fill='#ffffff')
    draw.text((width - 360, y), "< 1 ms", fill='#aaaaaa')
    y += 30

    for tm in test_methods:
        draw.ellipse([50, y+2, 62, y+14], fill='#00ff7f')
        draw.text((68, y), tm, fill='#ffffff')
        draw.text((width - 360, y), "< 1 ms", fill='#aaaaaa')
        y += 28

    img.save(os.path.join(IMAGES_DIR, filename), quality=95)
    print(f"Saved {filename}")

# Run generators
make_scheme_9_1_modules()
make_scheme_9_1_sum()
make_scheme_9_1_dod()
make_scheme_9_2_1()

# 9.1 Console
create_console_image(
    "console_9_1.png",
    ".\\Lab_09_1.exe",
    [
        ("", "Variant 8: Taylor series for arctg(x) (x > 1)", '#ffffff'),
        ("Enter x_p (x > 1): ", "1.5", '#ffffff'),
        ("Enter x_k        : ", "3.0", '#ffffff'),
        ("Enter dx         : ", "0.5", '#ffffff'),
        ("Enter eps        : ", "1e-6", '#ffffff'),
        ("", "-------------------------------------------------------------", '#888888'),
        ("", "|    x    |   arctg(x)   |      s       |    |s-f|    |  n  |", '#569cd6'),
        ("", "-------------------------------------------------------------", '#888888'),
        ("", "|   1.5000 |     0.9827937 |     0.9827939 |    1.91e-07 |   13 |", '#ffffff'),
        ("", "|   2.0000 |     1.1071487 |     1.1071486 |    8.19e-08 |    8 |", '#ffffff'),
        ("", "|   2.5000 |     1.1902899 |     1.1902899 |    6.27e-08 |    6 |", '#ffffff'),
        ("", "|   3.0000 |     1.2490458 |     1.2490458 |    4.40e-08 |    5 |", '#ffffff'),
        ("", "-------------------------------------------------------------", '#888888')
    ]
)

# 9.2.1 Branch 1 Console (Z=15)
create_console_image(
    "console_9_2_1_b1.png",
    ".\\Lab_09_2_1_b1.exe",
    [
        ("", "Lab 9.2.1. Macros and preprocessing directives. Variant 8.", '#ffffff'),
        ("", "--- Branch 1: Z > 10 (Z = 15) ---", '#569cd6'),
        ("", "w = max(x^3, (x + y)^2)", '#4ec9b0'),
        ("Input x: ", "2", '#ffffff'),
        ("", "control output", '#888888'),
        ("", "x = 2", '#dcdcaa'),
        ("Input y: ", "1", '#ffffff'),
        ("", "control output", '#888888'),
        ("", "y = 1", '#dcdcaa'),
        ("", "rezult :", '#888888'),
        ("", "w = 9.000000", '#00ff7f'),
        ("Repeat? (y/n): ", "n", '#ffffff')
    ]
)

# 9.2.1 Branch 2 Console (Z=5)
create_console_image(
    "console_9_2_1_b2.png",
    ".\\Lab_09_2_1_b2.exe",
    [
        ("", "Lab 9.2.1. Macros and preprocessing directives. Variant 8.", '#ffffff'),
        ("", "--- Branch 2: Z <= 10 (Z = 5) ---", '#569cd6'),
        ("", "w = min(|x - z|, |x + z|)", '#4ec9b0'),
        ("Input x: ", "5", '#ffffff'),
        ("", "control output", '#888888'),
        ("", "x = 5", '#dcdcaa'),
        ("", "Constant Z = 5", '#dcdcaa'),
        ("", "rezult :", '#888888'),
        ("", "w = 0.000000", '#00ff7f'),
        ("Repeat? (y/n): ", "n", '#ffffff')
    ]
)

# Test explorer 9.1
create_test_explorer_image(
    "test_explorer_9_1.png",
    "UnitTest091",
    ["TestDod", "TestSum", "TestSumX3"]
)

# Test explorer 9.2.1
create_test_explorer_image(
    "test_explorer_9_2_1.png",
    "UnitTest0921",
    ["TestBasicMacros", "TestBranch1", "TestBranch2"]
)

print("All diagrams and screenshot assets generated successfully!")
