#!/usr/bin/env python3
"""
NEXUS v2.0 - Suite d'outils médicaux et paramédicaux
Développé par Sidoine B. - Version modernisée

Application complète pour le personnel médical, paramédical et de laboratoire
avec interface graphique moderne et calculs automatisés.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PatientData:
    """Structure pour stocker les données patient"""
    nom: str = ""
    prenom: str = ""
    age: int = 0
    sexe: str = ""
    poids: float = 0.0
    taille: float = 0.0
    antecedents: str = ""
    
    def get_bmi(self) -> float:
        """Calcule l'IMC"""
        if self.poids > 0 and self.taille > 0:
            return self.poids / ((self.taille / 100) ** 2)
        return 0.0

class MedicalCalculators:
    """Classe contenant tous les calculateurs médicaux"""
    
    @staticmethod
    def glasgow_coma_scale(eyes: int, verbal: int, motor: int) -> Tuple[int, str]:
        """Calcule le score de Glasgow"""
        total = eyes + verbal + motor
        
        if total >= 15:
            interpretation = "Normal"
        elif total >= 13:
            interpretation = "Traumatisme crânien léger"
        elif total >= 9:
            interpretation = "Traumatisme crânien modéré"
        else:
            interpretation = "Traumatisme crânien sévère"
            
        return total, interpretation
    
    @staticmethod
    def apgar_score(freq_card: int, resp: int, tonus: int, reflexes: int, coloration: int) -> Tuple[int, str]:
        """Calcule le score d'APGAR"""
        total = freq_card + resp + tonus + reflexes + coloration
        
        if total >= 8:
            interpretation = "Excellent état"
        elif total >= 4:
            interpretation = "État modérément altéré"
        else:
            interpretation = "Détresse sévère"
            
        return total, interpretation
    
    @staticmethod
    def nih_stroke_scale(**kwargs) -> Tuple[int, str]:
        """Calcule le score NIH Stroke Scale"""
        score_items = [
            kwargs.get('vigilance', 0),
            kwargs.get('orientation', 0),
            kwargs.get('commandes', 0),
            kwargs.get('oculomotricite', 0),
            kwargs.get('champ_visuel', 0),
            kwargs.get('paralysie_faciale', 0),
            kwargs.get('motricite_ms', 0),
            kwargs.get('motricite_mi', 0),
            kwargs.get('ataxie', 0),
            kwargs.get('sensibilite', 0),
            kwargs.get('langage', 0),
            kwargs.get('dysarthrie', 0),
            kwargs.get('extinction', 0)
        ]
        
        total = sum(score_items)
        
        if total == 0:
            interpretation = "Pas de signe d'AVC"
        elif total < 5:
            interpretation = "AVC mineur"
        elif total < 16:
            interpretation = "AVC modéré"
        elif total < 21:
            interpretation = "AVC sévère"
        else:
            interpretation = "AVC très sévère"
            
        return total, interpretation
    
    @staticmethod
    def convert_glucose(value: float, from_unit: str) -> Dict[str, float]:
        """Convertit les unités de glycémie"""
        if from_unit == "g/L":
            mmol_l = value * 5.55
            mg_dl = value * 100
        elif from_unit == "mmol/L":
            g_l = value / 5.55
            mg_dl = value * 18.01
        else:  # mg/dL
            g_l = value / 100
            mmol_l = value / 18.01
            
        return {
            "g/L": g_l if from_unit != "g/L" else value,
            "mmol/L": mmol_l if from_unit != "mmol/L" else value,
            "mg/dL": mg_dl if from_unit != "mg/dL" else value
        }
    
    @staticmethod
    def cardiac_risk_framingham(age: int, sexe: str, cholesterol: float, hdl: float, 
                               systolic_bp: int, smoker: bool, diabetes: bool) -> Tuple[float, str]:
        """Calcule le risque cardiovasculaire selon Framingham"""
        # Algorithme simplifié de Framingham
        points = 0
        
        # Points selon l'âge
        if sexe.lower() == "homme":
            if age >= 70: points += 8
            elif age >= 60: points += 6
            elif age >= 50: points += 4
            elif age >= 40: points += 2
        else:  # femme
            if age >= 70: points += 8
            elif age >= 60: points += 6
            elif age >= 50: points += 3
            elif age >= 40: points += 1
        
        # Cholestérol total
        if cholesterol >= 280: points += 3
        elif cholesterol >= 240: points += 2
        elif cholesterol >= 200: points += 1
        
        # HDL
        if hdl < 35: points += 2
        elif hdl < 45: points += 1
        elif hdl >= 60: points -= 1
        
        # Tension artérielle
        if systolic_bp >= 160: points += 2
        elif systolic_bp >= 140: points += 1
        
        # Facteurs de risque
        if smoker: points += 2
        if diabetes: points += 2
        
        # Conversion en pourcentage de risque
        risk_percent = min(max(points * 2, 0), 40)  # Limité entre 0 et 40%
        
        if risk_percent < 10:
            interpretation = "Risque faible"
        elif risk_percent < 20:
            interpretation = "Risque modéré"
        else:
            interpretation = "Risque élevé"
            
        return risk_percent, interpretation

class NormalValues:
    """Valeurs normales biologiques et constantes"""
    
    HEMATOLOGIE = {
        "Hémoglobine H": (13.0, 17.0, "g/dL"),
        "Hémoglobine F": (11.5, 15.5, "g/dL"),
        "Hématocrite H": (40, 50, "%"),
        "Hématocrite F": (35, 45, "%"),
        "Globules blancs": (4000, 10000, "/mm³"),
        "Plaquettes": (150000, 400000, "/mm³"),
        "VGM": (82, 98, "fL"),
        "TCMH": (27, 32, "pg"),
        "CCMH": (32, 36, "g/dL")
    }
    
    BIOCHIMIE = {
        "Créatinine H": (0.7, 1.3, "mg/dL"),
        "Créatinine F": (0.6, 1.1, "mg/dL"),
        "Urée": (15, 45, "mg/dL"),
        "Glucose à jeun": (70, 110, "mg/dL"),
        "Cholestérol total": (0, 200, "mg/dL"),
        "Triglycérides": (0, 150, "mg/dL"),
        "HDL H": (40, 999, "mg/dL"),
        "HDL F": (50, 999, "mg/dL"),
        "LDL": (0, 130, "mg/dL"),
        "Bilirubine totale": (0.2, 1.2, "mg/dL"),
        "ASAT": (5, 40, "UI/L"),
        "ALAT": (5, 45, "UI/L"),
        "GammaGT": (10, 55, "UI/L"),
        "CRP": (0, 3, "mg/L")
    }
    
    GAZOMETRIE = {
        "pH": (7.35, 7.45, ""),
        "PCO2": (35, 45, "mmHg"),
        "PO2": (80, 100, "mmHg"),
        "HCO3-": (22, 28, "mmol/L"),
        "SaO2": (95, 100, "%"),
        "Lactates": (0.5, 2.0, "mmol/L")
    }
    
    CONSTANTES = {
        "FC adulte": (60, 100, "bpm"),
        "FC enfant": (80, 120, "bpm"),
        "FC bébé": (100, 160, "bpm"),
        "TA systolique": (100, 140, "mmHg"),
        "TA diastolique": (60, 90, "mmHg"),
        "FR adulte": (12, 20, "/min"),
        "FR enfant": (16, 25, "/min"),
        "Température": (36.1, 37.8, "°C"),
        "SpO2": (95, 100, "%")
    }

