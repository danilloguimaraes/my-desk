"""desk_triagem — revisão em lote das pendências abertas de uma frente, num buffer de editor.

Contrato do buffer: SOLUCAO.md. As transições são as de desk_escrita.
"""
from __future__ import annotations

import hashlib

import desk
import desk_escrita as esc

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
