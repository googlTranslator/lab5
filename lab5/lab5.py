import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons

class HarmonicVisualizer:
    def __init__(self):
        # Initial parameters
        self.amplitude = 1.0
        self.frequency = 1.0
        self.phase = 0.0
        self.noise_mean = 0.0
        self.noise_covariance = 0.2
        self.filter_window = 10
        self.t = np.linspace(0, 10, 1000)

        # Generate initial signals
        self.pure_signal = self._calculate_harmonic()
        self.noise = self._generate_noise()
        self.noisy_signal = self.pure_signal + self.noise
        self.filtered_signal = self._apply_filter()

        self._setup_plot()

    def _calculate_harmonic(self):
        return self.amplitude * np.sin(2 * np.pi * self.frequency * self.t + self.phase)

    def _generate_noise(self):
        return np.random.normal(self.noise_mean, np.sqrt(self.noise_covariance), len(self.t))

    def _apply_filter(self):
        window = np.ones(self.filter_window) / self.filter_window
        return np.convolve(self.noisy_signal, window, mode='same')

    def _setup_plot(self):
        # Create figure and axis
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(left=0.1, bottom=0.35)

        # Plot initial signals
        self.pure_line, = self.ax.plot(self.t, self.pure_signal, 'b-', label='Pure Signal')
        self.noisy_line, = self.ax.plot(self.t, self.noisy_signal, 'r:', label='Noisy Signal')
        self.filtered_line, = self.ax.plot(self.t, self.filtered_signal, 'g-', label='Filtered Signal')

        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Amplitude')
        self.ax.legend()

        # Add sliders
        self._add_sliders()

        # Add checkboxes for visibility
        self._add_checkboxes()

        # Add reset button
        self._add_reset_button()

    def _add_sliders(self):
        sliders_ax = [
            plt.axes([0.1, 0.25 - i * 0.05, 0.65, 0.03]) for i in range(4)
        ]

        self.sliders = {
            'amplitude': Slider(sliders_ax[0], 'Amplitude', 0.1, 5.0, valinit=self.amplitude),
            'frequency': Slider(sliders_ax[1], 'Frequency', 0.1, 3.0, valinit=self.frequency),
            'noise_mean': Slider(sliders_ax[2], 'Noise Mean', -1.0, 1.0, valinit=self.noise_mean),
            'covariance': Slider(sliders_ax[3], 'Noise Var', 0.0, 1.0, valinit=self.noise_covariance)
        }

        for slider in self.sliders.values():
            slider.on_changed(self._update)

    def _add_checkboxes(self):
        self.checkbox_ax = plt.axes([0.8, 0.15, 0.15, 0.15])
        self.check = CheckButtons(
            self.checkbox_ax,
            ['Show Noise', 'Show Filtered'],
            [True, True]
        )
        self.check.on_clicked(self._update_visibility)

    def _add_reset_button(self):
        self.reset_ax = plt.axes([0.8, 0.05, 0.1, 0.04])
        self.reset_button = Button(self.reset_ax, 'Reset')
        self.reset_button.on_clicked(self._reset)

    def _update(self, val):
        # Update parameters
        self.amplitude = self.sliders['amplitude'].val
        self.frequency = self.sliders['frequency'].val
        self.noise_mean = self.sliders['noise_mean'].val
        self.noise_covariance = self.sliders['covariance'].val

        # Update signals
        self.pure_signal = self._calculate_harmonic()
        self.noise = self._generate_noise()
        self.noisy_signal = self.pure_signal + self.noise
        self.filtered_signal = self._apply_filter()

        # Update plot
        self.pure_line.set_ydata(self.pure_signal)
        self.noisy_line.set_ydata(self.noisy_signal)
        self.filtered_line.set_ydata(self.filtered_signal)
        self.fig.canvas.draw_idle()

    def _update_visibility(self, label):
        if label == 'Show Noise':
            self.noisy_line.set_visible(not self.noisy_line.get_visible())
        elif label == 'Show Filtered':
            self.filtered_line.set_visible(not self.filtered_line.get_visible())
        plt.draw()

    def _reset(self, event):
        for slider in self.sliders.values():
            slider.reset()
        self._update(None)

    def show(self):
        plt.show()
visualizer = HarmonicVisualizer()
visualizer.show()
