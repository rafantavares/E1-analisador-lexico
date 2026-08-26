from mini_base import (afd, de, LETRAS, DIGITOS, SUBLIN, BRANCOS,
                       PONTO, BARRA, IGUAL, PVIRG, SIGMA)

afd_id = afd(
    estados=['i0', 'i1'],
    transicoes={
        'i0': de(LETRAS | SUBLIN, 'i1'),
        'i1': de(LETRAS | DIGITOS | SUBLIN, 'i1'),
    },
    inicial='i0',
    finais=['i1'],
)

afd_branco = afd(
    estados=['b0', 'b1'],
    transicoes={
        'b0': de(BRANCOS, 'b1'),
        'b1': de(BRANCOS, 'b1'),
    },
    inicial='b0',
    finais=['b1'],
)

afd_inteiro = afd(
    estados=['n0', 'n1'],
    transicoes={
        'n0': de(DIGITOS, 'n1'),
        'n1': de(DIGITOS, 'n1'),
    },
    inicial='n0',
    finais=['n1'],
)

afd_atrib = afd(
    estados=['a0', 'a1'],
    transicoes={
        'a0': de(IGUAL, 'a1'),
    },
    inicial='a0',
    finais=['a1'],
)

afd_pvirg = afd(
    estados=['p0', 'p1'],
    transicoes={
        'p0': de(PVIRG, 'p1'),
    },
    inicial='p0',
    finais=['p1'],
)

afd_real = afd(
    estados=['r0', 'r1', 'r2', 'r3'],
    transicoes={
        'r0': de(DIGITOS, 'r1'),
        'r1': {**de(DIGITOS, 'r1'), **de(PONTO, 'r2')},
        'r2': de(DIGITOS, 'r3'),
        'r3': de(DIGITOS, 'r3'),
    },
    inicial='r0',
    finais=['r3'],
)

afd_comentario = afd(
    estados=['c0', 'c1', 'c2'],
    transicoes={
        'c0': de(BARRA, 'c1'),
        'c1': de(BARRA, 'c2'),
        'c2': de(SIGMA - {'\n'}, 'c2'),
    },
    inicial='c0',
    finais=['c2'],
)

REGRAS = [
    ('COMENTARIO', afd_comentario),
    ('BRANCO',     afd_branco),
    ('REAL',       afd_real),
    ('INTEIRO',    afd_inteiro),
    ('ID',         afd_id),
    ('ATRIB',      afd_atrib),
    ('PVIRG',      afd_pvirg),
]

PALAVRAS = {
    'inteiro': 'TIPO',
    'real': 'TIPO',
    'logico': 'TIPO',
    'verdadeiro': 'LOGICO',
    'falso': 'LOGICO',
}

DESCARTAR = {'COMENTARIO', 'BRANCO'}
