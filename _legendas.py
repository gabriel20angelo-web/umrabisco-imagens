# -*- coding: utf-8 -*-
u"""Junta as legendas escritas para os 96 carrosseis e refaz o bulk do Zoho com o
texto de verdade no lugar do rascunho. A coluna de data continua EM BRANCO."""
import io, os, csv

REPO = r"C:\Users\gabri\umrabisco-imagens"
LEG = (r"C:\Users\gabri\AppData\Local\Temp\claude\C--Users-gabri"
       r"\31ff5ed1-13a3-4dfd-ae92-a0673f3f2be6\scratchpad\legendas")

# ordem -> (post, hashtag, [paragrafos])
leg = {}
for lote in ("A", "B", "C"):
    for l in io.open(os.path.join(LEG, "LOTE_%s.tsv" % lote),
                     encoding="utf-8").read().splitlines():
        if not l.strip():
            continue
        ordem, post, tag, texto = l.split("\t")
        leg[post] = (post, tag, [p.strip() for p in texto.split(u"¶")])

linhas_multi, linhas_plana, mestre = [], [], []
for l in io.open(os.path.join(REPO, "URLS.tsv"), encoding="utf-8").read().splitlines()[1:]:
    c = l.split("\t")
    ordem, conj, post, urls = c[0], c[1], c[2], c[4:]
    assert post in leg, post
    _, tag, paras = leg[post]
    multi = u"\n\n".join(paras) + u"\n\n" + tag
    plana = u"  ".join(paras) + u"  " + tag
    linhas_multi.append([u"", multi, u""] + urls)
    linhas_plana.append([u"", plana, u""] + urls)
    mestre.append(u"\t".join([ordem, conj, post, tag, u" ¶ ".join(paras)]))

def grava(nome, linhas):
    cam = os.path.join(REPO, nome)
    with io.open(cam, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(linhas)
    print(nome, len(linhas), "linhas")

grava("ZOHO_com_legenda.csv", linhas_multi)
grava("ZOHO_com_legenda_1linha.csv", linhas_plana)
grava("ZOHO_teste_2linhas.csv", linhas_multi[:2])

io.open(os.path.join(REPO, "LEGENDAS.tsv"), "w", encoding="utf-8").write(
    u"ordem\tconjunto\tpost\thashtag\tlegenda\n" + u"\n".join(mestre) + u"\n")
print("LEGENDAS.tsv", len(mestre), "linhas |",
      len(set(x.split("\t")[3] for x in mestre)), "hashtags distintas")
