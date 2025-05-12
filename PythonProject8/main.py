import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import random

# Modern color palette
COLORS = {
    "dark_bg": "#2D3748",
    "darker_bg": "#1A202C",
    "light_bg": "#F7FAFC",
    "accent": "#4299E1",
    "accent_dark": "#3182CE",
    "success": "#48BB78",
    "warning": "#ED8936",
    "danger": "#F56565",
    "text": "#2D3748",
    "text_light": "#F7FAFC"
}


class ModernTitleBar(tk.Frame):
    def __init__(self, parent, title, *args, **kwargs):
        super().__init__(parent, bg=COLORS["darker_bg"], *args, **kwargs)
        self.parent = parent

        # Title label
        self.title_label = tk.Label(
            self,
            text=title,
            bg=COLORS["darker_bg"],
            fg=COLORS["text_light"],
            font=("Segoe UI", 10, "bold")
        )
        self.title_label.pack(side=tk.LEFT, padx=10)

        # Close button
        self.close_btn = tk.Button(
            self,
            text="✕",
            bg=COLORS["darker_bg"],
            fg=COLORS["text_light"],
            activebackground=COLORS["danger"],
            activeforeground="white",
            border=0,
            command=self.parent.quit,
            font=("Arial", 10)
        )
        self.close_btn.pack(side=tk.RIGHT, padx=5)

        # Bind mouse events for window dragging
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.on_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.parent.winfo_x() + deltax
        y = self.parent.winfo_y() + deltay
        self.parent.geometry(f"+{x}+{y}")