class SplashScreenMedical:
    """Écran de démarrage médical"""
    
    def __init__(self, main_callback):
        self.main_callback = main_callback
        self.root = tk.Toplevel()
        self.setup_splash()
        self.animate()
    
    def setup_splash(self):
        """Configure l'écran de démarrage"""
        self.root.title("NEXUS Medical Suite")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f8ff')
        
        # Centrer la fenêtre
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 500) // 2
        y = (self.root.winfo_screenheight() - 350) // 2
        self.root.geometry(f"500x350+{x}+{y}")
        
        self.root.overrideredirect(True)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill='both', expand=True)
        
        # Logo médical
        title_label = tk.Label(
            main_frame,
            text="🏥 NEXUS",
            font=('Arial', 32, 'bold'),
            fg='#2c5aa0',
            bg='#f0f8ff'
        )
        title_label.pack(pady=30)
        
        # Sous-titre
        subtitle_label = tk.Label(
            main_frame,
            text="Suite Médicale & Paramedicale",
            font=('Arial', 14),
            fg='#4a90e2',
            bg='#f0f8ff'
        )
        subtitle_label.pack()
        
        # Version
        version_label = tk.Label(
            main_frame,
            text="Version 2.0 - Édition Professionnelle",
            font=('Arial', 10),
            fg='#666666',
            bg='#f0f8ff'
        )
        version_label.pack(pady=5)
        
        # Barre de progression
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=350,
            mode='determinate'
        )
        progress_bar.pack(pady=30)
        
        # Status
        self.status_label = tk.Label(
            main_frame,
            text="Initialisation des modules médicaux...",
            font=('Arial', 10),
            fg='#666666',
            bg='#f0f8ff'
        )
        self.status_label.pack()
        
        # Copyright
        copyright_label = tk.Label(
            main_frame,
            text="Développé par Sidoine B. - Sous licence GNU GPL v3",
            font=('Arial', 8),
            fg='#888888',
            bg='#f0f8ff'
        )
        copyright_label.pack(side='bottom', pady=15)
    
    def animate(self):
        """Animation de chargement"""
        steps = [
            (15, "Chargement des calculateurs médicaux..."),
            (30, "Initialisation des valeurs normales..."),
            (45, "Configuration des modules paramédicaux..."),
            (60, "Chargement de l'interface utilisateur..."),
            (75, "Préparation des outils de laboratoire..."),
            (90, "Finalisation de l'installation..."),
            (100, "NEXUS prêt à l'emploi !")
        ]
        
        def animate_step(index):
            if index < len(steps):
                progress, status = steps[index]
                self.progress_var.set(progress)
                self.status_label.config(text=status)
                self.root.after(600, lambda: animate_step(index + 1))
            else:
                self.root.after(1000, self.close_splash)
        
        animate_step(0)
    
    def close_splash(self):
        """Ferme le splash et lance l'application principale"""
        self.root.destroy()
        self.main_callback()

