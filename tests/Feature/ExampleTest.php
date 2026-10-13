<?php

namespace Tests\Feature;

// use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_the_application_returns_a_successful_response(): void
    {
        $response = $this->get('/');

        $response->assertOk()
            ->assertSee('SEU LINK, SEM COMPLICAÇÃO')
            ->assertSee('Seus links encurtados vão aparecer aqui.')
            ->assertSee('css/app.css')
            ->assertSee('livewire/livewire.js');
    }
}
