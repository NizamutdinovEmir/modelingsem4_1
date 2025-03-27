import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import e, m_e, mu_0


class MagnetronSolver:
    def __init__(self, D, n, Ra, Rk, U1, U2):
        """
        Инициализация параметров магнетрона:
        D - диаметр соленоида (м)
        n - число витков на единицу длины (витков/м)
        Ra - радиус анода (м)
        Rk - радиус катода (м)
        U1, U2 - диапазон напряжений (В)
        """
        self.D = D
        self.n = n
        self.Ra = Ra
        self.Rk = Rk
        self.U1 = U1
        self.U2 = U2

    def calculate_solenoid_current(self, U):
        """
        Рассчитывает ток соленоида, при котором электрон движется по окружности
        диаметром (Ra - Rk) для заданного напряжения U
        """
        r = (self.Ra - self.Rk) / 2  # радиус окружности
        B = np.sqrt(2 * U * m_e / e) / r  # необходимая индукция магнитного поля
        Ic = B / (mu_0 * self.n)  # ток соленоида
        return Ic

    def electron_trajectory(self, U, Ic, num_points=1000):
        B = mu_0 * self.n * Ic
        r = (self.Ra - self.Rk) / 2  # Фиксированный радиус
        theta = np.linspace(0, 2 * np.pi, num_points)
        x = (self.Rk + r) * np.cos(theta)  # Центр окружности: Rk + r
        y = (self.Rk + r) * np.sin(theta)
        return x, y

    def plot_ic_vs_u(self, num_points=100):
        """
        Строит диаграмму Ic от U и отмечает область окружности
        """
        U_values = np.linspace(self.U1, self.U2, num_points)
        Ic_values = [self.calculate_solenoid_current(U) for U in U_values]

        plt.figure(figsize=(10, 6))
        plt.plot(U_values, Ic_values, 'b-', linewidth=2, label='Кривая Ic(U)')

        # Выделяем область, где выполняется условие
        plt.fill_between(
            U_values,
            Ic_values,
            max(Ic_values),
            where=(U_values >= self.U1) & (U_values <= self.U2),
            color='green',
            alpha=0.2,
            label='Область окружности'
        )

        plt.xlabel('Напряжение U (В)', fontsize=12)
        plt.ylabel('Ток соленоида Ic (А)', fontsize=12)
        plt.title('Зависимость тока соленоида от напряжения', fontsize=14)
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_trajectory(self, U, Ic):
        """
        Строит траекторию электрона для заданных U и Ic
        """
        x, y = self.electron_trajectory(U, Ic)

        plt.figure(figsize=(8, 8))
        plt.plot(x, y, 'r-', linewidth=1.5)

        # Рисуем катод и анод
        circle_k = plt.Circle((0, 0), self.Rk, color='blue', fill=False, linestyle='--')
        circle_a = plt.Circle((0, 0), self.Ra, color='green', fill=False, linestyle='--')
        plt.gca().add_patch(circle_k)
        plt.gca().add_patch(circle_a)

        plt.xlim(-self.Ra * 1.2, self.Ra * 1.2)
        plt.ylim(-self.Ra * 1.2, self.Ra * 1.2)
        plt.gca().set_aspect('equal')
        plt.title(f'Траектория электрона при U={U} В, Ic={Ic:.2f} А', fontsize=12)
        plt.xlabel('x (м)', fontsize=10)
        plt.ylabel('y (м)', fontsize=10)
        plt.grid(True)
        plt.show()


# Пример использования
if __name__ == "__main__":
    # Параметры задачи (можно менять)
    D = 0.1  # диаметр соленоида (м)
    n = 1000  # число витков на единицу длины (витков/м)
    Ra = 0.03  # радиус анода (м)
    Rk = 0.01  # радиус катода (м)
    U1 = 100  # минимальное напряжение (В)
    U2 = 1000  # максимальное напряжение (В)

    solver = MagnetronSolver(D, n, Ra, Rk, U1, U2)

    # 1. Рассчитываем ток соленоида для среднего напряжения
    U = (U1 + U2) / 2
    Ic = solver.calculate_solenoid_current(U)
    print(f"Ток соленоида для U={U} В: {Ic:.4f} А")

    # 2. Строим траекторию электрона
    solver.plot_trajectory(U, Ic)

    # 3. Строим диаграмму Ic от U
    solver.plot_ic_vs_u()
