# ====================================================================
# NOME DO ARQUIVO: estrategia_hyperliquid.py
# TEMA: O Agente que Escolhe o Próprio Alvo e Atira
# ====================================================================

from eth_account import Account
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
import time
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

class OpenClawEstrategista:
    def __init__(self, private_key: str, account_address: str = None):
        print("\n" + "="*60)
        print("🧠 [OpenClaw] MOTOR DE INTELIGÊNCIA TÁTICA ATIVADO")
        print("="*60)
        
        self.conta = Account.from_key(private_key)
        self.base_url = constants.MAINNET_API_URL # MODO REAL: Dinheiro real na operação
        print(f"    🤖 Identidade do Agente: {self.conta.address}")
        if account_address:
            print(f"    🏦 Carteira Comandante (Alvo): {account_address}")
        
        self.info = Info(self.base_url, skip_ws=True)
        # O account_address informa à corretora de quem são os fundos que o Agente da API está manipulando
        self.exchange = Exchange(self.conta, self.base_url, account_address=account_address)
        
        # A sua lista VIP (Sem ADA!)
        self.alvos_autorizados = ["BTC", "ETH", "TAO", "SOL", "SUI"]
        
    def escolher_melhor_alvo(self):
        """Lê a Hyperliquid e escolhe a moeda com maior força nas últimas 24h."""
        print("\n    📡 Escaneando o mercado em busca do alvo com maior Força Relativa (Momentum)...")
        time.sleep(1)
        
        estado_mercado = self.info.meta_and_asset_ctxs()
        meta = estado_mercado[0]['universe']
        ctxs = estado_mercado[1]
        
        tabela_forca = {}
        
        for i, ativo_meta in enumerate(meta):
            nome = ativo_meta['name']
            if nome in self.alvos_autorizados:
                ctx = ctxs[i]
                preco_atual = float(ctx['markPx'])
                preco_ontem = float(ctx['prevDayPx'])
                
                # A Matemática do Momentum: (Preço Atual - Preço Ontem) / Preço Ontem
                variacao_24h = ((preco_atual - preco_ontem) / preco_ontem) * 100
                tabela_forca[nome] = {'preco': preco_atual, 'variacao': variacao_24h}
                
                print(f"    📊 {nome}: Preço ${preco_atual:.2f} | Variação 24h: {variacao_24h:+.2f}%")
        
        # A IA escolhe a moeda com o MAIOR número de variação
        melhor_moeda = max(tabela_forca, key=lambda k: tabela_forca[k]['variacao'])
        preco_alvo = tabela_forca[melhor_moeda]['preco']
        
        print(f"\n    🏆 [DECISÃO DA IA] O alvo escolhido para LONG é: {melhor_moeda}")
        return melhor_moeda, preco_alvo

    def calcular_lote(self, preco_ativo: float, tamanho_em_dolar: float):
        """
        Não podemos comprar 10 BTC para testar, custaria $600.000!
        O robô divide os dólares de teste pelo preço da moeda para saber a fração exata.
        """
        tamanho_moeda = tamanho_em_dolar / preco_ativo
        # Arredondando para 3 casas decimais para a Hyperliquid aceitar a ordem
        return round(tamanho_moeda, 3) 

    def registrar_trade_no_diario(self, ativo: str, tamanho: float, preco: float):
        """A Caixa Preta: Salva o tiro real para o Painel Streamlit poder ler."""
        arquivo = "historico_trades.csv"
        # Verifica se o arquivo já existe para colocar o cabeçalho
        precisa_cabecalho = not os.path.exists(arquivo)
        
        with open(arquivo, mode="a", newline="") as f:
            escritor = csv.writer(f)
            if precisa_cabecalho:
                escritor.writerow(["Data_Hora", "Ativo", "Operacao", "Tamanho_Moedas", "Preco_USD"])
            
            # Registra o momento exato do disparo
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            escritor.writerow([agora, ativo, "LONG 📈", tamanho, preco])

    def atirar(self, ativo: str, tamanho_moeda: float, preco_alvo: float):
        """Abre uma posição de LONG (Compra) no alvo escolhido."""
        print(f"\n    ⚡ PREPARANDO DISPARO: LONG em {ativo} (Tamanho do Lote: {tamanho_moeda} moedas)")
        print("    ⏳ Assinando transação on-chain (Zero Gas)...")
        time.sleep(1)
        
        try:
            # is_buy=True (LONG), slippage=1% (0.01)
            # Obs: Alguns ativos na testnet não deixam operar com float fracionado, mas testaremos.
            resultado = self.exchange.market_open(ativo, is_buy=True, sz=tamanho_moeda, px=None, slippage=0.01)
            
            if resultado["status"] == "ok":
                print("\n    🎯 [IMPACTO CONFIRMADO] Operação executada com sucesso!")
                print("    🧾 Vá olhar a sua conta na Hyperliquid agora!")
                self.registrar_trade_no_diario(ativo, tamanho_moeda, preco_alvo)
            else:
                print(f"\n    ❌ [FALHA NO DISPARO] A corretora rejeitou. Motivo: {resultado}")
                
        except Exception as e:
            print(f"    🚨 [ERRO CRÍTICO]: {e}")


