import tkinter as tk
import tkinter.messagebox
import math

# Константа - удельная теплота плавления для стали (примерное значение)

class LaserCutterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Модель лазерного резчика")

        # Начальные значения
        self.default_hole_diameter = 10  # мм
        self.default_metal_thickness = 50  # мм
        self.default_laser_power = 1000  # Вт
        self.default_metal_density = 7874  # кг/м³
        self.default_specific_heat_capacity = 640.57 # Дж/(кг·К)

        # Параметры резки
        self.hole_diameter = tk.DoubleVar(value=self.default_hole_diameter)
        self.metal_thickness = tk.DoubleVar(value=self.default_metal_thickness)
        self.laser_power = tk.DoubleVar(value=self.default_laser_power)
        self.metal_density = tk.DoubleVar(value=self.default_metal_density)
        self.specific_heat_capacity = tk.DoubleVar(value=self.default_specific_heat_capacity)

        # Позиция лазера (DoubleVar для связи со слайдером)
        self.laser_position = tk.DoubleVar(value=250)
        self.hole_cut = False
        self.animation_running = False

        # Список вырезанных отверстий (сохраняем координаты и размеры)
        self.holes = []

        # Элементы интерфейса для ввода данных
        tk.Label(self.root, text="Диаметр отверстия (мм):").pack()
        tk.Entry(self.root, textvariable=self.hole_diameter).pack()

        tk.Label(self.root, text="Толщина металла (мм):").pack()
        tk.Entry(self.root, textvariable=self.metal_thickness).pack()

        tk.Label(self.root, text="Мощность лазера (Вт):").pack()
        tk.Entry(self.root, textvariable=self.laser_power).pack()

        tk.Label(self.root, text="Плотность металла (кг/м³):").pack()
        tk.Entry(self.root, textvariable=self.metal_density).pack()

        self.start_cutting_button = tk.Button(self.root, text="Начать резку", command=self.start_cutting)
        self.start_cutting_button.pack()

        self.instant_cutting_button = tk.Button(self.root, text="Мгновенная симуляция", command=self.instant_cutting)
        self.instant_cutting_button.pack()

        self.reset_button = tk.Button(self.root, text="Восстановить пластину", command=self.reset_holes)
        self.reset_button.pack()

        # Поле для вывода времени резки
        self.time_label = tk.Label(self.root, text="Время резки: 0 сек")
        self.time_label.pack()

        # Поле для визуализации
        self.canvas = tk.Canvas(self.root, width=500, height=300)
        self.canvas.pack()

        # Cлайдер для управления положением лазера
        tk.Label(self.root, text="Положение лазера:").pack()
        self.position_slider = tk.Scale(self.root, from_=0, to=500, orient=tk.HORIZONTAL, variable=self.laser_position, command=self.update_from_slider)
        self.position_slider.pack()

        # Ввод точной координаты положения лазера
        tk.Label(self.root, text="Положение лазера (введите значение):").pack()
        self.position_entry = tk.Entry(self.root)
        self.position_entry.pack()
        self.position_entry.bind("<Return>", self.update_from_entry)

        self.update_canvas()

    """Обновление координаты лазера при перемещении слайдера."""
    def update_from_slider(self, event):
        # Ограничение позицию лазера в зависимости от диаметра отверстия
        half_hole_diameter = self.hole_diameter.get() / 2
        min_position = half_hole_diameter
        max_position = 500 - half_hole_diameter

        # Проверка текущего положения лазера
        if self.laser_position.get() < min_position:
            self.laser_position.set(min_position)
        elif self.laser_position.get() > max_position:
            self.laser_position.set(max_position)

        # Обновление текстового поля с координатой
        self.position_entry.delete(0, tk.END)
        self.position_entry.insert(0, str(int(self.laser_position.get())))
        self.update_canvas()

    """Обновление координаты лазера при вводе в текстовое поле."""
    def update_from_entry(self, event):
        try:
            position = float(self.position_entry.get())
            half_hole_diameter = self.hole_diameter.get() / 2
            min_position = half_hole_diameter
            max_position = 500 - half_hole_diameter

            if min_position <= position <= max_position:
                self.laser_position.set(position)
                self.position_slider.set(position)
                self.update_canvas()
            else:
                tk.messagebox.showerror("Ошибка", f"Координата должна быть в пределах от {min_position} до {max_position}.")
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Введите корректное число для координаты лазера.")

    def update_canvas(self):
        self.canvas.delete("all")

        # Вывод толщины пластины (1 пиксель = 1 мм)
        thickness_px = self.metal_thickness.get()
        if thickness_px < 1:
            thickness_px = 1

        # Координаты верхней и нижней границы пластины
        plate_top = 200
        plate_bottom = plate_top + thickness_px

        # Отрисовка металлической пластины с введённой толщиной
        self.canvas.create_rectangle(0, plate_top, 500, plate_bottom, fill="grey")

        # Отрисовка лазера
        self.canvas.create_line(self.laser_position.get(), 50, self.laser_position.get(), plate_top, fill="red", width=2)

        # Отрисовка отверстий
        for hole in self.holes:
            x_position, diameter, depth = hole
            hole_radius = diameter / 2
            self.canvas.create_rectangle(x_position - hole_radius, plate_top,
                                         x_position + hole_radius, plate_top + depth, fill="black")

    def calculate_cutting_time(self):
        # мм в м
        hole_radius_m = (self.hole_diameter.get() / 2) / 1000  # в метры
        thickness_m = self.metal_thickness.get() / 1000  # в метры

        # Площадь отверстия (м2)
        hole_area = math.pi * (hole_radius_m ** 2)

        # Объем отверстия (м³)
        hole_volume =  hole_area * thickness_m  # м³

        # Время резки (в секундах)
        time_required = (self.metal_thickness.get() * self.specific_heat_capacity.get() * hole_area * self.metal_density.get()) / (self.laser_power.get())
        return time_required

    """анимация резки"""
    def start_cutting(self):
        self.animation_running = True
        self.cut_depth = 0
        self.target_depth = self.metal_thickness.get()

        try:
            # Расчёт времени резки
            self.total_cutting_time = self.calculate_cutting_time()

            # Установка интервала анимации
            self.interval = self.total_cutting_time / 100  # 100 шагов анимации

            # Добавление нового отверстия в список вырезанных отверстий
            self.holes.append([self.laser_position.get(), self.hole_diameter.get(), 0])

            # Запуск анимации
            self.animate_cutting()
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Введите корректные данные для всех параметров.")

    """Анимация прорезания отверстия"""
    def animate_cutting(self):
        if not self.animation_running:
            return

        if self.cut_depth < self.target_depth:
            self.cut_depth += self.target_depth / 100
            self.holes[-1][2] = self.cut_depth
            self.update_canvas()

            # Обновление времени резки
            elapsed_time = (self.cut_depth / self.target_depth) * self.total_cutting_time
            self.time_label.config(text=f"Прошло времени: {elapsed_time:.2f} сек")

            # Рекурсивный вызов через заданный интервал
            self.root.after(int(self.interval * 1000), self.animate_cutting)
        else:
            self.time_label.config(text=f"Время прорезания отверстия: {self.total_cutting_time:.2f} сек")
            self.animation_running = False

    """Мгновенное завершение анимации"""
    def instant_cutting(self):
        if self.animation_running:
            self.cut_depth = self.target_depth
            self.holes[-1][2] = self.cut_depth
            self.update_canvas()

            self.time_label.config(text=f"Время прорезания отверстия: {self.total_cutting_time:.2f} сек")
            self.animation_running = False

    """Очистка поверхности"""
    def reset_holes(self):
        self.holes = []
        self.update_canvas()
        self.time_label.config(text="Прошло времени: 0 сек")  # Сброс времени

if __name__ == "__main__":
    root = tk.Tk()
    app = LaserCutterApp(root)
    root.mainloop()
