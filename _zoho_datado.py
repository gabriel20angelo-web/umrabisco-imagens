# -*- coding: utf-8 -*-
u"""ZOHO_AGENDA.csv — o bulk final, com legenda, URLs publicas e DATA.

Grade decidida por ele em 10/09: comeca **segunda 14/09/2026**, um post por dia as 19:00,
alternando — **dia par da contagem = carrossel de cards de tweet**, **dia impar = post de
arte**, que e' o desenho que ja' estava montado em `PLANO.tsv` (D+0, D+2, ...) e em
`ORDEM_EMBARALHADA.tsv` (D+1, D+3, ...).

⭐ Sao 51 artes para 45 vagas: as **6 ultimas da ordem embaralhada ficam de reserva**, no
fim do arquivo e **sem data** — e' so' preencher se ele quiser esticar a grade.

Formato Zoho: sem cabecalho · `data MM/DD/AAAA HH:MM, texto, link, img1..img8`.
"""
import io, os, csv, datetime

REPO = r"C:\Users\gabri\umrabisco-imagens"
INICIO = datetime.date(2026, 9, 14)          # segunda-feira
HORA = "19:00"

leg = {}
for l in io.open(os.path.join(REPO, "LEGENDAS.tsv"), encoding="utf-8").read().splitlines()[1:]:
    ordem, conj, post, tag, texto = l.split("\t")
    leg[post] = (tag, [p.strip() for p in texto.split(u"¶")])

linhas_multi, linhas_plana, agenda = [], [], []
i_arte = i_tweet = 0
for l in io.open(os.path.join(REPO, "URLS.tsv"), encoding="utf-8").read().splitlines()[1:]:
    c = l.split("\t")
    conj, post, urls = c[1], c[2], c[4:]
    tag, paras = leg[post]
    if conj == "tweet":
        dia = INICIO + datetime.timedelta(days=2 * i_tweet)
        i_tweet += 1
    else:
        # ⛔ as 6 ultimas artes nao tem vaga na grade de 90 dias: ficam sem data
        dia = (INICIO + datetime.timedelta(days=1 + 2 * i_arte)) if i_arte < 45 else None
        i_arte += 1
    quando = u"%s %s" % (dia.strftime("%m/%d/%Y"), HORA) if dia else u""
    multi = u"\n\n".join(paras) + u"\n\n" + tag
    plana = u"  ".join(paras) + u"  " + tag
    linhas_multi.append([quando, multi, u""] + urls)
    linhas_plana.append([quando, plana, u""] + urls)
    agenda.append((dia or datetime.date(2099, 1, 1), quando, conj, post, tag))

# ⭐ o Zoho le' na ordem do arquivo; ordenar por data deixa a fila legivel para ele tambem
ordem = sorted(range(len(agenda)), key=lambda k: agenda[k][0])
linhas_multi = [linhas_multi[k] for k in ordem]
linhas_plana = [linhas_plana[k] for k in ordem]
agenda = [agenda[k] for k in ordem]


def grava(nome, linhas):
    cam = os.path.join(REPO, nome)
    with io.open(cam, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(linhas)
    print(nome, len(linhas), "linhas")


grava("ZOHO_AGENDA.csv", linhas_multi)
grava("ZOHO_AGENDA_1linha.csv", linhas_plana)
grava("ZOHO_AGENDA_teste2.csv", linhas_multi[:2])

L = [u"data\tconjunto\tpost\thashtag"]
for _d, quando, conj, post, tag in agenda:
    L.append(u"%s\t%s\t%s\t%s" % (quando or u"— reserva —", conj, post, tag))
io.open(os.path.join(REPO, "AGENDA.tsv"), "w", encoding="utf-8").write(u"\n".join(L) + u"\n")
com = sum(1 for a in agenda if a[1])
print(u"AGENDA.tsv - %d datados (%s a %s) - %d de reserva"
      % (com, agenda[0][1], agenda[com - 1][1], len(agenda) - com))
