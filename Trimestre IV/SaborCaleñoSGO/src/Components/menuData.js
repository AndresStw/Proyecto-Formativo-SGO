// src/Components/menuData.js

// Importa todas las imagenes
import arepaPanela from "../assets/Img/Desayunos/Arepapanela-modified.png";
import changua from "../assets/Img/Desayunos/Changua-modified.png";
import chocolateCampesino from "../assets/Img/Desayunos/chocolate-campesino.png";
import pandebonos from "../assets/Img/Desayunos/pandebonos-modified.png";
import pasabocasCalenos from "../assets/Img/Desayunos/pasabocas-calenos-modified.png";

import ajiaco from "../assets/Img/caldos/ajiaco.png";
import changuaCaldos from "../assets/Img/caldos/Changua.jpg";
import mondongo from "../assets/Img/caldos/mondongo-modified.png";
import sancochoGallina from "../assets/Img/caldos/sancocho-gallina-modified.png";
import sancochoPescado from "../assets/Img/caldos/sancocho-pescado-modified.png";

import champusValluno from "../assets/Img/Bebida/champus-valluno-modified.png";
import lulada from "../assets/Img/Bebida/lulada-individual-modified.png";

import arrozAtollado from "../assets/Img/platos/arroz-atollado-modified.png";
import carneBistec from "../assets/Img/platos/carne-bistec-modified.png";
import cazuelaMariscos from "../assets/Img/platos/cazuela-mariscos-modified.png";
import chuletaAlmuerzo from "../assets/Img/platos/chuleta-almuerzo-modified.png";
import chuletaValluna from "../assets/Img/platos/chuleta-valluna-modified.png";
import costillasGuayaba from "../assets/Img/platos/costillas-guayaba-modified.png";
import mojarraFrita from "../assets/Img/platos/Mojarra-frita-modified.png";
import pastaCasera from "../assets/Img/platos/pasta-casera.png";
import sobrebarrigaHogao from "../assets/Img/platos/sobrebarriga-hogao-modified.png";

// Logo
import logo from "../assets/Img/logos/logo.png";

