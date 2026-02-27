# ====================================================================
# NOME DO ARQUIVO: hyperliquid_conexao.py
# TEMA: Login Seguro (Agent Keys) na Corretora Hyperliquid
# ====================================================================

from eth_account import Account
import time

class ConexaoHyperliquid:
    def __init__(self, chave_privada_comandante: str):
        print("\n" + "="*60)
        print("🔐 [OpSec] INICIANDO PROTOCOLO DE CONEXÃO HYPERLIQUID")
        print("="*60)
        
        # 1. A CHAVE MESTRA (Sua carteira que guarda os fundos)
        self.carteira_mestra = Account.from_key(chave_privada_comandante)
        print(f"    🏦 Cofre Principal Identificado: {self.carteira_mestra.address}")
        
        # 2. A CHAVE DO AGENTE (Criada na hora, só serve para trading)
        # O OpenClaw gera uma chave temporária e descartável para operar
        self.carteira_agente = Account.create()
        print(f"    🤖 Crachá de Agente Gerado: {self.carteira_agente.address}")

    def autorizar_agente(self):
        """
        O Comandante assina uma permissão dizendo:
        'A corretora pode aceitar ordens deste Agente em meu nome.'
        """
        print("\n    ✍️ Solicitando autorização on-chain para o Agente operar...")
        time.sleep(1.5)
        
        # Na Hyperliquid real, usaríamos a SDK deles aqui:
        # setup = eth_web3.setup(self.carteira_mestra)
        # agente_aprovado = setup.approve_agent(self.carteira_agente)
        
        print("    ✅ [SUCESSO] O Agente agora tem permissão exclusiva para TRADING.")
        print("    🛡️ [SEGURANÇA] O Agente NÃO tem permissão para realizar SAQUES.")

    def executar_ordem_segura(self, ativo: str, acao: str):
        """O Agente usa o seu próprio crachá para enviar a ordem."""
        print(f"\n    ⚡ [Hyperliquid DEX] O Agente está enviando uma ordem de {acao} para {ativo}...")
        time.sleep(1)
        
        # A ordem é assinada APENAS com a carteira do agente, a chave mestra fica segura offline
        # tx = hyperliquid.exchange.order(ativo, is_buy=True, ..., wallet=self.carteira_agente)
        
        print("    🧾 Ordem executada com sucesso e sem taxas de Gas (Zero-Gas)!")

# ==========================================
# TESTE DE SEGURANÇA
# ==========================================
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    # Carrega as variáveis do arquivo .env
    load_dotenv()
    
    # Carregando a chave secreta de uma variável de ambiente (NUNCA hardcode isso)
    chave_simulada = os.environ.get("COMMANDER_PRIVATE_KEY")
    
    if not chave_simulada:
        print("❌ ERRO: Variável de ambiente 'COMMANDER_PRIVATE_KEY' não encontrada.")
        print("Certifique-se de que ela está corretamente salva no arquivo .env!")
        exit(1)
        
    # Limpeza de aspas ou espaços acidentais esquecidos no arquivo .env
    chave_simulada = chave_simulada.strip().strip('"').strip("'")
    if not chave_simulada.startswith("0x"):
        chave_simulada = "0x" + chave_simulada
        
    try:
        conexao = ConexaoHyperliquid(chave_simulada)
        conexao.autorizar_agente()
        conexao.executar_ordem_segura("BTC", "SHORT")
    except Exception as e:
        print("\n❌ [ERRO] A chave privada no seu arquivo .env contém caracteres inválidos.")
        print("Uma chave hexadecimal Ethereum só pode conter números de 0-9 e letras de A-F.")
        print("Verifique se você colou a chave completa (64 caracteres) corretamente.")
        print(f"Erro original: {e}")
        exit(1)
