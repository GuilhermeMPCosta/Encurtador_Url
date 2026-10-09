# Encurtador de URL

Interface web estática para encurtar links usando a API Flask existente.

## Front-end

Abra `frontend/index.html` diretamente ou sirva a pasta `frontend` com qualquer servidor estático. Não há dependências de build.

Por padrão, a interface envia as requisições para `http://localhost:5000`. Para usar outra URL de API, informe-a na query string, por exemplo:

```text
http://localhost:5500/?api=https://api.exemplo.com
```

Se o front-end e a API estiverem em origens diferentes, a API precisa permitir a origem do front-end via CORS. O front-end usa `POST /encurtar` com o corpo JSON `{ "url": "https://exemplo.com" }`.

O histórico dos últimos cinco links fica salvo no armazenamento local do navegador.
