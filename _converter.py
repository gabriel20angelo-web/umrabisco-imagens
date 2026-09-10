# -*- coding: utf-8 -*-
u"""Converte os PNG das pecas para JPEG q95 4:4:4 dentro do repo de imagens.
Os PNG originais continuam sendo os mestres; aqui so mora a copia para a web."""
import os, io, glob, sys
from PIL import Image

REPO = r"C:\Users\gabri\umrabisco-imagens"
ARTE = r"C:\Users\gabri\OneDrive\Desktop\Arquivos do Claude\Um rabisco\5 - POSTS DE ARTE"
TWEE = r"C:\Users\gabri\_RECON_EPSTEMIA\AGENDA\POSTS"
Q = 95

def slides(pasta):
    return sorted(x for x in glob.glob(os.path.join(pasta, "*.png"))
                  if "_FOLHA" not in os.path.basename(x))

def converter(origem, destino_rel, mapa):
    n_img = 0
    for pasta in sorted(os.listdir(origem)):
        p = os.path.join(origem, pasta)
        if not os.path.isdir(p) or pasta.startswith("_"):
            continue
        fs = slides(p)
        if not fs:
            continue
        saida = os.path.join(REPO, destino_rel, pasta)
        if not os.path.isdir(saida):
            os.makedirs(saida)
        urls = []
        for i, f in enumerate(fs, 1):
            nome = "%02d.jpg" % i
            alvo = os.path.join(saida, nome)
            if not os.path.exists(alvo):
                Image.open(f).convert("RGB").save(
                    alvo, "JPEG", quality=Q, subsampling=0, optimize=True)
            urls.append("%s/%s/%s" % (destino_rel, pasta, nome))
            n_img += 1
        mapa.append((pasta, len(fs), urls))
        sys.stdout.write(".")
        sys.stdout.flush()
    return n_img

for origem, rel in ((ARTE, "arte"), (TWEE, "tweets")):
    mapa = []
    n = converter(origem, rel, mapa)
    with io.open(os.path.join(REPO, "_caminhos_%s.tsv" % rel), "w", encoding="utf-8") as f:
        f.write(u"post\tslides\tcaminhos\n")
        for pasta, k, urls in mapa:
            f.write(u"%s\t%d\t%s\n" % (pasta, k, u"\t".join(urls)))
    print(u"\n%s: %d pastas, %d imagens" % (rel, len(mapa), n))
