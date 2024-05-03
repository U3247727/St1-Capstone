import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import Model
import Graphs
import price_prediction as pp


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Car Price Analysis")
        self.geometry("400x200")

        # creates all my tabs
        tab_control = ttk.Notebook(self)
        model_tab = ttk.Frame(tab_control)
        bar_chart_tab = ttk.Frame(tab_control)
        scatter_plot_tab = ttk.Frame(tab_control)
        prediction_tab = ttk.Frame(tab_control)
        histogram_tab = ttk.Frame(tab_control)  # New histogram tab
        tab_control.add(model_tab, text="Model Evaluation")
        tab_control.add(bar_chart_tab, text="Bar Chart")
        tab_control.add(scatter_plot_tab, text="Scatter Plot")
        tab_control.add(prediction_tab, text="Price Prediction")
        tab_control.add(histogram_tab, text="Histogram")  # New tab for histogram
        tab_control.pack(expand=1, fill="both")

        # model evaluation tab
        model_frame = ttk.LabelFrame(model_tab, text="Model Evaluation")
        model_frame.pack(padx=20, pady=20)
        evaluate_button = ttk.Button(model_frame, text="Evaluate Models", command=self.evaluate_models)
        evaluate_button.pack()
        self.model_output = tk.Text(model_frame, height=10, width=50)
        self.model_output.pack()

        # bar chart tab
        bar_chart_frame = ttk.LabelFrame(bar_chart_tab, text="Bar Chart")
        bar_chart_frame.pack(padx=20, pady=20)
        bar_chart_button = ttk.Button(bar_chart_frame, text="Plot Bar Chart", command=self.plot_bar_chart)
        bar_chart_button.pack()

        # scatter plots tab
        scatter_plot_frame = ttk.LabelFrame(scatter_plot_tab, text="Scatter Plot")
        scatter_plot_frame.pack(padx=20, pady=20)
        scatter_plot_button = ttk.Button(scatter_plot_frame, text="Plot Scatter Plot", command=self.plot_scatter_plot)
        scatter_plot_button.pack()

        # price prediction tab
        prediction_frame = ttk.LabelFrame(prediction_tab, text="Price Prediction")
        prediction_frame.pack(padx=20, pady=20)
        self.year_entry = ttk.Entry(prediction_frame, width=10)
        self.year_entry.grid(row=0, column=1, padx=5, pady=5)
        self.brand_entry = ttk.Entry(prediction_frame, width=10)
        self.brand_entry.grid(row=1, column=1, padx=5, pady=5)
        self.kilometers_entry = ttk.Entry(prediction_frame, width=10)
        self.kilometers_entry.grid(row=2, column=1, padx=5, pady=5)
        self.model_choice_var = tk.StringVar()
        self.model_choice_var.set("linear")
        ttk.Label(prediction_frame, text="Year:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(prediction_frame, text="Brand:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(prediction_frame, text="Kilometers:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(prediction_frame, text="Model:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        model_choices = ["linear", "random_forest"]
        for i, model in enumerate(model_choices):
            ttk.Radiobutton(prediction_frame, text=model.capitalize(), variable=self.model_choice_var, value=model).grid(row=3, column=i+1, padx=5, pady=5)
        predict_button = ttk.Button(prediction_frame, text="Predict Price", command=self.predict_price)
        predict_button.grid(row=4, columnspan=2, pady=10)

        # the histogram tab
        histogram_frame = ttk.LabelFrame(histogram_tab, text="Histogram")
        histogram_frame.pack(padx=20, pady=20)
        histogram_button = ttk.Button(histogram_frame, text="Plot Histogram", command=self.plot_histogram)
        histogram_button.pack()

    def evaluate_models(self):
        filepath = 'Australian Vehicle Prices.csv'
        df_encoded = Model.load_and_preprocess_data(filepath)
        X, y = Model.setup_data(df_encoded)
        model_scores = Model.evaluate_models(X, y)
        self.model_output.delete('1.0', tk.END)
        for model_name, score in model_scores.items():
            self.model_output.insert(tk.END, f"{model_name} RMSE: {score:.2f}\n")

    def plot_bar_chart(self):
        filepath = 'Australian Vehicle Prices.csv'
        df = Graphs.load_data(filepath)
        df = Graphs.convert_to_numeric(df, ['Kilometres', 'Price'])

        average_price_by_year = Model.calculate_average_price_by_year(df)  # Use Model module for calculation
        plot_window = tk.Toplevel(self)
        plot_window.title("Bar Chart")
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        average_price_by_year.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_xlabel('Year')
        ax.set_ylabel('Average Price')
        ax.set_title('Average Car Price by Year of Manufacture')
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "${:,.0f}".format(int(x))))
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, plot_window)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def plot_scatter_plot(self):
        filepath = 'Australian Vehicle Prices.csv'
        df = Graphs.load_data(filepath)
        df = Graphs.convert_to_numeric(df, ['Kilometres', 'Price'])

        plot_window = tk.Toplevel(self)
        plot_window.title("Scatter Plot")
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.scatter(df['Kilometres'], df['Price'], alpha=0.5, color='blue')
        ax.set_xlabel('Kilometres')
        ax.set_ylabel('Price')
        ax.set_title('Scatter Plot of Kilometres vs. Price')
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "${:,.0f}".format(int(x))))
        ax.set_ylim([0, max(df['Price']) + 5000])
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, plot_window)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def predict_price(self):
        try:
            year = int(self.year_entry.get())
            brand = self.brand_entry.get()
            kilometers = int(self.kilometers_entry.get())
            model_choice = self.model_choice_var.get()

            predicted_price = pp.make_prediction(year, brand, kilometers, model_choice)
            messagebox.showinfo("Prediction", f"Predicted Price: ${predicted_price:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid values.")

    def plot_histogram(self):
        filepath = 'Australian Vehicle Prices.csv'
        df = Graphs.load_data(filepath)
        df = Graphs.convert_to_numeric(df, ['Kilometres', 'Price'])

        price_range_by_kilometer = Graphs.calculate_price_range(df)
        plot_window = tk.Toplevel(self)
        plot_window.title("Histogram")
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        price_range_by_kilometer.plot(kind='bar', color='orange', ax=ax)
        ax.set_xlabel('Kilometer Range')
        ax.set_ylabel('Average Price')
        ax.set_title('Average Car Price by Kilometer Range')
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "${:,.0f}".format(int(x))))
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, plot_window)
        toolbar.update()
        canvas.get_tk_widget().pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
