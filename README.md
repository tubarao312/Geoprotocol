# Geoprotocol
O GeoProtocol é uma base de dados descentralizada que se alimenta a si própria e permite às cidades e aos seus habitantes contribuir e desfrutar de uma vasta rede de informação baseada em técnicas de Machine Learning e Blockchain.

Bubble.io Link: https://github.com/tubarao312/Geoprotocol

### Como Usar
Para fazer fetch da informação da blockchain, basta importar *scripts/interact.ipynb* e utilizar o seguinte código:

```python
# Easy as cake!
bank = get_contract() # Communicate with Blockchain
df = build_report_df(bank, 3) # Fetch reports
df.to_csv('out.zip', index=False) # Print Excel

# Done :)
```

Também é necessário criar um ficheiro JSON na pasta *scripts* com o nome *walletInfo*. Este deverá ter três fields:
```json
{
    "main": {
        "private": "A TUA CHAVE PRIVADA",
        "public": "O TEU ENDEREÇO PÚBLICO"
    },
    "infuraURL": "O URL DA TUA NODE DE ACESSO À BLOCKCHAIN (POLYGON)"
}
```

Para criares uma chave privada, basta usares o Metamask e será tudo muito explícitio. Para criares uma node de acesso à blockchain, vai a https://infura.io/ e também será muito simples.

**Boa Sorte!**

### Programas e Linguagens:
- Solidity (Brownie)
- Python (Web3.py, ML Libraries)
- Jupyter
