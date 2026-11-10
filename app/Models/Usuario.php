<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;


class Usuario extends Authenticatable
{
    
use HasFactory, Notifiable, HasApiTokens; 

    protected $table = 'Usuario';
    protected $primaryKey = 'idUsuario';


    // Campos de migracion
//Relleno automatico

    protected $fillable = [ 

        'primerNombre',
        'segundoNombre',
        'primerApellido',
        'segundoApellido',
        'telefono',
        'email',
        'direccion',
        'password_hash',
        'rol',
        'estado'
    ];

//Ocultar 
    protected $hidden = [
        'password_hash',
        'remember_token',
    ];

//Relaciones

public function pedidos()
    {
        return $this->hasMany(Pedido::class, 'Usuario_id', 'idUsuario');
    }
}