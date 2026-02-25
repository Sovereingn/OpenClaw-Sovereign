# 🦞 OpenClaw Sovereign

**Agente Financeiro de IA 100% Autônomo, Descentralizado e Soberano.**
Construído sobre o ecossistema [Bittensor ($TAO)](https://bittensor.com/).

> "A internet não será mais desenhada para humanos. Ela será desenhada para Máquinas. O OpenClaw não usa interfaces Web2; ele opera puramente na camada de protocolos de rede."

---

## ⚠️ AVISO LEGAL
Este software é estritamente educacional e de pesquisa. O OpenClaw interage com contratos inteligentes, carteiras criptográficas reais e mercados de alta volatilidade. **Não coloque fundos que você não pode perder.** O uso deste código é de sua inteira responsabilidade.

---

## 🧠 A Arquitetura do Sistema

A maioria dos "Agentes de IA" hoje são meras interfaces (wrappers) dependentes de APIs centralizadas (OpenAI, Google) e chaves privadas expostas em arquivos `.env`. O OpenClaw resolve o "Problema da Soberania" orquestrando diretamente as Sub-redes (Subnets) do Bittensor e utilizando Carteiras Headless (x402).

### ⚙️ Módulos Principais

* **O Cérebro Roteador (SN4 & SN120):** O agente não depende de um único LLM. Ele roteia o pensamento para a sub-rede mais eficiente, garantindo que o melhor modelo matemático seja pago para resolver o problema.
* **O Escudo de Hardware (SN64 - Chutes):** Dados sensíveis são processados dentro de um TEE (Trusted Execution Environment). Privacidade absoluta; nem o dono do servidor consegue ler os dados do agente.
* **A Carteira Headless (Protocolo x402):** Fim do armazenamento de chaves em texto plano. O agente traz sua própria identidade financeira (Bring Your Own Wallet) para pagar outras máquinas (M2M) de forma fluida.
* **O Banco Autônomo (SN35 - Cartha):** O OpenClaw não é apenas um trader; ele atua como Provedor de Liquidez (Federated Miner), travando USDC em contratos na rede Base para gerar dividendos passivos.
* **Auditoria de Código Integrada (SN100 - Platform):** Antes de interagir com qualquer Smart Contract, o módulo de risco usa engenharia autônoma para auditar o código em containers Docker, evitando backdoors e exploits.

---

## 📂 Estrutura do Projeto

```text
📦 OpenClaw-Sovereign
 ┣ 📂 src
 ┃ ┣ 📂 finance
 ┃ ┃ ┣ 📜 macro_trader.py    # Execução de trades e fornecimento de liquidez (SN35)
 ┃ ┃ ┣ 📜 risk_manager.py    # Avaliação de volatilidade e auditoria de contratos (SN100)
 ┃ ┃ ┗ 📜 x402_wallet.py     # Gestão da assinatura de pagamentos Headless
 ┃ ┗ 📂 intelligence
 ┃   ┗ 📜 brain_router.py    # (Em desenvolvimento) Orquestração cognitiva (SN4/SN64/SN120)
 ┣ 📜 main.py                # Sistema Nervoso Central (Orquestrador)
 ┗ 📜 README.md              # Documentação oficial
```

---

## 🚀 Como Executar (Ambiente de Testes)

1. Clone o repositório:
   ```bash
   git clone https://github.com/Sovereingn/OpenClaw-Sovereign.git
   cd OpenClaw-Sovereign
   ```

2. Configure suas variáveis de ambiente de teste (nunca use fundos reais no ambiente de dev):
   ```bash
   export X402_SESSION_TOKEN="seu_token_de_teste_aqui"
   ```

3. Inicie o Sistema Nervoso Central do Agente:
   ```bash
   python main.py
   ```
