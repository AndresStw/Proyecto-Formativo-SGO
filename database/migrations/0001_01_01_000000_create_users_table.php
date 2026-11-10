<?php

// database/migrations/..._create_usuarios_table.php

// Este archivo define la estructura básica de un usuario en el sistema.
// Utiliza una estrategia de Tabla Única donde el campo 'rol' diferencia
// si es cliente, mesero, cocinero, cajero o administrador.

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('Usuario', function (Blueprint $table) {
            
           //TABLA USUARIO
            $table->id('idUsuario'); 

            // 1. INFORMACION BASICA
            $table->string('primerNombre', 45);
            $table->string('segundoNombre', 45)->nullable();//P.Vacio
            $table->string('primerApellido', 45);
            $table->string('segundoApellido', 45)->nullable();//P.Vacio 

            // 2. CONTACTO
            $table->string('telefono', 15)->unique(); 
            $table->string('email', 150)->unique();
            $table->string('direccion', 255)->nullable(); // Para el admi
            $table->string('password_hash', 255);
            $table->rememberToken();

            // 3. PARAMETROS DE LA CUENTA Y ROL
            $table->timestamps(); //Avisa el tiempo de inicio de session y cierre control
            // Roles permitidos: 'cliente', 'admin', 'mesero', 'cocinero', 'cajero'
            $table->string('rol', 20)->default('cliente');//se asignan manualmente por admi
            $table->boolean('estado')->default(true); // true = activo, false = bloqueado

        }); 
    }

    public function down(): void
    {
        Schema::dropIfExists('Usuario');//eliminar si existe 
    }
};