<?php

// database/migrations/..._create_usuarios_table.php

// Este archivo define la estructura de la tabla 'Usuario', 
// incluyendo los campos comunes y los campos específicos para cada rol 
// (cliente, mesero, cocinero, cajero, admin) usando la estrategia de Tabla Única.

//Partiendo 
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {

    public function up(): void
    {
        Schema::create('Usuario', function (Blueprint $table) {
           
            $table->id('idUsuario'); 

            // 1. INFORMACION BASICA (Todos)
            $table->string('primerNombre', 45);
            $table->string('segundoNombre', 45)->nullable(); 
            $table->string('primerApellido', 45);
            $table->string('segundoApellido', 45)->nullable(); 

            // 2. CONTACTO (Todos)
            $table->string('telefono', 15)->unique(); 
            $table->string('email', 150)->unique();
            $table->string('ciudad',150);//Ciduad
            $table->string('direccion', 255)->unique(); // Nullable por si el Admin no da dirección
            $table->string('password_hash', 255);
            $table->rememberToken(); //Requerido por Laravel para Auth

            // 3. PARAMETROS DE LA CUENTA
            $table->timestamps(); 
            // Roles permitidos: 'cliente', 'admin', 'mesero', 'cocinero', 'cajero'
            $table->string('rol', 20)->default('cliente'); 
            $table->boolean('estado')->default(true); 

            // 4. CAMPOS ESPECIFICOS POR ROL (Nullables)
            
            // - Cliente (EP-01, EP-03)
            $table->string('nivelCliente', 45)->nullable()->default('Estandar');
            $table->string('estadoMembresia', 45)->nullable()->default('Activa');

            // - Mesero (EP-04)
            $table->string('zona_asignada', 45)->nullable(); 
            
            // - Cocinero (EP-06)
            $table->string('especialidad', 45)->nullable();
            $table->string('turno', 45)->nullable();
            
            // - Cajero (EP-06)
            $table->string('caja_asignada', 45)->nullable();
            
            // - Administrador (EP-05)
            $table->string('nivel_acceso', 45)->nullable();

        }); 
    }

    public function down(): void
    {
        Schema::dropIfExists('Usuario');
    }
};