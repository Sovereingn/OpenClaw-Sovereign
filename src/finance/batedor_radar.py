import requests
import time
import json
import uuid
import os
from datetime import datetime
import pandas as pd

class AgenteBatedorQuant:
    def __init__(self):
        print("\n" + "="*60)
        print("🕵️♂️ [Agente Batedor] RADAR QUANTITATIVO ATIVADO (RSI + EMA NATIVO)")
        print("="*60)
        
        # Alvos na sintaxe da Binance (Adicionamos o USDT e o Ouro)
        self.radar_alvos = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "TAOUSDT", "INJUSDT", "PAXGUSDT"]
        self.arquivo_sinal = "sinal_combate.json"
        
        # Parâmetros Táticos
        self.tempo_grafico = "15m" # Gráfico de 15 minutos (Filtra o ruído da guerra)
        self.limite_rsi = 30       # Compra quando o RSI cai abaixo de 30 (Sobrevendido)

    def _calcular_rsi(self, series: pd.Series, periodos: int = 14) -> pd.Series:
        delta = series.diff()
        ganho = (delta.where(delta > 0, 0)).fillna(0)
        perda = (-delta.where(delta < 0, 0)).fillna(0)
        
        # Usando a média móvel exponencial suavizada (Wilder's Smoothing) típica do RSI
        media_ganho = ganho.ewm(alpha=1/periodos, min_periods=periodos, adjust=False).mean()
        media_perda = perda.ewm(alpha=1/periodos, min_periods=periodos, adjust=False).mean()
        
        rs = media_ganho / media_perda
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _calcular_ema(self, series: pd.Series, periodos: int = 200) -> pd.Series:
        return series.ewm(span=periodos, adjust=False).mean()

    def _obter_dados_binance(self, simbolo: str) -> pd.DataFrame:
        """Puxa as últimas 250 velas (candlesticks) da Binance em tempo real."""
        url = f"https://api.binance.com/api/v3/klines?symbol={simbolo}&interval={self.tempo_grafico}&limit=250"
        try:
            resposta = requests.get(url, timeout=5).json()
            # Organiza os dados numa tabela Pandas
            df = pd.DataFrame(resposta, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume', 
                'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'
            ])
            # Converte os preços para números decimais
            df['close'] = pd.to_numeric(df['close'])
            return df
        except Exception as e:
            return None

    def _analisar_indicadores(self) -> dict:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🔍 Escaneando gráficos de 15 Minutos...")
        
        for simbolo in self.radar_alvos:
            df = self._obter_dados_binance(simbolo)
            
            if df is not None and not df.empty:
                # ---------------------------------------------------
                # 🧮 A MAGIA QUANTITATIVA ACONTECE AQUI (VIA PANDAS)
                # ---------------------------------------------------
                # 1. Calcula o RSI de 14 períodos
                df['RSI'] = self._calcular_rsi(df['close'], periodos=14)
                
                # 2. Calcula a Média Móvel Exponencial (EMA) de 200 períodos
                df['EMA_200'] = self._calcular_ema(df['close'], periodos=200)
                
                # Pega a leitura exata do momento atual (a última linha da tabela)
                linha_atual = df.iloc[-1]
                preco_atual = linha_atual['close']
                rsi_atual = linha_atual['RSI']
                ema_200 = linha_atual['EMA_200']
                
                ativo_limpo = simbolo.replace("USDT", "") # Limpa para TAO, BTC, etc
                
                print(f"    📊 {ativo_limpo} | Preço: ${preco_atual:.2f} | RSI: {rsi_atual:.2f} | EMA200: ${ema_200:.2f}")
                
                # ---------------------------------------------------
                # 🎯 GATILHO DE COMBATE (A Regra de Ouro)
                # ---------------------------------------------------
                # Regra: Preço acima da Média de 200 (Tendência de Alta) E RSI menor que 30 (Promoção)
                if pd.notna(rsi_atual) and pd.notna(ema_200):
                    if preco_atual > ema_200 and rsi_atual < self.limite_rsi:
                        print(f"    🟢 [GATILHO DETECTADO] {ativo_limpo} está sobrevendido em forte tendência de alta!")
                        
                        return {
                            "ativo": ativo_limpo,
                            "forca_percentual": round(rsi_atual, 2), # Usamos o RSI como "força" agora
                            "preco_alvo": preco_atual
                        }
        
        print("    ⚪ Nenhum alvo perfeito encontrado nesta patrulha.")
        return None

    def _verificar_mesa_limpa(self) -> bool:
        """Verifica se o papel na mesa (sinal_combate.json) já foi resolvido."""
        if not os.path.exists(self.arquivo_sinal):
            return True
        try:
            with open(self.arquivo_sinal, "r") as f:
                sinal = json.load(f)
                status = sinal.get("status", "")
                if status in ["PENDENTE", "AUTORIZADO", "EM_ANDAMENTO"]:
                    return False
        except Exception:
            pass
        return True

    def gerar_sinal(self):
        while True:
            if not self._verificar_mesa_limpa():
                print("⏳ [Mesa Ocupada] Batedor em compasso de espera. Trade em andamento ou pendente...")
                time.sleep(30)
                continue
                
            analise = self._analisar_indicadores()
            
            if analise:
                sinal = {
                    "id_sinal": "SIG-" + str(uuid.uuid4())[:8].upper(),
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "ativo": analise["ativo"],
                    "direcao": "LONG",
                    "preco_sugerido": analise["preco_alvo"],
                    "forca_relativa": analise["forca_percentual"], # O valor do RSI vai aqui
                    "status": "PENDENTE" 
                }
                
                with open(self.arquivo_sinal, "w") as f:
                    json.dump(sinal, f, indent=4)
                    
                print(f"🎯 [MESA] Relatório gerado para {sinal['ativo']}! RSI em {sinal['forca_relativa']}.")
                
                # Como achou um alvo, dorme um pouco mais para não floodar
                time.sleep(120) 
            else:
                # Se não achou nada, descansa só 1 minuto e procura de novo
                print("⏳ Aguardando 1 minuto para refazer a leitura dos gráficos...\n")
                time.sleep(60)

if __name__ == "__main__":
    batedor = AgenteBatedorQuant()
    batedor.gerar_sinal()
