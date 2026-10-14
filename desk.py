#!/usr/bin/env python3
"""desk — leitura, verificação e ingestão assistida do my-desk.

Contrato: SOLUCAO.md. Modelo: DOMINIO.md. Python 3.10+, apenas stdlib.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Callable

RAIZ = Path(__file__).resolve().parent
SITUACOES = ("ativa", "pausada", "arquivada")
SECOES = ("Urgente", "Em aberto", "Concluídas", "Descartadas")
SECOES_ABERTAS = ("Urgente", "Em aberto")
MARCA_SITUACAO = {" ": "aberta", "x": "concluída", "-": "descartada"}
SECAO_FINAL = {"concluída": "Concluídas", "descartada": "Descartadas"}
ARQUIVOS_FRENTE = ("README.md", "PENDENCIAS.md", "DECISOES.md", "PESSOAS.md")
PASTAS_ARTEFATO = ("reunioes", "rascunhos", "leituras")
LEGACY_MD = ("monitoramento.md", "projeto.md", "planejamento.md", "calendario.md", "comunicacoes.md", "plano_acoes.md")
LARGURA_PAINEL = 40
SEPARADOR = " — "

PENDENCIA_RE = re.compile(r"^- \[( |x|-)\] (.+)$")
NUMERADA_RE = re.compile(r"^\s*\d+\. \[[ x-]\]")
FICHA_LINHA_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$")
DATA_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATA_BR_RE = re.compile(r"^\d{2}/\d{2}/\d{4}$")


@dataclass
class Erro:
    arquivo: str
    linha: int | None
    mensagem: str

    def __str__(self) -> str:
        local = self.arquivo if self.linha is None else f"{self.arquivo}:{self.linha}"
        return f"{local}: {self.mensagem}"


@dataclass
class Pendencia:
    descricao: str
    secao: str
    linha: int
    situacao: str = "aberta"
    responsavel: str | None = None
    prazo: str | None = None
    origem: str | None = None
    critica: bool = False
    concluida_em: str | None = None
    descartada_em: str | None = None
    motivo: str | None = None

    @property
    def aberta(self) -> bool:
        return self.situacao == "aberta"

    @property
    def urgente(self) -> bool:
        return self.aberta and self.secao == "Urgente"


@dataclass
class Frente:
    id: str
    pasta: Path
    ficha: dict[str, str] = field(default_factory=dict)
    pendencias: list[Pendencia] = field(default_factory=list)

    @property
    def situacao(self) -> str | None:
        return self.ficha.get("situacao")

    def criticas_abertas(self) -> list[Pendencia]:
        return [p for p in self.pendencias if p.aberta and p.critica]


# --- utilidades -----------------------------------------------------------

def _eh_data(texto: str) -> bool:
    try:
        if DATA_RE.match(texto):
            date.fromisoformat(texto)
            return True
        if DATA_BR_RE.match(texto):
            date.fromisoformat(f"{texto[6:10]}-{texto[3:5]}-{texto[0:2]}")
            return True
    except ValueError:
        return False
    return False


def _normalizar_data(texto: str) -> str:
    if DATA_RE.match(texto):
        return texto
    if DATA_BR_RE.match(texto):
        return f"{texto[6:10]}-{texto[3:5]}-{texto[0:2]}"
    return texto


def _eh_url(texto: str) -> bool:
    return texto.startswith(("http://", "https://"))


def _sufixo(p: Pendencia) -> str:
    partes = [x for x in (p.responsavel, p.prazo) if x]
    return "".join(f"{SEPARADOR}{x}" for x in partes)


def _proxima(f: Frente) -> str:
    criticas = f.criticas_abertas()
    return criticas[0].descricao if len(criticas) == 1 else "(sem crítica única)"


# --- leitura --------------------------------------------------------------

def ler_ficha(texto: str) -> tuple[dict[str, str] | None, int]:
    linhas = texto.splitlines()
    for i, linha in enumerate(linhas):
        if linha.strip().lower() == "| campo | valor |":
            ficha: dict[str, str] = {}
            for linha_ficha in linhas[i + 2:]:  # pula o separador |---|---|
                m = FICHA_LINHA_RE.match(linha_ficha)
                if not m:
                    break
                ficha[m.group(1)] = m.group(2)
            return ficha, i + 1
    return None, 0


def _coerencia(p: Pendencia) -> list[str]:
    erros: list[str] = []
    if p.concluida_em and p.situacao != "concluída":
        erros.append(f"pendência {p.situacao} com data de conclusão")
    if p.descartada_em and p.situacao != "descartada":
        erros.append(f"pendência {p.situacao} com data de descarte")
    if p.situacao == "concluída" and not p.concluida_em:
        erros.append("pendência concluída sem 'concluída em AAAA-MM-DD'")
    if p.situacao == "descartada":
        if not p.descartada_em:
            erros.append("pendência descartada sem 'descartada em AAAA-MM-DD'")
        if not p.motivo:
            erros.append("pendência descartada sem 'motivo: ...'")
    esperada = SECAO_FINAL.get(p.situacao)
    if esperada is None and p.secao not in SECOES_ABERTAS:
        erros.append(f"pendência aberta em '{p.secao}'")
    if esperada and p.secao != esperada:
        erros.append(f"pendência {p.situacao} fora de '{esperada}' (está em '{p.secao}')")
    return erros


def interpretar_pendencia(linha: str, secao: str, numero: int) -> tuple[Pendencia | None, list[str]]:
    m = PENDENCIA_RE.match(linha)
    if m is None:
        return None, ["linha malformada: esperado '- [ ] ', '- [x] ' ou '- [-] ' no início"]
    partes = [p.strip() for p in m.group(2).split(SEPARADOR)]
    p = Pendencia(descricao=partes[0], secao=secao, linha=numero, situacao=MARCA_SITUACAO[m.group(1)])
    erros: list[str] = []
    if not p.descricao:
        erros.append("descrição vazia")
    for campo in partes[1:]:
        if campo.startswith("@") and len(campo) > 1:
            if p.responsavel:
                p.responsavel = f"{p.responsavel} {campo}".strip()
            else:
                p.responsavel = campo
        elif _eh_data(campo) or campo in ("sem prazo", "imediato", "próxima sessão", "esta semana", "próximo"):
            if p.prazo is None:
                p.prazo = campo
            else:
                erros.append(f"prazo repetido ou mal posicionado: '{campo}'")
        elif campo.startswith("concluída em "):
            data_txt = campo[len("concluída em "):]
            if _eh_data(data_txt):
                p.concluida_em = _normalizar_data(data_txt)
            else:
                erros.append(f"data de conclusão inválida: {data_txt}")
        elif campo.startswith("descartada em "):
            data_txt = campo[len("descartada em "):]
            if _eh_data(data_txt):
                p.descartada_em = _normalizar_data(data_txt)
            else:
                erros.append(f"data de descarte inválida: {data_txt}")
        elif campo.startswith("motivo: "):
            p.motivo = campo[len("motivo: "):].strip() or None
        elif campo.startswith("origem: "):
            p.origem = campo[len("origem: "):].strip()
        elif campo == "crítica":
            p.critica = True
        elif p.motivo is not None:
            erros.append("trecho após 'motivo:' — o motivo não pode conter ' — '")
        else:
            # Compatibilidade legada: campos textuais livres viram contexto e não bloqueiam a leitura.
            pass
    erros += _coerencia(p)
    return p, erros


def ler_pendencias_texto(texto: str, rel: str) -> tuple[list[Pendencia], list[Erro]]:
    pendencias: list[Pendencia] = []
    erros: list[Erro] = []
    secao = ""
    for numero, linha in enumerate(texto.splitlines(), start=1):
        if linha.startswith("## "):
            secao = linha[3:].strip()
            continue
        if NUMERADA_RE.match(linha):
            erros.append(Erro(rel, numero, "pendência em lista numerada: use '- [ ] ' (invisível ao painel)"))
            continue
        if not linha.lstrip().startswith("- ["):
            continue
        if secao not in SECOES:
            erros.append(Erro(rel, numero, f"pendência fora das seções {', '.join(SECOES)}"))
            continue
        pend, problemas = interpretar_pendencia(linha, secao, numero)
        erros += [Erro(rel, numero, msg) for msg in problemas]
        if pend:
            pendencias.append(pend)
    return pendencias, erros


def ler_pendencias(arquivo: Path, rel: str) -> tuple[list[Pendencia], list[Erro]]:
    return ler_pendencias_texto(arquivo.read_text(encoding="utf-8"), rel)


def descobrir_pastas(raiz: Path) -> list[Path]:
    """Frente = pasta (fora da raiz) com ao menos um .md direto."""
    encontradas: list[Path] = []

    def percorrer(pasta: Path) -> None:
        for sub in sorted(pasta.iterdir()):
            if not sub.is_dir() or sub.name.startswith(".") or sub.name in PASTAS_ARTEFATO:
                continue
            if any(f.is_file() and f.suffix == ".md" for f in sub.iterdir()):
                encontradas.append(sub)
            percorrer(sub)

    percorrer(raiz)
    return encontradas


def verificar_artefatos(pasta: Path, rel: str) -> list[Erro]:
    erros: list[Erro] = []
    for item in sorted(pasta.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir():
            if item.name not in PASTAS_ARTEFATO:
                erros.append(Erro(f"{rel}/{item.name}/", None, "pasta não reconhecida (invariante 6)"))
                continue
            for arq in sorted(item.iterdir()):
                if arq.name.startswith("."):
                    continue
                if arq.is_dir() or arq.suffix != ".md":
                    erros.append(Erro(f"{rel}/{item.name}/{arq.name}", None,
                                      "artefato não reconhecido (invariante 6)"))
        elif item.suffix.lower() == ".pdf":
            continue
        elif item.suffix == ".md" and item.name not in ARQUIVOS_FRENTE and item.name not in LEGACY_MD:
            erros.append(Erro(f"{rel}/{item.name}", None, "artefato não reconhecido (invariante 6)"))
    return erros


def validar_ficha(ficha: dict[str, str], arquivo: str, linha: int) -> list[Erro]:
    erros: list[Erro] = []
    if ficha.get("situacao") not in SITUACOES:
        erros.append(Erro(arquivo, linha, f"situacao deve ser uma de {SITUACOES}"))
    for campo in ("papel", "estado"):
        if not ficha.get(campo):
            erros.append(Erro(arquivo, linha, f"campo '{campo}' ausente ou vazio"))
    return erros


def verificar_cruzado(frentes: list[Frente]) -> list[Erro]:
    erros: list[Erro] = []
    urgentes_vistas: dict[str, str] = {}
    for f in frentes:
        arq = f"{f.id}/PENDENCIAS.md"
        for p in f.pendencias:
            if p.urgente:
                if p.descricao in urgentes_vistas:
                    erros.append(Erro(arq, p.linha, f"urgência duplicada (já em {urgentes_vistas[p.descricao]}) "
                                                    "(invariante 1)"))
                else:
                    urgentes_vistas[p.descricao] = f"{arq}:{p.linha}"
            if p.origem and not _eh_url(p.origem) and not (f.pasta / p.origem.split("#")[0]).is_file():
                erros.append(Erro(arq, p.linha, f"origem inexistente: {p.origem} (invariante 5)"))
        if f.situacao == "ativa":
            n = len(f.criticas_abertas())
            if n != 1:
                erros.append(Erro(arq, None, f"frente ativa precisa de exatamente 1 pendência aberta crítica "
                                             f"(tem {n}) (invariante 3)"))
    return erros


def resolver_frente(frentes: list[Frente], texto: str) -> Frente:
    exata = next((f for f in frentes if f.id == texto), None)
    if exata:
        return exata
    por_sufixo = [f for f in frentes if f.id.rsplit("/", 1)[-1] == texto]
    if len(por_sufixo) == 1:
        return por_sufixo[0]
    if por_sufixo:
        raise ValueError(f"frente ambígua '{texto}': {', '.join(f.id for f in por_sufixo)}")
    raise ValueError(f"frente não encontrada: {texto}")


def carregar(raiz: Path = RAIZ) -> tuple[list[Frente], list[Erro]]:
    frentes: list[Frente] = []
    erros: list[Erro] = []
    for pasta in descobrir_pastas(raiz):
        rel = pasta.relative_to(raiz).as_posix()
        frente = Frente(id=rel, pasta=pasta)
        frentes.append(frente)
        erros += verificar_artefatos(pasta, rel)
        readme = pasta / "README.md"
        if not readme.is_file():
            erros.append(Erro(f"{rel}/README.md", None, "ficha ausente: README.md não existe"))
        else:
            ficha, linha = ler_ficha(readme.read_text(encoding="utf-8"))
            if ficha is None:
                erros.append(Erro(f"{rel}/README.md", None,
                                  "ficha ausente: falta a tabela '| campo | valor |'"))
            else:
                frente.ficha = ficha
                erros += validar_ficha(ficha, f"{rel}/README.md", linha)
        pend = pasta / "PENDENCIAS.md"
        if pend.is_file():
            frente.pendencias, errs = ler_pendencias(pend, f"{rel}/PENDENCIAS.md")
            erros += errs
    erros += verificar_cruzado(frentes)
    return frentes, erros


# --- renderização ---------------------------------------------------------

def renderizar_painel(frentes: list[Frente], erros: list[Erro]) -> list[str]:
    ativas = [f for f in frentes if f.situacao == "ativa"]
    linhas: list[str] = []
    if erros:
        linhas += [f"ATENÇÃO: {len(erros)} inconsistência(s) — rode `desk check`", ""]
    linhas += ["## Frentes ativas", "", "| Frente | Papel | Estado | Próxima ação crítica |", "|---|---|---|---|"]
    linhas += [f"| {f.id} | {f.ficha.get('papel', '')} | {f.ficha.get('estado', '')} | {_proxima(f)} |"
               for f in ativas]
    linhas += ["", "## Urgentes", ""]
    urgentes = [(f, p) for f in ativas for p in f.pendencias if p.urgente]
    linhas += [f"- [{f.id}] {p.descricao}{_sufixo(p)}" for f, p in urgentes] or ["Nenhuma urgência aberta."]
    if len(linhas) > LARGURA_PAINEL:
        linhas.append(f"(saída com {len(linhas)} linhas; o limite é {LARGURA_PAINEL} — RF-N1.5)")
    return linhas


def renderizar_frente(f: Frente, erros: list[Erro]) -> list[str]:
    linhas = [f"## {f.id}", ""]
    linhas += [f"- {campo}: {f.ficha.get(campo, '—')}" for campo in ("situacao", "papel", "estado")]
    linhas.append(f"- próxima ação crítica: {_proxima(f)}")
    abertas = [p for p in f.pendencias if p.aberta and p.secao in SECOES_ABERTAS]
    linhas += ["", f"### Pendências abertas ({len(abertas)})"]
    linhas += [f"{n}. {'[URGENTE] ' if p.urgente else ''}{p.descricao}{_sufixo(p)}"
               for n, p in enumerate(abertas, start=1)]
    reunioes = sorted((f.pasta / "reunioes").glob("*.md"), reverse=True)[:3]
    if reunioes:
        linhas += ["", "### Últimos registros"] + [f"- reunioes/{r.name}" for r in reunioes]
    proprias = [e for e in erros if e.arquivo.startswith(f"{f.id}/")]
    if proprias:
        linhas += ["", f"### Inconsistências ({len(proprias)})"] + [f"- {e}" for e in proprias]
    return linhas


# --- escrita assistida ----------------------------------------------------

def validar_descricao(texto: str) -> str:
    if not texto.strip():
        raise ValueError("descrição não pode ser vazia")
    if SEPARADOR in texto:
        raise ValueError("descrição não pode conter ' — ' (é o separador de campos)")
    return texto.strip()


def validar_responsavel(texto: str) -> str:
    nome = texto.strip().lstrip("@")
    if not nome or " " in nome:
        raise ValueError("responsável: um nome, sem espaços (ex.: Danillo)")
    return f"@{nome}"


def validar_prazo(texto: str) -> str:
    if not _eh_data(texto):
        raise ValueError("prazo: data no formato AAAA-MM-DD")
    return texto


def validar_origem(texto: str, pasta: Path) -> str:
    if _eh_url(texto):
        return texto
    if not (pasta / texto.split("#")[0]).is_file():
        raise ValueError(f"origem: arquivo não encontrado a partir da frente ({texto})")
    return texto


def inserir_em_secao(linhas: list[str], secao: str, novas: list[str], topo: bool) -> list[str]:
    """Insere `novas` em `## secao`: no topo (encerradas, mais recente primeiro) ou no fim do
    bloco de topo, antes da primeira subseção `###`. Cria a seção no fim se não existir."""
    cabecalho = f"## {secao}"
    if cabecalho not in linhas:
        linhas = linhas + ["", cabecalho]
    i = linhas.index(cabecalho)
    fim = i + 1
    while fim < len(linhas) and not linhas[fim].startswith("## "):
        fim += 1
    if topo:
        k = i + 1
        dentro = False  # dentro de um comentário HTML que abre e fecha em linhas diferentes
        while k < fim:
            limpa = linhas[k].strip()
            if dentro or limpa.startswith("<!--"):
                dentro = "-->" not in limpa
            elif limpa:
                break
            k += 1
    else:
        k = next((j for j in range(i + 1, fim) if linhas[j].startswith("### ")), fim)
        while k > i + 1 and not linhas[k - 1].strip():
            k -= 1
    return linhas[:k] + novas + linhas[k:]


def gravar_atomico(arquivo: Path, texto: str) -> None:
    tmp = arquivo.with_name(f".{arquivo.name}.tmp")
    tmp.write_text(texto, encoding="utf-8")
    os.replace(tmp, arquivo)


def adicionar_pendencia(frente: Frente, descricao: str, responsavel: str, urgente: bool = False,
                        critica: bool = False, prazo: str | None = None,
                        origem: str | None = None) -> str:
    partes = [validar_descricao(descricao), validar_responsavel(responsavel)]
    if prazo:
        partes.append(validar_prazo(prazo))
    if origem:
        partes.append(f"origem: {validar_origem(origem, frente.pasta)}")
    if critica:
        existentes = frente.criticas_abertas()
        if existentes:
            raise ValueError(f"a frente já tem crítica aberta: '{existentes[0].descricao}'. "
                             "Conclua-a ou retire a marca antes")
        partes.append("crítica")
    linha = "- [ ] " + SEPARADOR.join(partes)
    arquivo = frente.pasta / "PENDENCIAS.md"
    texto = arquivo.read_text(encoding="utf-8") if arquivo.is_file() else "# Pendências\n"
    linhas = inserir_em_secao(texto.splitlines(), "Urgente" if urgente else "Em aberto", [linha], topo=False)
    gravar_atomico(arquivo, "\n".join(linhas) + "\n")
    return linha


def assistente(raiz: Path = RAIZ, entrada: Callable[[str], str] = input,
               saida: Callable[[str], None] = print) -> int:
    frentes, _ = carregar(raiz)
    por_id = {f.id: f for f in frentes if f.ficha}
    saida("Frentes disponíveis: " + ", ".join(sorted(por_id)))

    def perguntar(rotulo: str, validar: Callable[[str], object]):
        while True:
            resposta = entrada(f"{rotulo}: ").strip()
            try:
                return validar(resposta)
            except ValueError as e:
                saida(f"  ! {e}")

    def sim_nao(texto: str) -> bool:
        if texto.lower() in ("", "n", "nao", "não"):
            return False
        if texto.lower() in ("s", "sim"):
            return True
        raise ValueError("responda s ou n")

    def frente_valida(texto: str) -> Frente:
        if texto not in por_id:
            raise ValueError(f"frente desconhecida: '{texto}'")
        return por_id[texto]

    frente = perguntar("Frente", frente_valida)
    descricao = perguntar("Descrição", validar_descricao)
    responsavel = perguntar("Responsável (nome)", validar_responsavel)
    urgente = perguntar("Urgente? [s/N]", sim_nao)

    def critica_valida(texto: str) -> bool:
        quer = sim_nao(texto)
        if quer and frente.criticas_abertas():
            raise ValueError(f"a frente já tem crítica aberta: '{frente.criticas_abertas()[0].descricao}'")
        return quer

    critica = perguntar("Crítica da frente? [s/N]", critica_valida)
    prazo = perguntar("Prazo AAAA-MM-DD (vazio = nenhum)", lambda t: validar_prazo(t) if t else None)
    origem = perguntar("Origem: caminho relativo ou URL (vazio = nenhuma)",
                       lambda t: validar_origem(t, frente.pasta) if t else None)
    linha = adicionar_pendencia(frente, descricao, responsavel, urgente, critica, prazo, origem)
    saida(f"Registrado em {frente.id}/PENDENCIAS.md:\n{linha}")
    return 0


# --- CLI ------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="desk", description="Painel, verificação e ingestão assistida do my-desk.")
    sub = parser.add_subparsers(dest="comando")
    sub.add_parser("painel", help="painel consolidado (padrão)")
    p_frente = sub.add_parser("frente", help="visão de uma frente")
    p_frente.add_argument("id")
    sub.add_parser("check", help="verifica as invariantes; exit 1 se houver erro")
    sub.add_parser("add", help="registra uma pendência por perguntas")
    for verbo, ajuda in (("feito", "conclui uma pendência"), ("descartar", "descarta uma pendência, com motivo"),
                         ("urgente", "move para Urgente"), ("normal", "move para Em aberto"),
                         ("critica", "transfere a marca de crítica da frente")):
        p = sub.add_parser(verbo, help=ajuda)
        p.add_argument("frente")
        p.add_argument("alvo", nargs="*", help="nº de `desk frente` ou trecho do texto; vazio = menu")
        p.add_argument("--sim", action="store_true", help="não pergunta (uso por agentes)")
        if verbo == "descartar":
            p.add_argument("--motivo")
    args = parser.parse_args(argv)
    comando = args.comando or "painel"

    if comando == "add":
        return assistente(RAIZ)

    frentes, erros = carregar(RAIZ)
    if comando in ("feito", "descartar", "urgente", "normal", "critica"):
        import desk_escrita
        try:
            f = resolver_frente(frentes, args.frente)
            return desk_escrita.executar(comando, f, " ".join(args.alvo) or None,
                                         motivo=getattr(args, "motivo", None), sim=args.sim)
        except ValueError as e:
            print(f"erro: {e}")
            return 1
    if comando == "check":
        if not erros:
            print("ok: nenhuma inconsistência")
            return 0
        for e in erros:
            print(e)
        print(f"{len(erros)} inconsistência(s)")
        return 1
    if comando == "frente":
        try:
            f = resolver_frente(frentes, args.id)
        except ValueError as e:
            print(e)
            return 1
        print("\n".join(renderizar_frente(f, erros)))
        return 0
    print("\n".join(renderizar_painel(frentes, erros)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