export const menuData = {
  // Lista completa de productos
  productos: [
    // ========== DESAYUNOS ==========
    {
      id: 1,
      nombre: "Arepa con Panela",
      descripcion: "Arepa recién hecha acompañada de panela con queso y mantequilla.",
      precio: 8000,
      categoria: "desayunos",
      imagen: arepaPanela,
      rating: 4.7,
      tiempo: "15min",
      calorias: "280"
    },
    {
      id: 2,
      nombre: "Changua",
      descripcion: "Sopa tradicional de leche, huevo y cebolla, perfecta para empezar el día.",
      precio: 10000,
      categoria: "desayunos",
      imagen: changua,
      rating: 4.5,
      tiempo: "20min",
      calorias: "320"
    },
    {
      id: 3,
      nombre: "Chocolate Campesino",
      descripcion: "Chocolate caliente con queso y pan, energía para toda la mañana.",
      precio: 9000,
      categoria: "desayunos",
      imagen: chocolateCampesino,
      rating: 4.8,
      tiempo: "10min",
      calorias: "350"
    },
    {
      id: 4,
      nombre: "Pandebonos",
      descripcion: "Deliciosos pandebonos recién horneados, esponjosos y llenos de sabor.",
      precio: 6000,
      categoria: "desayunos",
      imagen: pandebonos,
      rating: 4.6,
      tiempo: "10min",
      calorias: "200"
    },
    {
      id: 5,
      nombre: "Pasabocas Caleños",
      descripcion: "Selección de pasabocas típicos para acompañar el desayuno.",
      precio: 12000,
      categoria: "desayunos",
      imagen: pasabocasCalenos,
      rating: 4.4,
      tiempo: "15min",
      calorias: "400"
    },

    // ========== CALDOS ==========
    {
      id: 6,
      nombre: "Ajiaco",
      descripcion: "Sopa tradicional con pollo, papas, mazorca y guasca, acompañada de arroz y aguacate.",
      precio: 18000,
      categoria: "caldos",
      imagen: ajiaco,
      rating: 4.9,
      tiempo: "35min",
      calorias: "450"
    },
    {
      id: 7,
      nombre: "Changua (Caldos)",
      descripcion: "Changua caliente con huevo, cebolla y cilantro, acompañada de pan.",
      precio: 12000,
      categoria: "caldos",
      imagen: changuaCaldos,
      rating: 4.3,
      tiempo: "20min",
      calorias: "300"
    },
    {
      id: 8,
      nombre: "Mondongo",
      descripcion: "Sopa de mondongo con verduras, acompañada de arroz y aguacate.",
      precio: 22000,
      categoria: "caldos",
      imagen: mondongo,
      rating: 4.7,
      tiempo: "40min",
      calorias: "500"
    },
    {
      id: 9,
      nombre: "Sancocho de Gallina",
      descripcion: "Sancocho tradicional con gallina criolla, plátano, yuca y mazorca.",
      precio: 25000,
      categoria: "caldos",
      imagen: sancochoGallina,
      rating: 4.8,
      tiempo: "45min",
      calorias: "520"
    },
    {
      id: 10,
      nombre: "Sancocho de Pescado",
      descripcion: "Sancocho de pescado fresco con verduras y arroz, el favorito de la costa.",
      precio: 23000,
      categoria: "caldos",
      imagen: sancochoPescado,
      rating: 4.6,
      tiempo: "35min",
      calorias: "400"
    },

    // ========== BEBIDAS ==========
    {
      id: 11,
      nombre: "Champús Caleño",
      descripcion: "Bebida tradicional a base de maíz, lulo, piña y hojas de naranjo.",
      precio: 8000,
      categoria: "bebidas",
      imagen: champusValluno,
      rating: 4.5,
      tiempo: "5min",
      calorias: "180"
    },
    {
      id: 12,
      nombre: "Lulada",
      descripcion: "Refrescante bebida de lulo con hielo y limón, la favorita de los caleños.",
      precio: 7000,
      categoria: "bebidas",
      imagen: lulada,
      rating: 4.4,
      tiempo: "5min",
      calorias: "150"
    },

    // ========== PLATOS FUERTES ==========
    {
      id: 13,
      nombre: "Arroz Atollado",
      descripcion: "Arroz con carnes, verduras y especias, el sabor tradicional del Valle.",
      precio: 28000,
      categoria: "platos",
      imagen: arrozAtollado,
      rating: 4.9,
      tiempo: "35min",
      calorias: "600"
    },
    {
      id: 14,
      nombre: "Carne Bistec",
      descripcion: "Bistec de res a la plancha, acompañado de papas, ensalada y arroz.",
      precio: 26000,
      categoria: "platos",
      imagen: carneBistec,
      rating: 4.6,
      tiempo: "30min",
      calorias: "550"
    },
    {
      id: 15,
      nombre: "Cazuela de Mariscos",
      descripcion: "Exquisita cazuela con mariscos frescos, verduras y un toque especial.",
      precio: 35000,
      categoria: "platos",
      imagen: cazuelaMariscos,
      rating: 4.8,
      tiempo: "40min",
      calorias: "580"
    },
    {
      id: 16,
      nombre: "Chuleta Almuerzo",
      descripcion: "Chuleta de cerdo empanizada, papas fritas y ensalada fresca.",
      precio: 24000,
      categoria: "platos",
      imagen: chuletaAlmuerzo,
      rating: 4.5,
      tiempo: "25min",
      calorias: "520"
    },
    {
      id: 17,
      nombre: "Chuleta Valluna",
      descripcion: "Filete de cerdo apanado crujiente, papas fritas, ensalada y arroz.",
      precio: 22000,
      categoria: "platos",
      imagen: chuletaValluna,
      rating: 4.9,
      tiempo: "25min",
      calorias: "500"
    },
    {
      id: 18,
      nombre: "Costillas con Guayaba",
      descripcion: "Costillas de cerdo bañadas en salsa de guayaba, acompañadas de arroz y papas.",
      precio: 32000,
      categoria: "platos",
      imagen: costillasGuayaba,
      rating: 4.7,
      tiempo: "35min",
      calorias: "620"
    },
    {
      id: 19,
      nombre: "Mojarra Frita",
      descripcion: "Mojarra frita acompañada de arroz, ensalada y patacones.",
      precio: 27000,
      categoria: "platos",
      imagen: mojarraFrita,
      rating: 4.4,
      tiempo: "30min",
      calorias: "480"
    },
    {
      id: 20,
      nombre: "Pasta Casera",
      descripcion: "Pasta hecha en casa con salsa de la casa y queso parmesano.",
      precio: 20000,
      categoria: "platos",
      imagen: pastaCasera,
      rating: 4.3,
      tiempo: "25min",
      calorias: "450"
    },
    {
      id: 21,
      nombre: "Sobrebarriga con Hogao",
      descripcion: "Sobrebarriga cocinada lentamente con hogao criollo, arroz y papas.",
      precio: 30000,
      categoria: "platos",
      imagen: sobrebarrigaHogao,
      rating: 4.8,
      tiempo: "40min",
      calorias: "560"
    }
  ],

  // Exportar logo separado
  logo
};

// Función para obtener productos por categoría
export const getProductosByCategoria = (categoria) => {
  if (categoria === 'todos') return menuData.productos;
  return menuData.productos.filter(p => p.categoria === categoria);
};

// Función para obtener un producto por ID
export const getProductoById = (id) => {
  return menuData.productos.find(p => p.id === id);
};

// Categorías disponibles
export const categorias = [
  { id: 'todos', label: 'Todos' },
  { id: 'desayunos', label: 'Desayunos' },
  { id: 'caldos', label: 'Caldos' },
  { id: 'bebidas', label: 'Bebidas' },
  { id: 'platos', label: 'Platos Fuertes' }
];

export default menuData;