# ====================================================================
# NOME DO ARQUIVO: tiro_real_hyperliquid.py
# TEMA: Teste de Fogo (Operação Real na Hyperliquid)
# ====================================================================

from eth_account import Account
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
import time
import os
from dotenv import load_dotenv

class OpenClawAtirador:
    def __init__(self, private_key: str, usar_testnet: bool = False):
        print("\n" + "="*60)
        print("💥 [OpenClaw] SISTEMA DE ARMAMENTO ONLINE")
        print("="*60)
        
        # 1. Carrega a carteira do Agente
        self.conta = Account.from_key(private_key)
        print(f"    🤖 Identidade do Agente: {self.conta.address}")
        
        # 2. Define o campo de batalha (Mainnet = Dinheiro Real | Testnet = Dinheiro Falso)
        self.base_url = constants.TESTNET_API_URL if usar_testnet else constants.MAINNET_API_URL
        ambiente = "TESTNET (Simulação)" if usar_testnet else "MAINNET (Dinheiro Real ⚠️)"
        print(f"    🌍 Campo de Batalha: {ambiente}")
        
        # 3. Conecta aos servidores da Hyperliquid
        self.info = Info(self.base_url, skip_ws=True)
        self.exchange = Exchange(self.conta, self.base_url)
        print("    🟢 Conexão com os servidores da DEX estabelecida.")

    def verificar_preco(self, ativo: str):
        """Puxa o preço exato do ativo no livro de ofertas da corretora."""
        try:
            # Puxa os dados de todos os mercados e filtra o nosso alvo
            estado_mercado = self.info.meta_and_asset_ctxs()
            for mercado in estado_mercado[1]:
                if mercado['coin'] == ativo:
                    preco = float(mercado['markPx'])
                    print(f"    📡 Radar: Preço atual do {ativo} na Hyperliquid = ${preco:.2f}")
                    return preco
            print(f"    ❌ Ativo {ativo} não encontrado no radar.")
        except Exception as e:
            print(f"    ❌ Erro ao ler o radar: {e}")
        return None

    def atirar(self, ativo: str, is_buy: bool, tamanho_lote: float):
        """
        Puxa o gatilho!
        is_buy = True (LONG/COMPRA) | False (SHORT/VENDA)
        """
        direcao = "LONG 📈" if is_buy else "SHORT 📉"
        print(f"\n    ⚡ PREPARANDO DISPARO: Ordem de {direcao} no {ativo} (Tamanho: {tamanho_lote})")
        
        print("    ⏳ Assinando transação on-chain...")
        time.sleep(1)
        
        try:
            # Executa a ordem a mercado
            # O último parâmetro (0.01) é o slippage (margem de erro de preço de 1%)
            resultado = self.exchange.market_open(ativo, is_buy, tamanho_lote, None, 0.01)
            
            if resultado["status"] == "ok":
                print("    🎯 [IMPACTO CONFIRMADO] A ordem foi executada com sucesso na blockchain!")
                print(f"    🧾 Recibo da Corretora: {resultado['response']['data']['statuses'][0]}")
            else:
                print(f"    ❌ [FALHA NO DISPARO] O tiro falhou. Motivo: {resultado}")
                
        except Exception as e:
            print(f"    🚨 [ERRO CRÍTICO]: {e}")

# ==========================================
# TESTE TÁTICO (O GATILHO)
# ==========================================
if __name__ == "__main__":
    load_dotenv()
    
    # OPSEC: Puxando do arquivo .env
    chave_simulada = os.environ.get("COMMANDER_PRIVATE_KEY")
    
    if not chave_simulada:
        print("❌ ERRO: Variável de ambiente 'COMMANDER_PRIVATE_KEY' não encontrada no arquivo .env!")
        exit(1)
        
    chave_simulada = chave_simulada.strip().strip('"').strip("'")
    if not chave_simulada.startswith("0x"):
        chave_simulada = "0x" + chave_simulada
    
    CHAVE_DO_AGENTE = chave_simulada
    
    # Se quiser testar com dinheiro de mentira primeiro, mude para True.
    # Se for para valer, deixe False.
    MODO_TESTNET = True # Sugerindo TRUE por padrão para testar sem sustos
    
    try:
        atirador = OpenClawAtirador(private_key=CHAVE_DO_AGENTE, usar_testnet=MODO_TESTNET)
        
        # Vamos usar um ativo barato para o teste (ex: ADA, DOGE, ou uma fração mínima de ETH)
        ALVO = "ADA" 
        TAMANHO = 10.0 # Ex: Comprar 10 moedas de ADA (apenas alguns dólares de teste)
        
        # 1. Verifica o preço
        atirador.verificar_preco(ALVO)
        
        # 2. Tira a trava de segurança?
        resposta = input("\n⚠️ Comandante, você autoriza o disparo na DEX? (s/n): ")
        if resposta.lower() == 's':
            # is_buy=True significa que estamos a abrir um LONG (apostando na alta)
            atirador.atirar(ativo=ALVO, is_buy=True, tamanho_lote=TAMANHO)
        else:
            print("🛡️ Disparo abortado. Armas travadas.")
            
    except Exception as e:
        print(f"\n❌ [ERRO DE ARRANQUE] Erro de inicialização. Detalhes: {e}")
