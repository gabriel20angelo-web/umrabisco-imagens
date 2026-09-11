# -*- coding: utf-8 -*-
u"""Reescreve a hashtag de cada post para UMA PALAVRA + #psicologia.

⛔ 10/09, ele: *«a hashtag e' UMA palavra, nao um conjunto de palavras. Bote a hashtag uma
palavra e outra hashtag psicologia»*. A primeira rodada saiu em camelCase com 2-3 palavras
coladas (#silencioQueViraConflito) — reprovada inteira.

⭐ A palavra sai do proprio tema do post (a primeira palavra cheia da hashtag antiga);
onde duas caiam na mesma, a segunda foi escolhida a mao — a lista `MANUAL` — para que as
96 continuem distintas.
"""
import io, os, re

REPO = r"C:\Users\gabri\umrabisco-imagens"
STOP = set(u"""o a os as do da de dos das que se e em nao mais por para com ou um uma ja
ao aos na no nas nos seu sua meu minha mesmo mesma foi ser estar vira fica ficou tem
acaba basta sem antes depois todo toda""".split())

# desempate das 12 colisoes (post -> palavra)
MANUAL = {
    "POST_032": u"pausa",        "POST_005": u"reciprocidade",
    "75_o_barulho_ai_dentro": u"incomodo", "08_escolher_e_metodo": u"metodo",
    "POST_024": u"afastamento",  "22_quem_vai_embora_te_devolve": u"ausencia",
    "POST_014": u"manipulacao",      "POST_028": u"erro",
    "POST_041": u"sentir",       "69_conforto_no_caos": u"caos",
    "74_insistir_onde_nao_te_veem": u"morada", "POST_016": u"maturidade",
    "POST_040": u"inquietacao",
    # ⭐ 2a passada: a primeira palavra da hashtag antiga as vezes caia num verbo ou num
    #    pronome (#assusta, #quem, #como, #escolhi) — hashtag boa e' SUBSTANTIVO.
    "09_autoconhecimento": u"autoconhecimento", "51_nada_e_mais_barulhento": u"promessa",
    "23_se_adaptar_demais": u"adaptacao",      "19_dar_conta_de_tudo": u"produtividade",
    "81_o_que_julgamos_possivel": u"possibilidade", "15_chao_da_infancia": u"paz",
    "93_nunca_o_que_o_outro_escutou": u"malentendido",
    "37_bem_vindo_ou_necessario": u"utilidade",
    "POST_001": u"desgaste",   "POST_004": u"dor",         "POST_010": u"silenciar",
    "POST_023": u"recolhimento", "POST_031": u"conversa",  "POST_034": u"encanto",
    "POST_036": u"duvida",     "POST_043": u"sinais",      "POST_045": u"convivencia",
}

L = io.open(os.path.join(REPO, "LEGENDAS.tsv"), encoding="utf-8").read().splitlines()
saida, usadas = [L[0]], set()
for l in L[1:]:
    ordem, conj, post, tag, txt = l.split("\t")
    if post in MANUAL:
        p = MANUAL[post]
    else:
        ps = [x.lower() for x in re.findall(r"[a-z]+|[A-Z][a-z]*", tag[1:])]
        cheias = [x for x in ps if x not in STOP and len(x) > 3]
        # ⭐ em colisao, desce para a proxima palavra cheia antes de desistir — sem isso
        #   cada empate novo virava uma rodada de conserto a mao.
        p = next((x for x in cheias if x not in usadas),
                 cheias[0] if cheias else ps[0])
    assert p not in usadas, (post, p)
    usadas.add(p)
    saida.append(u"\t".join([ordem, conj, post, u"#%s #psicologia" % p, txt]))

io.open(os.path.join(REPO, "LEGENDAS.tsv"), "w", encoding="utf-8").write(
    u"\n".join(saida) + u"\n")
print(len(saida) - 1, "legendas ·", len(usadas), "palavras distintas")
