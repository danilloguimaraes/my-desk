"""desk_escrita — transições do ciclo de vida da pendência sobre PENDENCIAS.md.

Funções puras sobre texto; gravar é responsabilidade do chamador. Contrato: SOLUCAO.md.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from typing import Callable

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


def selecionar(itens: list[Item], alvo: str | None, escolher: Callable[[list[Item]], Item]) -> Item:
    if not itens:
        raise ValueError("a frente não tem pendências abertas")
    if alvo and alvo.isdigit():
        achado = next((it for it in itens if it.chave == int(alvo)), None)
        if achado is None:
            raise ValueError(f"não há pendência aberta nº {alvo} (veja `desk frente`)")
        return achado
    candidatos = [it for it in itens if not alvo or alvo.casefold() in it.conteudo.casefold()]
    if not candidatos:
        raise ValueError(f"nenhuma pendência aberta contém '{alvo}'")
    return candidatos[0] if len(candidatos) == 1 else escolher(candidatos)


def menu(candidatos: list[Item], entrada: Callable[[str], str], saida: Callable[[str], None]) -> Item:
    for n, it in enumerate(candidatos, start=1):
        saida(f"  {n}. [{it.secao}] {it.conteudo}")
    while True:
        resposta = entrada("Qual? (nº): ").strip()
        if resposta.isdigit() and 1 <= int(resposta) <= len(candidatos):
            return candidatos[int(resposta) - 1]
        saida(f"  ! responda um número de 1 a {len(candidatos)}")


def sem_escolha(candidatos: list[Item]) -> Item:
    lista = "; ".join(f"{it.chave}: {it.conteudo}" for it in candidatos)
    raise ValueError(f"{len(candidatos)} pendências casam com o trecho; use o nº. {lista}")


def transicao(verbo: str, it: Item, itens: list[Item], motivo: str | None) -> dict[int, Mudanca]:
    if verbo == "feito":
        return {it.chave: Mudanca("concluída", it.secao, it.conteudo)}
    if verbo == "descartar":
        return {it.chave: Mudanca("descartada", it.secao, juntar(campos(it.conteudo) + [f"motivo: {motivo}"]))}
    if verbo in ("urgente", "normal"):
        secao = "Urgente" if verbo == "urgente" else "Em aberto"
        return {it.chave: Mudanca("aberta", secao, it.conteudo)}
    if verbo == "critica":
        mudancas = {o.chave: Mudanca("aberta", o.secao, sem_critica(o.conteudo))
                    for o in itens if o.chave != it.chave and "crítica" in campos(o.conteudo)}
        mudancas[it.chave] = Mudanca("aberta", it.secao, com_critica(it.conteudo))
        return mudancas
    raise ValueError(f"verbo desconhecido: {verbo}")


VERBOS = ("feito", "descartar", "urgente", "normal", "critica")


def executar(verbo: str, frente: desk.Frente, alvo: str | None, *, motivo: str | None = None,
             sim: bool = False, hoje: date | None = None, entrada: Callable[[str], str] = input,
             saida: Callable[[str], None] = print) -> int:
    if verbo == "descartar" and motivo and desk.SEPARADOR in motivo:
        raise ValueError("motivo não pode conter ' — ' (é o separador de campos)")
    hoje = hoje or date.today()
    arquivo = frente.pasta / "PENDENCIAS.md"
    texto = arquivo.read_text(encoding="utf-8")
    itens = itens_abertos(texto)
    escolher = sem_escolha if sim else (lambda c: menu(c, entrada, saida))
    it = selecionar(itens, alvo, escolher)

    if verbo == "descartar":
        while True:
            if not (motivo and motivo.strip()):
                if sim:
                    raise ValueError("descartar exige --motivo em modo --sim")
                motivo = entrada("Motivo do descarte: ").strip()
                if not motivo:
                    saida("  ! o motivo é obrigatório")
                    continue
            if desk.SEPARADOR in motivo:
                saida("  ! motivo não pode conter ' — ' (é o separador de campos)")
                motivo = None
                continue
            break
    mudancas = transicao(verbo, it, itens, motivo)

    encerra_critica = verbo in ("feito", "descartar") and "crítica" in campos(it.conteudo)
    if encerra_critica and frente.situacao == "ativa":
        outros = [o for o in itens if o.chave != it.chave]
        if sim or not outros:
            raise ValueError(f"'{it.conteudo}' é a crítica de {frente.id}; "
                             f"rode `desk critica {frente.id} <nº>` antes")
        saida(f"Este item é a crítica de {frente.id}. Qual passa a ser a crítica?")
        sucessora = menu(outros, entrada, saida)
        mudancas[sucessora.chave] = Mudanca("aberta", sucessora.secao, com_critica(sucessora.conteudo))

    novo = reescrever(texto, mudancas, [], hoje)
    problemas = erros_novos(frente, texto, novo)
    if problemas:  # valida antes de pedir confirmação
        saida("recusado: a mudança criaria inconsistência(s):")
        for p in problemas:
            saida(f"  ! {p}")
        return 1
    for chave, m in mudancas.items():
        saida(f"  - {itens[chave - 1].conteudo}\n  + {linha_de(m, hoje)[6:]}  [{m.situacao}]")
    if not sim and entrada("Confirmar? [S/n]: ").strip().lower() not in ("", "s", "sim"):
        saida("nada foi gravado")
        return 1
    desk.gravar_atomico(arquivo, novo)
    saida(f"ok: {frente.id}/PENDENCIAS.md atualizado")
    return 0