class NexusApp:
    """Application principale NEXUS"""
    
    def __init__(self):
        self.root = None
        self.patient_data = PatientData()
        self.calculators = MedicalCalculators()
        self.normal_values = NormalValues()
        self.setup_styles()
        
    def setup_styles(self):
        """Configure les styles de l'application"""
        self.colors = {
            'primary': '#2c5aa0',
            'secondary': '#4a90e2',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#f8f9fa',
            'dark': '#2c3e50',
            'background': '#f0f8ff'
        }
    
    def start_app(self):
        """Démarre l'application avec splash screen"""
        SplashScreenMedical(self.create_main_window)
    
    def create_main_window(self):
        """Crée la fenêtre principale"""
        self.root = tk.Tk()
        self.root.title("🏥 NEXUS - Suite Médicale v2.0")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        self.root.configure(bg=self.colors['background'])
        
        # Configuration de la grille
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.create_menu()
        self.create_header()
        self.create_main_interface()
        self.create_status_bar()
        
        # Centrer la fenêtre
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 1200) // 2
        y = (self.root.winfo_screenheight() - 800) // 2
        self.root.geometry(f"1200x800+{x}+{y}")
        
        self.root.mainloop()
    
    def create_menu(self):
        """Crée la barre de menu"""
        menubar = tk.Menu(self.root)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nouveau Patient", command=self.new_patient, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Exporter Rapport", command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Menu Calculateurs
        calc_menu = tk.Menu(menubar, tearoff=0)
        calc_menu.add_command(label="Score de Glasgow", command=lambda: self.show_calculator("glasgow"))
        calc_menu.add_command(label="Score APGAR", command=lambda: self.show_calculator("apgar"))
        calc_menu.add_command(label="Score NIH", command=lambda: self.show_calculator("nih"))
        calc_menu.add_separator()
        calc_menu.add_command(label="Conversion Glycémie", command=lambda: self.show_calculator("glucose"))
        calc_menu.add_command(label="Risque Cardiovasculaire", command=lambda: self.show_calculator("cardiac"))
        
        # Menu Valeurs Normales
        values_menu = tk.Menu(menubar, tearoff=0)
        values_menu.add_command(label="Hématologie", command=lambda: self.show_normal_values("HEMATOLOGIE"))
        values_menu.add_command(label="Biochimie", command=lambda: self.show_normal_values("BIOCHIMIE"))
        values_menu.add_command(label="Gazométrie", command=lambda: self.show_normal_values("GAZOMETRIE"))
        values_menu.add_command(label="Constantes Vitales", command=lambda: self.show_normal_values("CONSTANTES"))
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Guide Utilisateur", command=self.show_help)
        help_menu.add_command(label="À propos", command=self.show_about)
        
        menubar.add_cascade(label="Fichier", menu=file_menu)
        menubar.add_cascade(label="Calculateurs", menu=calc_menu)
        menubar.add_cascade(label="Valeurs Normales", menu=values_menu)
        menubar.add_cascade(label="Aide", menu=help_menu)
        
        self.root.config(menu=menubar)
        
        # Raccourcis clavier
        self.root.bind('<Control-n>', lambda e: self.new_patient())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
    
    def create_header(self):
        """Crée l'en-tête avec informations patient"""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        header_frame.grid(row=0, column=0, sticky='ew', padx=0, pady=0)
        header_frame.grid_propagate(False)
        
        # Titre principal
        title_label = tk.Label(header_frame, text="🏥 NEXUS - Suite Médicale", 
                              font=('Arial', 20, 'bold'), fg='white', bg=self.colors['primary'])
        title_label.pack(side='left', padx=20, pady=10)
        
        # Informations patient
        patient_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        patient_frame.pack(side='right', padx=20, pady=10)
        
        self.patient_info_label = tk.Label(patient_frame, text="Aucun patient sélectionné", 
                                          font=('Arial', 12), fg='white', bg=self.colors['primary'])
        self.patient_info_label.pack()
        
        # Bouton nouveau patient
        new_patient_btn = tk.Button(patient_frame, text="Nouveau Patient", 
                                   command=self.new_patient, bg='white', fg=self.colors['primary'],
                                   font=('Arial', 10, 'bold'))
        new_patient_btn.pack(pady=5)
    
    def create_main_interface(self):
        """Crée l'interface principale avec onglets"""
        # Notebook pour les onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        
        # Onglet Calculateurs
        self.create_calculators_tab()
        
        # Onglet Valeurs Normales
        self.create_normal_values_tab()
        
        # Onglet Outils
        self.create_tools_tab()
        
        # Onglet Rapports
        self.create_reports_tab()
    
    def create_calculators_tab(self):
        """Crée l'onglet des calculateurs"""
        calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(calc_frame, text="📊 Calculateurs")
        
        # Frame de gauche - Liste des calculateurs
        left_frame = tk.Frame(calc_frame, bg='white', relief='raised', bd=1)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        calc_frame.grid_columnconfigure(1, weight=1)
        calc_frame.grid_rowconfigure(0, weight=1)
        
        tk.Label(left_frame, text="Calculateurs Disponibles", font=('Arial', 14, 'bold'),
                bg='white').pack(pady=10)
        
        calculators = [
            ("🧠 Score de Glasgow", "glasgow"),
            ("👶 Score APGAR", "apgar"),
            ("🧬 Score NIH (AVC)", "nih"),
            ("🍬 Conversion Glycémie", "glucose"),
            ("❤️ Risque Cardiovasculaire", "cardiac"),
            ("📏 Calcul IMC", "bmi"),
            ("💊 Clairance Créatinine", "creatinine")
        ]
        
        for name, calc_type in calculators:
            btn = tk.Button(left_frame, text=name, 
                           command=lambda t=calc_type: self.show_calculator(t),
                           bg=self.colors['light'], fg=self.colors['dark'],
                           font=('Arial', 11), relief='flat', bd=0,
                           padx=20, pady=8, anchor='w')
            btn.pack(fill='x', padx=10, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors['secondary'], fg='white'))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.colors['light'], fg=self.colors['dark']))
        
        # Frame de droite - Zone de calcul
        self.calc_display_frame = tk.Frame(calc_frame, bg='white', relief='raised', bd=1)
        self.calc_display_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # Message d'accueil
        welcome_label = tk.Label(self.calc_display_frame, 
                                text="Sélectionnez un calculateur dans la liste de gauche",
                                font=('Arial', 14), bg='white', fg=self.colors['dark'])
        welcome_label.pack(expand=True)
    
    def create_normal_values_tab(self):
        """Crée l'onglet des valeurs normales"""
        values_frame = ttk.Frame(self.notebook)
        self.notebook.add(values_frame, text="📋 Valeurs Normales")
        
        # Frame avec onglets secondaires
        values_notebook = ttk.Notebook(values_frame)
        values_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Créer les sous-onglets
        for category_name, category_data in [
            ("Hématologie", self.normal_values.HEMATOLOGIE),
            ("Biochimie", self.normal_values.BIOCHIMIE),
            ("Gazométrie", self.normal_values.GAZOMETRIE),
            ("Constantes", self.normal_values.CONSTANTES)
        ]:
            self.create_values_subtab(values_notebook, category_name, category_data)
    
    def create_values_subtab(self, parent, category_name, data):
        """Crée un sous-onglet de valeurs normales"""
        frame = ttk.Frame(parent)
        parent.add(frame, text=category_name)
        
        # Créer un tableau avec Treeview
        columns = ("Paramètre", "Valeur Normale", "Unité")
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        # Configuration des colonnes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Remplir les données
        for param, (min_val, max_val, unit) in data.items():
            if min_val == max_val:
                value_range = f"{min_val}"
            else:
                value_range = f"{min_val} - {max_val}"
            tree.insert("", "end", values=(param, value_range, unit))
        
        # Pack les widgets
        tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
    
    def create_tools_tab(self):
        """Crée l'onglet des outils"""
        tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(tools_frame, text="🔧 Outils")
        
        # Zone de contenu
        content_frame = tk.Frame(tools_frame, bg='white')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Titre
        tk.Label(content_frame, text="Outils Médicaux", font=('Arial', 18, 'bold'),
                bg='white', fg=self.colors['primary']).pack(pady=20)
        
        # Grille d'outils
        tools_grid = tk.Frame(content_frame, bg='white')
        tools_grid.pack(expand=True)
        
        tools = [
            ("🩺 Algorithme Collier Cervical", self.cervical_collar_algorithm),
            ("💉 Calcul Posologies", self.dosage_calculator),
            ("🔍 Recherche Médicament", self.drug_search),
            ("📊 Graphiques Tendances", self.show_trends)
        ]
        
        row = 0
        col = 0
        for tool_name, tool_func in tools:
            tool_btn = tk.Button(tools_grid, text=tool_name,
                               command=tool_func, bg=self.colors['secondary'],
                               fg='white', font=('Arial', 12, 'bold'),
                               width=25, height=3, relief='raised', bd=2)
            tool_btn.grid(row=row, column=col, padx=15, pady=15)
            
            col += 1
            if col > 1:  # 2 colonnes
                col = 0
                row += 1
    
    def create_reports_tab(self):
        """Crée l'onglet des rapports"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="📄 Rapports")
        
        # Zone de texte pour les rapports
        self.report_text = scrolledtext.ScrolledText(reports_frame, wrap=tk.WORD,
                                                    font=('Courier', 11),
                                                    bg='white', fg='black')
        self.report_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Barre de boutons
        btn_frame = tk.Frame(reports_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(btn_frame, text="Nouveau Rapport", command=self.new_report,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Sauvegarder", command=self.save_report,
                 bg=self.colors['primary'], fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Imprimer", command=self.print_report,
                 bg=self.colors['warning'], fg='white').pack(side='left', padx=5)
    
    def create_status_bar(self):
        """Crée la barre de statut"""
        self.status_bar = tk.Frame(self.root, bg=self.colors['light'], height=30)
        self.status_bar.grid(row=2, column=0, sticky='ew', padx=0, pady=0)
        self.status_bar.grid_propagate(False)
        
        # Status text
        self.status_text = tk.Label(self.status_bar, text="NEXUS prêt", 
                                   bg=self.colors['light'], fg=self.colors['dark'],
                                   font=('Arial', 10))
        self.status_text.pack(side='left', padx=10, pady=5)
        
        # Heure
        self.time_label = tk.Label(self.status_bar, text="", 
                                  bg=self.colors['light'], fg=self.colors['dark'],
                                  font=('Arial', 10))
        self.time_label.pack(side='right', padx=10, pady=5)
        
        self.update_time()
    
    def update_time(self):
        """Met à jour l'heure dans la barre de statut"""
        current_time = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def new_patient(self):
        """Dialogue pour nouveau patient"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nouveau Patient")
        dialog.geometry("400x500")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrer la fenêtre
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 500) // 2
        dialog.geometry(f"400x500+{x}+{y}")
        
        # Titre
        tk.Label(dialog, text="Informations Patient", font=('Arial', 16, 'bold'),
                bg='white', fg=self.colors['primary']).pack(pady=20)
        
        # Frame pour les champs
        fields_frame = tk.Frame(dialog, bg='white')
        fields_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Variables pour les champs
        vars_dict = {}
        
        fields = [
            ("Nom:", "nom"),
            ("Prénom:", "prenom"),
            ("Âge:", "age"),
            ("Poids (kg):", "poids"),
            ("Taille (cm):", "taille")
        ]
        
        for i, (label_text, var_name) in enumerate(fields):
            tk.Label(fields_frame, text=label_text, font=('Arial', 12),
                    bg='white', fg=self.colors['dark']).grid(row=i, column=0, 
                    sticky='w', pady=5)
            
            entry = tk.Entry(fields_frame, font=('Arial', 12), width=20)
            entry.grid(row=i, column=1, pady=5, padx=10)
            vars_dict[var_name] = entry
        
        # Sexe
        tk.Label(fields_frame, text="Sexe:", font=('Arial', 12),
                bg='white', fg=self.colors['dark']).grid(row=len(fields), column=0, 
                sticky='w', pady=5)
        
        sexe_var = tk.StringVar(value="Homme")
        sexe_frame = tk.Frame(fields_frame, bg='white')
        sexe_frame.grid(row=len(fields), column=1, pady=5, sticky='w')
        
        tk.Radiobutton(sexe_frame, text="Homme", variable=sexe_var, value="Homme",
                      bg='white', font=('Arial', 11)).pack(side='left')
        tk.Radiobutton(sexe_frame, text="Femme", variable=sexe_var, value="Femme",
                      bg='white', font=('Arial', 11)).pack(side='left', padx=10)
        
        # Antécédents
        tk.Label(fields_frame, text="Antécédents:", font=('Arial', 12),
                bg='white', fg=self.colors['dark']).grid(row=len(fields)+1, column=0, 
                sticky='nw', pady=5)
        
        antecedents_text = tk.Text(fields_frame, height=4, width=25, font=('Arial', 10))
        antecedents_text.grid(row=len(fields)+1, column=1, pady=5, padx=10)
        
        def save_patient():
            try:
                self.patient_data.nom = vars_dict['nom'].get()
                self.patient_data.prenom = vars_dict['prenom'].get()
                self.patient_data.age = int(vars_dict['age'].get()) if vars_dict['age'].get() else 0
                self.patient_data.poids = float(vars_dict['poids'].get()) if vars_dict['poids'].get() else 0.0
                self.patient_data.taille = float(vars_dict['taille'].get()) if vars_dict['taille'].get() else 0.0
                self.patient_data.sexe = sexe_var.get()
                self.patient_data.antecedents = antecedents_text.get("1.0", tk.END).strip()
                
                # Mettre à jour l'affichage
                patient_info = f"{self.patient_data.prenom} {self.patient_data.nom}"
                if self.patient_data.age > 0:
                    patient_info += f" - {self.patient_data.age} ans"
                if self.patient_data.get_bmi() > 0:
                    patient_info += f" - IMC: {self.patient_data.get_bmi():.1f}"
                
                self.patient_info_label.config(text=patient_info)
                self.status_text.config(text=f"Patient {patient_info} enregistré")
                
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez vérifier les données numériques")
        
        # Boutons
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Enregistrer", command=save_patient,
                 bg=self.colors['success'], fg='white', font=('Arial', 12, 'bold'),
                 width=12).pack(side='left', padx=10)
        tk.Button(btn_frame, text="Annuler", command=dialog.destroy,
                 bg=self.colors['danger'], fg='white', font=('Arial', 12, 'bold'),
                 width=12).pack(side='left', padx=10)
    
    def show_calculator(self, calc_type):
        """Affiche le calculateur sélectionné"""
        # Nettoyer le frame d'affichage
        for widget in self.calc_display_frame.winfo_children():
            widget.destroy()
        
        if calc_type == "glasgow":
            self.create_glasgow_calculator()
        elif calc_type == "apgar":
            self.create_apgar_calculator()
        elif calc_type == "nih":
            self.create_nih_calculator()
        elif calc_type == "glucose":
            self.create_glucose_calculator()
        elif calc_type == "cardiac":
            self.create_cardiac_calculator()
        elif calc_type == "bmi":
            self.create_bmi_calculator()
        elif calc_type == "creatinine":
            self.create_creatinine_calculator()
    
    def create_glasgow_calculator(self):
        """Crée le calculateur de Glasgow"""
        tk.Label(self.calc_display_frame, text="Score de Glasgow", 
                font=('Arial', 18, 'bold'), bg='white', fg=self.colors['primary']).pack(pady=20)
        
        # Variables
        eyes_var = tk.IntVar(value=4)
        verbal_var = tk.IntVar(value=5)
        motor_var = tk.IntVar(value=6)
        
        # Frame principal
        main_frame = tk.Frame(self.calc_display_frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Ouverture des yeux
        eyes_frame = tk.LabelFrame(main_frame, text="Ouverture des yeux", 
                                  font=('Arial', 12, 'bold'), bg='white', fg=self.colors['primary'])
        eyes_frame.pack(fill='x', pady=10)
        
        eyes_options = [
            (4, "Spontanée"),
            (3, "À la demande"),
            (2, "À la douleur"),
            (1, "Aucune")
        ]
        
        for value, text in eyes_options:
            tk.Radiobutton(eyes_frame, text=f"{value} - {text}", variable=eyes_var, 
                          value=value, bg='white', font=('Arial', 11)).pack(anchor='w', padx=10)
        
        # Réponse verbale
        verbal_frame = tk.LabelFrame(main_frame, text="Réponse verbale", 
                                    font=('Arial', 12, 'bold'), bg='white', fg=self.colors['primary'])
        verbal_frame.pack(fill='x', pady=10)
        
        verbal_options = [
            (5, "Orientée"),
            (4, "Confuse"),
            (3, "Inappropriée"),
            (2, "Incompréhensible"),
            (1, "Aucune")
        ]
        
        for value, text in verbal_options:
            tk.Radiobutton(verbal_frame, text=f"{value} - {text}", variable=verbal_var, 
                          value=value, bg='white', font=('Arial', 11)).pack(anchor='w', padx=10)
        
        # Réponse motrice
        motor_frame = tk.LabelFrame(main_frame, text="Réponse motrice", 
                                   font=('Arial', 12, 'bold'), bg='white', fg=self.colors['primary'])
        motor_frame.pack(fill='x', pady=10)
        
        motor_options = [
            (6, "Aux ordres"),
            (5, "Orientée"),
            (4, "Évitement"),
            (3, "Flexion stéréotypée"),
            (2, "Extension stéréotypée"),
            (1, "Aucune")
        ]
        
        for value, text in motor_options:
            tk.Radiobutton(motor_frame, text=f"{value} - {text}", variable=motor_var, 
                          value=value, bg='white', font=('Arial', 11)).pack(anchor='w', padx=10)
        
        # Résultat
        result_frame = tk.Frame(main_frame, bg=self.colors['light'], relief='raised', bd=2)
        result_frame.pack(fill='x', pady=20)
        
        result_label = tk.Label(result_frame, text="Résultat: ", 
                               font=('Arial', 14, 'bold'), bg=self.colors['light'])
        result_label.pack(pady=10)
        
        def calculate_glasgow():
            total, interpretation = self.calculators.glasgow_coma_scale(
                eyes_var.get(), verbal_var.get(), motor_var.get()
            )
            
            color = self.colors['success'] if total >= 13 else self.colors['warning'] if total >= 9 else self.colors['danger']
            
            result_text = f"Score: {total}/15\n{interpretation}"
            result_label.config(text=result_text, fg=color)
            
            # Ajouter au rapport
            self.add_to_report(f"Score de Glasgow: {total}/15 - {interpretation}")
        
        # Bouton calcul
        tk.Button(main_frame, text="Calculer", command=calculate_glasgow,
                 bg=self.colors['primary'], fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(pady=10)
    
    def create_apgar_calculator(self):
        """Crée le calculateur APGAR"""
        tk.Label(self.calc_display_frame, text="Score APGAR", 
                font=('Arial', 18, 'bold'), bg='white', fg=self.colors['primary']).pack(pady=20)
        
        # Variables
        freq_card_var = tk.IntVar(value=2)
        resp_var = tk.IntVar(value=2)
        tonus_var = tk.IntVar(value=2)
        reflexes_var = tk.IntVar(value=2)
        coloration_var = tk.IntVar(value=2)
        
        main_frame = tk.Frame(self.calc_display_frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Configuration des critères
        criteria = [
            ("Fréquence cardiaque", freq_card_var, [
                (2, "> 100 bpm"), (1, "< 100 bpm"), (0, "Absente")
            ]),
            ("Respiration", resp_var, [
                (2, "Régulière, cri vigoureux"), (1, "Lente, irrégulière"), (0, "Absente")
            ]),
            ("Tonus musculaire", tonus_var, [
                (2, "Actif"), (1, "Flexion des extrémités"), (0, "Flasque")
            ]),
            ("Réflexes", reflexes_var, [
                (2, "Cri vigoureux"), (1, "Grimace"), (0, "Aucune réponse")
            ]),
            ("Coloration", coloration_var, [
                (2, "Rose"), (1, "Cyanose extrémités"), (0, "Cyanose généralisée")
            ])
        ]
        
        for title, var, options in criteria:
            frame = tk.LabelFrame(main_frame, text=title, 
                                 font=('Arial', 11, 'bold'), bg='white', fg=self.colors['primary'])
            frame.pack(fill='x', pady=5)
            
            for value, text in options:
                tk.Radiobutton(frame, text=f"{value} - {text}", variable=var, 
                              value=value, bg='white', font=('Arial', 10)).pack(anchor='w', padx=10)
        
        # Résultat
        result_frame = tk.Frame(main_frame, bg=self.colors['light'], relief='raised', bd=2)
        result_frame.pack(fill='x', pady=15)
        
        result_label = tk.Label(result_frame, text="Résultat: ", 
                               font=('Arial', 14, 'bold'), bg=self.colors['light'])
        result_label.pack(pady=10)
        
        def calculate_apgar():
            total, interpretation = self.calculators.apgar_score(
                freq_card_var.get(), resp_var.get(), tonus_var.get(),
                reflexes_var.get(), coloration_var.get()
            )
            
            color = self.colors['success'] if total >= 8 else self.colors['warning'] if total >= 4 else self.colors['danger']
            
            result_text = f"Score APGAR: {total}/10\n{interpretation}"
            result_label.config(text=result_text, fg=color)
            
            self.add_to_report(f"Score APGAR: {total}/10 - {interpretation}")
        
        tk.Button(main_frame, text="Calculer", command=calculate_apgar,
                 bg=self.colors['primary'], fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(pady=10)
    
    def create_glucose_calculator(self):
        """Crée le convertisseur de glycémie"""
        tk.Label(self.calc_display_frame, text="Conversion Glycémie", 
                font=('Arial', 18, 'bold'), bg='white', fg=self.colors['primary']).pack(pady=20)
        
        main_frame = tk.Frame(self.calc_display_frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Entrée
        input_frame = tk.LabelFrame(main_frame, text="Valeur à convertir", 
                                   font=('Arial', 12, 'bold'), bg='white', fg=self.colors['primary'])
        input_frame.pack(fill='x', pady=15)
        
        tk.Label(input_frame, text="Valeur:", bg='white', font=('Arial', 12)).pack(anchor='w', padx=10, pady=5)
        value_entry = tk.Entry(input_frame, font=('Arial', 12), width=15)
        value_entry.pack(padx=10)
        
        tk.Label(input_frame, text="Unité d'origine:", bg='white', font=('Arial', 12)).pack(anchor='w', padx=10, pady=5)
        unit_var = tk.StringVar(value="g/L")
        unit_frame = tk.Frame(input_frame, bg='white')
        unit_frame.pack(padx=10, pady=5)
        
        for unit in ["g/L", "mmol/L", "mg/dL"]:
            tk.Radiobutton(unit_frame, text=unit, variable=unit_var, value=unit,
                          bg='white', font=('Arial', 11)).pack(side='left', padx=10)
        
        # Résultats
        results_frame = tk.LabelFrame(main_frame, text="Conversions", 
                                     font=('Arial', 12, 'bold'), bg='white', fg=self.colors['primary'])
        results_frame.pack(fill='x', pady=15)
        
        results_text = tk.Text(results_frame, height=8, width=50, font=('Courier', 11),
                              bg=self.colors['light'], state='disabled')
        results_text.pack(padx=10, pady=10)
        
        def convert_glucose():
            try:
                value = float(value_entry.get())
                unit = unit_var.get()
                
                conversions = self.calculators.convert_glucose(value, unit)
                
                results_text.config(state='normal')
                results_text.delete(1.0, tk.END)
                
                results_text.insert(tk.END, "CONVERSIONS GLYCÉMIE\n")
                results_text.insert(tk.END, "=" * 30 + "\n\n")
                
                for conv_unit, conv_value in conversions.items():
                    results_text.insert(tk.END, f"{conv_unit:>8}: {conv_value:>8.2f}\n")
                
                results_text.insert(tk.END, "\n" + "=" * 30 + "\n")
                results_text.insert(tk.END, "INTERPRÉTATION:\n")
                
                # Interprétation (en g/L)
                g_l_value = conversions["g/L"]
                if g_l_value < 0.7:
                    interpretation = "Hypoglycémie sévère"
                    color = "red"
                elif g_l_value < 1.0:
                    interpretation = "Hypoglycémie modérée"
                    color = "orange"
                elif g_l_value <= 1.26:
                    interpretation = "Normal à jeun"
                    color = "green"
                elif g_l_value <= 2.0:
                    interpretation = "Hyperglycémie modérée"
                    color = "orange"
                else:
                    interpretation = "Hyperglycémie sévère"
                    color = "red"
                
                results_text.insert(tk.END, f"{interpretation}\n")
                
                results_text.config(state='disabled')
                
                self.add_to_report(f"Glycémie: {value} {unit} = {g_l_value:.2f} g/L - {interpretation}")
                
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer une valeur numérique valide")
        
        tk.Button(main_frame, text="Convertir", command=convert_glucose,
                 bg=self.colors['primary'], fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(pady=15)
    
    def create_cardiac_calculator(self):
        """Crée le calculateur de risque cardiovasculaire"""
        tk.Label(self.calc_display_frame, text="Risque Cardiovasculaire", 
                font=('Arial', 18, 'bold'), bg='white', fg=self.colors['primary']).pack(pady=20)
        
        main_frame = tk.Frame(self.calc_display_frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Si patient enregistré, préremplir
        age_var = tk.IntVar(value=self.patient_data.age if self.patient_data.age > 0 else 50)
        sexe_var = tk.StringVar(value=self.patient_data.sexe if self.patient_data.sexe else "Homme")
        
        # Variables
        cholesterol_var = tk.DoubleVar(value=200)
        hdl_var = tk.DoubleVar(value=50)
        systolic_var = tk.IntVar(value=120)
        smoker_var = tk.BooleanVar()
        diabetes_var = tk.BooleanVar()
        
        # Interface
        params_frame = tk.LabelFrame(main_frame, text="Paramètres du patient", 
                                    font=('Arial', 12, 'bold'), bg='white', fg=self.colors['primary'])
        params_frame.pack(fill='x', pady=10)
        
        # Grille de paramètres
        params = [
            ("Âge:", age_var, "ans"),
            ("Cholestérol total:", cholesterol_var, "mg/dL"),
            ("HDL:", hdl_var, "mg/dL"),
            ("Tension systolique:", systolic_var, "mmHg")
        ]
        
        for i, (label, var, unit) in enumerate(params):
            tk.Label(params_frame, text=label, bg='white', font=('Arial', 11)).grid(
                row=i, column=0, sticky='w', padx=10, pady=5)
            tk.Entry(params_frame, textvariable=var, font=('Arial', 11), width=10).grid(
                row=i, column=1, padx=5, pady=5)
            tk.Label(params_frame, text=unit, bg='white', font=('Arial', 11)).grid(
                row=i, column=2, sticky='w', padx=5, pady=5)
        
        # Sexe
        tk.Label(params_frame, text="Sexe:", bg='white', font=('Arial', 11)).grid(
            row=len(params), column=0, sticky='w', padx=10, pady=5)
        sexe_frame = tk.Frame(params_frame, bg='white')
        sexe_frame.grid(row=len(params), column=1, columnspan=2, sticky='w', padx=5, pady=5)
        
        tk.Radiobutton(sexe_frame, text="Homme", variable=sexe_var, value="Homme",
                      bg='white', font=('Arial', 11)).pack(side='left')
        tk.Radiobutton(sexe_frame, text="Femme", variable=sexe_var, value="Femme",
                      bg='white', font=('Arial', 11)).pack(side='left', padx=10)
        
        # Facteurs de risque
        factors_frame = tk.LabelFrame(main_frame, text="Facteurs de risque", 
                                     font=('Arial', 12, 'bold'), bg='white', fg=self.colors['primary'])
        factors_frame.pack(fill='x', pady=10)
        
        tk.Checkbutton(factors_frame, text="Tabagisme", variable=smoker_var,
                      bg='white', font=('Arial', 11)).pack(anchor='w', padx=10, pady=2)
        tk.Checkbutton(factors_frame, text="Diabète", variable=diabetes_var,
                      bg='white', font=('Arial', 11)).pack(anchor='w', padx=10, pady=2)
        
        # Résultat
        result_frame = tk.Frame(main_frame, bg=self.colors['light'], relief='raised', bd=2)
        result_frame.pack(fill='x', pady=15)
        
        result_label = tk.Label(result_frame, text="Résultat: ", 
                               font=('Arial', 14, 'bold'), bg=self.colors['light'])
        result_label.pack(pady=10)
        
        def calculate_risk():
            try:
                risk_percent, interpretation = self.calculators.cardiac_risk_framingham(
                    age_var.get(), sexe_var.get(), cholesterol_var.get(),
                    hdl_var.get(), systolic_var.get(), smoker_var.get(), diabetes_var.get()
                )
                
                color = self.colors['success'] if risk_percent < 10 else self.colors['warning'] if risk_percent < 20 else self.colors['danger']
                
                result_text = f"Risque à 10 ans: {risk_percent:.1f}%\n{interpretation}"
                result_label.config(text=result_text, fg=color)
                
                self.add_to_report(f"Risque cardiovasculaire: {risk_percent:.1f}% - {interpretation}")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de calcul: {str(e)}")
        
        tk.Button(main_frame, text="Calculer Risque", command=calculate_risk,
                 bg=self.colors['primary'], fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(pady=15)
    
    def show_normal_values(self, category):
        """Affiche les valeurs normales d'une catégorie"""
        self.notebook.select(1)  # Sélectionner l'onglet valeurs normales
        self.status_text.config(text=f"Consultation des valeurs normales - {category}")
    
    def add_to_report(self, text):
        """Ajoute du texte au rapport"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.report_text.insert(tk.END, f"[{timestamp}] {text}\n")
        self.report_text.see(tk.END)
    
    def new_report(self):
        """Nouveau rapport"""
        result = messagebox.askyesno("Nouveau Rapport", 
                                   "Effacer le rapport actuel ?")
        if result:
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, f"=== RAPPORT MEDICAL ===\n")
            self.report_text.insert(tk.END, f"Date: {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n")
            if self.patient_data.nom:
                self.report_text.insert(tk.END, f"Patient: {self.patient_data.prenom} {self.patient_data.nom}\n")
            self.report_text.insert(tk.END, f"=" * 50 + "\n\n")
    
    def save_report(self):
        """Sauvegarde le rapport"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.report_text.get(1.0, tk.END))
                messagebox.showinfo("Succès", f"Rapport sauvegardé: {filename}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de sauvegarde: {str(e)}")
    
    def print_report(self):
        """Imprime le rapport"""
        messagebox.showinfo("Impression", "Fonctionnalité d'impression à venir")
    
    # Outils additionnels
    def cervical_collar_algorithm(self):
        """Algorithme de décision pour collier cervical"""
        messagebox.showinfo("Collier Cervical", "Algorithme de décision pour immobilisation cervicale\n(Fonctionnalité en développement)")
    
    def dosage_calculator(self):
        """Calculateur de posologies"""
        messagebox.showinfo("Posologies", "Calculateur de doses médicamenteuses\n(Fonctionnalité en développement)")
    
    def drug_search(self):
        """Recherche de médicaments"""
        messagebox.showinfo("Médicaments", "Base de données médicamenteuse\n(Fonctionnalité en développement)")
    
    def show_trends(self):
        """Affiche les tendances graphiques"""
        messagebox.showinfo("Graphiques", "Analyse des tendances patient\n(Fonctionnalité en développement)")
    
    def create_bmi_calculator(self):
        """Calculateur d'IMC"""
        tk.Label(self.calc_display_frame, text="Calcul de l'IMC", 
                font=('Arial', 18, 'bold'), bg='white', fg=self.colors['primary']).pack(pady=20)
        
        main_frame = tk.Frame(self.calc_display_frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
    def create_bmi_calculator(self):
        """Calculateur d'IMC"""
        tk.Label(self.calc_display_frame, text="Calcul de l'IMC", 
                font=('Arial', 18, 'bold'), bg='white', fg=self.colors['primary']).pack(pady=20)
        
        main_frame = tk.Frame(self.calc_display_frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Variables (préremplies si patient enregistré)
        poids_var = tk.DoubleVar(value=self.patient_data.poids if self.patient_data.poids > 0 else 70)
        taille_var = tk.DoubleVar(value=self.patient_data.taille if self.patient_data.taille > 0 else 170)
        
        # Interface
        input_frame = tk.LabelFrame(main_frame, text="Données anthropométriques", 
                                   font=('Arial', 12, 'bold'), bg='white', fg=self.colors['primary'])
        input_frame.pack(fill='x', pady=15)
        
        tk.Label(input_frame, text="Poids (kg):", bg='white', font=('Arial', 12)).grid(
            row=0, column=0, sticky='w', padx=10, pady=10)
        tk.Entry(input_frame, textvariable=poids_var, font=('Arial', 12), width=10).grid(
            row=0, column=1, padx=10, pady=10)
        
        tk.Label(input_frame, text="Taille (cm):", bg='white', font=('Arial', 12)).grid(
            row=1, column=0, sticky='w', padx=10, pady=10)
        tk.Entry(input_frame, textvariable=taille_var, font=('Arial', 12), width=10).grid(
            row=1, column=1, padx=10, pady=10)
        
        # Résultat
        result_frame = tk.Frame(main_frame, bg=self.colors['light'], relief='raised', bd=2)
        result_frame.pack(fill='x', pady=20)
        
        result_label = tk.Label(result_frame, text="IMC: ", 
                               font=('Arial', 16, 'bold'), bg=self.colors['light'])
        result_label.pack(pady=15)
        
        def calculate_bmi():
            try:
                poids = poids_var.get()
                taille = taille_var.get() / 100  # conversion en mètres
                
                if poids <= 0 or taille <= 0:
                    messagebox.showerror("Erreur", "Veuillez entrer des valeurs positives")
                    return
                
                bmi = poids / (taille ** 2)
                
                # Interprétation
                if bmi < 16.5:
                    interpretation = "Dénutrition sévère"
                    color = self.colors['danger']
                elif bmi < 18.5:
                    interpretation = "Maigreur"
                    color = self.colors['warning']
                elif bmi < 25:
                    interpretation = "Normal"
                    color = self.colors['success']
                elif bmi < 30:
                    interpretation = "Surpoids"
                    color = self.colors['warning']
                elif bmi < 35:
                    interpretation = "Obésité modérée"
                    color = self.colors['danger']
                elif bmi < 40:
                    interpretation = "Obésité sévère"
                    color = self.colors['danger']
                else:
                    interpretation = "Obésité morbide"
                    color = self.colors['danger']
                
                result_text = f"IMC: {bmi:.1f} kg/m²\n{interpretation}"
                result_label.config(text=result_text, fg=color)
                
                self.add_to_report(f"IMC: {bmi:.1f} kg/m² - {interpretation}")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de calcul: {str(e)}")
        
        tk.Button(main_frame, text="Calculer IMC", command=calculate_bmi,
                 bg=self.colors['primary'], fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(pady=15)
    
    def create_creatinine_calculator(self):
        """Calculateur de clairance de la créatinine"""
        tk.Label(self.calc_display_frame, text="Clairance de la Créatinine", 
                font=('Arial', 18, 'bold'), bg='white', fg=self.colors['primary']).pack(pady=20)
        
        main_frame = tk.Frame(self.calc_display_frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Variables
        age_var = tk.IntVar(value=self.patient_data.age if self.patient_data.age > 0 else 50)
        poids_var = tk.DoubleVar(value=self.patient_data.poids if self.patient_data.poids > 0 else 70)
        sexe_var = tk.StringVar(value=self.patient_data.sexe if self.patient_data.sexe else "Homme")
        creatinine_var = tk.DoubleVar(value=10)  # mg/L
        
        # Interface
        params_frame = tk.LabelFrame(main_frame, text="Paramètres patient", 
                                    font=('Arial', 12, 'bold'), bg='white', fg=self.colors['primary'])
        params_frame.pack(fill='x', pady=15)
        
        params = [
            ("Âge:", age_var, "ans"),
            ("Poids:", poids_var, "kg"),
            ("Créatininémie:", creatinine_var, "mg/L")
        ]
        
        for i, (label, var, unit) in enumerate(params):
            tk.Label(params_frame, text=label, bg='white', font=('Arial', 11)).grid(
                row=i, column=0, sticky='w', padx=10, pady=8)
            tk.Entry(params_frame, textvariable=var, font=('Arial', 11), width=10).grid(
                row=i, column=1, padx=5, pady=8)
            tk.Label(params_frame, text=unit, bg='white', font=('Arial', 11)).grid(
                row=i, column=2, sticky='w', padx=5, pady=8)
        
        # Sexe
        tk.Label(params_frame, text="Sexe:", bg='white', font=('Arial', 11)).grid(
            row=len(params), column=0, sticky='w', padx=10, pady=8)
        sexe_frame = tk.Frame(params_frame, bg='white')
        sexe_frame.grid(row=len(params), column=1, columnspan=2, sticky='w', padx=5, pady=8)
        
        tk.Radiobutton(sexe_frame, text="Homme", variable=sexe_var, value="Homme",
                      bg='white', font=('Arial', 11)).pack(side='left')
        tk.Radiobutton(sexe_frame, text="Femme", variable=sexe_var, value="Femme",
                      bg='white', font=('Arial', 11)).pack(side='left', padx=10)
        
        # Résultats
        results_frame = tk.LabelFrame(main_frame, text="Résultats", 
                                     font=('Arial', 12, 'bold'), bg='white', fg=self.colors['primary'])
        results_frame.pack(fill='x', pady=15)
        
        results_text = tk.Text(results_frame, height=8, width=60, font=('Courier', 10),
                              bg=self.colors['light'], state='disabled')
        results_text.pack(padx=10, pady=10)
        
        def calculate_creatinine():
            try:
                age = age_var.get()
                poids = poids_var.get()
                sexe = sexe_var.get()
                creat_mg_l = creatinine_var.get()
                
                # Conversion mg/L -> mg/dL
                creat_mg_dl = creat_mg_l / 10
                
                # Formule de Cockcroft-Gault
                if sexe.lower() == "homme":
                    clairance = ((140 - age) * poids) / (72 * creat_mg_dl)
                else:  # femme
                    clairance = ((140 - age) * poids * 0.85) / (72 * creat_mg_dl)
                
                # Formule MDRD simplifiée
                if sexe.lower() == "homme":
                    mdrd = 186 * (creat_mg_dl ** -1.154) * (age ** -0.203)
                else:
                    mdrd = 186 * (creat_mg_dl ** -1.154) * (age ** -0.203) * 0.742
                
                # Interprétation
                if clairance >= 90:
                    interpretation = "Fonction rénale normale"
                    color = "green"
                elif clairance >= 60:
                    interpretation = "Insuffisance rénale légère"
                    color = "orange"
                elif clairance >= 30:
                    interpretation = "Insuffisance rénale modérée"
                    color = "red"
                elif clairance >= 15:
                    interpretation = "Insuffisance rénale sévère"
                    color = "red"
                else:
                    interpretation = "Insuffisance rénale terminale"
                    color = "red"
                
                # Affichage des résultats
                results_text.config(state='normal')
                results_text.delete(1.0, tk.END)
                
                results_text.insert(tk.END, "CLAIRANCE DE LA CRÉATININE\n")
                results_text.insert(tk.END, "=" * 35 + "\n\n")
                results_text.insert(tk.END, f"Paramètres:\n")
                results_text.insert(tk.END, f"  Âge: {age} ans\n")
                results_text.insert(tk.END, f"  Poids: {poids} kg\n")
                results_text.insert(tk.END, f"  Sexe: {sexe}\n")
                results_text.insert(tk.END, f"  Créatininémie: {creat_mg_l} mg/L ({creat_mg_dl:.2f} mg/dL)\n\n")
                
                results_text.insert(tk.END, f"Résultats:\n")
                results_text.insert(tk.END, f"  Cockcroft-Gault: {clairance:.1f} mL/min\n")
                results_text.insert(tk.END, f"  MDRD: {mdrd:.1f} mL/min/1.73m²\n\n")
                results_text.insert(tk.END, f"Interprétation: {interpretation}\n")
                
                results_text.config(state='disabled')
                
                self.add_to_report(f"Clairance créatinine: {clairance:.1f} mL/min - {interpretation}")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de calcul: {str(e)}")
        
        tk.Button(main_frame, text="Calculer", command=calculate_creatinine,
                 bg=self.colors['primary'], fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(pady=15)
    
    def create_nih_calculator(self):
        """Crée le calculateur NIH Stroke Scale"""
        tk.Label(self.calc_display_frame, text="Score NIH Stroke Scale", 
                font=('Arial', 18, 'bold'), bg='white', fg=self.colors['primary']).pack(pady=20)
        
        main_frame = tk.Frame(self.calc_display_frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Créer un canvas avec scrollbar pour tous les éléments
        canvas = tk.Canvas(main_frame, bg='white')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Variables pour chaque critère
        nih_vars = {
            'vigilance': tk.IntVar(value=0),
            'orientation': tk.IntVar(value=0),
            'commandes': tk.IntVar(value=0),
            'oculomotricite': tk.IntVar(value=0),
            'champ_visuel': tk.IntVar(value=0),
            'paralysie_faciale': tk.IntVar(value=0),
            'motricite_ms': tk.IntVar(value=0),
            'motricite_mi': tk.IntVar(value=0),
            'ataxie': tk.IntVar(value=0),
            'sensibilite': tk.IntVar(value=0),
            'langage': tk.IntVar(value=0),
            'dysarthrie': tk.IntVar(value=0),
            'extinction': tk.IntVar(value=0)
        }
        
        # Configuration des critères NIH
        nih_criteria = [
            ("Vigilance", 'vigilance', [
                (0, "Normal"),
                (1, "Somnolence légère"),
                (2, "Stupeur"),
                (3, "Coma")
            ]),
            ("Orientation", 'orientation', [
                (0, "2 réponses correctes"),
                (1, "1 réponse correcte"),
                (2, "0 réponse correcte")
            ]),
            ("Commandes", 'commandes', [
                (0, "2 tâches correctes"),
                (1, "1 tâche correcte"),
                (2, "0 tâche correcte")
            ]),
            ("Oculomotricité", 'oculomotricite', [
                (0, "Normale"),
                (1, "Paralysie partielle"),
                (2, "Déviation forcée")
            ]),
            ("Champ visuel", 'champ_visuel', [
                (0, "Normal"),
                (1, "Quadranopsie"),
                (2, "Hémianopsie"),
                (3, "Cécité bilatérale")
            ]),
            ("Paralysie faciale", 'paralysie_faciale', [
                (0, "Normale"),
                (1, "Asymétrie mineure"),
                (2, "Paralysie faciale"),
                (3, "Paralysie complète")
            ]),
            ("Motricité membre supérieur", 'motricite_ms', [
                (0, "Normal"),
                (1, "Chute lente"),
                (2, "Effort contre pesanteur"),
                (3, "Pas d'effort"),
                (4, "Pas de mouvement")
            ]),
            ("Motricité membre inférieur", 'motricite_mi', [
                (0, "Normal"),
                (1, "Chute lente"),
                (2, "Effort contre pesanteur"),
                (3, "Pas d'effort"),
                (4, "Pas de mouvement")
            ]),
            ("Ataxie", 'ataxie', [
                (0, "Absente"),
                (1, "1 membre"),
                (2, "2 membres ou plus")
            ]),
            ("Sensibilité", 'sensibilite', [
                (0, "Normale"),
                (1, "Hypoesthésie légère"),
                (2, "Hypoesthésie sévère")
            ]),
            ("Langage", 'langage', [
                (0, "Normal"),
                (1, "Aphasie légère"),
                (2, "Aphasie sévère"),
                (3, "Mutisme")
            ]),
            ("Dysarthrie", 'dysarthrie', [
                (0, "Normale"),
                (1, "Légère à modérée"),
                (2, "Sévère")
            ]),
            ("Extinction/Négligence", 'extinction', [
                (0, "Absente"),
                (1, "Partielle"),
                (2, "Complète")
            ])
        ]
        
        # Créer les frames pour chaque critère
        for title, var_name, options in nih_criteria:
            frame = tk.LabelFrame(scrollable_frame, text=title, 
                                 font=('Arial', 10, 'bold'), bg='white', fg=self.colors['primary'])
            frame.pack(fill='x', pady=5, padx=10)
            
            for value, text in options:
                tk.Radiobutton(frame, text=f"{value} - {text}", variable=nih_vars[var_name], 
                              value=value, bg='white', font=('Arial', 9)).pack(anchor='w', padx=5)
        
        # Résultat
        result_frame = tk.Frame(scrollable_frame, bg=self.colors['light'], relief='raised', bd=2)
        result_frame.pack(fill='x', pady=15, padx=10)
        
        result_label = tk.Label(result_frame, text="Score NIH: ", 
                               font=('Arial', 14, 'bold'), bg=self.colors['light'])
        result_label.pack(pady=15)
        
        def calculate_nih():
            kwargs = {key: var.get() for key, var in nih_vars.items()}
            total, interpretation = self.calculators.nih_stroke_scale(**kwargs)
            
            color = self.colors['success'] if total < 5 else self.colors['warning'] if total < 16 else self.colors['danger']
            
            result_text = f"Score NIH: {total}/42\n{interpretation}"
            result_label.config(text=result_text, fg=color)
            
            self.add_to_report(f"Score NIH Stroke Scale: {total}/42 - {interpretation}")
        
        tk.Button(scrollable_frame, text="Calculer NIH", command=calculate_nih,
                 bg=self.colors['primary'], fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(pady=15)
        
        # Pack le canvas et scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def export_report(self):
        """Exporte le rapport actuel"""
        self.save_report()
    
    def show_help(self):
        """Affiche l'aide"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Guide Utilisateur - NEXUS")
        help_window.geometry("600x400")
        help_window.configure(bg='white')
        
        # Centrer la fenêtre
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() - 600) // 2
        y = (help_window.winfo_screenheight() - 400) // 2
        help_window.geometry(f"600x400+{x}+{y}")
        
        help_text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, 
                                             font=('Arial', 11), bg='white')
        help_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        help_content = """
GUIDE UTILISATEUR - NEXUS v2.0
==============================

NEXUS est une suite complète d'outils médicaux et paramédicaux conçue pour aider les professionnels de santé dans leurs prises de décision.

FONCTIONNALITÉS PRINCIPALES:

1. CALCULATEURS MÉDICAUX
   • Score de Glasgow: Évaluation neurologique
   • Score APGAR: Évaluation néonatale
   • Score NIH: Évaluation des AVC
   • Conversion glycémie: Unités multiples
   • Risque cardiovasculaire: Framingham
   • IMC: Indice de masse corporelle
   • Clairance créatinine: Fonction rénale

2. VALEURS NORMALES
   • Hématologie: Numération, hémostase
   • Biochimie: Fonction hépatique, rénale, lipidique
   • Gazométrie: Équilibre acido-basique
   • Constantes vitales: Tous âges

3. GESTION PATIENTS
   • Création de fiches patient
   • Historique des calculs
   • Rapports médicaux

4. RAPPORTS
   • Génération automatique
   • Export en format texte
   • Impression (à venir)

UTILISATION:

1. Créer un nouveau patient (Menu Fichier > Nouveau Patient)
2. Sélectionner un calculateur dans l'onglet correspondant
3. Saisir les valeurs requises
4. Les résultats sont automatiquement ajoutés au rapport
5. Consulter les valeurs normales dans l'onglet dédié

RACCOURCIS CLAVIER:
• Ctrl+N: Nouveau patient
• Ctrl+Q: Quitter

SUPPORT:
En cas de problème, consulter la documentation complète ou contacter le développeur.

Version: 2.0
Développeur: Sidoine B.
Licence: GNU GPL v3
        """
        
        help_text.insert(tk.END, help_content)
        help_text.config(state='disabled')
    
    def show_about(self):
        """Affiche les informations sur l'application"""
        about_window = tk.Toplevel(self.root)
        about_window.title("À propos de NEXUS")
        about_window.geometry("500x400")
        about_window.configure(bg='white')
        about_window.transient(self.root)
        about_window.resizable(False, False)
        
        # Centrer la fenêtre
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() - 500) // 2
        y = (about_window.winfo_screenheight() - 400) // 2
        about_window.geometry(f"500x400+{x}+{y}")
        
        # Logo et titre
        title_frame = tk.Frame(about_window, bg='white')
        title_frame.pack(pady=30)
        
        tk.Label(title_frame, text="🏥", font=('Arial', 48),
                bg='white', fg=self.colors['primary']).pack()
        
        tk.Label(title_frame, text="NEXUS", font=('Arial', 24, 'bold'),
                bg='white', fg=self.colors['primary']).pack()
        
        tk.Label(title_frame, text="Suite Médicale & Paramedicale", font=('Arial', 12),
                bg='white', fg=self.colors['secondary']).pack()
        
        tk.Label(title_frame, text="Version 2.0", font=('Arial', 12, 'bold'),
                bg='white', fg=self.colors['dark']).pack(pady=5)
        
        # Description
        desc_frame = tk.Frame(about_window, bg='white')
        desc_frame.pack(pady=20, padx=30)
        
        description = """Suite complète d'outils pour professionnels de santé:

• Calculateurs médicaux avancés
• Valeurs normales biologiques
• Gestion de patients
• Rapports médicaux automatisés

Destiné aux:
- Médecins et internes
- Infirmiers
- Techniciens de laboratoire  
- Personnel paramédical
- Étudiants en médecine

Développé avec Python et Tkinter
Interface moderne et intuitive"""
        
        tk.Label(desc_frame, text=description, font=('Arial', 10),
                bg='white', fg=self.colors['dark'], justify='left').pack()
        
        # Copyright et licence
        tk.Label(about_window, text="Développé par Sidoine B.",
                font=('Arial', 10, 'bold'), bg='white', 
                fg=self.colors['primary']).pack(side='bottom', pady=5)
        
        tk.Label(about_window, text="Sous licence GNU General Public License v3",
                font=('Arial', 9), bg='white', 
                fg=self.colors['secondary']).pack(side='bottom', pady=5)
        
        # Bouton fermer
        tk.Button(about_window, text="Fermer", command=about_window.destroy,
                 bg=self.colors['primary'], fg='white', font=('Arial', 10)).pack(side='bottom', pady=15)

def main():
    """Point d'entrée principal"""
    try:
        app = NexusApp()
        app.start_app()
    except Exception as e:
        logger.error(f"Erreur critique: {e}")
        messagebox.showerror("Erreur critique", f"Impossible de démarrer NEXUS:\n{str(e)}")

if __name__ == "__main__":
    main()