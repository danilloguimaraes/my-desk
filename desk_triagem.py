"""desk_triagem — revisão em lote das pendências abertas de uma frente, num buffer de editor.

Contrato do buffer: SOLUCAO.md. As transições são as de desk_escrita.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import date

import desk
import desk_escrita as esc

LINHA_RE = re.compile(r"^(?:(\d+)\s+)?\[( |x|-)\]\s+(.+?)\s*$")

AJUDA = [
    "# Marcas: [ ] aberta · [x] concluir hoje · [-] descartar (exige '— motivo: ...')",
    "# Mover a linha para a outra seção muda a prioridade. '— crítica' marca a crítica da frente.",
    "# Linha sem número = pendência nova (exige @responsável). Apagar linha numerada é erro.",
    "# Remover todas as linhas de item cancela. Linhas iniciadas por '#' são ignoradas.",
]


def versao(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:8]


def renderizar_buffer(frente_id: str, texto: str) -> str:
    itens = {it.indice: it for it in esc.itens_abertos(texto)}
    blocos: dict[str, list[str]] = {s: [] for s in desk.SECOES_ABERTAS}
    secao = ""
    for i, linha in enumerate(texto.splitlines()):
        if linha.startswith("## "):
            secao = linha[3:].strip()
        elif secao in blocos and linha.startswith("### "):
            blocos[secao].append(f"# {linha}")
        elif i in itens:
            blocos[itens[i].secao].append(f"{itens[i].chave} [ ] {itens[i].conteudo}")
    saida = [f"# desk triagem {frente_id} — versão {versao(texto)}", *AJUDA]
    for s in desk.SECOES_ABERTAS:
        saida += ["", f"## {s}", *blocos[s]]
    return "\n".join(saida) + "\n"


@dataclass
class Leitura:
    mudancas: dict[int, esc.Mudanca] = field(default_factory=dict)
    novas: list[esc.Mudanca] = field(default_factory=list)
    erros: list[str] = field(default_factory=list)
    cancelado: bool = False


def interpretar_buffer(buffer: str, itens: list[esc.Item]) -> Leitura:
    por_chave = {it.chave: it for it in itens}
    r, vistas, secao, algum = Leitura(), set(), None, False
    for bruta in buffer.splitlines():
        linha = bruta.strip()
        if linha.startswith("## "):
            nome = linha[3:].strip()
            secao = nome if nome in desk.SECOES_ABERTAS else None
            if secao is None:
                r.erros.append(f"seção desconhecida '{nome}' (use Urgente ou Em aberto)")
            continue
        if not linha or linha.startswith("#"):
            continue
        m = LINHA_RE.match(linha)
        if not m:
            r.erros.append(f"'{linha[:50]}': esperado '<nº> [ ] texto' ou '[ ] texto'")
            continue
        algum = True
        chave, situacao, conteudo = m.group(1), desk.MARCA_SITUACAO[m.group(2)], m.group(3)
        ref = f"nº {chave}" if chave else f"'{linha[:50]}'"
        if chave is not None:
            k = int(chave)
            if k not in por_chave:
                r.erros.append(f"{ref}: não existe nesta versão do arquivo")
                continue
            if k in vistas:
                r.erros.append(f"{ref}: repetido")
                continue
            vistas.add(k)
        if secao is None:
            r.erros.append(f"{ref}: item fora de '## Urgente' ou '## Em aberto'")
            continue
        if situacao == "descartada" and not esc.tem_motivo(conteudo):
            r.erros.append(f"{ref}: descarte exige '— motivo: ...'")
            continue
        if chave is None:
            if situacao != "aberta":
                r.erros.append(f"{ref}: pendência nova não nasce encerrada")
            elif not any(c.startswith("@") and len(c) > 1 for c in esc.campos(conteudo)[1:]):
                r.erros.append(f"{ref}: pendência nova exige '— @responsável'")
            else:
                r.novas.append(esc.Mudanca("aberta", secao, conteudo))
            continue
        it = por_chave[int(chave)]
        if situacao == "aberta" and secao == it.secao and conteudo == it.conteudo.strip():
            continue
        r.mudancas[int(chave)] = esc.Mudanca(situacao, secao, conteudo)
    if not algum:
        return Leitura(cancelado=True)
    faltando = sorted(set(por_chave) - vistas)
    if faltando:
        r.erros.append(f"nº {', '.join(map(str, faltando))} sumiram do buffer; para encerrar use [x] ou [-]")
    return r


def aplicar_buffer(frente: desk.Frente, texto: str, buffer: str,
                   hoje: date) -> tuple[str | None, list[str], Leitura]:
    """(texto novo, erros, leitura). Texto None = cancelado; com erros, nada deve ser gravado."""
    leitura = interpretar_buffer(buffer, esc.itens_abertos(texto))
    if leitura.cancelado:
        return None, [], leitura
    if leitura.erros:
        return texto, leitura.erros, leitura
    novo = esc.reescrever(texto, leitura.mudancas, leitura.novas, hoje)
    return novo, esc.erros_novos(frente, texto, novo), leitura


def resumir(leitura: Leitura) -> str:
    rotulos = (("concluída", "concluída(s)"), ("descartada", "descartada(s)"), ("aberta", "alterada(s)"))
    partes = [f"{n} {rotulo}" for situacao, rotulo in rotulos
              if (n := sum(m.situacao == situacao for m in leitura.mudancas.values()))]
    if leitura.novas:
        partes.append(f"{len(leitura.novas)} nova(s)")
    return ", ".join(partes) or "nada mudou"
