# umrabisco-imagens

Hospedagem das imagens dos carrosséis do **@UmRabiscoPsi**, só para que o agendador
(Zoho Social) consiga buscá-las por URL — ele não aceita arquivo local.

- `arte/<post>/NN.jpg` — os 51 posts de arte, na ordem dos slides.
- `tweets/<POST_NNN>/NN.jpg` — os 45 carrosséis de card de tweet.

Os **mestres em PNG** continuam fora daqui (`Um rabisco\5 - POSTS DE ARTE` e
`_RECON_EPSTEMIA\AGENDA\POSTS`). O que está neste repo é cópia JPEG q95 sem
subamostragem de croma, gerada por `_converter.py`.

⚠️ Os cards de tweet trazem no próprio recorte o nome e o @ de quem escreveu.

## Os arquivos do agendador

| arquivo | o que é |
|---|---|
| `LEGENDAS.tsv` | as 96 legendas de Instagram, uma hashtag por post (todas distintas) |
| `AGENDA.tsv` | a grade legível: data, conjunto, post, hashtag |
| `ZOHO_AGENDA.csv` | **o bulk final**: data, legenda, URLs — pronto para importar |
| `ZOHO_AGENDA_1linha.csv` | igual, sem quebra de linha dentro do campo (plano B do importador) |
| `ZOHO_AGENDA_teste2.csv` | as 2 primeiras linhas, para testar a importação antes das 96 |
| `ZOHO_sem_data.csv` | a versão antiga, rascunho e sem data (mantida só como histórico) |

**A grade**: começa segunda **14/09/2026**, um post por dia às **19:00**, alternando card
de tweet (dias pares da contagem) e post de arte (ímpares), até **12/12/2026**. São 51
artes para 45 vagas — as 6 últimas ficam no fim do arquivo **sem data**, de reserva.
