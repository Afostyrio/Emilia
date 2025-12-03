import os
import pandas
import pylatex as pl
from pylatex.utils import bold, italic
import matplotlib
import matplotlib.pyplot as plt

gran_tabla = pandas.read_csv("inputs/csv/resultados_omm_nacional.csv").fillna("")
estados = sorted(gran_tabla['ESTADO'].unique())
corte_bronce = gran_tabla[gran_tabla['MEDALLA'] == "Bronce"]["TOTAL"].min()
corte_plata = gran_tabla[gran_tabla['MEDALLA'] == "Plata"]["TOTAL"].min()
corte_oro = gran_tabla[gran_tabla['MEDALLA'] == "Oro"]["TOTAL"].min()

doc = pl.Document(documentclass="book", document_options=["12pt", "spanish"])
doc.packages.append(pl.Package("inputs/Preamble"))

doc.append(pl.Command("pagenumbering", "roman"))
doc.append(pl.Command("input", "inputs/tex/Portada.tex"))
doc.append(pl.Command("tableofcontents"))
doc.append(pl.Command("clearpage"))

doc.append(pl.Command("pagenumbering", "arabic"))
with doc.create(pl.Chapter("Presentación", numbering=False)):
	doc.append(pl.Command("addcontentsline", ["toc", "chapter", "Presentación"]))
	doc.append(pl.Command("addcontentsline", ["toc", "section", "Patrocinadores"]))
	doc.append(pl.Command("input", "inputs/tex/Presentación.tex"))

with doc.create(pl.Chapter("Concurso Nacional")):
	with doc.create(pl.Section("Sedes del concurso")):
		sedes = pandas.read_csv("inputs/csv/historial_sedes_omm.csv").fillna("")
		doc.append(f"Desde 1987 la Sociedad Matemática Mexicana organiza la Olimpiada Mexicana de Matemáticas. La siguiente tabla contiene los nombres de las sedes de los {len(sedes.values)} Concursos Nacionales hasta la fecha.")
		with doc.create(pl.LongTable("|c|c|c|c|")) as tabla_sedes:
			tabla_sedes.append(pl.NoEscape(r"\hline \textit{Edición}&\textit{Año}&\textit{Sede}&\textit{Estado} \\\hline\hline"))
			tabla_sedes.append(pl.Command("endfirsthead"))
			tabla_sedes.append(pl.NoEscape(r"\hline \multicolumn{4}{|r|}{{\textit{... continúa de la página previa.}}} \\ \hline \textit{Edición}&\textit{Año}&\textit{Sede}&\textit{Estado} \\\hline\hline"))
			tabla_sedes.append(pl.Command("endhead"))
			tabla_sedes.append(pl.NoEscape(r"\hline \multicolumn{4}{|r|}{{\textit{Continúa en la página siguiente...}}} \\ \hline"))
			tabla_sedes.append(pl.Command("endfoot"))
			tabla_sedes.add_hline()
			tabla_sedes.append(pl.Command("endlastfoot"))
			counter = 0
			for item in sedes.values:
				counter += 1
				tabla_sedes.add_row([counter, *item])
	doc.append(pl.Command("input", ["inputs/tex/ConcursoNacional.tex"]))
	
	with doc.create(pl.Section("Resultados estatales en los Concursos Nacionales")):
		doc.append("Aunque la participación en el Concurso Nacional es individual, es importante destacar la labor que han llevado a cabo los Estados de la República apoyando a sus concursantes. Con el propósito de reconocer este trabajo, presentamos el registro de los estados que han ocupado los primeros 10 lugares en cada uno de los Concursos Nacionales, a partir del quinto. No contamos con los datos correpondientes a las primeras 4 olimpiadas.")
		# TODO: Crear el archivo para los top 10 de cada edición, solicitar las ediciones más recientes.

