import ccee_extractor

payload = {
    "url" : "https://www.ccee.org.br/dados-e-analises/dados-mercado-mensal",
    "profile"     : "default",
    "search_file" : "InfoMercado_Dados_Individuais"
}

ccee_extractor.lambda_handler(event=payload)


# {
#     "url" : "https://www.ccee.org.br/dados-e-analises/dados-mercado-mensal",
#     "profile"     : null,
#     "search_file" : "InfoMercado_Dados_Individuais"
# }