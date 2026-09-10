# -*- coding: utf-8 -*-
u"""Gera as URLs publicas de cada carrossel a partir dos _caminhos_*.tsv."""
import io, os

BASE = "https://gabriel20angelo-web.github.io/umrabisco-imagens"
REPO = r"C:\Users\gabri\umrabisco-imagens"
ORDEM = (r"C:\Users\gabri\OneDrive\Desktop\Arquivos do Claude"
         r"\Um rabisco\5 - POSTS DE ARTE\ORDEM_EMBARALHADA.tsv")

def ler(rel):
    d = {}
    for l in io.open(os.path.join(REPO, "_caminhos_%s.tsv" % rel),
                     encoding="utf-8").read().splitlines()[1:]:
        c = l.split("\t")
        d[c[0]] = [BASE + "/" + x for x in c[2:]]
    return d

arte, tweets = ler("arte"), ler("tweets")

# arte na ordem embaralhada; tweets na ordem do plano
linhas = [u"ordem\tconjunto\tpost\tslides\turls"]
for l in io.open(ORDEM, encoding="utf-8").read().splitlines()[1:]:
    c = l.split("\t")
    u = arte[c[2]]
    linhas.append(u"%s\tarte\t%s\t%d\t%s" % (c[0], c[2], len(u), u"\t".join(u)))
for i, p in enumerate(sorted(tweets), 1):
    u = tweets[p]
    linhas.append(u"%03d\ttweet\t%s\t%d\t%s" % (i, p, len(u), u"\t".join(u)))

cam = os.path.join(REPO, "URLS.tsv")
io.open(cam, "w", encoding="utf-8").write(u"\n".join(linhas) + u"\n")
print(cam, len(linhas) - 1, "carrosseis")
print(linhas[1][:160])
