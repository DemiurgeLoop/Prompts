#!/usr/bin/env python3
"""Sincroniza e verifica os módulos embutidos (Lectern e Vernacular) nos prompts da Mundo Livre FM.

Uso (da raiz do repositório):
    python3 -I tools/sync_modules.py check   # só confere; sai com código 1 se achar divergência
    python3 -I tools/sync_modules.py sync    # regrava os blocos embutidos a partir das fontes e confere de novo

Fontes únicas: `Mundo Livre FM/Lectern v*.md` e `Vernacular v*.md`. Os blocos embutidos nos prompts
nunca se editam à mão: muda-se a fonte e roda-se `sync`. Só usa a biblioteca padrão.
O `sync` não renomeia arquivos nem mexe em versões: depois dele, suba a versão de cada prompt alterado
e acrescente a nota de versão (ver CLAUDE.md).
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML = os.path.join(ROOT, "Mundo Livre FM")

# Quais seções da Vernacular cada prompt embute (títulos exatos da fonte).
TODO_CANONE = "*"  # todas as seções do Cânone, menos "Texto para o ouvido"
MUNDO_LIVRE_BASE = ["O leitor da casa", "Registro por parte do texto", "Proibidos da casa", "Fontes da casa"]
EMBEDS = {
    "Gazette": {"canone": TODO_CANONE, "ml": MUNDO_LIVRE_BASE, "perfis": ["CONTEÚDO", "NOTÍCIA"],
                "titulo": "CÂNONE + MUNDO LIVRE + PERFIL CONTEÚDO + PERFIL NOTÍCIA"},
    "Aion": {"canone": TODO_CANONE, "ml": MUNDO_LIVRE_BASE, "perfis": ["CONTEÚDO", "NARRATIVA"],
             "titulo": "CÂNONE + MUNDO LIVRE + PERFIL CONTEÚDO + PERFIL NARRATIVA"},
    "Pantheon": {"canone": TODO_CANONE, "ml": MUNDO_LIVRE_BASE, "perfis": ["CONTEÚDO", "NARRATIVA"],
                 "titulo": "CÂNONE + MUNDO LIVRE + PERFIL CONTEÚDO + PERFIL NARRATIVA"},
    "Herodotus": {"canone": TODO_CANONE, "ml": MUNDO_LIVRE_BASE, "perfis": ["CONTEÚDO", "NARRATIVA"],
                  "titulo": "CÂNONE + MUNDO LIVRE + PERFIL CONTEÚDO + PERFIL NARRATIVA"},
    "Hermes": {"canone": ["Registro", "Voz de máquina", "O leitor", "Frase", "Palavra", "Texto para a tela",
                          "Texto para o ouvido"],
               "ml": ["O leitor da casa", "Proibidos da casa"], "perfis": ["LOCUÇÃO"],
               "titulo": "RECORTE LOCUÇÃO", "sufixo": " (RECORTE)"},
}

erros, avisos = [], []
HEAD = re.compile(r"^(#{1,6}) (.*)$", re.M)


def find(pattern):
    r = sorted(glob.glob(pattern))
    return r[0] if r else None


def read(path):
    with open(path, encoding="utf8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf8") as f:
        f.write(text)


def version_of(path):
    m = re.search(r" v(\d+\.\d+\.\d+) - ", os.path.basename(path))
    return m.group(1) if m else None


# ---------------------------------------------------------------- Lectern
def lectern_body(text):
    a = text.index("### Por que ainda se lê")
    b = text.index("\n---\n", text.index("### Teste da Lectern"))
    return text[a:b].rstrip() + "\n"


def lectern_region(text):
    h = re.search(r"^## LEITOR E BUSCA: LECTERN v[\d.]+$", text, re.M)
    if not h:
        return None
    s = text.index("### Por que ainda se lê", h.end())
    n = re.search(r"^## (?!#)", text[s:], re.M)
    return h, s, s + n.start()


def embedded_lectern(text, s, e):
    return re.sub(r"\n---\s*$", "", text[s:e].rstrip()).rstrip() + "\n"


# ---------------------------------------------------------------- Vernacular
def parse_sections(text):
    """Lista de (nivel, titulo, corpo): o corpo vai até o próximo título, de qualquer nível."""
    ms = list(HEAD.finditer(text))
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        out.append((len(m.group(1)), m.group(2).strip(), text[m.end():end]))
    return out


def norm(body):
    lines = [l.rstrip() for l in body.strip().split("\n")]
    while lines and lines[-1].strip() in ("", "---"):
        lines.pop()
    return "\n".join(lines)


def bare(title):
    return re.sub(r"\s*\[[^\]]*\]\s*$", "", title).strip()


def expected_sequence(vtext, cfg):
    """Sequência (titulo, corpo normalizado) que o embutimento deve ter, a partir da Vernacular."""
    secs = parse_sections(vtext)
    suf = cfg.get("sufixo", "")

    def bloco(nome_h2):
        i = next(k for k, s in enumerate(secs) if s[0] == 2 and s[1] == nome_h2)
        j = next((k for k in range(i + 1, len(secs)) if secs[k][0] <= 2), len(secs))
        return secs[i:j]

    seq = [("CÂNONE" + suf, "")]
    for lvl, tit, corpo in bloco("CÂNONE")[1:]:
        if lvl != 3:
            continue
        if cfg["canone"] == TODO_CANONE:
            if bare(tit) == "Texto para o ouvido":
                continue
        elif bare(tit) not in cfg["canone"]:
            continue
        seq.append((tit, norm(corpo)))
    ml = bloco("CONTEXTO MUNDO LIVRE")
    seq.append(("CONTEXTO MUNDO LIVRE" + suf, ""))
    for lvl, tit, corpo in ml[1:]:
        if lvl == 3 and bare(tit) in cfg["ml"]:
            seq.append((tit, norm(corpo)))
    for nome in cfg["perfis"]:
        i = next(k for k, s in enumerate(ml) if s[0] == 3 and s[1] == f"PERFIL {nome}")
        j = next((k for k in range(i + 1, len(ml)) if ml[k][0] <= 3), len(ml))
        for lvl, tit, corpo in ml[i:j]:
            seq.append((tit, norm(corpo)))
    return seq


def vernacular_header(text):
    return re.search(r"^## PROSA: VERNACULAR v([\d.]+), (.*)$", text, re.M)


def actual_sequence(text, h, n):
    secs = parse_sections(text[h.end():])[:n]
    return [(t, norm(c)) for _, t, c in secs]


# ---------------------------------------------------------------- verificações
def check_modules(lec_path, ver_path):
    lec_ver, ver_ver = version_of(lec_path), version_of(ver_path)
    body = lectern_body(read(lec_path))
    vtext = read(ver_path)
    for nome, cfg in EMBEDS.items():
        p = find(os.path.join(ML, f"{nome} v*.md"))
        if not p:
            erros.append(f"{nome}: arquivo não encontrado")
            continue
        t = read(p)
        reg = lectern_region(t)
        if not reg:
            erros.append(f"{nome}: sem bloco 'LEITOR E BUSCA: LECTERN'")
        else:
            h, s, e = reg
            if embedded_lectern(t, s, e) != body:
                erros.append(f"{nome}: a Lectern embutida difere da fonte (v{lec_ver})")
            v = re.search(r"v([\d.]+)$", h.group(0)).group(1)
            if v != lec_ver:
                erros.append(f"{nome}: o título diz Lectern v{v}, a fonte é v{lec_ver}")
        h = vernacular_header(t)
        if not h:
            erros.append(f"{nome}: sem bloco 'PROSA: VERNACULAR'")
            continue
        if h.group(1) != ver_ver:
            erros.append(f"{nome}: o título diz Vernacular v{h.group(1)}, a fonte é v{ver_ver}")
        if h.group(2).strip() != cfg["titulo"]:
            avisos.append(f"{nome}: partes do título ('{h.group(2).strip()}') diferem do esperado ('{cfg['titulo']}')")
        esp = expected_sequence(vtext, cfg)
        act = actual_sequence(t, h, len(esp))
        if len(act) < len(esp):
            erros.append(f"{nome}: faltam seções da Vernacular embutida ({len(act)} de {len(esp)})")
        for k, (e_, a_) in enumerate(zip(esp, act)):
            if e_[0] != a_[0]:
                erros.append(f"{nome}: a seção {k + 1} da Vernacular embutida devia ser '{e_[0]}' e é '{a_[0]}'")
                break
            if e_[1] != a_[1]:
                erros.append(f"{nome}: a seção '{e_[0]}' da Vernacular embutida difere da fonte")


def check_names():
    gp = os.path.join(ROOT, "docs", "Nomes e filosofia dos prompts.md")
    guia = read(gp) if os.path.exists(gp) else None
    for p in sorted(glob.glob(os.path.join(ROOT, "*.md")) + glob.glob(os.path.join(ML, "*.md"))):
        b = os.path.basename(p)
        if b in ("README.md", "CLAUDE.md"):
            continue
        m = re.match(r"^([A-Z][A-Za-z]+) v(\d+\.\d+\.\d+) - .+\.md$", b)
        if not m:
            erros.append(f"{b}: nome fora do padrão 'Codename vX.Y.Z - Descrição.md'")
            continue
        nome, ver = m.group(1), m.group(2)
        t = read(p)
        h1 = re.search(r"^# (\w+) v([\d.]+)", t, re.M)
        if not h1 or h1.group(1) != nome:
            avisos.append(f"{b}: sem H1 '# {nome} vX.Y.Z | ...'")
        elif h1.group(2) != ver:
            erros.append(f"{b}: o H1 diz v{h1.group(2)} e o nome do arquivo diz v{ver}")
        if guia is not None and not re.search(r"^### " + nome + r"\s*$", guia, re.M):
            erros.append(f"{b}: sem entrada em docs/Nomes e filosofia dos prompts.md")
        notas = re.findall(r"^\*" + nome + r" v(\d+\.\d+\.\d+)[:.]", t, re.M)
        if not notas:
            avisos.append(f"{b}: sem nota de versão no rodapé")
        elif notas[0] != ver:
            erros.append(f"{b}: a nota mais recente é v{notas[0]} e o arquivo é v{ver}")


# ---------------------------------------------------------------- sincronização
def sync(lec_path, ver_path):
    lec_ver, ver_ver = version_of(lec_path), version_of(ver_path)
    body = lectern_body(read(lec_path))
    vtext = read(ver_path)
    for nome, cfg in EMBEDS.items():
        p = find(os.path.join(ML, f"{nome} v*.md"))
        t = read(p)
        # Lectern: troca o módulo e o título, sem tocar no que o rodeia
        h, s, e = lectern_region(t)
        t = t[:s] + t[s:e].replace(embedded_lectern(t, s, e), body, 1) + t[e:]
        t = re.sub(r"^## LEITOR E BUSCA: LECTERN v[\d.]+$", f"## LEITOR E BUSCA: LECTERN v{lec_ver}", t, count=1, flags=re.M)
        # Vernacular: título e corpo de cada seção esperada
        hv = vernacular_header(t)
        t = t[:hv.start()] + f"## PROSA: VERNACULAR v{ver_ver}, {cfg['titulo']}" + t[hv.end():]
        pos = vernacular_header(t).end()
        for tit, corpo in expected_sequence(vtext, cfg):
            m = re.compile(r"^#{1,6} " + re.escape(tit) + r"$", re.M).search(t, pos)
            if not m:
                erros.append(f"{nome}: não achei a seção '{tit}' para sincronizar")
                break
            prox = HEAD.search(t, m.end())
            fim = prox.start() if prox else len(t)
            if corpo:
                regiao = t[m.end():fim]
                nucleo = re.sub(r"\n+---\s*$", "", regiao.rstrip()).strip("\n")
                t = t[:m.end()] + regiao.replace(nucleo, corpo, 1) + t[fim:]
                prox = HEAD.search(t, m.end())
            pos = prox.start() if prox else len(t)
        write(p, t)
        print("sync:", os.path.basename(p))


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "check"
    if modo not in ("check", "sync"):
        sys.exit(__doc__)
    lec = find(os.path.join(ML, "Lectern v*.md"))
    ver = find(os.path.join(ROOT, "Vernacular v*.md"))
    if not lec or not ver:
        sys.exit("Lectern ou Vernacular não encontradas.")
    if modo == "sync":
        sync(lec, ver)
    check_modules(lec, ver)
    check_names()
    print(f"Lectern v{version_of(lec)} · Vernacular v{version_of(ver)}")
    for a in avisos:
        print("  aviso:", a)
    for e in erros:
        print("  ERRO :", e)
    print(f"{len(erros)} erro(s), {len(avisos)} aviso(s)")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
