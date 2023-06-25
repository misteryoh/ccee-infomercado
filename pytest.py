import ccee_extractor

events = {
    "url" : "https://dadosabertos.camara.leg.br/api/v2/proposicoes",
    "params" : {
        "siglaTipo" : "PL",
        "ano" : "2023",
        "itens" : "100",
        "ordem" : "ASC",
        "ordenarPor" : "id"
    }
}

ccee_extractor.lambda_handler(events=events, context=None)


