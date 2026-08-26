# Relatório - Atividade 1 (Analisador Léxico)

Faltei na aula 4, então fiz esse relatório meio que "reconstruindo" o raciocínio a partir do que já vinha pronto no nível 0 (afd_id e afd_branco) e das dicas que o testar.py ia dando quando eu errava. Vou explicar autômato por autômato, o que cada estado tá guardando na cabeça, e onde eu mais apanhei.

## Nível 0 (já vinha pronto, mas é o modelo pra tudo)

```
         letra ou _         letra, digito ou _
  -> ( i0 ) -----------> (( i1 ))  <-------,
                              |_____________|
```

i0 é "não vi nada ainda". i1 é "já vi o primeiro caractere válido e agora aceito qualquer coisa em cima disso". Usei essa mesma lógica de "estado inicial x estado que já satisfez o mínimo" em quase tudo depois.

## Nível 1 - inteiro (2 estados)

```
        digito          digito
  -> (n0) --------> (( n1 ))  <---,
                          |________|
```

n0 = nenhum dígito lido ainda. n1 (final) = já tenho pelo menos 1 dígito, e fico voltando pra n1 lendo mais dígitos. Esse foi tranquilo, praticamente copiei a estrutura do afd_id trocando letra por dígito.

## Nível 2 - `=` e `;` (2 estados cada)

```
afd_atrib:   -> (a0) --- '=' ---> (( a1 ))
afd_pvirg:   -> (p0) --- ';' ---> (( p1 ))
```

Só um cuidado aqui que quase passou batido: não pode ter seta de a1 voltando pra a1. Se colocar, "==" vira um token ATRIB só (tipo "=="), e o esperado é dois tokens ATRIB separados. Sem loop, resolve.

## Nível 3 - palavras de tipo (inteiro, real, logico)

Esse nível não pede autômato novo, e no começo eu fiquei procurando onde criar um afd_tipo achando que tinha esquecido de algo. Só que a palavra "inteiro" já bate certinho no afd_id (é só letra). O que acontece é que, depois do texto casar como ID, o mini_base.py olha se aquele lexema tá dentro do dicionário PALAVRAS, e se estiver, troca a categoria de ID pra TIPO. Então o trabalho aqui foi só preencher o dicionário:

```python
PALAVRAS = {
    'inteiro': 'TIPO',
    'real': 'TIPO',
    'logico': 'TIPO',
}
```

Isso também explica por que "inteirox" continua sendo ID: o dicionário só bate na palavra inteira, "inteirox" não está lá.

## Nível 4 - real (4 estados) - o que mais me quebrou a cabeça

```
        digito     digito      ponto        digito       digito
  -> (r0) -----> (r1) ---'.'---> (r2) -----> (( r3 )) <----,
                   ^_____|                        |________|
```

r0 = início. r1 = já li dígito(s) da parte inteira. r2 = acabei de ler o ponto. r3 (final) = já tenho pelo menos um dígito depois do ponto.

Na minha primeira tentativa eu botei r2 como final também, porque pensei "ele já leu dígito + ponto, então já é um número válido". Rodei o testar.py e ele acusou que "12." tava passando como REAL, quando devia dar erro. Foi aí que caiu a ficha: o enunciado já avisava dessa pegadinha e mesmo assim caí nela. O certo é só r3 ser final, porque um real de verdade PRECISA ter pelo menos um dígito depois do ponto - "12." para bem no meio do caminho e não pode contar.

Outro detalhe que só percebi depois: r1 também não pode ser final. Se fosse, "42" (sem ponto nenhum) bateria tanto em REAL quanto em INTEIRO com o mesmo tamanho, e como REAL vem antes de INTEIRO na lista REGRAS, o "42" ia virar REAL errado no desempate. Então precisa mesmo dos 4 estados separados, cada um representando uma fase que aceita coisas diferentes.

## Nível 5 - verdadeiro / falso

Mesma ideia do nível 3, só que mapeando pra LOGICO:

```python
'verdadeiro': 'LOGICO',
'falso': 'LOGICO',
```

Rápido depois de já ter entendido o nível 3.

## Nível 6 - comentário (3 estados)

```
        '/'        '/'        qualquer coisa menos \n
  -> (c0) ----> (c1) ----> (( c2 ))  <-----,
                                |___________|
```

c0 = nada ainda. c1 = já li uma barra (não é final - uma barra sozinha tem que dar erro, já que divisão fica pra outra atividade). c2 (final) = já li as duas barras, e a partir daí continuo engolindo qualquer caractere, menos quebra de linha, porque o comentário morre no fim da linha e o \n não faz parte dele. Usei o SIGMA - {'\n'} que tava sugerido no comentário do arquivo.

## Nível 7

Não precisou mexer em nada, é só juntar tudo e testar num arquivo com várias linhas de declaração.

## Quantos estados usei, e por quê

- afd_inteiro: 2 (sem dígito / com dígito)
- afd_atrib, afd_pvirg: 2 cada (não visto / visto, sem loop)
- afd_real: 4 (antes do ponto, depois do ponto sem dígito ainda, depois do ponto com dígito)
- afd_comentario: 3 (nada, uma barra, duas barras)

Não dá pra usar menos que isso em nenhum dos casos, porque cada estado a menos juntaria duas fases que precisam se comportar diferente na hora de aceitar ou não (o nível 4 é o exemplo mais claro disso).

## Nível que mais deu trabalho

Sem dúvida o nível 4. Não foi a lógica de "dígito ponto dígito" que travou, foi a parte de decidir QUAL estado marcar como final. Minha primeira versão tava semanticamente errada (r2 final) mesmo eu achando que tava certa, e só o testar.py rodando o caso "12." me mostrou o erro na prática.

## Como rodar

```
python testar.py
python lexico.py niveis/n7.mini
```

Os 8 níveis passam, 38/38 casos.
