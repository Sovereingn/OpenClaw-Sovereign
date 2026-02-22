from src.finance.x402_wallet import HeadlessWalletX402

class MacroTrader:
    """
    Módulo Financeiro Global do OpenClaw Sovereign.
    Agora protegido pelo protocolo de carteiras portáteis x402.
    """
    def __init__(self):
        self.endpoint = "https://api.0xmarkets.tao/v1/trade"
        # O Trader agora "veste" a carteira headless
        self.wallet = HeadlessWalletX402()

    def execute_trade(self, asset: str, side: str, amount_usd: float, leverage: int = 1):
        target_symbol = asset.upper()
        print(f"\n🌍 [MacroTrader] Iniciando Execução Financeira: {side} {target_symbol} | ${amount_usd}")

        try:
            # 1. O agente prepara o pagamento (M2M Payment)
            auth_headers = self.wallet.sign_payment_request(self.endpoint, amount_usd)
            
            # 2. O agente envia a ordem para a rede com o pagamento embutido no Header HTTP
            payload = {"pair": target_symbol, "side": side, "amount": amount_usd}
            
            # Simulação: requests.post(self.endpoint, json=payload, headers=auth_headers)
            print(f"    💎 [Sucesso] Ordem enviada via Subnet 35. Pagamento x402 liquidado em milissegundos.")
            return f"Trade executado de forma soberana."

        except Exception as e:
            print(f"❌ [Erro Fatal] Falha na execução da ordem: {e}")
            return None

    def provide_liquidity(self, amount_usdc: float, pool_name: str, principal_hotkey: str) -> bool:
        """
        Simula o provimento de liquidez para uma pool DeFi (ex: ETH/USD) operada na rede TAO.
        """
        print(f"\n💧 [MacroTrader] Solicitando provisão de liquidez na pool {pool_name}...")
        print(f"    Montante: ${amount_usdc} USDC | Hotkey Delegada: {principal_hotkey}")

        try:
            # Assinatura do x402
            auth_headers = self.wallet.sign_payment_request(self.endpoint, amount_usdc)
            
            # Simulação de post na rede
            print(f"    🏦 [Liquidez Ativa] Depósito de ${amount_usdc} confirmado no smart contract.")
            return True
        except Exception as e:
            print(f"    ❌ [Liquidez Falhou] Erro no depósito: {e}")
            return False

# ==========================================
# TESTE DO SISTEMA (Para você rodar localmente)
# ==========================================
if __name__ == "__main__":
    # Para testar, vamos definir o token na variável de ambiente localmente
    import os
    os.environ["X402_SESSION_TOKEN"] = "teste_sessao_local_123"
    
    trader = MacroTrader()
    
    # Simulação 1: O OpenClaw detectou queda no Bitcoin e decide fazer "Hedge" (Proteção) em Ouro
    print("\n--- Cenário 1: Proteção de Capital (Hedge) ---")
    resultado_ouro = trader.execute_trade(asset="GOLD", side="BUY", amount_usd=5000)
    
    # Simulação 2: O OpenClaw detecta inflação no Dólar e aposta no Euro
    print("\n--- Cenário 2: Arbitragem de Moedas Fiduciárias ---")
    resultado_euro = trader.execute_trade(asset="EURO", side="BUY", amount_usd=1500, leverage=2)