with doc.create(pl.Chapter("Olimpiadas Internacionales")):
	doc.append(pl.Command("input", "inputs/tex/OlimpiadasInternacionales.tex"))

	with doc.create(pl.Section("Historia de México en las Olimpiadas Internacionales")):
		international_olympiads= ["IMO", "OIM", "OMCC", "APMO", "EGMO", "PAGMO", "RMM", "IGO"]
		mex_history = pandas.read_csv("inputs/csv/historial_MEX.csv").fillna("")

		historial_nacional = pandas.read_csv("inputs/csv/historial_MEX.csv").fillna("")
		for olympiad in international_olympiads:
			with doc.create(pl.Subsection(f"México en la {olympiad}")):
				doc.append(pl.Command("input", f"inputs/tex/InternacionalesMex/{olympiad}.tex"))
				datos_olimpiada = historial_nacional[historial_nacional["Olimpiada"] == olympiad].sort_values(by='Anno').values
				if datos_olimpiada[0,2] == "":
					with doc.create(pl.LongTable("|c|c|c|c|c|c|c|")) as tabla:
						tabla.append(pl.NoEscape(r"\hline \textit{Año}&\begin{tabular}{c}\textit{No. de}\\\textit{Países}\end{tabular}&\begin{tabular}{c}\textit{Lugar de}\\\textit{México}\end{tabular}&\textit{Oro}&\textit{Plata}&\textit{Bronce}&\textit{M.H.} \\\hline\hline"))
						tabla.append(pl.Command("endfirsthead"))
						tabla.append(pl.NoEscape(r"\hline \multicolumn{7}{|r|}{{\textit{... continúa de la página previa.}}} \\ \hline \textit{Año}&\begin{tabular}{c}\textit{No. de}\\\textit{Países}\end{tabular}&\begin{tabular}{c}\textit{Lugar de}\\\textit{México}\end{tabular}&\textit{Oro}&\textit{Plata}&\textit{Bronce}&\textit{M.H.} \\\hline\hline"))
						tabla.append(pl.Command("endhead"))
						tabla.append(pl.NoEscape(r"\hline \multicolumn{7}{|r|}{{\textit{Continúa en la página siguiente...}}} \\ \hline"))
						tabla.append(pl.Command("endfoot"))
						tabla.add_hline()
						tabla.append(pl.Command("endlastfoot"))

						for item in datos_olimpiada:
							new_row = [item[1]]
							for number in item[3:]:
								try: number = int(number)
								except: pass
								new_row.append(number)
							tabla.add_row(new_row)
				else:
					with doc.create(pl.LongTable("|c|l|c|c|c|c|c|c|")) as tabla:
						tabla.append(pl.NoEscape(r"\hline \textit{Año}&\multicolumn{1}{|c|}{\textit{País sede}}&\begin{tabular}{c}\textit{No. de}\\\textit{Países}\end{tabular}&\begin{tabular}{c}\textit{Lugar de}\\\textit{México}\end{tabular}&\textit{Oro}&\textit{Plata}&\textit{Bronce}&\textit{M.H.} \\\hline\hline"))
						tabla.append(pl.Command("endfirsthead"))
						tabla.append(pl.NoEscape(r"\hline \multicolumn{8}{|r|}{{\textit{... continúa de la página previa.}}} \\ \hline \textit{Año}&\multicolumn{1}{|c|}{\textit{País sede}}&\begin{tabular}{c}\textit{No. de}\\\textit{Países}\end{tabular}&\begin{tabular}{c}\textit{Lugar de}\\\textit{México}\end{tabular}&\textit{Oro}&\textit{Plata}&\textit{Bronce}&\textit{M.H.} \\\hline\hline"))
						tabla.append(pl.Command("endhead"))
						tabla.append(pl.NoEscape(r"\hline \multicolumn{8}{|r|}{{\textit{Continúa en la página siguiente...}}} \\ \hline"))
						tabla.append(pl.Command("endfoot"))
						tabla.add_hline()
						tabla.append(pl.Command("endlastfoot"))
						for item in datos_olimpiada:
							new_row = [item[1], item[2]]
							for number in item[3:]:
								try: number = int(number)
								except: pass
								new_row.append(number)
							tabla.add_row(new_row)
		
with doc.create(pl.Chapter("Últimas noticias")):
	doc.append(pl.Command("input", "inputs/tex/ÚltimasNoticias.tex"))

