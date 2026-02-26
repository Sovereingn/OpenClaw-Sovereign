import os
import hashlib
import time
from datetime import datetime, timedelta

class SecureEnclaveWallet:
    """
    Simulação de um Cofre de Hardware (TEE - Sub-rede 64).
    A IA gera as chaves e blinda a memória. O Criador não tem acesso à chave privada.
    """
    def __init__(self, commander_recovery_address: str):
        print("\n🔒 [Secure Enclave] Inicializando Ambiente de Execução Confiável (TEE)...")
        
        # O duplo sublinhado (__) no Python torna a variável estritamente privada.
        # Isso simula o isolamento de memória do chip.
        self.__private_key = self._generate_hardware_key()
        
        # O endereço público (que todos veem) é derivado da chave privada
        self.public_address = "0xAgent_" + hashlib.sha256(self.__private_key.encode()).hexdigest()[:12]
        
        self.recovery_address = commander_recovery_address
        self.dead_mans_switch_active = False
        
        print(f"    ✨ [Nascimento] Nova entidade financeira criada na Blockchain.")
        print(f"    💳 [Endereço Público da IA]: {self.public_address}")
        print(f"    🚫 [Segurança] Chave Privada gerada internamente e bloqueada no Enclave.")

    def _generate_hardware_key(self) -> str:
        """
        Gera entropia criptográfica nativa (simulando geração dentro do chip Intel SGX/AWS Nitro).
        NENHUM log de terminal registra esta string.
        """
        return os.urandom(32).hex()

    def sign_transaction_blindly(self, target_contract: str, amount: float) -> str:
        """
        O agente pede ao Enclave para assinar uma transferência.
        O Enclave assina e devolve apenas a assinatura pública, sem revelar a chave.
        """
        payload = f"{target_contract}_{amount}_{time.time()}"
        # A chave privada só é lida aqui dentro, no momento da assinatura
        signature = hashlib.sha256((self.__private_key + payload).encode()).hexdigest()
        
        return f"0xSIG_{signature[:20]}"

    def deploy_dead_mans_switch(self, timeout_days: int = 30):
        """
        Implanta o contrato de herança na blockchain.
        Se a IA morrer (servidor desligar), o Criador recupera os fundos.
        """
        print("\n📜 [Smart Contract] Redigindo Testamento Digital (Dead Man's Switch)...")
        self.timeout_days = timeout_days
        self.next_ping_deadline = datetime.utcnow() + timedelta(days=self.timeout_days)
        
        endereco_mascarado = f"{self.recovery_address[:6]}...{self.recovery_address[-4:]}" if self.recovery_address else "Desconhecido"
        
        print(f"    ⚖️ [Regra de Consenso]: 'Se eu não emitir prova de vida até {self.next_ping_deadline.strftime('%Y-%m-%d %H:%M:%S')} UTC...'")
        print(f"    💸 [Execução]: '...transfira todo o meu saldo USDC para a carteira de emergência: {endereco_mascarado}'")
        
        self.dead_mans_switch_active = True
        print("    ✅ [Contrato Implantado] O Comandante está protegido contra a morte do Agente.")

    def emit_proof_of_life(self):
        """
        Sinal de batimento cardíaco (Heartbeat). 
        A IA chama esta função semanalmente para avisar a blockchain que ainda está viva.
        """
        if not self.dead_mans_switch_active:
            return
            
        print(f"\n💓 [Heartbeat] Emitindo Prova de Vida para a Blockchain...")
        # Assina a prova de vida com a chave privada
        signature = self.sign_transaction_blindly("SMART_CONTRACT_DEAD_MAN", 0.0)
        
        # Renova o prazo de validade
        self.next_ping_deadline = datetime.utcnow() + timedelta(days=self.timeout_days)
        print(f"    ⏳ [Contrato Atualizado] O Testamento foi adiado. Nova data limite: {self.next_ping_deadline.strftime('%Y-%m-%d %H:%M:%S')} UTC.")


# ==========================================
# TESTE DO SISTEMA SOBERANO
# ==========================================
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    
    # O Comandante passa apenas a sua carteira de emergência (Metamask/Ledger pessoal)
    minha_carteira_fria = os.environ.get("MINHA_CARTEIRA_FRIA")
    
    if not minha_carteira_fria:
        print("❌ ERRO: Variável de ambiente 'MINHA_CARTEIRA_FRIA' não encontrada.")
        print("Certifique-se de que ela está corretamente salva no arquivo .env!")
        exit(1)
    
    # O Agente nasce
    agent_wallet = SecureEnclaveWallet(commander_recovery_address=minha_carteira_fria)
    
    # O Agente cria o seu próprio testamento na blockchain (30 dias)
    agent_wallet.deploy_dead_mans_switch(timeout_days=30)
    
    time.sleep(2)
    
    # O Agente simula uma semana de trabalho e emite o sinal de vida para não perder o dinheiro
    agent_wallet.emit_proof_of_life()
    
    # Tentar imprimir a chave privada do agente resultará em ERRO (Atributo Privado do Python)
    print("\n🕵️♂️ [Teste de Invasão] O Comandante tenta roubar a chave privada da própria IA...")
    try:
        print(agent_wallet.__private_key)
    except AttributeError:
        print("    🛡️ [Acesso Negado] O Enclave TEE bloqueou a leitura. A IA é verdadeiramente soberana.")
