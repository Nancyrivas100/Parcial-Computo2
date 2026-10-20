import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
)


def analizar_datos(df):
    print("="*50)
    print("1. ESTRUCTURA Y CABECERA DEL DATASET:")
    print("="*50)
    print(df.head())

    print("\n" + "="*50)
    print("2. INFORMACIÓN DEL DATASET (TIPOS DE DATOS Y NULOS):")
    print("="*50)
    print(df.info())

    print("\n" + "="*50)
    print("3. ESTADÍSTICAS BÁSICAS (NUMÉRICAS):")
    print("="*50)
    print(df.describe())

    print("\n" + "="*50)
    print("4. TOTAL DE STOCK Y VALOR POR SUCURSAL:")
    print("="*50)
    resumen = df.groupby('Sucursal')[['Cantidad', 'Valor_Total']].sum()
    print(resumen)
    print("="*50 + "\n")


class InventarioApp(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Dashboard de Inventario - Empresa Salvadoreña")
        self.setGeometry(100, 100, 1100, 700)

        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()

        
        lbl_titulo = QLabel("Panel de Control de Inventario por Sucursal")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #1E293B; margin-bottom: 10px;")
        main_layout.addWidget(lbl_titulo)

        
        content_layout = QHBoxLayout()

       
        self.tabla = QTableWidget()
        self.tabla.setRowCount(len(self.df))
        self.tabla.setColumnCount(len(self.df.columns))
        self.tabla.setHorizontalHeaderLabels(self.df.columns)
        
        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                self.tabla.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))
                
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        content_layout.addWidget(self.tabla, stretch=1)

        
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvas(self.fig)
        content_layout.addWidget(self.canvas, stretch=1)

        main_layout.addLayout(content_layout)
        main_widget.setLayout(main_layout)

        
        self.generar_graficos()

    def generar_graficos(self):
        resumen_valor = self.df.groupby('Sucursal')['Valor_Total'].sum()
        self.ax1.bar(resumen_valor.index, resumen_valor.values, color='#2563EB')
        self.ax1.set_title('Valor Total ($) por Sucursal', fontsize=11, fontweight='bold')
        self.ax1.set_ylabel('USD ($)')
        self.ax1.tick_params(axis='x', rotation=45)

        
        resumen_cat = self.df.groupby('Categoria')['Cantidad'].sum()
        self.ax2.pie(resumen_cat.values, labels=resumen_cat.index, autopct='%1.1f%%', colors=["#28DD2B", "#C50B24", "#A410DF"])
        self.ax2.set_title('Distribución de Unidades por Categoria', fontsize=11, fontweight='bold')

        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    
    try:
        data = pd.read_csv('inventario.csv')
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'inventario.csv'")
        sys.exit()

   
    analizar_datos(data)

    
    app = QApplication(sys.argv)
    window = InventarioApp(data)
    window.show()
    sys.exit(app.exec_())