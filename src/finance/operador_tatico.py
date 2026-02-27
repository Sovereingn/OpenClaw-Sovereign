# ====================================================================
# NOME DO ARQUIVO: operador_tatico.py
# TEMA: Dupla Proteção (Stop Nativo + Vigília do Agente) na Hyperliquid
# ====================================================================

import time
import random # Apenas para simular a variação de preço no nosso teste

class OperadorEstrategico:
    def __init__(self, ativo: str, tamanho_posicao_usd: float):
        self.ativo = ativo
        self.tamanho = tamanho_posicao_usd
        self.posicao_aberta = False
        
        print("\n" + "="*60)
        print(f"🎯 [Operador Tático] INICIANDO PROTOCOLO DE DUPLA EXTRAÇÃO PARA {self.ativo}")
        print("="*60)

    # ---------------------------------------------------------
    # TÁTICA 1: PROTEÇÃO NATIVA (A Armadura da Corretora)
    # ---------------------------------------------------------
    def executar_entrada_com_escudo(self, preco_atual: float):
        print(f"\n🚀 [Fogo Real] Abrindo posição LONG de ${self.tamanho} a ${preco_atual:.2f}...")
        time.sleep(1)
        
        # 1. O Agente envia a Ordem Principal (Comprar agora)
        # hyperliquid.exchange.market_open(...)
        self.posicao_aberta = True
        
        # 2. O Agente calcula os limites de vida ou morte
        # Exemplo: Take Profit em +10%, Stop Loss em -5%
        preco_take_profit = preco_atual * 1.10
        preco_stop_loss = preco_atual * 0.95
        
        print(f"    🛡️ [TÁTICA 1] Enviando ordens de proteção nativas para a Hyperliquid:")
        print(f"       🟢 Take Profit (Alvo): Vender se bater ${preco_take_profit:.2f}")
        print(f"       🔴 Stop Loss (Escudo): Vender se cair para ${preco_stop_loss:.2f}")
        
        # 3. O Agente envia as ordens condicionais para a corretora
        # hyperliquid.exchange.sl_tp(...)
        time.sleep(1)
        print("    ✅ Proteção nativa ancorada no servidor da corretora. Mesmo se o Agente morrer, o dinheiro está seguro.")

    # ---------------------------------------------------------
    # TÁTICA 2: VIGÍLIA ATIVA (O Cérebro do Agente)
    # ---------------------------------------------------------
    def iniciar_vigilia(self, preco_entrada: float):
        print("\n👁️ [TÁTICA 2] Agente entrando em Modo de Vigília Ativa...")
        
        ciclo = 1
        preco_simulado = preco_entrada
        
        while self.posicao_aberta:
            # O Agente lê o mercado a cada ciclo (Aqui simulamos a variação)
            variacao = random.uniform(-0.03, 0.04) # Varia entre -3% e +4%
            preco_simulado = preco_simulado * (1 + variacao)
            
            lucro_percentual = ((preco_simulado - preco_entrada) / preco_entrada) * 100
            
            print(f"    ⏱️ [Ciclo {ciclo}] Preço Atual: ${preco_simulado:.2f} | PnL: {lucro_percentual:.2f}%")
            
            # --- A INTELIGÊNCIA DE SAÍDA DO AGENTE ---
            
            # Condição A: O Agente percebe um lucro bom e decide sair ANTES do Take Profit da corretora
            if lucro_percentual >= 5.0:
                print(f"\n    ⚡ [DECISÃO IA] Lucro de +{lucro_percentual:.2f}% atingido. O Agente decidiu embolsar agora!")
                self._fechar_posicao_agora("TAKE PROFIT ANTECIPADO")
                break
                
            # Condição B: O Agente percebe que o mercado está esquisito e aborta ANTES do Stop Loss ser atingido
            elif lucro_percentual <= -3.0:
                print(f"\n    ⚠️ [DECISÃO IA] Sangramento de {lucro_percentual:.2f}%. O Agente abortou a missão para salvar capital!")
                self._fechar_posicao_agora("STOP LOSS ANTECIPADO")
                break
                
            ciclo += 1
            time.sleep(2) # O Agente espera 2 segundos antes de checar de novo

    def _fechar_posicao_agora(self, motivo: str):
        """O Agente executa uma ordem a mercado para fechar tudo instantaneamente."""
        print(f"    💸 [Hyperliquid] Enviando ordem de CLOSE POSITION (Vender Tudo)...")
        time.sleep(1)
        # hyperliquid.exchange.market_close(...)
        self.posicao_aberta = False
        print(f"    🎯 Operação encerrada com sucesso. Motivo: {motivo}.")


# ==========================================
# CAMPO DE TREINAMENTO (Teste Local)
# ==========================================
if __name__ == "__main__":
    # O Comandante quer operar $15 no Ethereum (que está custando $3000)
    operador = OperadorEstrategico(ativo="ETH", tamanho_posicao_usd=15.0)
    
    preco_mercado = 3000.00
    
    # Passo 1: O Agente entra atirando e já coloca o escudo da corretora
    operador.executar_entrada_com_escudo(preco_atual=preco_mercado)
    
    # Passo 2: O Agente não desliga. Ele fica acordado monitorando a operação.
    operador.iniciar_vigilia(preco_entrada=preco_mercado)
