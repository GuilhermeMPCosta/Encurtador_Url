<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Encurte seus links e compartilhe com mais praticidade." />
    <meta name="theme-color" content="#f6f7fb" />
    <title>encurta. — Links mais curtos, ideias mais longe</title>
    <link rel="stylesheet" href="{{ asset('css/app.css') }}" />
    @livewireStyles
  </head>
  <body>
    {{ $slot }}
    @livewireScripts
  </body>
</html>