# ==========================================
# TESTE DE EXECUÇÃO
# ==========================================
if __name__ == "__main__":
    load_dotenv()
    
    # OPSEC: Buscando a chave da API do Agente e a Chave Mestra
    chave_agente_bruta = os.environ.get("AGENT_PRIVATE_KEY")
    chave_mestra_bruta = os.environ.get("COMMANDER_PRIVATE_KEY")
    
    if not chave_agente_bruta or not chave_mestra_bruta:
        print("❌ ERRO: Faltam chaves no arquivo .env (Verifique COMMANDER_PRIVATE_KEY e AGENT_PRIVATE_KEY)!")
        exit(1)
        
    # Limpeza de Segurança
    chave_agente = chave_agente_bruta.strip().strip('"').strip("'")
    if not chave_agente.startswith("0x"): chave_agente = "0x" + chave_agente

    chave_mestra = chave_mestra_bruta.strip().strip('"').strip("'")
    if not chave_mestra.startswith("0x"): chave_mestra = "0x" + chave_mestra
    
    # Derivamos o endereço público da carteira principal para ser o 'Cofre' do Agente
    endereco_mestre = Account.from_key(chave_mestra).address
    
    # Quanto de margem em dólares vamos usar para este teste real?
    TAMANHO_DA_POSICAO_USD = 15.0 
    
    try:
        agente = OpenClawEstrategista(private_key=chave_agente, account_address=endereco_mestre)
        
        # 1. A IA lê as 5 moedas e escolhe a mais forte
        alvo, preco_alvo = agente.escolher_melhor_alvo()
        
        # 2. O Agente calcula quantas moedas ele consegue comprar com $15 dólares
        tamanho_do_lote = agente.calcular_lote(preco_alvo, TAMANHO_DA_POSICAO_USD)
        
        # 3. Trava de Segurança Humana
        resposta = input(f"\n⚠️ Comandante, você autoriza injetar ${TAMANHO_DA_POSICAO_USD} num LONG de {alvo}? (s/n): ")
        
        if resposta.lower() == 's':
            agente.atirar(ativo=alvo, tamanho_moeda=tamanho_do_lote, preco_alvo=preco_alvo)
        else:
            print("🛡️ Operação abortada. Motores em standby.")
            
    except Exception as e:
        print("\n❌ [ERRO CRIPTOGRÁFICO] A chave do Agente ou a Chave Mestra no arquivo .env contém um caractere inválido.")
        print("Verifique se você substituiu 'cole_sua_nova_chave_de_agente_aqui' pela chave hexadecimal real (que contém apenas números de 0-9 e letras de A-F).")
        print(f"Erro original do Python: {e}")
        exit(1)
