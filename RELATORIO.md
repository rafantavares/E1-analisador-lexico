# Relatório — Atividade 1: Analisador Léxico

## Nível 0 — Identificador e Branco (prontos, referência)

**afd_id** (2 estados: `i0`, `i1`)
```
        letra/_           letra/digito/_
  ->(i0) --------> ((i1)) ----------------,
                      ^_______________________|
```
- `i0`: nada lido ainda.
- `i1` *(final)*: já leu ao menos um caractere válido; continua aceitando letras, dígitos ou `_`.

**afd_branco** (2 estados: `b0`, `b1`) — mesmo desenho, trocando o alfabeto por espaço/tab/quebra de linha.

## Nível 1 — Literal inteiro (2 estados: `n0`, `n1`)

```
        digito         digito
  ->(n0) -------> ((n1)) ------,
                      ^_________|
```
- `n0`: início, nenhum dígito lido.
- `n1` *(final)*: já leu um ou mais dígitos.

Dois estados bastam: um para "ainda não vi dígito nenhum" e outro para "já vi pelo menos um e posso continuar vendo mais".

## Nível 2 — Atribuição e ponto-e-vírgula (2 estados cada)

```
afd_atrib:  ->(a0) --'='--> ((a1))
afd_pvirg:  ->(p0) --';'--> ((p1))
```
- `a0`/`p0`: estado inicial.
- `a1`/`p1` *(final)*: símbolo já reconhecido; sem self-loop, então `"=="` vira dois tokens `ATRIB` e não um só.

## Nível 3 — Palavras reservadas de tipo

Não é autômato novo: `inteiro`, `real` e `logico` batem no `afd_id` normalmente (viram lexema `ID`), e o **dicionário `PALAVRAS`** reclassifica o lexema inteiro para `TIPO` depois do casamento. Por isso `inteirox` continua `ID` — a palavra tem que casar por completo, não como prefixo.

## Nível 4 — Literal real (4 estados: `r0`, `r1`, `r2`, `r3`)

```
        digito      digito       ponto        digito       digito
  ->(r0) -----> (r1) -----(loop)---> (r2) -----> ((r3)) -----(loop)
                  |________________________________________________
```
- `r0`: início.
- `r1`: já leu dígitos da parte inteira (**não é final** — sozinho, um número sem ponto deve virar `INTEIRO`, não `REAL`).
- `r2`: acabou de ler o ponto (**não pode ser final** — é a armadilha do enunciado: se fosse final, `"12."` seria aceito como real).
- `r3` *(final)*: já leu ao menos um dígito depois do ponto.

Precisa de 4 estados porque há 4 "fases" distintas da palavra: antes do ponto, logo após o ponto (fase perigosa, não aceita), e depois de garantir um dígito pós-ponto.

## Nível 5 — Literais lógicos

Mesmo mecanismo do nível 3: `verdadeiro` e `falso` também são reconhecidos pelo `afd_id` e depois reclassificados via `PALAVRAS` para a categoria `LOGICO`.

## Nível 6 — Comentário de linha (3 estados: `c0`, `c1`, `c2`)

```
        '/'        '/'         qualquer, exceto '\n'
  ->(c0) ----> (c1) ----> ((c2)) ------------(loop)
```
- `c0`: início.
- `c1`: leu uma barra só (**não é final** — uma barra sozinha deve dar erro léxico, divisão é assunto de outra atividade).
- `c2` *(final)*: já leu `//`; continua consumindo qualquer caractere que não seja quebra de linha, que é justamente onde o comentário para (não faz parte dele).

## Nível 7 — Integração

Nenhum autômato novo: é só a combinação de todos os anteriores sobre um arquivo com várias declarações.

---

## Quantos estados, resumo

| Autômato | Estados | Por quê |
|---|---|---|
| `afd_id` / `afd_branco` | 2 | prontos (referência) |
| `afd_inteiro` | 2 | "nada ainda" vs "já vi ≥1 dígito" |
| `afd_atrib` / `afd_pvirg` | 2 cada | símbolo único, sem loop |
| `afd_real` | 4 | parte inteira / ponto (não-final) / parte decimal |
| `afd_comentario` | 3 | primeira barra / segunda barra (final) / corpo |

Não usei estados a mais: cada autômato tem exatamente um estado por "fase" que muda o comportamento de aceitação. Reduzir qualquer um deles junta fases que precisam de status de aceitação diferente (por exemplo, juntar `r1` e `r3` faria `"12"` virar `REAL`; juntar `c1` e `c2` faria uma barra sozinha ser aceita).

## O nível que deu mais trabalho

O **nível 4 (real)** foi o mais traiçoeiro. Na primeira tentativa marquei `r2` (o estado logo depois do ponto) como final, seguindo o mesmo padrão "raso" que usei nos outros autômatos — resultado: `testar.py` acusava que `"12."` estava sendo aceito como `REAL`, quebrando exatamente o caso de teste `ERRO_ESPERADO`. A correção foi perceber que "aceitar o ponto" e "aceitar o número" são coisas diferentes: só depois de ver pelo menos um dígito *após* o ponto (estado `r3`) é que a palavra vira um real válido. Isso também exigiu cuidado para `r1` não ser final, senão `"42"` empataria em tamanho entre `REAL` e `INTEIRO`, e como `REAL` vem primeiro em `REGRAS`, o desempate por ordem faria `"42"` virar `REAL` incorretamente.

## Como rodar

```
python testar.py                  # roda os 8 níveis
python lexico.py niveis/n7.mini   # roda o analisador em um arquivo completo
```

Todos os 8 níveis passam (`38/38` casos de teste).
