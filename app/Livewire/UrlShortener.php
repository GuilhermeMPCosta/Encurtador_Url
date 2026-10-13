<?php

namespace App\Livewire;

use Illuminate\Contracts\View\View;
use Livewire\Component;

class UrlShortener extends Component
{
    public string $url = '';

    public ?string $notice = null;

    public ?string $shortUrl = null;

    public function shorten(): void
    {
        $this->validate([
            'url' => ['required', 'string', 'max:2048'],
        ]);

        $this->notice = 'O encurtamento será habilitado quando o backend for integrado.';
    }

    public function clearUrl(): void
    {
        $this->reset('url', 'notice', 'shortUrl');
        $this->resetValidation();
    }

    public function render(): View
    {
        return view('livewire.url-shortener')
            ->layout('layouts.app');
    }
}