class ModernButton(ttk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.style = ttk.Style()
        self.style.configure("Modern.TButton",
                             foreground=COLORS["text_light"],
                             background=COLORS["accent"],
                             bordercolor=COLORS["accent"],
                             font=("Segoe UI", 9),
                             padding=6)
        self.style.map("Modern.TButton",
                       background=[("active", COLORS["accent_dark"])])
        self.configure(style="Modern.TButton")


class FarmingAdvisorySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Farming Advisory System")
        self.root.geometry("1100x750")
        self.root.configure(bg=COLORS["light_bg"])

        # Remove default title bar
        self.root.overrideredirect(True)

        # Add custom title bar
        self.title_bar = ModernTitleBar(root, "AI Farming Advisory System")
        self.title_bar.pack(fill=tk.X)

        # Main container
        self.main_frame = tk.Frame(root, bg=COLORS["light_bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Load mock data
        self.crop_db = self.load_crop_database()
        self.soil_types = ["Sandy", "Clay", "Loamy", "Silty", "Peaty"]
        self.pest_db = self.load_pest_database()

        # Create GUI
        self.create_gui()

        # Initialize models
        self.weather_model = WeatherModel()
        self.pest_model = PestModel()

    def load_crop_database(self):
        return {
            "Maize": {"soil": ["Loamy", "Silty"], "rainfall": "medium", "temp_range": (18, 32)},
            "Wheat": {"soil": ["Clay", "Loamy"], "rainfall": "low", "temp_range": (12, 25)},
            "Rice": {"soil": ["Clay", "Silty"], "rainfall": "high", "temp_range": (20, 35)},
            "Beans": {"soil": ["Loamy", "Sandy"], "rainfall": "medium", "temp_range": (15, 30)}
        }

    def load_pest_database(self):
        return {
            "Aphids": {"solution": "Use neem oil or insecticidal soap", "prevention": "Encourage beneficial insects"},
            "Cutworms": {"solution": "Apply diatomaceous earth around plants",
                         "prevention": "Use collars around seedlings"},
            "Powdery Mildew": {"solution": "Apply sulfur or potassium bicarbonate",
                               "prevention": "Ensure good air circulation"}
        }

    def create_gui(self):
        # Create notebook style
        style = ttk.Style()
        style.theme_create("modern", parent="alt", settings={
            "TNotebook": {
                "configure": {
                    "background": COLORS["dark_bg"],
                    "tabmargins": [2, 5, 2, 0]
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "background": COLORS["dark_bg"],
                    "foreground": COLORS["text_light"],
                    "padding": [10, 5],
                    "font": ("Segoe UI", 9)
                },
                "map": {
                    "background": [("selected", COLORS["accent"])],
                    "foreground": [("selected", "white")]
                }
            }
        })
        style.theme_use("modern")

        self.notebook = ttk.Notebook(self.main_frame)

        self.create_dashboard_tab()
        self.create_soil_analysis_tab()
        self.create_weather_tab()
        self.create_pest_id_tab()
        self.create_crop_advice_tab()

        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

    def create_dashboard_tab(self):
        tab = tk.Frame(self.notebook, bg=COLORS["light_bg"])
        self.notebook.add(tab, text="Dashboard")

        # Header
        header = tk.Frame(tab, bg=COLORS["accent"])
        header.pack(fill=tk.X, pady=(0, 20))
        tk.Label(header,
                 text="Personalized Ai Farming Advisory",
                 bg=COLORS["accent"],
                 fg="white",
                 font=("Segoe UI", 14, "bold")).pack(pady=15)

        # Quick actions frame
        actions_frame = tk.Frame(tab, bg=COLORS["light_bg"])
        actions_frame.pack(fill=tk.X, padx=20, pady=10)

        buttons = [
            ("Get Crop Advice", lambda: self.notebook.select(4), COLORS["success"]),
            ("Check Soil Needs", lambda: self.notebook.select(1), COLORS["warning"]),
            ("Weather Forecast", lambda: self.notebook.select(2), COLORS["accent"]),
            ("Pest Identification", lambda: self.notebook.select(3), COLORS["danger"])
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                actions_frame,
                text=text,
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                relief=tk.FLAT,
                font=("Segoe UI", 10),
                command=command,
                padx=20,
                pady=10
            )
            btn.pack(side=tk.LEFT, expand=True, padx=5)

        # Stats cards
        stats_frame = tk.Frame(tab, bg=COLORS["light_bg"])
        stats_frame.pack(fill=tk.X, padx=20, pady=10)

        stats = [
            ("Crops in Database", len(self.crop_db), COLORS["accent"]),
            ("Common Pests", len(self.pest_db), COLORS["warning"]),
            ("Soil Types", len(self.soil_types), COLORS["success"])
        ]

        for title, value, color in stats:
            card = tk.Frame(stats_frame, bg="white", relief=tk.RAISED, borderwidth=1)
            card.pack(side=tk.LEFT, expand=True, padx=5)

            tk.Label(card,
                     text=title,
                     bg="white",
                     fg=COLORS["text"],
                     font=("Segoe UI", 9)).pack(pady=(10, 0))

            tk.Label(card,
                     text=str(value),
                     bg="white",
                     fg=color,
                     font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))

        # Recent alerts
        alert_frame = tk.LabelFrame(
            tab,
            text=" Recent Alerts ",
            bg=COLORS["light_bg"],
            fg=COLORS["text"],
            font=("Segoe UI", 10, "bold"),
            labelanchor="n"
        )
        alert_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)

        alert_text = tk.Text(
            alert_frame,
            bg="white",
            fg=COLORS["text"],
            height=6,
            wrap=tk.WORD,
            font=("Segoe UI", 9),
            padx=10,
            pady=10
        )
        alert_text.pack(fill=tk.BOTH, expand=True)
        alert_text.insert(tk.END,
                          "• System updated to v2.1\n• New pest database available\n• Weather API connection stable")
        alert_text.config(state=tk.DISABLED)

    def create_soil_analysis_tab(self):
        tab = tk.Frame(self.notebook, bg=COLORS["light_bg"])
        self.notebook.add(tab, text="Soil Analysis")

        # Input frame
        input_frame = tk.Frame(tab, bg=COLORS["light_bg"])
        input_frame.pack(fill=tk.X, padx=20, pady=10)

        # Soil type selection
        tk.Label(input_frame,
                 text="Select Your Soil Type:",
                 bg=COLORS["light_bg"],
                 fg=COLORS["text"],
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=5)

        self.soil_var = tk.StringVar()
        soil_combo = ttk.Combobox(
            input_frame,
            textvariable=self.soil_var,
            values=self.soil_types,
            font=("Segoe UI", 9),
            state="readonly"
        )
        soil_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # pH scale
        tk.Label(input_frame,
                 text="Soil pH Level:",
                 bg=COLORS["light_bg"],
                 fg=COLORS["text"],
                 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=5)

        self.ph_var = tk.DoubleVar(value=6.5)
        ph_scale = ttk.Scale(
            input_frame,
            from_=4,
            to=9,
            variable=self.ph_var,
            command=lambda e: self.update_ph_display()
        )
        ph_scale.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.ph_display = tk.Label(
            input_frame,
            text=f"Current pH: {self.ph_var.get():.1f}",
            bg=COLORS["light_bg"],
            fg=COLORS["text"],
            font=("Segoe UI", 9)
        )
        self.ph_display.grid(row=1, column=2, padx=5)

        # Analyze button
        analyze_btn = ModernButton(
            input_frame,
            text="Analyze Soil",
            command=self.analyze_soil
        )
        analyze_btn.grid(row=2, column=0, columnspan=3, pady=10)

        # Results frame
        result_frame = tk.Frame(tab, bg=COLORS["light_bg"])
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(result_frame,
                 text="Soil Analysis Results:",
                 bg=COLORS["light_bg"],
                 fg=COLORS["text"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")

        self.soil_result = tk.Text(
            result_frame,
            height=15,
            wrap=tk.WORD,
            bg="white",
            fg=COLORS["text"],
            font=("Segoe UI", 9),
            padx=10,
            pady=10
        )
        self.soil_result.pack(fill=tk.BOTH, expand=True)
        self.soil_result.insert(tk.END, "Soil analysis results will appear here.")
        self.soil_result.config(state=tk.DISABLED)

    def update_ph_display(self):
        self.ph_display.config(text=f"Current pH: {self.ph_var.get():.1f}")

    def analyze_soil(self):
        soil_type = self.soil_var.get()
        ph = self.ph_var.get()

        if not soil_type:
            messagebox.showerror("Error", "Please select a soil type")
            return

        if 6 <= ph <= 7.5:
            ph_status = "optimal"
        elif ph < 6:
            ph_status = "acidic (needs lime)"
        else:
            ph_status = "alkaline (needs sulfur)"

        suitable_crops = [crop for crop, data in self.crop_db.items()
                          if soil_type in data["soil"]]

        result = f"🌱 Soil Analysis Results 🌱\n\n"
        result += f"🔹 Soil Type: {soil_type}\n"
        result += f"🔹 pH Level: {ph:.1f} ({ph_status})\n\n"
        result += "📋 Recommendations:\n"
        result += f"• For pH adjustment: {self.get_ph_recommendation(ph)}\n"
        result += f"• Suitable crops: {', '.join(suitable_crops)}\n"
        result += f"• Fertilizer suggestion: {self.get_fertilizer_recommendation(soil_type, ph)}"

        self.soil_result.config(state=tk.NORMAL)
        self.soil_result.delete(1.0, tk.END)
        self.soil_result.insert(tk.END, result)
        self.soil_result.config(state=tk.DISABLED)

    def get_ph_recommendation(self, ph):
        if ph < 6:
            return "Apply agricultural lime to raise pH"
        elif ph > 7.5:
            return "Apply elemental sulfur to lower pH"
        return "pH is in optimal range, no adjustment needed"

    def get_fertilizer_recommendation(self, soil_type, ph):
        if soil_type == "Sandy":
            return "Slow-release nitrogen fertilizer"
        elif soil_type == "Clay":
            return "Phosphorus-rich fertilizer"
        return "Balanced NPK fertilizer"

    def create_weather_tab(self):
        tab = tk.Frame(self.notebook, bg=COLORS["light_bg"])
        self.notebook.add(tab, text="Weather Forecast")

        # Input frame
        input_frame = tk.Frame(tab, bg=COLORS["light_bg"])
        input_frame.pack(fill=tk.X, padx=20, pady=10)

        # Location input
        tk.Label(input_frame,
                 text="Enter Location:",
                 bg=COLORS["light_bg"],
                 fg=COLORS["text"],
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=5)

        self.location_var = tk.StringVar(value="Nairobi")
        location_entry = ttk.Entry(
            input_frame,
            textvariable=self.location_var,
            font=("Segoe UI", 9)
        )
        location_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Forecast period
        tk.Label(input_frame,
                 text="Forecast Period:",
                 bg=COLORS["light_bg"],
                 fg=COLORS["text"],
                 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=5)

        self.forecast_var = tk.StringVar(value="7-day")
        forecast_combo = ttk.Combobox(
            input_frame,
            textvariable=self.forecast_var,
            values=["7-day", "14-day", "Seasonal"],
            font=("Segoe UI", 9),
            state="readonly"
        )
        forecast_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Get forecast button
        forecast_btn = ModernButton(
            input_frame,
            text="Get Weather Forecast",
            command=self.get_weather_forecast
        )
        forecast_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Results notebook
        results_notebook = ttk.Notebook(tab)
        results_notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Forecast tab
        forecast_tab = tk.Frame(results_notebook, bg=COLORS["light_bg"])
        results_notebook.add(forecast_tab, text="Forecast")

        self.forecast_text = tk.Text(
            forecast_tab,
            height=10,
            wrap=tk.WORD,
            bg="white",
            fg=COLORS["text"],
            font=("Segoe UI", 9),
            padx=10,
            pady=10
        )
        self.forecast_text.pack(fill=tk.BOTH, expand=True)
        self.forecast_text.insert(tk.END, "Weather forecast will appear here.")
        self.forecast_text.config(state=tk.DISABLED)

        # Recommendations tab
        rec_tab = tk.Frame(results_notebook, bg=COLORS["light_bg"])
        results_notebook.add(rec_tab, text="Recommendations")

        self.weather_recommendations = tk.Text(
            rec_tab,
            height=10,
            wrap=tk.WORD,
            bg="white",
            fg=COLORS["text"],
            font=("Segoe UI", 9),
            padx=10,
            pady=10
        )
        self.weather_recommendations.pack(fill=tk.BOTH, expand=True)
        self.weather_recommendations.insert(tk.END, "Farming recommendations based on weather will appear here.")
        self.weather_recommendations.config(state=tk.DISABLED)

    def get_weather_forecast(self):
        location = self.location_var.get()
        period = self.forecast_var.get()

        if not location:
            messagebox.showerror("Error", "Please enter a location")
            return

        forecast = self.weather_model.predict(location, period)

        self.forecast_text.config(state=tk.NORMAL)
        self.forecast_text.delete(1.0, tk.END)
        self.forecast_text.insert(tk.END, forecast)
        self.forecast_text.config(state=tk.DISABLED)

        recommendations = self.generate_weather_recommendations(forecast)
        self.weather_recommendations.config(state=tk.NORMAL)
        self.weather_recommendations.delete(1.0, tk.END)
        self.weather_recommendations.insert(tk.END, recommendations)
        self.weather_recommendations.config(state=tk.DISABLED)

    def generate_weather_recommendations(self, forecast):
        if "heavy rain" in forecast.lower():
            return "⚠️ Weather Alert: Heavy Rain Expected ⚠️\n\nRecommendations:\n• Delay planting until after heavy rains\n• Ensure proper drainage in fields\n• Consider cover crops to prevent erosion"
        elif "drought" in forecast.lower():
            return "⚠️ Weather Alert: Drought Conditions ⚠️\n\nRecommendations:\n• Select drought-resistant crops\n• Implement water conservation techniques\n• Consider mulching to retain soil moisture"
        else:
            return "✅ Weather Conditions Normal\n\nRecommendations:\n• Proceed with normal planting schedule\n• Monitor local weather updates"

    def create_pest_id_tab(self):
        tab = tk.Frame(self.notebook, bg=COLORS["light_bg"])
        self.notebook.add(tab, text="Pest Identification")

        # Upload frame
        upload_frame = tk.Frame(tab, bg=COLORS["light_bg"])
        upload_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(upload_frame,
                 text="Upload Image of Affected Crop:",
                 bg=COLORS["light_bg"],
                 fg=COLORS["text"],
                 font=("Segoe UI", 9)).pack(anchor="w")

        self.image_path = tk.StringVar()
        upload_btn = ModernButton(
            upload_frame,
            text="Select Image",
            command=self.upload_image
        )
        upload_btn.pack(pady=5)

        # Image display
        self.image_label = tk.Label(
            tab,
            bg=COLORS["light_bg"],
            text="No image selected",
            fg=COLORS["text"],
            font=("Segoe UI", 9)
        )
        self.image_label.pack(pady=5)

        # Identify button
        identify_btn = ModernButton(
            tab,
            text="Identify Pest/Disease",
            command=self.identify_pest
        )
        identify_btn.pack(pady=10)

        # Results frame
        result_frame = tk.Frame(tab, bg=COLORS["light_bg"])
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(result_frame,
                 text="Identification Results:",
                 bg=COLORS["light_bg"],
                 fg=COLORS["text"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")

        self.pest_result = tk.Text(
            result_frame,
            height=15,
            wrap=tk.WORD,
            bg="white",
            fg=COLORS["text"],
            font=("Segoe UI", 9),
            padx=10,
            pady=10
        )
        self.pest_result.pack(fill=tk.BOTH, expand=True)
        self.pest_result.insert(tk.END, "Pest/disease identification results will appear here.")
        self.pest_result.config(state=tk.DISABLED)

    def upload_image(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if filepath:
            self.image_path.set(filepath)
            self.display_image(filepath)

    def display_image(self, filepath):
        try:
            img = Image.open(filepath)
            img.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.image_label.config(text="")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def identify_pest(self):
        if not self.image_path.get():
            messagebox.showerror("Error", "Please select an image first")
            return

        prediction = self.pest_model.predict(self.image_path.get())

        self.pest_result.config(state=tk.NORMAL)
        self.pest_result.delete(1.0, tk.END)

        if prediction in self.pest_db:
            info = self.pest_db[prediction]
            result = f"🔍 Identification: {prediction}\n\n"
            result += f"💊 Solution:\n{info['solution']}\n\n"
            result += f"🛡️ Prevention:\n{info['prevention']}"
        else:
            result = f"🔍 Identification: {prediction}\n\n"
            result += "ℹ️ No specific information found in database.\n"
            result += "Please contact your agricultural extension officer for assistance."

        self.pest_result.insert(tk.END, result)
        self.pest_result.config(state=tk.DISABLED)

    def create_crop_advice_tab(self):
        tab = tk.Frame(self.notebook, bg=COLORS["light_bg"])
        self.notebook.add(tab, text="Crop Advice")

        # Input frame
        input_frame = tk.Frame(tab, bg=COLORS["light_bg"])
        input_frame.pack(fill=tk.X, padx=20, pady=10)

        # Location
        tk.Label(input_frame,
                 text="Location:",
                 bg=COLORS["light_bg"],
                 fg=COLORS["text"],
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=5)

        self.crop_location_var = tk.StringVar(value="Nairobi")
        location_entry = ttk.Entry(
            input_frame,
            textvariable=self.crop_location_var,
            font=("Segoe UI", 9)
        )
        location_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Soil type
        tk.Label(input_frame,
                 text="Soil Type:",
                 bg=COLORS["light_bg"],
                 fg=COLORS["text"],
                 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=5)

        self.crop_soil_var = tk.StringVar()
        soil_combo = ttk.Combobox(
            input_frame,
            textvariable=self.crop_soil_var,
            values=self.soil_types,
            font=("Segoe UI", 9),
            state="readonly"
        )
        soil_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Season
        tk.Label(input_frame,
                 text="Current Season:",
                 bg=COLORS["light_bg"],
                 fg=COLORS["text"],
                 font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", pady=5)

        self.season_var = tk.StringVar()
        season_combo = ttk.Combobox(
            input_frame,
            textvariable=self.season_var,
            values=["Dry", "Rainy", "Planting", "Harvest"],
            font=("Segoe UI", 9),
            state="readonly"
        )
        season_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Get advice button
        advice_btn = ModernButton(
            input_frame,
            text="Get Crop Advice",
            command=self.generate_crop_advice
        )
        advice_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Results frame
        result_frame = tk.Frame(tab, bg=COLORS["light_bg"])
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.crop_advice_text = tk.Text(
            result_frame,
            height=20,
            wrap=tk.WORD,
            bg="white",
            fg=COLORS["text"],
            font=("Segoe UI", 9),
            padx=10,
            pady=10
        )
        self.crop_advice_text.pack(fill=tk.BOTH, expand=True)
        self.crop_advice_text.insert(tk.END, "Comprehensive crop advice will appear here.")
        self.crop_advice_text.config(state=tk.DISABLED)

    def generate_crop_advice(self):
        if not all([self.crop_location_var.get(),
                    self.crop_soil_var.get(),
                    self.season_var.get()]):
            messagebox.showerror("Error", "Please fill all fields")
            return

        location = self.crop_location_var.get()
        forecast = self.weather_model.predict(location, "Seasonal")

        soil_type = self.crop_soil_var.get()
        ph = 6.5  # Default for demo
        season = self.season_var.get()

        suitable_crops = []
        for crop, data in self.crop_db.items():
            if (soil_type in data["soil"] and
                    self.is_ph_suitable(ph, crop) and
                    self.is_season_suitable(season, crop)):
                suitable_crops.append(crop)

        advice = f"🌾 Comprehensive Crop Advice for {location} 🌾\n\n"
        advice += f"📌 Location: {location}\n"
        advice += f"🌱 Soil Type: {soil_type}\n"
        advice += f"🌦️ Season: {season}\n\n"
        advice += "📡 Weather Outlook:\n"
        advice += forecast + "\n\n"
        advice += "✅ Recommended Crops:\n"

        if suitable_crops:
            for crop in suitable_crops:
                advice += f"\n⭐ {crop}:\n"
                advice += f"   • {self.get_crop_details(crop)}\n"
        else:
            advice += "No suitable crops found for current conditions.\n"
            advice += "Consider adjusting soil parameters or selecting different season."

        self.crop_advice_text.config(state=tk.NORMAL)
        self.crop_advice_text.delete(1.0, tk.END)
        self.crop_advice_text.insert(tk.END, advice)
        self.crop_advice_text.config(state=tk.DISABLED)

    def is_ph_suitable(self, ph, crop):
        return 5.5 <= ph <= 7.5  # Simplified for demo

    def is_season_suitable(self, season, crop):
        if season == "Dry":
            return self.crop_db[crop]["rainfall"] in ["low", "medium"]
        return True

    def get_crop_details(self, crop):
        data = self.crop_db[crop]
        return (f"Prefers {data['rainfall']} rainfall, "
                f"temp range {data['temp_range'][0]}–{data['temp_range'][1]}°C, "
                f"best in {', '.join(data['soil'])} soil")


class WeatherModel:
    def predict(self, location, period):
        forecasts = {
            "7-day": f"Weather forecast for {location} next 7 days:\n"
                     "• Day 1: Sunny, 28°C\n• Day 2: Partly cloudy, 26°C\n"
                     "• Day 3: Light rain, 24°C\n• Day 4: Thunderstorms, 22°C\n"
                     "• Day 5: Cloudy, 25°C\n• Day 6: Sunny, 27°C\n"
                     "• Day 7: Sunny, 29°C",
            "14-day": f"14-day forecast for {location}:\n"
                      "First week: Mixed sun and rain, temps 24-28°C\n"
                      "Second week: Drier conditions, temps 26-30°C",
            "Seasonal": f"Seasonal outlook for {location}:\n"
                        "Expected above-average rainfall this season.\n"
                        "Temperatures will be slightly higher than normal."
        }
        return forecasts.get(period, "Forecast not available")


class PestModel:
    def predict(self, image_path):
        pests = ["Aphids", "Cutworms", "Powdery Mildew", "Leaf Rust"]
        return random.choice(pests)


if __name__ == "__main__":
    root = tk.Tk()
    app = FarmingAdvisorySystem(root)
    root.mainloop()