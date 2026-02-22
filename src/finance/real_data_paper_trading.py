import time
import requests
from datetime import datetime

class RealDataPaperTrading:
    """
    Simulador de Combate Avançado.
    O agente lê os preços REAIS do mercado via API antes de simular o trade.
    """
    def __init__(self):
        self.log_file = "historico_de_trades_reais.txt"
        self.caixa_virtual = 10000.00 # $10.000 dólares imaginários
        print("\n🌐 [Oráculo] Conectando aos sensores de mercado global...")
        print(f"💰 [Caixa Virtual]: ${self.caixa_virtual:.2f}\n")

        # Dicionário para traduzir o símbolo para o ID que a API entende
        self.crypto_ids = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "SOL": "solana"
        }

    def _get_real_price(self, asset: str) -> float:
        """
        Consulta a API pública da CoinGecko para pegar o preço em tempo real (em USD).
        """
        api_id = self.crypto_ids.get(asset)
        if not api_id:
            print(f"    ⚠️ Erro: Ativo {asset} não mapeado no radar.")
            return 0.0

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={api_id}&vs_currencies=usd"
        
        try:
            # O Agente faz a requisição HTTP (O "olhar" para o mercado)
            resposta = requests.get(url, timeout=5)
            dados = resposta.json()
            
            # Extrai o preço do JSON recebido
            preco = dados[api_id]["usd"]
            return float(preco)
            
        except Exception as e:
            print(f"    ❌ [Alerta] Falha de conexão com o Oráculo: {e}")
            return 0.0

    def execute_real_data_trade(self, asset: str, amount_usd: float):
        """O Agente lê o mercado real, decide e anota no diário."""
        print(f"🤖 [OpenClaw] Analisando o mercado REAL para {asset}...")
        
        preco_atual = self._get_real_price(asset)
        
        if preco_atual == 0.0:
            print("    🛑 Risco detectado: Oráculo cego. Abortando trade para proteger capital.")
            return

        print(f"    📡 [Oráculo] O preço exato do {asset} agora é: ${preco_atual}")
        time.sleep(1) # Agente calculando
        
        if amount_usd <= self.caixa_virtual:
            self.caixa_virtual -= amount_usd
            quantidade_comprada = amount_usd / preco_atual
            
            mensagem = (f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                        f"COMPRA (MERCADO REAL) | Ativo: {asset} | "
                        f"Cotação: ${preco_atual} | Investido: ${amount_usd} | "
                        f"Qtd: {quantidade_comprada:.6f} | Caixa: ${self.caixa_virtual:.2f}\n")
            
            print(f"    ✅ Trade Simulado com Sucesso! Comprado {quantidade_comprada:.6f} {asset}.")
            
            # Escreve no arquivo de log 
            with open(self.log_file, "a") as file:
                file.write(mensagem)
                
            print(f"    📝 Registro salvo no cofre de memória: {self.log_file}\n")
        else:
            print("    ❌ Saldo virtual insuficiente.\n")

# ==========================================
# EXECUTANDO A OPERAÇÃO COM DADOS REAIS
# ==========================================
if __name__ == "__main__":
    simulador = RealDataPaperTrading()
    
    # O agente vai consultar o preço real agora mesmo e anotar!
    simulador.execute_real_data_trade("BTC", 2500.00)
    time.sleep(3) # Pausa para não sobrecarregar a API gratuita
    simulador.execute_real_data_trade("ETH", 1000.00)
    time.sleep(3)
    simulador.execute_real_data_trade("SOL", 500.00)
    
    print(f"🏁 Fim do ciclo. O arquivo '{simulador.log_file}' foi atualizado com cotações reais.")
