# ====================================================================
# NOME DO ARQUIVO: atirador_hyperliquid.py
# TEMA: Agente 2 (Executor de Fogo Real na Hyperliquid)
# ====================================================================

import json
import time
import os
from datetime import datetime

# As armas da corretora
from dotenv import load_dotenv # >>> A CHAVE DO COFRE <<<
from eth_account import Account
from hyperliquid.utils import constants
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange

class AtiradorHyperliquid:
    def __init__(self):
        print("\n" + "="*60)
        print("🔫 [Agente Atirador] PRONTO PARA EXECUÇÃO TÁTICA (BLINDADO)")
        print("="*60)
        
        # O Atirador abre o cofre silenciosamente no sistema
        load_dotenv() 
        
        # Ele puxa a chave sem que ela jamais apareça no código
        chave_agente_bruta = os.environ.get("AGENT_PRIVATE_KEY", "")
        chave_mestra_bruta = os.environ.get("COMMANDER_PRIVATE_KEY", "")
        
        self.chave_agente = chave_agente_bruta.strip().strip('"').strip("'")
        chave_mestra = chave_mestra_bruta.strip().strip('"').strip("'")
        
        if self.chave_agente:
            if not self.chave_agente.startswith("0x"): self.chave_agente = "0x" + self.chave_agente
            if not chave_mestra.startswith("0x"): chave_mestra = "0x" + chave_mestra
            
            self.conta_agente = Account.from_key(self.chave_agente)
            endereco_mestre = Account.from_key(chave_mestra).address
            
            self.info = Info(constants.MAINNET_API_URL, skip_ws=True)
            self.exchange = Exchange(self.conta_agente, constants.MAINNET_API_URL, account_address=endereco_mestre)
            self.fogo_real = True
            print("    🔒 [OpSec] Chave criptografada carregada do cofre com sucesso.")
        else:
            print("    ⚠️ [Aviso] Cofre vazio. O Atirador vai apenas simular o tiro.")
            self.fogo_real = False
            
        self.arquivo_sinal = "sinal_combate.json"
        
        # DEFINIÇÃO DE ALVO DINÂMICA
        self.margem_usd = 12.0
        self.alavancagem = 10
        
        # Tenta pegar valor dinâmico se a chave existir
        if self.fogo_real:
             try:
                 estado = self.info.user_state(self.exchange.account_address)
                 saldo_real = float(estado.get("marginSummary", {}).get("accountValue", 0.0))
                 self.margem_usd = saldo_real * 0.99
             except Exception:
                 pass

    def _ler_sinal_na_mesa(self):
        """Abre a pasta e lê o papel que o Batedor deixou."""
        if not os.path.exists(self.arquivo_sinal):
            return None
        try:
            with open(self.arquivo_sinal, "r") as f:
                return json.load(f)
        except Exception:
            return None

    def _carimbar_sinal(self, sinal: dict, novo_status: str):
        """Reescreve o ficheiro JSON para os outros agentes saberem o que aconteceu."""
        sinal["status"] = novo_status
        with open(self.arquivo_sinal, "w") as f:
            json.dump(sinal, f, indent=4)
        print(f"    📝 [Mesa] Sinal {sinal['id_sinal']} carimbado como: {novo_status}")

    def _obter_pnl_real(self, ativo: str) -> float:
        """Puxa o PnL exato do servidor da Hyperliquid e converte em %."""
        if not self.fogo_real: return 0.0
        try:
            estado = self.info.user_state(self.exchange.account_address)
            for pos in estado.get("assetPositions", []):
                if pos.get("position", {}).get("coin") == ativo:
                    pnl_usd = float(pos.get("position", {}).get("unrealizedPnl", 0.0))
                    margem_usada = float(pos.get("position", {}).get("marginUsed", self.margem_usd))
                    # Retorna o lucro em percentagem exata (ROE)
                    if margem_usada > 0:
                        return (pnl_usd / margem_usada) * 100
            return 0.0
        except Exception: 
            return 0.0

    def registrar_trade_no_diario(self, ativo: str, tamanho: float, preco: float = 0.0, lucro_pnl: float = 0.0, motivo: str = ""):
        """Salva a operação num ficheiro CSV de 7 colunas originais para o Dashboard ler."""
        arquivo_csv = "historico_trades.csv" if self.fogo_real else "historico_simulacao.csv"
        existe = os.path.exists(arquivo_csv)
        
        try:
            with open(arquivo_csv, mode='a', encoding='utf-8') as f:
                if not existe:
                    f.write("Data_Hora,Ativo,Operacao,Tamanho_Moedas,Preco_USD,Tamanho_USDC,Lucro_Perda_USDC\n")
                    
                if tamanho > 0:
                    acao = "LONG 🟢"
                else:
                    acao = motivo if motivo else f"ENCERRADA 🛑"
                    
                data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                tam_usdc = abs(tamanho * preco)
                
                # Fetch balance again to append to log if needed, though usually the log has 7 cols.
                # The user asked: `acrescentar pnl e o saldo na carteira no arquivo`. 
                # Se for para acrescentar na coluna Ação/Operação:
                saldo_atual = 0.0
                if self.fogo_real:
                     try:
                         estado_user = self.info.user_state(self.exchange.account_address)
                         saldo_atual = float(estado_user.get("marginSummary", {}).get("accountValue", 0.0))
                     except Exception as e:
                         print(f"Erro ao obter saldo: {e}")
                
                acao = f"{acao} | Saldo: ${saldo_atual:.2f}"
                str_lucro = f"${lucro_pnl:.2f}" if lucro_pnl != 0.0 else "-"
                
                # Data_Hora,Ativo,Operacao,Tamanho_Moedas,Preco_USD,Tamanho_USDC,Lucro_Perda_USDC
                f.write(f"{data_atual},{ativo},{acao},{abs(tamanho):.4f},${preco:.2f},${tam_usdc:.2f},{str_lucro}\n")
            print(f"    📝 [Diário] Trade ({ativo}) registado no histórico.")
        except Exception as e:
            print(f"    ⚠️ Erro ao escrever no diário: {e}")

    def _executar_e_vigiar(self, ativo: str, preco_sugerido: float = None):
        """O tiro e a vigília com Time Stop de 10 minutos."""
        
        # Se for um re-entry (Time Stop), buscaremos o preço de mercado na hora para calcular o tamanho
        if not preco_sugerido:
             estado_mercado = self.info.meta_and_asset_ctxs()
             meta = estado_mercado[0]['universe']
             ctxs = estado_mercado[1]
             for i, ativo_meta in enumerate(meta):
                 if ativo_meta['name'] == ativo:
                     preco_sugerido = float(ctxs[i]['markPx'])
                     break
                     
        if not preco_sugerido:
             print(f"    ❌ Sem preço para calcular lote do {ativo}. Abortando disparo.")
             return False
             
        tamanho_total = self.margem_usd * self.alavancagem
        
        # Heurística para evitar o erro "Order has invalid size" da Hyperliquid
        if preco_sugerido > 1000:
            tamanho_moeda = round(tamanho_total / preco_sugerido, 4) # BTC, ETH
        elif preco_sugerido > 100:
            tamanho_moeda = round(tamanho_total / preco_sugerido, 2) # SOL, TAO
        elif preco_sugerido > 10:
            tamanho_moeda = round(tamanho_total / preco_sugerido, 1) # AVAX, LINK
        else:
            tamanho_moeda = round(tamanho_total / preco_sugerido, 0) # DOT, ADA (Inteiros)
        
        if tamanho_moeda <= 0: tamanho_moeda = 1.0
        
        # Obter o saldo atual da carteira
        saldo_atual_carteira = 0.0
        if self.fogo_real:
             try:
                 estado_user = self.info.user_state(self.exchange.account_address)
                 saldo_atual_carteira = float(estado_user.get("marginSummary", {}).get("accountValue", 0.0))
             except Exception:
                 pass
        
        print(f"\n    🚀 [Fogo Real] SALDO: ${saldo_atual_carteira:.2f} | Puxando o gatilho: COMPRAR {tamanho_moeda} {ativo}")
        
        if self.fogo_real:
            try:
                resultado = self.exchange.market_open(ativo, is_buy=True, sz=tamanho_moeda, px=None, slippage=0.01)
                if resultado["status"] == "ok":
                    statuses = resultado.get("response", {}).get("data", {}).get("statuses", [])
                    if statuses and isinstance(statuses[0], dict) and "error" in statuses[0]:
                        print(f"    ❌ [ERRO DA CORRETORA] A ordem falhou: {statuses[0]['error']}")
                        return False
                    print("    🎯 [IMPACTO CONFIRMADO] Operação executada com sucesso na rede!")
                    self.registrar_trade_no_diario(ativo, tamanho_moeda, preco_sugerido)
                else:
                    print(f"    ❌ Falha no disparo: {resultado}")
                    return False
            except Exception as e:
                print(f"    ❌ Falha no disparo: {e}")
                return False

        # VIGÍLIA COM TIME STOP E TRAILING STOP SÍNCRONO (45 MINUTOS)
        print("    👁️ [Vigília] Atirador aguardando alvo, limite de tempo ou Trailing Stop. (Pressione Ctrl+C para o Menu Manual)")
        tempo_inicio = time.time()
        limite_tempo = 45 * 60 # 45 Minutos
        alvo_lucro = 4.0 # Take profit inicial de 4%
        time_stop_triggered = False
        
        # --- PARÂMETROS DO TRAILING STOP (A Nova Arma) ---
        max_lucro_alcancado = 0.0
        gatilho_trailing = 2.0     # Só ativa o Trailing Stop quando chegar a +2% de lucro
        distancia_trailing = 1.0   # Se o lucro cair 1% em relação ao topo máximo, corta a posição
        
        try:
            while True:
                lucro_atual = self._obter_pnl_real(ativo)
                tempo_em_batalha = time.time() - tempo_inicio
                minutos = int(tempo_em_batalha / 60)
                
                # Atualiza o "High Water Mark" (O maior lucro que o robô já viu nesta operação)
                if lucro_atual > max_lucro_alcancado:
                    max_lucro_alcancado = lucro_atual
                
                limite_str = "∞" if limite_tempo == float('inf') else str(int(limite_tempo/60))
                print(f"       ⏱️ {ativo} | PnL: {lucro_atual:+.2f}% | Max: {max_lucro_alcancado:+.2f}% | Alvo: +{alvo_lucro:.1f}% | Relógio: {minutos}/{limite_str} min", end="\r")
                
                # -------------------------------------------------------------
                # AS 4 REGRAS DE SAÍDA (A ORDEM IMPORTA!)
                # -------------------------------------------------------------
                
                # 1. TRAILING STOP (A Defesa Ativa)
                if max_lucro_alcancado >= gatilho_trailing and lucro_atual <= (max_lucro_alcancado - distancia_trailing):
                    msg = f"🛡️ Trailing Stop ativado! O preço corrigiu. Saída com +{lucro_atual:.2f}% (Topo foi {max_lucro_alcancado:.2f}%)."
                    print(f"\n    {msg}")
                    motivo_saida = f"TRAILING STOP (PnL: +{lucro_atual:.2f}%) 🛑"
                    break
                    
                # 2. TAKE PROFIT FIXO (Garantia de Nocaute)
                elif lucro_atual >= alvo_lucro:
                    print(f"\n    ⚡ Take Profit (+{lucro_atual:.2f}%). Alvo abatido.")
                    motivo_saida = f"TAKE PROFIT (PnL: +{lucro_atual:.2f}%) 🛑"
                    break
                    
                # 3. STOP LOSS (Recuo Tático Inicial)
                elif lucro_atual <= -2.5:
                    print(f"\n    ⚠️ Stop Loss ({lucro_atual:.2f}%). Recuo tático.")
                    motivo_saida = f"STOP LOSS (PnL: {lucro_atual:.2f}%) 🛑"
                    break
                    
                # 4. FADIGA DE COMBATE (Time Stop de 45 minutos)
                elif tempo_em_batalha > limite_tempo:
                    print(f"\n    ⌛ Fadiga de Combate. 45 minutos excedidos.")
                    time_stop_triggered = True
                    motivo_saida = f"FADIGA COMBATE (PnL: {lucro_atual:+.2f}%) 🛑"
                    break
                    
                time.sleep(5)
                
        except KeyboardInterrupt:
            res = self._mostrar_menu_emergencia(ativo_atual=ativo)
            if res == "PROLONG":
                limite_tempo += 10 * 60
                print(f"    ⏳ [REFORÇO] Tempo estendido. Novo limite: {int(limite_tempo / 60)} Minutos totais.")
                return self._continuar_vigilia_prolongada(ativo, tamanho_moeda, tempo_inicio, limite_tempo, alvo_lucro)
            elif res == "EXTEND_PROFIT":
                alvo_lucro += 4.0
                print(f"    🚀 [AVANÇO] Take Profit ampliado! Novo Alvo: +{alvo_lucro:.1f}%.")
                return self._continuar_vigilia_prolongada(ativo, tamanho_moeda, tempo_inicio, limite_tempo, alvo_lucro)
            elif res == "INFINITE_TIME":
                limite_tempo = float('inf')
                print(f"    🌌 [VIGÍLIA INFINITA] Limite de tempo removido! {ativo} rodará até atingir Alvo ou Stop.")
                return self._continuar_vigilia_prolongada(ativo, tamanho_moeda, tempo_inicio, limite_tempo, alvo_lucro)
            elif res == "CONTINUAR":
                print(f"    🔙 [RETORNO] Retomando a vigília ativa de {ativo}...")
                return self._continuar_vigilia_prolongada(ativo, tamanho_moeda, tempo_inicio, limite_tempo, alvo_lucro)
            elif res:
                motivo_saida = f"INTERRUPÇÃO MANUAL (PnL: {lucro_atual:+.2f}%) 🛑"
                alvo_novo, preco_novo = res
                self.exchange.market_close(ativo) if self.fogo_real else None
                self.registrar_trade_no_diario(ativo, -tamanho_moeda, preco_sugerido, 0.0, motivo_saida)
                self._executar_e_vigiar(alvo_novo, preco_novo)
                return False
            return False

        if self.fogo_real:
            print(f"\n    🛑 ENCERRANDO POSIÇÃO: Vendendo a mercado...")
            self.exchange.market_close(ativo)
            
            # Puxa preço exato de saída para o log não ficar zerado
            preco_saida = preco_sugerido
            try:
                ctxs = self.info.meta_and_asset_ctxs()[1]
                for idx, a in enumerate(self.info.meta_and_asset_ctxs()[0]['universe']):
                    if a['name'] == ativo:
                        preco_saida = float(ctxs[idx]['markPx'])
            except: pass
            
            self.registrar_trade_no_diario(ativo, -tamanho_moeda, preco_saida, 0.0, motivo_saida)
            print("    ✅ Posição fechada e capital protegido.")
            
        return time_stop_triggered

    def _continuar_vigilia_prolongada(self, ativo: str, tamanho_moeda: float, tempo_inicio: float, limite_tempo: float, alvo_lucro: float = 4.0):
        """Retoma a vigília exatamente de onde parou após um PROLONG ou EXTEND_PROFIT."""
        time_stop_triggered = False
        
        # --- PARÂMETROS DO TRAILING STOP (A Nova Arma) ---
        max_lucro_alcancado = 0.0
        gatilho_trailing = 2.0     # Só ativa o Trailing Stop quando chegar a +2% de lucro
        distancia_trailing = 1.0   # Se o lucro cair 1% em relação ao topo máximo, corta a posição
        
        try:
            while True:
                lucro_atual = self._obter_pnl_real(ativo)
                tempo_em_batalha = time.time() - tempo_inicio
                minutos = int(tempo_em_batalha / 60)
                
                # Atualiza o "High Water Mark" (O maior lucro que o robô já viu nesta operação)
                if lucro_atual > max_lucro_alcancado:
                    max_lucro_alcancado = lucro_atual
                
                limite_str = "∞" if limite_tempo == float('inf') else str(int(limite_tempo/60))
                print(f"       ⏱️ {ativo} | PnL: {lucro_atual:+.2f}% | Max: {max_lucro_alcancado:+.2f}% | Alvo: +{alvo_lucro:.1f}% | Relógio: {minutos}/{limite_str} min", end="\r")
                
                # -------------------------------------------------------------
                # AS 4 REGRAS DE SAÍDA (A ORDEM IMPORTA!)
                # -------------------------------------------------------------
                
                # 1. TRAILING STOP (A Defesa Ativa)
                if max_lucro_alcancado >= gatilho_trailing and lucro_atual <= (max_lucro_alcancado - distancia_trailing):
                    msg = f"🛡️ Trailing Stop ativado! O preço corrigiu. Saída com +{lucro_atual:.2f}% (Topo foi {max_lucro_alcancado:.2f}%)."
                    print(f"\n    {msg}")
                    motivo_saida = f"TRAILING STOP (PnL: +{lucro_atual:.2f}%) 🛑"
                    break
                    
                # 2. TAKE PROFIT FIXO (Garantia de Nocaute)
                elif lucro_atual >= alvo_lucro:
                    print(f"\n    ⚡ Take Profit (+{lucro_atual:.2f}%). Alvo abatido.")
                    motivo_saida = f"TAKE PROFIT (PnL: +{lucro_atual:.2f}%) 🛑"
                    break
                    
                # 3. STOP LOSS (Recuo Tático Inicial)
                elif lucro_atual <= -2.5:
                    print(f"\n    ⚠️ Stop Loss ({lucro_atual:.2f}%). Recuo tático.")
                    motivo_saida = f"STOP LOSS (PnL: {lucro_atual:.2f}%) 🛑"
                    break
                    
                # 4. FADIGA DE COMBATE (Time Stop)
                elif tempo_em_batalha > limite_tempo:
                    print(f"\n    ⌛ Fadiga de Combate. Tempo prolongado excedido.")
                    time_stop_triggered = True
                    motivo_saida = f"FADIGA COMBATE (PnL: {lucro_atual:+.2f}%) 🛑"
                    break
                time.sleep(5)
        except KeyboardInterrupt:
            res = self._mostrar_menu_emergencia(ativo_atual=ativo)
            if res == "PROLONG":
                limite_tempo += 10 * 60
                print(f"    ⏳ [REFORÇO] Tempo estendido. Novo limite: {int(limite_tempo / 60)} Minutos totais.")
                return self._continuar_vigilia_prolongada(ativo, tamanho_moeda, tempo_inicio, limite_tempo, alvo_lucro)
            elif res == "EXTEND_PROFIT":
                alvo_lucro += 4.0
                print(f"    🚀 [AVANÇO] Take Profit ampliado! Novo Alvo: +{alvo_lucro:.1f}%.")
                return self._continuar_vigilia_prolongada(ativo, tamanho_moeda, tempo_inicio, limite_tempo, alvo_lucro)
            elif res == "INFINITE_TIME":
                limite_tempo = float('inf')
                print(f"    🌌 [VIGÍLIA INFINITA] Limite de tempo removido! {ativo} rodará até atingir Alvo ou Stop.")
                return self._continuar_vigilia_prolongada(ativo, tamanho_moeda, tempo_inicio, limite_tempo, alvo_lucro)
            elif res == "CONTINUAR":
                print(f"    🔙 [RETORNO] Retomando a vigília ativa de {ativo}...")
                return self._continuar_vigilia_prolongada(ativo, tamanho_moeda, tempo_inicio, limite_tempo, alvo_lucro)
            elif res:
                motivo_saida = f"INTERRUPÇÃO MANUAL (PnL: {lucro_atual:+.2f}%) 🛑"
                alvo_novo, preco_novo = res
                self.exchange.market_close(ativo) if self.fogo_real else None
                self.registrar_trade_no_diario(ativo, -tamanho_moeda, 0.0, 0.0, motivo_saida)
                self._executar_e_vigiar(alvo_novo, preco_novo)
                return False
            return False

        if self.fogo_real:
            print(f"\n    🛑 ENCERRANDO POSIÇÃO: Vendendo a mercado...")
            self.exchange.market_close(ativo)
            
            # Resgata preço online atual para o registo do log
            preco_saida = 0.0
            try:
                estado_mercado = self.info.meta_and_asset_ctxs()
                for idx, a in enumerate(estado_mercado[0]['universe']):
                    if a['name'] == ativo:
                        preco_saida = float(estado_mercado[1][idx]['markPx'])
            except: pass
            
            self.registrar_trade_no_diario(ativo, -tamanho_moeda, preco_saida, 0.0, motivo_saida)
            print("    ✅ Posição fechada e capital protegido.")
            
        return time_stop_triggered

    def _mostrar_menu_emergencia(self, ativo_atual=None):
        print("\n\n" + "="*50)
        print("🛑 [INTERRUPÇÃO TÁTICA] MENU DE COMANDO MANUAL")
        print("="*50)
        
        print("    📡 Buscando inteligência de mercado em tempo real...")
        estado_mercado = self.info.meta_and_asset_ctxs()
        meta = estado_mercado[0]['universe']
        ctxs = estado_mercado[1]
        
        dados_mercado = {}
        for i, ativo_meta in enumerate(meta):
            nome = ativo_meta['name']
            if nome in ["BTC", "ETH", "SOL", "TAO", "PAXG"]:
                ctx = ctxs[i]
                preco = float(ctx['markPx'])
                preco_ontem = float(ctx['prevDayPx'])
                variacao = ((preco - preco_ontem) / preco_ontem) * 100
                dados_mercado[nome] = {"preco": preco, "variacao": variacao}

        if ativo_atual:
            print(f"0. 🔙 VOLTAR À VIGÍLIA: Continuar monitorizando {ativo_atual} sem alterações")
            print(f"1. 🛑 Encerrar Posição Atual ({ativo_atual}) e voltar a Patrulhar")
            print(f"8. ⏳ PROLONGAR TEMPO: Adicionar +10 minutos na vigília de {ativo_atual}!")
            print(f"9. 📈 ALONGAR ALVO: Adicionar +4% no limite de Take Profit de {ativo_atual}!")
            print(f"10. 🧹 ENCERRAR AGORA E FICAR AQUI: Fechar {ativo_atual} e manter menu aberto")
            print(f"11. 🛌 VIGÍLIA INFINITA: Remover limite de tempo (Até bater no alvo/stop)")
        else:
            print("1. 🛑 Voltar a Patrulhar (Nenhuma posição ativa)")
            
        opcoes = ["BTC", "ETH", "SOL", "TAO", "PAXG"]
        for idx, moeda in enumerate(opcoes):
            if moeda in dados_mercado:
                var = dados_mercado[moeda]['variacao']
                label = "GOLD" if moeda == "PAXG" else moeda
                print(f"{idx+2}. 🚀 Operar {label} (Força: {var:+.2f}%)")
        print("7. 💀 DERRUBAR O AGENTE (Encerrar Script)")

        try:
            escolha = input("\n👉 Escolha uma opção (0-11): ").strip()
        except KeyboardInterrupt:
            print("\n    💀 Interrupção confirmada. Encerrando agente.")
            exit(0)
            
        if escolha == '0' and ativo_atual:
            return "CONTINUAR"
        if escolha == '8' and ativo_atual:
            return "PROLONG"
        if escolha == '9' and ativo_atual:
            return "EXTEND_PROFIT"
        if escolha == '10' and ativo_atual:
            if self.fogo_real:
                print(f"\n    🛑 ENCERRANDO POSIÇÃO ATUAL ({ativo_atual})...")
                self.exchange.market_close(ativo_atual)
                self.registrar_trade_no_diario(ativo_atual, -1.0, 0.0, 0.0, "FECHADA PELO COMANDO 🛑")
                print("    ✅ Posição fechada com lucro embolsado.")
            return self._mostrar_menu_emergencia(ativo_atual=None)
        if escolha == '11' and ativo_atual:
            return "INFINITE_TIME"
        
        if ativo_atual and self.fogo_real and escolha != '1':
            # Se for iniciar um novo trade ou matar, fecha a atual primeiro (se ainda não escolheu 1)
            print(f"\n    🛑 ENCERRANDO POSIÇÃO ATUAL ({ativo_atual}) ANTES DA NOVA ORDEM...")
            self.exchange.market_close(ativo_atual)
            print("    ✅ Posição fechada.")

        if escolha == '1':
            if ativo_atual and self.fogo_real:
                print(f"\n    🛑 ENCERRANDO POSIÇÃO ATUAL ({ativo_atual})...")
                self.exchange.market_close(ativo_atual)
                print("    ✅ Posição fechada.")
            return False
            
        if escolha == '7':
            if ativo_atual and self.fogo_real:
                print(f"\n    🛑 ENCERRANDO POSIÇÃO ATUAL ({ativo_atual}) ANTES DE DERRUBAR O AGENTE...")
                self.exchange.market_close(ativo_atual)
                self.registrar_trade_no_diario(ativo_atual, -1.0, 0.0, 0.0, "DERRUBADA MANUAL 💀")
                print("    ✅ Posição fechada.")
            print("    💀 Agente desativado permanentemente.")
            exit(0)
            
        alvo_novo = None
        if escolha == '2': alvo_novo = "BTC"
        elif escolha == '3': alvo_novo = "ETH"
        elif escolha == '4': alvo_novo = "SOL"
        elif escolha == '5': alvo_novo = "TAO"
        elif escolha == '6': alvo_novo = "PAXG"
        
        if alvo_novo and alvo_novo in dados_mercado:
            return (alvo_novo, dados_mercado[alvo_novo]["preco"])
            
        print("    ⚠️ Opção inválida. Retornando à patrulha.")
        return False

    def iniciar_patrulha(self):
        """O loop infinito de leitura da mesa de operações."""
        print("    👁️ Inicializando sistemas. Abrindo Painel de Comando...")
        
        # MOSTRAR MENU DE COMANDO APENAS UMA VEZ NO INICIO
        try:
            res_inicial = self._mostrar_menu_emergencia(ativo_atual=None)
            if res_inicial:
                alvo_novo, preco_novo = res_inicial
                while True:
                    reabrir = self._executar_e_vigiar(alvo_novo, preco_novo)
                    if not reabrir:
                        break
                    preco_novo = None # Na próxima reabertura, força a buscar o preço em tempo real
        except KeyboardInterrupt:
            print("\n    💀 Interrupção durante a inicialização. Encerrando agente.")
            exit(0)
            
        print("    👁️ Patrulha automática em andamento. (Pressione Ctrl+C a qualquer momento para o Menu Manual)")
        while True:
            try:
                sinal = self._ler_sinal_na_mesa()
                
                if sinal and sinal["status"] == "AUTORIZADO":
                    print(f"\n🔔 [ALERTA] Novo pacote de inteligência na mesa!")
                    print(f"    🎯 Alvo Selecionado: {sinal['ativo']} | Força Relativa: {sinal['forca_relativa']}%")
                    print(f"    🛡️ [Comando] Executando o líder da cesta, independentemente da força absoluta.")
                    
                    self._carimbar_sinal(sinal, "EM_COMBATE")
                    preco_loop = sinal["preco_sugerido"]
                    while True:
                        reabrir = self._executar_e_vigiar(sinal["ativo"], preco_loop)
                        if not reabrir:
                            break
                        preco_loop = None # Forçar busca de preço real ao reabrir
                    self._carimbar_sinal(sinal, "FINALIZADO")
                
                time.sleep(10)
            except KeyboardInterrupt:
                res = self._mostrar_menu_emergencia(ativo_atual=None)
                if res:
                    alvo_novo, preco_novo = res
                    while True:
                        reabrir = self._executar_e_vigiar(alvo_novo, preco_novo)
                        if not reabrir:
                            break
                        preco_novo = None # Atualiza no próximo looping

if __name__ == "__main__":
    atirador = AtiradorHyperliquid()
    atirador.iniciar_patrulha()
