import os
import pandas
import pylatex as pl
from pylatex.utils import bold

gran_tabla = pandas.read_csv("resultados_omm_nacional.csv").fillna("")
estados = gran_tabla['ESTADO'].unique()

doc = pl.Document()

with doc.create(pl.Section("Ganadores del concurso nacional")):
	doc.append(f"Los {len(gran_tabla[gran_tabla['MEDALLA']=='Oro'].values)} alumnos ganadores son:\n")
	with doc.create(pl.Itemize()) as itemize:
		for ganador in gran_tabla[gran_tabla['MEDALLA']=='Oro'].values:
			itemize.add_item(f"{ganador[2]} ({ganador[1]})")

with doc.create(pl.Section('Lista de participantes')):
	for estado in estados:
		doc.append(bold(estado))
		doc.append("\n")
		with doc.create(pl.Tabular("c l")) as participantes_por_estado:
			for participante in gran_tabla[gran_tabla["ESTADO"] == estado].sort_values(by=['CLAVE']).values:
				participantes_por_estado.add_row([bold(participante[0]), participante[2]])
		doc.append("\n\n")

with doc.create(pl.Section('Puntajes por estado')):
	for estado in estados:
		doc.append(bold(estado))
		doc.append("\n")
		with doc.create(pl.Tabular("c c c c c c c c c")) as puntajes_por_estado:
			puntajes_por_estado.add_row([bold("Concursante"), bold("P1"), bold("P2"), bold("P3"), bold("P4"), bold("P5"), bold("P6"), bold("Final"), bold("Premio")])
			for participante in gran_tabla[gran_tabla["ESTADO"] == estado].sort_values(by=['CLAVE']).values:
				puntajes_por_estado.add_row([bold(participante[0]), *participante[3:]])
		doc.append("\n\n")

with doc.create(pl.Section("Promedio/dificultad de los problemas")):
	with doc.create(pl.Tabular("c c c c c c c")) as tabla_puntos:
		tabla_puntos.add_row([bold("Puntaje"), bold("P1"), bold("P2"), bold("P3"), bold("P4"), bold("P5"), bold("P6")])
		for points in range(7,-1,-1):
			tabla_puntos.add_row([
				bold(str(points)),
				len(gran_tabla[gran_tabla['P1'] == points]),
				len(gran_tabla[gran_tabla['P2'] == points]),
				len(gran_tabla[gran_tabla['P3'] == points]),
				len(gran_tabla[gran_tabla['P4'] == points]),
				len(gran_tabla[gran_tabla['P5'] == points]),
				len(gran_tabla[gran_tabla['P6'] == points])
				])
		tabla_puntos.add_row(
			bold("Promedio"),
			bold("%1.2f" % gran_tabla['P1'].mean()),
			bold("%1.2f" % gran_tabla['P2'].mean()),
			bold("%1.2f" % gran_tabla['P3'].mean()),
			bold("%1.2f" % gran_tabla['P4'].mean()),
			bold("%1.2f" % gran_tabla['P5'].mean()),
			bold("%1.2f" % gran_tabla['P6'].mean())
		)
		


with doc.create(pl.Section("Medallas y menciones honoríficas")):
	with doc.create(pl.Subsection("Medallas de Oro")):
		with doc.create(pl.LongTable("l l")) as medallas:
			for medallista in gran_tabla[gran_tabla['MEDALLA'] == 'Oro'].values:
				medallas.add_row([medallista[1], medallista[2]])

	with doc.create(pl.Subsection("Medallas de Plata")):
		with doc.create(pl.LongTable("l l")) as medallas:
			for medallista in gran_tabla[gran_tabla['MEDALLA'] == 'Plata'].values:
				medallas.add_row([medallista[1], medallista[2]])

	with doc.create(pl.Subsection("Medallas de Bronce")):
		with doc.create(pl.LongTable("l l")) as medallas:
			for medallista in gran_tabla[gran_tabla['MEDALLA'] == 'Bronce'].values:
				medallas.add_row([medallista[1], medallista[2]])

	with doc.create(pl.Subsection("Menciones honoríficas")):
		with doc.create(pl.LongTable("l l")) as medallas:
			for medallista in gran_tabla[gran_tabla['MEDALLA'] == 'M. H.'].values:
				medallas.add_row([medallista[1], medallista[2]])

with doc.create(pl.Section("Medallas por estado")):
	with doc.create(pl.LongTable("l c c c c c c")) as medallas_estado:
		medallas_estado.add_row([bold("Estado"), bold("Oros"), bold("Platas"), bold("Bronces"), bold("M.H."), bold("# Alumnos"), bold("Puntaje")])
		for estado in sorted(gran_tabla['ESTADO'].unique()):
			datos_estado = [
				estado,
				len(gran_tabla[(gran_tabla['ESTADO'] == estado) & (gran_tabla['MEDALLA'] == "Oro")].values),
				len(gran_tabla[(gran_tabla['ESTADO'] == estado) & (gran_tabla['MEDALLA'] == "Plata")].values),
				len(gran_tabla[(gran_tabla['ESTADO'] == estado) & (gran_tabla['MEDALLA'] == "Bronce")].values),
				len(gran_tabla[(gran_tabla['ESTADO'] == estado) & (gran_tabla['MEDALLA'] == "M. H.")].values),
				len(gran_tabla[gran_tabla['ESTADO'] == estado].values),
				gran_tabla[gran_tabla['ESTADO'] == estado]['TOTAL'].sum()
			]
			medallas_estado.add_row(datos_estado)

doc.generate_pdf('Engargolado', clean_tex=False)
