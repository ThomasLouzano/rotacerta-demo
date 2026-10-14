# Verificação desta entrega

## Executado no ambiente de trabalho

- Análise sintática com `node --check` do script do protótipo, `pwa.js` e `sw.js`.
- Verificação estática do manifesto e dos ícones requeridos.
- Renderização da interface local no Chromium, incorporando recursos no DOM de teste.
- Login e logo Amaro, com larguras de 320, 360, 390, 430, 768 e 1280 pixels; sem rolagem horizontal na tela de login.
- Entrada dos quatro perfis e redirecionamento às suas jornadas.
- Cadastro fictício novo, duas caixas (uma refrigerada), seleção de carga, conferência física, geração de romaneio, início da viagem e conclusão de uma entrega.
- Conferência bloqueia geração de romaneio enquanto há volumes pendentes.
- Os avisos simulados são criados ao iniciar a rota e concluir a parada, não no cadastro/carregamento.
- Controles de instalação e explicação do modo local.
- Ausência de erros JavaScript não tratados e de requisições externas no cenário de interface executado.
- Testes unitários do service worker com APIs de navegador simuladas: lista de arquivos, fallback de cache, exclusão de terceiros, isolamento por caminho e atualização mediante comando.

## Não foi possível verificar aqui

O Chromium disponível bloqueia navegação em URLs por política do ambiente (`ERR_BLOCKED_BY_ADMINISTRATOR`), inclusive localhost. A política não foi alterada. Por isso, a interface foi testada com recursos locais incorporados ao DOM, e o service worker foi testado com mocks.

**Registro real do service worker, recarga offline real e instalação no Android/iOS permanecem pendentes** de execução em navegador que permita o servidor local ou no endereço HTTPS após a publicação. Testes unitários não substituem esse teste de dispositivo.

O repositório e a hospedagem também não foram criados: dependem da conexão e das autorizações do usuário.

## Como repetir os testes

Teste unitário, com Node.js instalado:

```sh
node tests/service-worker.test.cjs
```

Teste completo em um ambiente de desenvolvimento que permita localhost:

```sh
python -m pip install -r tests/requirements.txt
python -m playwright install chromium
python tests/smoke.py
```

Pode-se informar `CHROMIUM_PATH` quando o executável está em outro local. O teste completo abre seu próprio servidor HTTP temporário e o encerra ao concluir.

Teste de interface sem navegação de rede (preview de DOM; não testa instalação):

```sh
python tests/ui_preview.py
```

O preview substitui somente a chave de armazenamento dependente da origem no documento de teste. O arquivo publicado permanece intacto. A captura é salva em `test-results/`.
