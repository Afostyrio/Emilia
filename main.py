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

doc.append(pl.Command("title", "Olimpiada Mexicana de Matemáticas"))
doc.append(pl.Command("author", "TEST"))
doc.append(pl.Command("maketitle"))
doc.append(pl.Command("tableofcontents"))

with doc.create(pl.Chapter("Presentación", numbering=False)):
	doc.append(pl.Command("addcontentsline", ["toc", "chapter", "Presentación"]))
	doc.append(pl.Command("input", "inputs/tex/Presentacion.tex"))

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
		international_olympiads= ["IMO", "OIM", "OMCC", "APMO", "EGMO", "RMM", "IGO"]
		mex_history = pandas.read_csv("inputs/csv/historial_MEX.csv").fillna("")

		with doc.create(pl.Subsection("México en la IMO")):
			doc.append("En 1959 Rumania organizó la Primera Olimpiada Internacional de Matemáticas con la participación de sólo 7 países: Hungría, la URSS, Bulgaria, Polonia, Checoslovaquia, la República Democrática Alemana y Rumania. A partir de entonces la Olimpiada Internacional se celebra año con año (casi siempre en julio) con la participación de países de los cinco continentes.")
			doc.append(pl.NoEscape("\n"))
			doc.append(pl.NoEscape(r"Los ganadores del primer Concurso Nacional asistieron a la 29\textsuperscript{a} Olimpiada Internacional de Matemáticas, celebrada en Canberra, Australia, en julio de 1988; a partir de ese año México ha asistido a la emisión anual de la Olimpiada Internacional de Matemáticas. México organizó la 46\textsuperscript{a} Olimpiada Internacional en Mérida, Yucatán en julio de 2005."))
			doc.append(pl.NoEscape("\n"))
			doc.append("Los resultados de las delegaciones mexicanas en la Olimpiada Internacional han sido:")


			with doc.create(pl.LongTable("|c|l|c|c|")) as tabla_IMO:
				tabla_IMO.append(pl.NoEscape(r"\hline \textit{Año}&\multicolumn{1}{|c|}{\textit{País sede}}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_IMO.append(pl.Command("endfirsthead"))
				tabla_IMO.append(pl.NoEscape(r"\hline \multicolumn{4}{|r|}{{\textit{... continúa de la página previa.}}} \\ \hline \textit{Año}&\multicolumn{1}{|c|}{\textit{País sede}}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_IMO.append(pl.Command("endhead"))
				tabla_IMO.append(pl.NoEscape(r"\hline \multicolumn{4}{|r|}{{\textit{Continúa en la página siguiente...}}} \\ \hline"))
				tabla_IMO.append(pl.Command("endfoot"))
				tabla_IMO.add_hline()
				tabla_IMO.append(pl.Command("endlastfoot"))
				IMO_Mex = pandas.read_csv("inputs/csv/historial_IMO.csv").values
				for item in IMO_Mex:
					tabla_IMO.add_row(item)
		with doc.create(pl.Subsection("México en la OIM")):
			doc.append(pl.NoEscape(r"""En 1985 la Organización de Estados Iberoamericanos para la Educación, la Ciencia y la Cultura, convocó a la Primera Olimpiada Iberoamericana de Matemáticas, celebrada en Colombia con la participación de 10 países. A partir de la 4\textsuperscript{a} Olimpiada Iberoamericana de Matemáticas, celebrada en La Habana, Cuba, México ha participado anualmente en esta Olimpiada.
			
México ha organizado ya cuatro Olimpiadas Iberoamericanas de Matemáticas: la 8\textsuperscript{a} en 1993, la 12\textsuperscript{a} en 1997, la 24\textsuperscript{a} en 2009 y la 34\textsuperscript{a} en 2019.
			
Los resultados de las Delegaciones Mexicanas en las Olimpiadas Iberoamericanas han sido:"""
			))
			with doc.create(pl.LongTable("|c|l|c|c|")) as tabla_OIM:
				tabla_OIM.append(pl.NoEscape(r"\hline \textit{Año}&\multicolumn{1}{|c|}{\textit{País sede}}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_OIM.append(pl.Command("endfirsthead"))
				tabla_OIM.append(pl.NoEscape(r"\hline \multicolumn{4}{|r|}{{\textit{... continúa de la página previa.}}} \\ \hline \textit{Año}&\multicolumn{1}{|c|}{\textit{País sede}}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_OIM.append(pl.Command("endhead"))
				tabla_OIM.append(pl.NoEscape(r"\hline \multicolumn{4}{|r|}{{\textit{Continúa en la página siguiente...}}} \\ \hline"))
				tabla_OIM.append(pl.Command("endfoot"))
				tabla_OIM.add_hline()
				tabla_OIM.append(pl.Command("endlastfoot"))

				OIM_Mex = pandas.read_csv("inputs/csv/historial_OIM.csv").values
				for item in OIM_Mex:
					tabla_OIM.add_row(item)
		
		with doc.create(pl.Subsection("México en la OMCC")):
			doc.append(pl.NoEscape(r"Para promover la participación de los países de América Central y el Caribe en concursos de matemáticas, a partir de 1999 se organizó la Olimpiada Matemática de Centroamérica y el Caribe, con sede en Costa Rica. A la primera olimpiada asistieron 10 delegaciones. Desde entonces México ha participado en cada una de las ediciones y la ha organizado tres veces. La 4\textsuperscript{a} en 2002 con sede en Mérida, Yucatán, la 13\textsuperscript{a} en 2012 con sede en Colima, Colima y la 16\textsuperscript{a} en Cuernavaca, Morelos."))
			doc.append(pl.NoEscape("\n"))
			doc.append("Los resultados de las Delegaciones Mexicanas en las Olimpiadas Centroamericanas y del Caribe han sido:")
			with doc.create(pl.LongTable("|c|l|c|c|")) as tabla_OMCC:
				tabla_OMCC.append(pl.NoEscape(r"\hline \textit{Año}&\multicolumn{1}{|c|}{\textit{País sede}}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_OMCC.append(pl.Command("endfirsthead"))
				tabla_OMCC.append(pl.NoEscape(r"\hline \multicolumn{4}{|r|}{{\textit{... continúa de la página previa.}}} \\ \hline \textit{Año}&\multicolumn{1}{|c|}{\textit{País sede}}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_OMCC.append(pl.Command("endhead"))
				tabla_OMCC.append(pl.NoEscape(r"\hline \multicolumn{4}{|r|}{{\textit{Continúa en la página siguiente...}}} \\ \hline"))
				tabla_OMCC.append(pl.Command("endfoot"))
				tabla_OMCC.add_hline()
				tabla_OMCC.append(pl.Command("endlastfoot"))

				OMCC_Mex = pandas.read_csv("inputs/csv/historial_OMCC.csv").values
				for item in OMCC_Mex:
					tabla_OMCC.add_row(item)
		with doc.create(pl.Subsection("México en la APMO")):
			doc.append("Desde 1990, los ganadores del Concurso Nacional participan anualmente en la Olimpiada de Matemáticas de la Cuenca del Pacífico. En el 2000 y en el 2009 México no participó en esta olimpiada. En el 2001 y en el 2002 se participó, mas no se publicaron resultados. Del 2016 al 2019, México fue el país organizador de esta olimpiada.")
			with doc.create(pl.LongTable("|c|c|c|")) as tabla_APMO:
				tabla_APMO.append(pl.NoEscape(r"\hline \textit{Año}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_APMO.append(pl.Command("endfirsthead"))
				tabla_APMO.append(pl.NoEscape(r"\hline \multicolumn{3}{|r|}{{\textit{... continúa de la página previa.}}} \\ \hline \textit{Año}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_APMO.append(pl.Command("endhead"))
				tabla_APMO.append(pl.NoEscape(r"\hline \multicolumn{3}{|r|}{{\textit{Continúa en la página siguiente...}}} \\ \hline"))
				tabla_APMO.append(pl.Command("endfoot"))
				tabla_APMO.add_hline()
				tabla_APMO.append(pl.Command("endlastfoot"))

				APMO_Mex = pandas.read_csv("inputs/csv/historial_APMO.csv").values
				for item in APMO_Mex:
					tabla_APMO.add_row(item)
		with doc.create(pl.Subsection("México en la EGMO")):
			doc.append("En abril del 2014 México participó por primera vez en la III Olimpiada Europea Femenil de Matemáticas (EGMO, por sus siglas en inglés) en Antalya, Turquía. Esta olimpiada es para países europeos pero se permite la participación por invitación de equipos no europeos.")
			with doc.create(pl.LongTable("|c|l|c|c|")) as tabla_EGMO:
				tabla_EGMO.append(pl.NoEscape(r"\hline \textit{Año}&\multicolumn{1}{|c|}{\textit{País sede}}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_EGMO.append(pl.Command("endfirsthead"))
				tabla_EGMO.append(pl.NoEscape(r"\hline \multicolumn{4}{|r|}{{\textit{... continúa de la página previa.}}} \\ \hline \textit{Año}&\multicolumn{1}{|c|}{\textit{País sede}}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_EGMO.append(pl.Command("endhead"))
				tabla_EGMO.append(pl.NoEscape(r"\hline \multicolumn{4}{|r|}{{\textit{Continúa en la página siguiente...}}} \\ \hline"))
				tabla_EGMO.append(pl.Command("endfoot"))
				tabla_EGMO.add_hline()
				tabla_EGMO.append(pl.Command("endlastfoot"))

				EGMO_Mex = pandas.read_csv("inputs/csv/historial_EGMO.csv").values
				for item in EGMO_Mex:
					tabla_EGMO.add_row(item)
		with doc.create(pl.Subsection("México en la RMM")):
			doc.append("En 2015 México participó por primera vez en la Rumana de Campeones con un equipo de 3 estudiantes. La última vez que se participó en esta competencia fue en el 2017.")
			with doc.create(pl.LongTable("|c|c|c|")) as tabla_RMM:
				tabla_RMM.append(pl.NoEscape(r"\hline \textit{Año}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_RMM.append(pl.Command("endfirsthead"))
				tabla_RMM.append(pl.NoEscape(r"\hline \multicolumn{3}{|r|}{{\textit{... continúa de la página previa.}}} \\ \hline \textit{Año}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_RMM.append(pl.Command("endhead"))
				tabla_RMM.append(pl.NoEscape(r"\hline \multicolumn{3}{|r|}{{\textit{Continúa en la página siguiente...}}} \\ \hline"))
				tabla_RMM.append(pl.Command("endfoot"))
				tabla_RMM.add_hline()
				tabla_RMM.append(pl.Command("endlastfoot"))

				RMM_Mex = pandas.read_csv("inputs/csv/historial_RMM.csv").values
				for item in RMM_Mex:
					tabla_RMM.add_row(item)
		with doc.create(pl.Subsection("México en la IGO")):
			doc.append("En el 2015 se realizó por primera vez esta olimpiada a nivel internacional. México ha participado en las tres primeras con un equipo completo de 12 estudiantes.")
			with doc.create(pl.LongTable("|c|c|c|")) as tabla_IGO:
				tabla_IGO.append(pl.NoEscape(r"\hline \textit{Año}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_IGO.append(pl.Command("endfirsthead"))
				tabla_IGO.append(pl.NoEscape(r"\hline \multicolumn{3}{|r|}{{\textit{... continúa de la página previa.}}} \\ \hline \textit{Año}&\textit{No. de Países}&\textit{Lugar de México} \\\hline\hline"))
				tabla_IGO.append(pl.Command("endhead"))
				tabla_IGO.append(pl.NoEscape(r"\hline \multicolumn{3}{|r|}{{\textit{Continúa en la página siguiente...}}} \\ \hline"))
				tabla_IGO.append(pl.Command("endfoot"))
				tabla_IGO.add_hline()
				tabla_IGO.append(pl.Command("endlastfoot"))

				IGO_Mex = pandas.read_csv("inputs/csv/historial_IGO.csv").values
				for item in IGO_Mex:
					tabla_IGO.add_row(item)
			


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


doc.generate_pdf('Engargolado', clean_tex=False)
