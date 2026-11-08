from io import BytesIO
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
import pandas as pd

def generar_excel(datos):
    archivo = BytesIO()

    with pd.ExcelWriter(archivo, engine="openpyxl") as escritor:
        datos.to_excel(escritor, index=False, sheet_name="Transportes")
        hoja = escritor.sheets["Transportes"]

        hoja.freeze_panes = "A2"
        hoja.auto_filter.ref = hoja.dimensions

        for celda in hoja[1]:
            celda.fill = PatternFill("solid", fgColor="17365D")
            celda.font = Font(color="FFFFFF", bold=True)
            celda.alignment = Alignment(horizontal="center")

        for columna in hoja.columns:
            letra = get_column_letter(columna[0].column)
            ancho = max(len(str(celda.value or "")) for celda in columna)
            hoja.column_dimensions[letra].width = min(ancho + 3, 45)

        encabezados = [celda.value for celda in hoja[1]]

        if "nivel_riesgo" in encabezados:
            numero = encabezados.index("nivel_riesgo") + 1

            colores = {
                "bajo": "C6EFCE",
                "medio": "FFEB9C",
                "alto": "FFC7CE"
            }

            for fila in range(2, hoja.max_row + 1):
                celda = hoja.cell(fila, numero)
                riesgo = str(celda.value or "").strip().lower()

                if riesgo in colores:
                    celda.fill = PatternFill(
                        "solid",
                        fgColor=colores[riesgo]
                    )

    archivo.seek(0)
    return archivo.getvalue()
