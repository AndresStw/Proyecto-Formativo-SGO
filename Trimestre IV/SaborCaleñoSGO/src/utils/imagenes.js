// src/utils/imagenes.js
// Vite carga TODAS las imágenes de src/assets/Img como URLs al iniciar.
const imagenes = import.meta.glob(
  "../assets/Img/**/*.{png,jpg,jpeg,webp,svg,PNG,JPG,JPEG}",
  { eager: true, as: "url" }
);

/**
 * Convierte la ruta de la DB ("/assets/Img/platos/x.png")
 * en la URL real que Vite generó.
 */
export function resolverImagen(rutaDB) {
  if (!rutaDB) return "";

  // "/assets/Img/platos/x.png" => "Img/platos/x.png"
  const limpia = rutaDB.replace(/^\/?assets\//, "");

  // key que usa import.meta.glob (relativa a src/utils/)
  const key = `../assets/${limpia}`;

  return imagenes[key] || "";
}