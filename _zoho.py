# -*- coding: utf-8 -*-
u"""ZOHO_sem_data.csv — o bulk do Zoho ja com as URLs publicas, com a coluna de
data EM BRANCO de proposito. Preencher so quando a grade de datas for decidida."""
import io, os, re, csv

REPO = r"C:\Users\gabri\umrabisco-imagens"
ARTE = (r"C:\Users\gabri\OneDrive\Desktop\Arquivos do Claude"
        r"\Um rabisco\5 - POSTS DE ARTE")
PLANO = r"C:\Users\gabri\_RECON_EPSTEMIA\AGENDA\PLANO.tsv"

def frases_da_ficha(slug):
    u"""le a tabela de slides da FICHA e devolve as frases, menos o encerramento"""
    t = io.open(os.path.join(ARTE, slug, "FICHA.md"), encoding="utf-8").read()
    fs = []
    for l in t.splitlines():
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) == 5 and re.match(r"^S\d+$", c[0]) and c[1] != "encerramento":
            fs.append(c[4])
    return fs

legendas = {}
for l in io.open(PLANO, encoding="utf-8").read().splitlines()[1:]:
    c = l.split("\t")
    legendas[c[0]] = c[-1].replace(u" ¶ ", u" · ")

linhas = []
for l in io.open(os.path.join(REPO, "URLS.tsv"), encoding="utf-8").read().splitlines()[1:]:
    c = l.split("\t")
    post, urls = c[2], c[4:]
    if c[1] == "arte":
        texto = u" · ".join(frases_da_ficha(post))
    else:
        texto = legendas.get(post, u"")
    linhas.append([u""] + [texto + u"  —  @UmRabiscoPsi", u""] + urls)

cam = os.path.join(REPO, "ZOHO_sem_data.csv")
with io.open(cam, "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows(linhas)
print(cam, len(linhas), "linhas |", max(len(x) - 3 for x in linhas), "imagens no maior")
