"""desk_escrita — transições do ciclo de vida da pendência sobre PENDENCIAS.md.

Funções puras sobre texto; gravar é responsabilidade do chamador. Contrato: SOLUCAO.md.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date

import desk

SITUACOES = ("aberta", "concluída", "descartada")


@dataclass
class Item:
    chave: int      # 1..n na ordem do arquivo; vale para a versão atual do texto
    indice: int     # índice 0-based da linha no texto
    secao: str
    conteudo: str   # tudo após '- [ ] '


@dataclass
class Mudanca:
    situacao: str   # uma de SITUACOES
    secao: str      # seção de destino enquanto aberta ("Urgente" | "Em aberto")
    conteudo: str   # campos desejados, sem marca de encerramento


def itens_abertos(texto: str) -> list[Item]:
    itens: list[Item] = []
    secao = ""
    for i, linha in enumerate(texto.splitlines()):
        if linha.startswith("## "):
            secao = linha[3:].strip()
        elif secao in desk.SECOES_ABERTAS and linha.startswith("- [ ] "):
            itens.append(Item(len(itens) + 1, i, secao, linha[6:]))
    return itens


def campos(conteudo: str) -> list[str]:
    return [c.strip() for c in conteudo.split(desk.SEPARADOR)]


def juntar(lista: list[str]) -> str:
    return desk.SEPARADOR.join(lista)


def sem_critica(conteudo: str) -> str:
    return juntar([c for c in campos(conteudo) if c != "crítica"]) if "crítica" in campos(conteudo) else conteudo


def com_critica(conteudo: str) -> str:
    return conteudo if "crítica" in campos(conteudo) else juntar(campos(conteudo) + ["crítica"])


def tem_motivo(conteudo: str) -> bool:
    return any(c.startswith("motivo: ") and c[len("motivo: "):].strip() for c in campos(conteudo))


def linha_de(m: Mudanca, hoje: date) -> str:
    if m.situacao == "aberta":
        return f"- [ ] {m.conteudo}"
    base = campos(sem_critica(m.conteudo))
    if m.situacao == "concluída":
        return "- [x] " + juntar(base + [f"concluída em {hoje.isoformat()}"])
    motivo = [c for c in base if c.startswith("motivo: ")]
    resto = [c for c in base if not c.startswith("motivo: ")]
    return "- [-] " + juntar(resto + [f"descartada em {hoje.isoformat()}"] + motivo)


def reescrever(texto: str, mudancas: dict[int, Mudanca], novas: list[Mudanca], hoje: date) -> str:
    """`mudancas`: chave do Item -> estado desejado. Itens ausentes ficam intactos."""
    if not mudancas and not novas:
        return texto
    linhas = texto.splitlines()
    por_chave = {it.chave: it for it in itens_abertos(texto)}
    destino: dict[str, list[str]] = {s: [] for s in desk.SECOES}
    remover: set[int] = set()
    for chave, m in mudancas.items():
        it = por_chave[chave]
        alvo = m.secao if m.situacao == "aberta" else desk.SECAO_FINAL[m.situacao]
        if alvo == it.secao:
            linhas[it.indice] = linha_de(m, hoje)
        else:
            remover.add(it.indice)
            destino[alvo].append(linha_de(m, hoje))
    destino_novas = [linha_de(m, hoje) for m in novas]
    linhas = [l for i, l in enumerate(linhas) if i not in remover]
    for secao in desk.SECOES:
        extras = destino[secao] + [l for l, m in zip(destino_novas, novas) if m.secao == secao]
        if extras:
            topo = secao in desk.SECAO_FINAL.values()
            linhas = desk.inserir_em_secao(linhas, secao, extras, topo=topo)
    return "\n".join(linhas) + "\n"


def validar_texto(frente: desk.Frente, texto: str) -> list[desk.Erro]:
    rel = f"{frente.id}/PENDENCIAS.md"
    pendencias, erros = desk.ler_pendencias_texto(texto, rel)
    copia = desk.Frente(id=frente.id, pasta=frente.pasta, ficha=frente.ficha, pendencias=pendencias)
    return erros + desk.verificar_cruzado([copia])


def erros_novos(frente: desk.Frente, antes: str, depois: str) -> list[str]:
    """Mensagens que aparecem em `depois` e não em `antes` (multiconjunto; ignora nº de linha)."""
    contar = lambda t: Counter(err.mensagem for err in validar_texto(frente, t))
    return sorted((contar(depois) - contar(antes)).elements())
