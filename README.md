# Encurta.

Interface frontend do encurtador de URLs construída com Laravel e Livewire. A integração e a lógica de encurtamento ainda não estão implementadas.

## Requisitos

- PHP 8.2 ou superior
- Composer

## Como executar

```powershell
composer install
Copy-Item .env.example .env
php artisan key:generate
php artisan serve
```

Acesse `http://127.0.0.1:8000`. O formulário, a área de resultado e o histórico são apenas a interface; o botão de encurtar informa que o backend ainda precisa ser integrado.
