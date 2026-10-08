import random

def fifo(paginas, quantidade_frames):

    frames = []
    fila = []

    page_faults = 0
    hits = 0

    resultados = []

    for pagina in paginas:

        if pagina in frames:
            resultado = "HIT"
            hits += 1

        else:
            resultado = "PAGE FAULT"
            page_faults += 1

            # Ainda existe espaço nos frames
            if len(frames) < quantidade_frames:

                frames.append(pagina)
                fila.append(pagina)

            # Memória cheia
            else:

                pagina_removida = fila.pop(0)

                indice = frames.index(pagina_removida)

                frames[indice] = pagina

                fila.append(pagina)

        resultados.append({
            "pagina": pagina,
            "frames": frames.copy(),
            "resultado": resultado
        })

    return resultados, page_faults, hits

def lru(paginas, quantidade_frames):

    frames = []
    ordem_uso = []

    page_faults = 0
    hits = 0

    resultados = []

    for pagina in paginas:

        # Página já está na memória
        if pagina in frames:

            resultado = "HIT"
            hits += 1

            # Atualiza a página como a mais recentemente usada
            ordem_uso.remove(pagina)
            ordem_uso.append(pagina)

        else:

            resultado = "PAGE FAULT"
            page_faults += 1

            # Ainda existe espaço
            if len(frames) < quantidade_frames:

                frames.append(pagina)

            # Memória cheia
            else:

                pagina_removida = ordem_uso.pop(0)

                indice = frames.index(pagina_removida)

                frames[indice] = pagina

            ordem_uso.append(pagina)

        resultados.append({
            "pagina": pagina,
            "frames": frames.copy(),
            "resultado": resultado
        })

    return resultados, page_faults, hits


def otimo(paginas, quantidade_frames):

    frames = []

    page_faults = 0
    hits = 0

    resultados = []

    for i, pagina in enumerate(paginas):

        if pagina in frames:

            resultado = "HIT"
            hits += 1

        else:

            resultado = "PAGE FAULT"
            page_faults += 1

            # Ainda existe espaço
            if len(frames) < quantidade_frames:

                frames.append(pagina)

            else:

                proximos_acessos = paginas[i + 1:]

                pagina_remover = None
                maior_distancia = -1

                for pagina_frame in frames:

                    # A página não será mais utilizada
                    if pagina_frame not in proximos_acessos:

                        pagina_remover = pagina_frame
                        break

                    # Descobre quando será usada novamente
                    distancia = proximos_acessos.index(pagina_frame)

                    if distancia > maior_distancia:

                        maior_distancia = distancia
                        pagina_remover = pagina_frame

                indice = frames.index(pagina_remover)

                frames[indice] = pagina

        resultados.append({
            "pagina": pagina,
            "frames": frames.copy(),
            "resultado": resultado
        })

    return resultados, page_faults, hits


def mostrar_resultados(resultados, quantidade_frames):

    print("\nPágina | ", end="")

    for i in range(quantidade_frames):
        print(f"Frame {i + 1} | ", end="")

    print("Resultado")

    print("-" * 60)

    for item in resultados:

        print(f"{item['pagina']:6} | ", end="")

        frames = item["frames"]

        for i in range(quantidade_frames):

            if i < len(frames):
                print(f"{frames[i]:7} | ", end="")
            else:
                print(f"{'-':7} | ", end="")

        print(item["resultado"])


def mostrar_estatisticas(page_faults, hits, total):

    taxa_page_faults = (page_faults / total) * 100
    taxa_hits = (hits / total) * 100

    print(f"\nPage Faults: {page_faults}")
    print(f"Hits: {hits}")
    print(f"Taxa de Page Faults: {taxa_page_faults:.2f}%")
    print(f"Taxa de Hits: {taxa_hits:.2f}%")


entrada = input("Digite as páginas separadas por espaço: ")

paginas_usuario = [int(valor) for valor in entrada.split()]

quantidade_frames = int(
    input("Digite a quantidade de frames: ")
)

print("\nSequência:", paginas_usuario)
print("Frames:", quantidade_frames)


print("\n")
print("=" * 60)
print("FIFO")
print("=" * 60)

resultado_fifo, faults_fifo, hits_fifo = fifo(
    paginas_usuario,
    quantidade_frames
)

mostrar_resultados(
    resultado_fifo,
    quantidade_frames
)

mostrar_estatisticas(
    faults_fifo,
    hits_fifo,
    len(paginas_usuario)
)



print("\n")
print("=" * 60)
print("LRU")
print("=" * 60)

resultado_lru, faults_lru, hits_lru = lru(
    paginas_usuario,
    quantidade_frames
)

mostrar_resultados(
    resultado_lru,
    quantidade_frames
)

mostrar_estatisticas(
    faults_lru,
    hits_lru,
    len(paginas_usuario)
)


print("\n")
print("=" * 60)
print("ÓTIMO")
print("=" * 60)

resultado_otimo, faults_otimo, hits_otimo = otimo(
    paginas_usuario,
    quantidade_frames
)

mostrar_resultados(
    resultado_otimo,
    quantidade_frames
)

mostrar_estatisticas(
    faults_otimo,
    hits_otimo,
    len(paginas_usuario)
)


print("\n")
print("=" * 60)
print("COMPARAÇÃO DOS ALGORITMOS")
print("=" * 60)

print(f"FIFO   -> Page Faults: {faults_fifo} | Hits: {hits_fifo}")
print(f"LRU    -> Page Faults: {faults_lru} | Hits: {hits_lru}")
print(f"ÓTIMO  -> Page Faults: {faults_otimo} | Hits: {hits_otimo}")

print("\nMelhor resultado:")

menor_fault = min(
    faults_fifo,
    faults_lru,
    faults_otimo
)

if faults_fifo == menor_fault:
    print("FIFO apresentou o menor número de Page Faults.")

if faults_lru == menor_fault:
    print("LRU apresentou o menor número de Page Faults.")

if faults_otimo == menor_fault:
    print("ÓTIMO apresentou o menor número de Page Faults.")