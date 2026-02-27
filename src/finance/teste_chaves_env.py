import os
import binascii
from dotenv import load_dotenv

def testar_chave(nome_variavel):
    chave_bruta = os.environ.get(nome_variavel)
    if not chave_bruta:
        print(f"⚠️ {nome_variavel}: Não encontrada no arquivo .env")
        return

    chave = chave_bruta.strip().strip('"').strip("'")
    if not chave.startswith("0x"):
         chave = "0x" + chave
    
    hex_puro = chave[2:]
    
    # 1. Checa o tamanho primeiro
    if len(hex_puro) != 64:
         status_hexa = "Sim" if all(c.lower() in '0123456789abcdef' for c in hex_puro) else "Não"
         print(f"❌ {nome_variavel}: Tamanho incorreto! Você colou {len(hex_puro)} caracteres. Uma chave privada autêntica tem exatamente 64 caracteres. (Todos são Hexadecimais? {status_hexa})")
         return
    
    # 2. Checa blocos quebrando
    try:
        binascii.unhexlify(hex_puro)
        print(f"✅ {nome_variavel}: Chave perfeita e conectada à criptografia Ethereum.")
    except binascii.Error:
        # Encontra o caractere corrompido
        caracteres_invalidos = [c for c in hex_puro if c.lower() not in '0123456789abcdef']
        caracteres_unicos = list(set(caracteres_invalidos))
        print(f"❌ {nome_variavel}: A chave contém caracteres estranhos (letras de G a Z, espaços ou símbolos): {caracteres_unicos}")

if __name__ == "__main__":
    load_dotenv()
    print("========================================")
    print("🕵️  DIAGNÓSTICO OPSEC DE CHAVES CRYPTO")
    print("========================================\n")
    testar_chave("COMMANDER_PRIVATE_KEY")
    testar_chave("AGENT_PRIVATE_KEY")
    print("\n========================================")