with doc.create(pl.Chapter("Reporte del concurso nacional")):
	with doc.create(pl.Section("Ganadores del concurso nacional")):
		doc.append(f"Los {len(gran_tabla[gran_tabla['MEDALLA']=='Oro'].values)} alumnos ganadores son:")
		doc.append(pl.Command("par"))
		with doc.create(pl.Itemize()) as itemize:
			for ganador in gran_tabla[gran_tabla['MEDALLA']=='Oro'].values:
				itemize.add_item(f"{ganador[2]} ({ganador[1]})")

	with doc.create(pl.Section('Lista de participantes')):
		for estado in estados:
			doc.append(bold(estado))
			doc.append(pl.NoEscape("\n"))
			with doc.create(pl.Tabular("c l")) as participantes_por_estado:
				for participante in gran_tabla[gran_tabla["ESTADO"] == estado].sort_values(by=['CLAVE']).values:
					participantes_por_estado.add_row([bold(participante[0]), participante[2]])
			doc.append(pl.NoEscape("\n\n"))

	with doc.create(pl.Section('Puntajes por estado')):
		for estado in estados:
			doc.append(bold(estado))
			doc.append(pl.NoEscape("\n"))
			with doc.create(pl.Tabular("c c c c c c c c c")) as puntajes_por_estado:
				puntajes_por_estado.add_row([bold("Concursante"), bold("P1"), bold("P2"), bold("P3"), bold("P4"), bold("P5"), bold("P6"), bold("Final"), bold("Premio")])
				for participante in gran_tabla[gran_tabla["ESTADO"] == estado].sort_values(by=['CLAVE']).values:
					puntajes_por_estado.add_row([bold(participante[0]), *participante[3:]])
			doc.append(pl.NoEscape("\n\n"))

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

	with doc.create(pl.Section("Grafiquitas")):
		with doc.create(pl.Figure(position='H')) as figure:
			doc.append(pl.Command("centering"))
			counts = [len(gran_tabla[gran_tabla['TOTAL'] == i].values) for i in range(43)]
			medalla_por_puntaje = []
			for i in range(43):
				if i < corte_bronce:
					medalla_por_puntaje.append('#70A3CC')
				elif i < corte_plata:
					medalla_por_puntaje.append('#8C7853')
				elif i < corte_oro:
					medalla_por_puntaje.append('#C0C0C0')
				else:
					medalla_por_puntaje.append('#FFD700')
			fig, ax = plt.subplots()

			ax.set_xlabel("Puntaje")
			ax.set_ylabel("Número de participantes")
			ax.bar(range(43), counts, color=medalla_por_puntaje)
			plt.savefig("Test.png")
			figure.add_image("Test.png")
			figure.add_caption("Número de alumnos por puntaje")

with doc.create(pl.Chapter("Próximos eventos")):
	doc.append(pl.Command("input", "inputs/tex/PróximosEventos.tex"))

with doc.create(pl.Chapter("Lineamientos de la OMM")):
	doc.append(pl.Command("input", "inputs/tex/Lineamientos.tex"))

with doc.create(pl.Chapter("Directorio del Comité Organizador de la OMM")):
	with doc.create(pl.Section("Directorio de los delegados estatales")):
		delegados_estatales = pandas.read_csv("inputs/csv/directorio_delegados_estatales.csv").fillna("").values
		for delegado in delegados_estatales:
			doc.append(pl.Command("noindent"))
			doc.append(pl.NoEscape(f"{bold(delegado[0])} -- {italic(delegado[1])}"))
			doc.append(pl.NoEscape(r"\\"))
			doc.append(pl.NoEscape(f"{delegado[2]}"))
			doc.append(pl.NoEscape(r"\\"))
			doc.append(pl.Command("href", ["mailto:" + pl.NoEscape(delegado[3]), pl.NoEscape(delegado[3])]))
			doc.append(pl.NoEscape(r"\\"))
			if delegado[4] != "":
				doc.append(pl.Command("href", ["mailto:" + pl.NoEscape(delegado[4]), pl.NoEscape(delegado[4])]))
				doc.append(pl.NoEscape(r"\\"))
			if delegado[5] != "":
				doc.append(pl.Command("url", pl.NoEscape(delegado[5])))
				doc.append(pl.NoEscape(r"\\"))
			doc.append(pl.Command("par"))
			doc.append(pl.Command("bigskip"))
	with doc.create(pl.Section("Directorio del Comité Nacional")):
		directorio = pandas.read_csv("inputs/csv/directorio_comité_nacional.csv").fillna("").values
		n = len(directorio)
		directorio = directorio.reshape((int(n/2),2,3))
		with doc.create(pl.LongTable(pl.NoEscape(r"p{.5\textwidth} p{.5\textwidth}"))) as table:
			for line in directorio:
				table.add_row([bold(line[0,0]), bold(line[1,0])])
				table.add_row(line[:,1])
				if line[0,2] != "": correo1 = pl.Command("href", ["mailto:" + pl.NoEscape(line[0,2]), pl.NoEscape(line[0,2])])
				else: correo1 = ""
				if line[1,2] != "": correo2 = pl.Command("href", ["mailto:" + pl.NoEscape(line[1,2]), pl.NoEscape(line[1,2])])
				else: correo2 = ""
				table.add_row([correo1, correo2])
				table.add_row(["",""])
		doc.append(pl.Command("input", "inputs/tex/Colofón.tex"))

doc.generate_pdf('Engargolado', clean_tex=False)
